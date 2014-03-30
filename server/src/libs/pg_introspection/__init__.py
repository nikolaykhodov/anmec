# -*- coding: utf-8 -*-

from django.db import connection
from django.db import transaction
from random import randint

import hashlib
import re


def get_table_name(model):
    return model._meta.db_table


def get_model_indexes(model):
    """ Return a dictionary of CREATE statements with index names as keys """

    table_name = model._meta.db_table
    cursor = connection.cursor()

    cursor.execute("SELECT %s::regclass::oid", [table_name])
    table_oid = cursor.fetchone()[0]

    cursor.execute("""
        SELECT
            pg_index.indexrelid
        FROM
            pg_catalog.pg_index
        WHERE
            pg_index.indrelid = %s""", [table_oid])
    index_oids = [row[0] for row in cursor.fetchall()]

    if len(index_oids) == 0:
        return {}

    parts = ["pg_get_indexdef(%s)" for i in xrange(len(index_oids))]
    cursor.execute("SELECT " + ", ".join(parts), index_oids)
    statements = cursor.fetchone()

    indexes = {}
    for statement in statements:
        matches = re.findall(r'INDEX (.*?) ON', statement)
        if len(matches) == 0:
            raise Exception("Can't extract index name: " + statement)
        index_name = matches[0]
        indexes[index_name] = statement

    return indexes


def get_model_constraints(model):
    """ Return a dictionary of ALTER TABLE ADD statements with constraint names as keys """
    table_name = model._meta.db_table
    cursor = connection.cursor()

    cursor.execute("SELECT %s::regclass::oid", [table_name])
    table_oid = cursor.fetchone()[0]

    cursor.execute("""
        SELECT 'ALTER TABLE "'||relname||'" ADD CONSTRAINT "'||conname||'" '||
        pg_get_constraintdef(pg_constraint.oid)||';'
        FROM pg_constraint
        INNER JOIN pg_class ON conrelid=pg_class.oid
        INNER JOIN pg_namespace ON pg_namespace.oid=pg_class.relnamespace
        WHERE pg_constraint.conrelid=%s
        ORDER BY CASE WHEN contype='f' THEN 0 ELSE 1 END DESC,contype DESC,nspname DESC,relname DESC,conname DESC;
        """, [table_oid])

    add_statements = [row[0] for row in cursor.fetchall()]
    if len(add_statements) == 0:
        return {}

    constraints = {}
    for statement in add_statements:
        matches = re.findall(r'CONSTRAINT "(.*?)"', statement)
        if len(matches) == 0:
            raise Exception("Can't extract constraint name: " + statement)
        constraint_name = matches[0]
        constraints[constraint_name] = statement

    return constraints


def apply_model_indexes(indexes, table_name=None):
    """ Execute CREATE INDEX statements """
    if table_name is not None:
        new_suffix = hashlib.sha1(table_name + str(randint(1, 10 ** 9))).hexdigest()[:16]

        new_indexes = {}
        for index_name in indexes:
            parts = index_name.split('_')
            is_there_suffix = len(parts) > 0 and len(parts[-1]) == 16

            if is_there_suffix:
                parts[-1] = new_suffix
                new_index_name = "_".join(parts)
            else:
                new_index_name = index_name + '_' + new_suffix

            statement = indexes[index_name]
            statement = re.sub(r'ON (\w+)', "ON {0}".format(table_name), statement)
            statement = re.sub(r'INDEX (\w+)', "INDEX {0}".format(new_index_name), statement)

            new_indexes[new_index_name] = statement

        indexes = new_indexes

    cursor = connection.cursor()
    for statement in indexes.values():
        cursor.execute(statement)
    transaction.commit_unless_managed()


def apply_model_constraints(constraints):
    cursor = connection.cursor()
    for statement in constraints.values():
        cursor.execute(statement)
    transaction.commit_unless_managed()


def remove_model_constraints(model):
    constraints = get_model_constraints(model)
    table_name = get_table_name(model)

    cursor = connection.cursor()
    for constraint_name in constraints.keys():
        cursor.execute("ALTER TABLE {0} DROP CONSTRAINT {1}".format(table_name, constraint_name))
    transaction.commit_unless_managed()
