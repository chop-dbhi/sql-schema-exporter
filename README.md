# SQL Schema Exporter

This program exports table schema information from a relational database.

## Install

```
pip install -r requirements.txt
```

## Usage

The only argument is the URI of the database. The schema (as an array of tables) is emitted to stdout as JSON.

```bash
python main.py 'postgresql://postgres:secret@127.0.0.1:5432/data' > schema.json
```

Supported databases:

- PostgreSQL
- Oracle (requires instantclient libraries to be installed)
- MySQL
- SQLite

### Docker

A pre-baked Docker image is available which includes the Oracle driver.

```
docker run --rm dbhi/sql-schema-exporter 'postgresql://postgres:secret@127.0.0.1:5432/data' > schema.json
```

To build the Docker image locally, the instantclient-* libraries must be in this directly. See the Dockerfile for the file names.

## Data Model

```js
[
  {
    "schema": "<SCHEMA-NAME>",
    "table": "<TABLE-NAME>",
    "columns": [
      {
        "name": "<COLUMN-NAME>",
        "nullable": <BOOLEAN>,
        "type": "<DATA-TYPE>"
      },
      // ...
    ],

    "primary_key": [
      "<COLUMN-NAME>",
      // ...
    ],

    "foreign_keys": [
      {
        "constrained_columns": [
          "<COLUMN-NAME>",
          // ...
        ],
        "referred_schema": "<SCHEMA-NAME>",
        "referred_table": "<TABLE-NAME>",
        "referred_columns": [
          "<COLUMN-NAME>",
          // ...
        ]
      },
      //...
    ],

    "unique_constraints": [
      {
        "name": "<CONSTRAINT-NAME>",
        "columns": [
          "<COLUMN-NAME>",
          // ...
        ],
      },
      // ...
    ],
  },
  // ...
]
```
