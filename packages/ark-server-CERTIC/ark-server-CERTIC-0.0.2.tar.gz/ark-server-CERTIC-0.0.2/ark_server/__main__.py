#!/usr/bin/env python3
import csv
import hashlib
import hmac
import os
import secrets
import string
from json import dumps, loads
from time import time
import aiopg
import argh
import psycopg2
import psycopg2.extras
import sanic
import gzip
from asyncio_extras import async_contextmanager
from hashids import Hashids
from sanic import request as sanic_request
from sanic.exceptions import Forbidden, InvalidUsage, NotFound, ServerError
from sanic.response import json, text, HTTPResponse, redirect, raw, html
from sanic.views import HTTPMethodView


DB_CREATE_SCRIPT = """
DROP TABLE IF EXISTS arks;
DROP TABLE IF EXISTS apps;

CREATE TABLE apps (
    app_id serial NOT NULL,
    app_secret text NOT NULL,
    app_title text NULL,
    app_contact_email text NULL,
    PRIMARY KEY (app_id))
WITH (OIDS = FALSE);

CREATE TABLE arks (
    ark_id bigserial NOT NULL,
    ark_location text,
    ark_metas jsonb,
    ark_created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ark_last_changed_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ark_app_id integer REFERENCES apps (app_id),
    PRIMARY KEY (ark_id))
WITH (OIDS = FALSE);

CREATE OR REPLACE FUNCTION app_get_secret (_app_id integer)
    RETURNS TEXT
AS $$
SELECT
    app_secret
FROM
    apps
WHERE
    app_id = _app_id
$$
LANGUAGE sql;

CREATE OR REPLACE FUNCTION app_make_access (_app_secret TEXT, _app_id integer DEFAULT NULL, _app_title TEXT DEFAULT NULL)
    RETURNS integer
    LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
    IF _app_id IS NOT NULL THEN
        UPDATE
            apps
        SET
            app_secret = _app_secret,
            app_title = _app_title
        WHERE
            app_id = _app_id;
        IF FOUND THEN
            RETURN _app_id;
        ELSE
            RAISE
            EXCEPTION 'app not found';
        END IF;
    ELSE
        INSERT INTO apps (app_secret, app_title)
        VALUES (_app_secret, _app_title);
        RETURN LASTVAL();
    END IF;
END;
$BODY$;

CREATE OR REPLACE FUNCTION ark_create (ark_app_id integer, ark_location TEXT, ark_metas jsonb DEFAULT NULL)
    RETURNS integer
    LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
    INSERT INTO arks (ark_location, ark_metas, ark_app_id)
    VALUES (ark_location, ark_metas, ark_app_id);
    RETURN LASTVAL();
END;
$BODY$;

CREATE OR REPLACE FUNCTION ark_update (_ark_app_id integer, _ark_id integer, _ark_location TEXT, _ark_metas jsonb DEFAULT NULL)
    RETURNS BOOLEAN
    LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
    UPDATE
        arks
    SET
        ark_location = _ark_location,
        ark_metas = _ark_metas,
        ark_last_changed_at = NOW()
    WHERE
        ark_id = _ark_id
        AND ark_app_id = _ark_app_id;
    IF FOUND THEN
        RETURN TRUE;
    ELSE
        RAISE
        EXCEPTION 'ark not found';
    END IF;
END;
$BODY$;

CREATE OR REPLACE FUNCTION ark_read (_ark_id integer)
    RETURNS TABLE (ark_location TEXT, ark_metas jsonb)
    LANGUAGE 'plpgsql'
AS $BODY$
BEGIN
    RETURN QUERY
    SELECT
        arks.ark_location,
        arks.ark_metas
    FROM
        arks
    WHERE
        arks.ark_id = _ark_id;
END;
$BODY$;

"""

CONFIG = {
    "ARK_SERVER_ALPHABET": "0123456789BCDFGHJKLMNPQRSTVWXZ",
    "ARK_SERVER_NAAN": "44804",
    "ARK_SERVER_PGSQL_USER": "ark",
    "ARK_SERVER_PGSQL_PASSWORD": "1234",
    "ARK_SERVER_PGSQL_HOST": "localhost",
    "ARK_SERVER_PGSQL_PORT": "5432",
    "ARK_SERVER_PGSQL_DBNAME": "ark",
    "ARK_SERVER_HOST": "localhost",
    "ARK_SERVER_PORT": "8000",
    "ARK_SERVER_WORKERS": "1",
    "ARK_SERVER_DEBUG": False,
    "ARK_SERVER_HASH_MIN_LENGTH": "0",
    "ARK_SERVER_SALT": "",
    "ARK_SERVER_REQUEST_AGE_LIMIT": 60,
    "ARK_SERVER_ENDPOINT": "/api/v1/",
}

