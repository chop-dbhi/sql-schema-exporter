import os
import sys
import json
from time import time
from sqlalchemy import create_engine
from sqlalchemy.types import TypeEngine
from sqlalchemy.engine import reflection
from sqlalchemy.engine.url import URL


def default(o):
    if isinstance(o, TypeEngine):
        return o.__class__.__name__.lower()

    return o


def extract_schema(insp, schema):
    sys.stderr.write('Extacting schema [{}]\n'.format(schema))
    sys.stderr.write('Fetching table names...\n')

    t0 = time()
    table_names = insp.get_table_names(schema=schema)
    sys.stderr.write(' {:.2f}s\n'.format(time()-t0))

    for table in table_names:
        sys.stderr.write('Fetching {}\n'.format(table))

        sys.stderr.write('- columns...')
        sys.stderr.flush()
        t0 = time()

        columns = [{
            'name': c['name'],
            'nullable': c['nullable'],
            'type': c['type'],
        } for c in insp.get_columns(table, schema=schema)]

        sys.stderr.write(' {:.2f}s\n'.format(time()-t0))

        sys.stderr.write('- primary key...')
        sys.stderr.flush()
        t0 = time()

        primary_key = insp.get_pk_constraint(table, schema=schema)
        if primary_key:
            primary_key = primary_key['constrained_columns']

        sys.stderr.write(' {:.2f}s\n'.format(time()-t0))

        sys.stderr.write('- foreign keys...')
        sys.stderr.flush()
        t0 = time()

        foreign_keys = [{
            'name': fk['name'],
            'constrained_columns': fk['constrained_columns'],
            'referred_schema': fk['referred_schema'],
            'referred_table': fk['referred_table'],
            'referred_columns': fk['referred_columns'],
        } for fk in insp.get_foreign_keys(table, schema=schema)]

        sys.stderr.write(' {:.2f}s\n'.format(time()-t0))

        sys.stderr.write('- unique constraints...')
        sys.stderr.flush()
        t0 = time()

        unique_constraints = insp.get_unique_constraints(table, schema=schema)

        sys.stderr.write(' {:.2f}s\n'.format(time()-t0))

        yield {
            'schema': schema,
            'table': table,
            'columns': columns,
            'primary_key': primary_key,
            'foreign_keys': foreign_keys,
            'unique_constraints': [{
                'name': uc['name'],
                'columns': uc['column_names'],
            } for uc in unique_constraints],
        }


def extract(engine, options):
    insp = reflection.Inspector.from_engine(engine)

    schemata = options.get('schemata')
    if schemata:
        schemata = schemata.split(',')
    elif insp.default_schema_name:
        schemata = insp.default_schema_name.split(',')
    else:
        # Sentinenl for databases that don't have schemata (sqlite).
        schemata = (None,)

    for schema in schemata:
        for table in extract_schema(insp, schema):
            yield table


def main(args):
    if len(args) > 0:
        engine = create_engine(args[0])
    else:
        uri = os.environ.get('DB_URI')
        if uri:
            engine = create_engine(uri)
        else:
            url = URL(os.environ.get('DB_ENGINE'),
                      username=os.environ.get('DB_USER'),
                      password=os.environ.get('DB_PASSWORD'),
                      host=os.environ.get('DB_HOST'),
                      port=os.environ.get('DB_PORT'),
                      database=os.environ.get('DB_NAME'))

            engine = create_engine(url)

    gen = extract(engine, {})

    sys.stdout.write('[')

    for i, table in enumerate(gen):
        if i > 0:
            sys.stdout.write(',\n')
        json.dump(table, sys.stdout, default=default)

    sys.stdout.write(']')
    sys.stdout.flush()


if __name__ == '__main__':
    args = sys.argv[1:]
    main(args)
