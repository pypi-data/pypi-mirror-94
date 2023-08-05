# ARK (Archival Resource Key) Server

<!-- TOC -->

- [ARK (Archival Resource Key) Server](#ark-archival-resource-key-server)
    - [Goal](#goal)
    - [Dependencies](#dependencies)
    - [Install](#install)
    - [Command-line tools](#command-line-tools)
        - [Install (or re-install)](#install-or-re-install)
        - [Start web server](#start-web-server)
        - [Run tests](#run-tests)
        - [Add API account](#add-api-account)
        - [CSV import](#csv-import)
    - [Production deploy](#production-deploy)
    - [Basic Resolver](#basic-resolver)
    - [ReSTish API](#restish-api)
        - [Read](#read)
        - [Create](#create)
        - [Update](#update)
        - [API errors](#api-errors)
        - [Batch mode](#batch-mode)

<!-- /TOC -->

## Goal

The goal of this software is to offer a solution for a Name Assigning Authority to distribute Archival Resources Keys and maintain basic information about the resources. It offers a database, command-line tools and an HTTP API.

## Dependencies

- Python 3.6+ (async/await, secrets)
- PostgreSQL 9.4+ (jsonb)

## Install

Create a virtualenv and activate it:

```
python3 -m venv venv
. ./venv/bin/activate
```

Create a database and then override default env vars:

```
export ARK_SERVER_PGSQL_HOST=[pg_hostname]
```

```
export ARK_SERVER_PGSQL_USER=[pg_user]
```

```
export ARK_SERVER_PGSQL_PASSWORD=[pg_password]
```

```
export ARK_SERVER_DEBUG=0  # don't set to 1 in production
```

```
export ARK_SERVER_WORKERS=4  # as much as available cpu cores
```

Install Ark server:

```
pip install ark-server-CERTIC
```

Create tables:

```
ark install
```

## Command-line tools

All command-line tools support ```-h``` flag for help.

### Install (or re-install)

This command initializes the database.
**Warning !** This will wipe all data in your ARK database.

```
ark install
```

### Start web server

```
ark run-server
```

### Run tests

(Start web server first !)

```
pytest -vv tests.py
```

### Add API account

```
ark make-api-access
```

Would generate the following output:

```
Access granted to untitled app
id    : 3
secret: @-lQ,x}aZIT%Q}X&Dg!){zeq`pN:TOPt
```

Use ```ark make-api-access -h``` for help.

### CSV import

For mass-creation or update of ARK names. Must have columns app_id, ark_location, ark_name (empty value for creation). Any other column will be treated as meta:

```
ark csv-import /path/to/some/file.csv
```

A csv file is generated at /path/to/some/file-out.csv with added ARK names for creations.


## Basic Resolver

```https://yourhost.tld/ark:[your NAAN]/[ARK id]``` will redirect you to the location available in the db.

## ReSTish API

- An endpoint is available at http://whatever-your-host-is.tld/api/v1/
- Available HTTP verbs are GET, POST, PUT to respectively read, create or update ARKs to the database
- JSON body is used for POST and PUT

For POST and PUT, an Authorization HTTP header must contain a hmac256 of the request body, signed with your secret key (see [Add API account](#add-api-account) to generate your key). Example:

```
Authorization:16ac7bd2c03200935d72c3acbaaaf637afc7ba417d0bf6a4429379634268ecda
```
POST and PUT requests must also include the current Unix Epoch and the app_id.

### Read

```
GET /api/v1/?ark=[NAAN]/[ARK_ID]
```

If ARK exists, will return a response with a JSON body such as this:

```
{
    "ark_location": "http://somewhere.tld/some-resource/", 
    "ark_metas": 
    {
        "who": "someone", 
        "what": "something", 
        "where": "somewhere" 
    }
}
```

### Create

```
POST /api/v1/
```

With such JSON body:

```
{
    "app_id": 1,
    "timestamp": 1530798110,
    "ark_location": "http://somewhere.tld/some-resource/",
    "ark_metas": 
    {
        "who": "someone", 
        "what": "something", 
        "where": "somewhere" 
    }
}
```

A status code 200 is returned with a response body containing the ARK name. Example:

```
44804/MGQP4QLZ
```

### Update

```
PUT /api/v1/
```

With such JSON body:

```
{
    "app_id": 1,
    "timestamp": 1530798110,
    "ark_name": "44804/MGQP4QLZ"
    "ark_location": "http://somewhere.tld/some-resource/",
    "ark_metas": 
    {
        "who": "someone", 
        "what": "something", 
        "where": "somewhere" 
    }
}
```

A status code 200 is returned.

### API errors

Appropriate HTTP status codes are used (500, 400, 403, etc). Treat anything other than 200 as an error.

### Batch mode

An additional POST endpoint at ```/api/v1/batch/``` supports batch requests with mixed create, read or update. JSON document payload looks like this:

```
{
    "app_id": 1,
    "timestamp": 1530798110,
    "items":[
        ["r", "44408/TJX", null, null],
        ["c", null, "http://somewhere.tld/some-resource/", {
            "who": "someone", 
            "what": "something", 
            "where": "somewhere"}],
        ["u", "44408/JBN", "http://somewhere.tld/some-resource/", {
            "who": "someone", 
            "what": "something", 
            "where": "somewhere"}]
    ]
}
```

Each items is an array with the following informations: [crud_operation, ark_name, ark_location, ark_metas].
Letters "r", "c", "u" are used to explicitely indicate a read, a create or an update on the item. Unknown parameters are set to null.

The JSON payload MUST be gzip-encoded in the request body. As usual, the request MUST contain an authorization header signin the request body.

A (gzipped) response is sent with the completed items:

```
[
        ["r", "44408/TJX", "http://somewhere.tld/more-resource/", {
            "who": "someone", 
            "what": "something", 
            "where": "somewhere"}],
        ["c", "44408/FC2S", "http://somewhere.tld/some-resource/", {
            "who": "someone", 
            "what": "something", 
            "where": "somewhere"}],
        ["u", "44408/JBN", "http://somewhere.tld/some-resource/", {
            "who": "someone", 
            "what": "something", 
            "where": "somewhere"}]
]
```