ERROR_NO_SUCH_ARK = "No such ARK"
ERROR_NOT_ALLOWED = "Not allowed"
ERROR_BAD_ARK_NAME = "Bad ARK name"
ERROR_ARK_LOCATION_MISSING = "ark_location missing"
ERROR_ARK_NAME_MISSING = "ark_name missing"

IDX_CRUD_OPERATION = 0
IDX_ARK_NAME = 1
IDX_ARK_LOCATION = 2
IDX_ARK_METAS = 3

for key in CONFIG.keys():
    try:
        val = os.environ[key]
        if key in [
            "ARK_SERVER_DEBUG",
        ]:
            CONFIG[key] = True if val == "1" else False
        else:
            CONFIG[key] = val
    except KeyError:
        pass


hashids = Hashids(
    alphabet=CONFIG["ARK_SERVER_ALPHABET"],
    min_length=CONFIG["ARK_SERVER_HASH_MIN_LENGTH"],
    salt=CONFIG["ARK_SERVER_SALT"],
)


DSN = "postgres://{}:{}@{}:{}/{}".format(
    CONFIG["ARK_SERVER_PGSQL_USER"],
    CONFIG["ARK_SERVER_PGSQL_PASSWORD"],
    CONFIG["ARK_SERVER_PGSQL_HOST"],
    CONFIG["ARK_SERVER_PGSQL_PORT"],
    CONFIG["ARK_SERVER_PGSQL_DBNAME"],
)

# Server definition


@async_contextmanager
async def aiopg_cursor():
    try:
        async with aiopg.create_pool(DSN) as pool:
            async with pool.acquire() as conn:
                yield await conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    finally:
        pass


def psycopg2_cursor():
    conn = psycopg2.connect(DSN)
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return cur


async def check_hmac(app_id: int, request_body: str, hmac_digest: str):
    async with aiopg_cursor() as cur:
        await cur.callproc("app_get_secret", [app_id])
        res = await cur.fetchone()
        secret = res["app_get_secret"]
        if not secret:
            raise Forbidden(ERROR_NOT_ALLOWED)
        hmac_hash = hmac.new(secret.encode("utf-8"), request_body, hashlib.sha256)
        if hmac_hash.hexdigest() != hmac_digest:
            raise Forbidden(ERROR_NOT_ALLOWED)


def check_location(data: dict):
    if "ark_location" not in data.keys():
        raise InvalidUsage(ERROR_ARK_LOCATION_MISSING)


async def check_auth(request: sanic_request, data: dict):
    if (
        "Authorization" not in request.headers
        or "app_id" not in data.keys()
        or "timestamp" not in data.keys()
    ):
        raise Forbidden(ERROR_NOT_ALLOWED)
    time_diff = abs(int(time()) - data["timestamp"])
    if time_diff > CONFIG["ARK_SERVER_REQUEST_AGE_LIMIT"]:
        raise Forbidden(ERROR_NOT_ALLOWED)
    hmac_hash = request.headers["Authorization"]
    await check_hmac(data["app_id"], request.body, hmac_hash)


class APIView(HTTPMethodView):
    async def get(self, request: sanic_request):
        try:
            ark_arg = request.args.get("ark")
            if not ark_arg:
                return redirect("/")
            naan, ark_id = ark_arg.split("/")
            try:
                ark_id_int = hashids.decode(ark_id)[0]
            except IndexError:
                raise NotFound(ERROR_NO_SUCH_ARK)
        except ValueError:
            raise InvalidUsage(ERROR_BAD_ARK_NAME)
        if naan != CONFIG["ARK_SERVER_NAAN"]:
            raise NotFound(ERROR_NO_SUCH_ARK)
        async with aiopg_cursor() as cur:
            await cur.callproc("ark_read", [ark_id_int])
            res = await cur.fetchone()
            if res:
                return json(res)
            else:
                raise NotFound(ERROR_NO_SUCH_ARK)

    async def post(self, request: sanic_request):
        data = request.json
        await check_auth(request, data)
        check_location(data)
        async with aiopg_cursor() as cur:
            await cur.callproc(
                "ark_create",
                (
                    data["app_id"],
                    data["ark_location"],
                    dumps(data["ark_metas"]) if "ark_metas" in data.keys() else None,
                ),
            )
            record = await cur.fetchone()
            ark_id = "{}/{}".format(
                CONFIG["ARK_SERVER_NAAN"], hashids.encode(record["ark_create"])
            )
            await cur.execute("COMMIT;")
            return text(ark_id)

    async def put(self, request: sanic_request):
        data = request.json
        if "ark_name" not in data.keys():
            raise InvalidUsage(ERROR_ARK_NAME_MISSING)
        await check_auth(request, data)
        check_location(data)
        try:
            naan, ark_id = data["ark_name"].split("/")
            ark_id_int = hashids.decode(ark_id)[0]
        except (ValueError, AttributeError, IndexError):
            raise InvalidUsage(ERROR_BAD_ARK_NAME)
        if naan != CONFIG["ARK_SERVER_NAAN"]:
            raise NotFound(ERROR_NO_SUCH_ARK)
        async with aiopg_cursor() as cur:
            try:
                await cur.callproc(
                    "ark_update",
                    (
                        data["app_id"],
                        ark_id_int,
                        data["ark_location"],
                        dumps(data["ark_metas"])
                        if "ark_metas" in data.keys()
                        else None,
                    ),
                )
                await cur.execute("COMMIT;")
                return HTTPResponse(status=200)
            except psycopg2.InternalError:
                raise NotFound(ERROR_NO_SUCH_ARK)


server = sanic.Sanic(name="ark")


def find_inflection(request: sanic_request):
    try:
        url = request.raw_url.decode("utf-8")
        if url[-2] == "??":
            return "??"
        if url[-1] == "?":
            return "?"
    except AttributeError:
        pass


@server.route("/")
async def arks(request: sanic_request):
    page = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8"/>
        <title>Ark Server</title>
    </head>
    <body style="font-family: monospace;">
        <h1>Ark Server</h1>
        <dl>
            <dt><strong>API Endpoint</strong></dt>
            <dd>{}</dd>
            <dt><strong>NAAN</strong></dt>
            <dd>{}</dd>
            <dt><strong>Debug mode</strong></dt>
            <dd>{}</dd>
        </dl>
    </body>
</html>
    """
    return html(
        page.format(
            CONFIG["ARK_SERVER_ENDPOINT"],
            CONFIG["ARK_SERVER_NAAN"],
            "yes" if CONFIG["ARK_SERVER_DEBUG"] else "no",
        )
    )


@server.route("{}batch/".format(CONFIG["ARK_SERVER_ENDPOINT"]), methods=["POST"])
async def batch(request: sanic_request):
    data = loads(gzip.decompress(request.body))
    await check_auth(request, data)
    async with aiopg_cursor() as cur:
        for item in data["items"]:
            # BATCH READ
            if item[IDX_CRUD_OPERATION] == "r":
                try:
                    naan, ark_id = item[IDX_ARK_NAME].split("/")
                    if naan != CONFIG["ARK_SERVER_NAAN"]:
                        raise NotFound(ERROR_NO_SUCH_ARK)
                    ark_id_int = hashids.decode(ark_id)[0]
                    await cur.callproc("ark_read", [ark_id_int])
                    res = await cur.fetchone()
                    if res:
                        item[IDX_ARK_LOCATION] = res["ark_location"]
                        item[IDX_ARK_METAS] = res["ark_metas"]
                    else:
                        raise NotFound(ERROR_NO_SUCH_ARK)
                except (ValueError, AttributeError, IndexError):
                    raise InvalidUsage(ERROR_BAD_ARK_NAME)
            # BATCH CREATE
            if item[IDX_CRUD_OPERATION] == "c":
                await cur.callproc(
                    "ark_create",
                    (
                        data["app_id"],
                        item[IDX_ARK_LOCATION],
                        dumps(item[IDX_ARK_METAS]),
                    ),
                )
                record = await cur.fetchone()
                ark_name = "{}/{}".format(
                    CONFIG["ARK_SERVER_NAAN"], hashids.encode(record["ark_create"])
                )
                item[IDX_ARK_NAME] = ark_name
            # BATCH UPDATE
            if item[IDX_CRUD_OPERATION] == "u":
                try:
                    naan, ark_id = item[IDX_ARK_NAME].split("/")
                    if naan != CONFIG["ARK_SERVER_NAAN"]:
                        raise NotFound(ERROR_NO_SUCH_ARK)
                    ark_id_int = hashids.decode(ark_id)[0]
                    await cur.callproc(
                        "ark_update",
                        (
                            data["app_id"],
                            ark_id_int,
                            item[IDX_ARK_LOCATION],
                            dumps(item[IDX_ARK_METAS])
                            if "ark_metas" in data.keys()
                            else None,
                        ),
                    )
                except psycopg2.InternalError:
                    raise NotFound(ERROR_NO_SUCH_ARK)
                except (ValueError, AttributeError, IndexError):
                    raise InvalidUsage(ERROR_BAD_ARK_NAME)
        await cur.execute("COMMIT;")
    return raw(
        gzip.compress(dumps(data["items"]).encode("utf-8")),
        headers={"Content-Encoding": "gzip", "Content-Type": "application/json"},
    )


@server.route(
    "/ark:{}/<ark_name:[{}]+>".format(
        CONFIG["ARK_SERVER_NAAN"], CONFIG["ARK_SERVER_ALPHABET"]
    )
)
async def resolve(request: sanic_request, ark_name):
    async with aiopg_cursor() as cur:
        try:
            ark_id_int = hashids.decode(ark_name)[0]
        except IndexError:
            raise InvalidUsage(ERROR_BAD_ARK_NAME)
        await cur.callproc("ark_read", [ark_id_int])
        res = await cur.fetchone()
        if res:
            inflection = find_inflection(request)
            if inflection == "?":
                return json(res)
            return redirect(res["ark_location"])
        else:
            raise NotFound(ERROR_NO_SUCH_ARK)


@server.exception(ServerError)
def on_server_error(request: sanic_request, exception):
    # do something useful here, then crash.
    raise exception


server.add_route(APIView().as_view(), CONFIG["ARK_SERVER_ENDPOINT"])

# Command-line tools


def run_server():
    """
    Run server according to env vars.
    """
    server.run(
        host=CONFIG["ARK_SERVER_HOST"],
        port=int(CONFIG["ARK_SERVER_PORT"]),
        workers=int(CONFIG["ARK_SERVER_WORKERS"]),
        debug=bool(int(CONFIG["ARK_SERVER_DEBUG"])),
        auto_reload=bool(int(CONFIG["ARK_SERVER_DEBUG"])),
    )


def make_api_access(
    app_id: "specify app id to change existing access. Ignore to create new access." = None,
    title: "Title of access (name of app)." = None,
    out: "output credentials in json format to given file" = None,
):
    """
    Create new app id / secret couple for api access.

    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    secret = "".join(secrets.choice(alphabet) for i in range(32))
    title = title or "untitled app"

    cur = psycopg2_cursor()
    cur.callproc("app_make_access", (secret, app_id, title))
    record = cur.fetchone()
    cur.execute("COMMIT;")

    if out:
        data = {"id": record["app_make_access"], "title": title, "secret": secret}
        with open(out, "w") as json_file:
            json_file.write(dumps(data))

    return """Access granted to {}
id    : {}
secret: {}
    """.format(
        title, record["app_make_access"], secret
    )


def install():
    """
    Create tables and functions in PostgreSQL. Database must exist.
    Create api test account.
    """
    confirm_token = "".join(
        secrets.choice(string.ascii_letters + string.digits) for i in range(8)
    )
    message = """Warning ! This will completely remove existing data and reset all tables. 
If this is really what you want, enter the string: "{}": """
    confirm = input(message.format(confirm_token))
    if confirm != confirm_token:
        return "String does not match, abandon."

    cur = psycopg2_cursor()
    cur.execute(DB_CREATE_SCRIPT)
    cur.execute("COMMIT;")
    make_api_access(title="API Test account", out=True)


def csv_import(csv_file: "path to csv file input"):
    """
    Import CSV file.
    Must have columns: ark_id, app_id, ark_location
    Any optional column will be treated as text meta
    """
    out_file = os.path.splitext(csv_file)[0] + "-out.csv"
    with open(out_file, "w") as csv_out:
        writer = csv.writer(csv_out)
        with open(csv_file, "r") as csv_in:
            cur = psycopg2_cursor()
            headers = []
            reader = csv.reader(csv_in)
            for row in reader:
                if not headers:
                    headers = row
                    if (
                        "app_id" not in headers
                        or "ark_name" not in headers
                        or "ark_location" not in headers
                    ):
                        return "Bad CSV format. Missing one of app_id, ark_name or ark_location columns."
                    writer.writerow(headers)
                    continue
                row = dict(zip(headers, row))
                metas = {}
                for column in row.keys():
                    if column not in ["app_id", "ark_name", "ark_location"]:
                        metas[column] = row[column]
                app_id = int(row["app_id"])
                if not app_id:
                    return "Missing app id"
                ark_name = row["ark_name"]
                ark_location = row["ark_location"]
                if not ark_name:
                    cur.callproc(
                        "ark_create",
                        (app_id, ark_location, dumps(metas) if metas else None),
                    )
                    record = cur.fetchone()
                    ark_id = "{}/{}".format(
                        CONFIG["ARK_SERVER_NAAN"], hashids.encode(record["ark_create"])
                    )
                    row["ark_name"] = ark_id
                else:
                    ark_id_int = hashids.decode(ark_name)[0]
                    cur.callproc(
                        "ark_update",
                        (
                            app_id,
                            ark_id_int,
                            ark_location,
                            dumps(metas) if metas else None,
                        ),
                    )
                writer.writerow(list(row.values()))
        cur.execute("COMMIT;")


def run_cli():
    parser = argh.ArghParser()
    parser.add_commands([run_server, make_api_access, install, csv_import])
    parser.dispatch()
