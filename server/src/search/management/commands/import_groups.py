# -*- coding: utf-8 -*-

"""
Import groups data
"""

from django.core.management.base import BaseCommand
from django.db import connection
from django.db import transaction
from search.models import Group
from search.models import Audience
from search.models import TrafficByCountries
from search.models import TrafficByCities
from datetime import datetime

import pg_introspection
import logging


class Command(BaseCommand):

    args = '<CSV with raw groups data>>'
    help = "Import groups"

    def get_table_name(self, model):
        return model._meta.db_table

    def get_new_tablename(self, model, suffix):
        return model._meta.db_table + '_' + suffix

    def create_new_table(self, model, table_name):
        cursor = connection.cursor()

        cursor.execute("DROP TABLE IF EXISTS {0}".format(table_name))
        cursor.execute("CREATE TABLE {0} AS SELECT * FROM {1} LIMIT 1".format(
            table_name,
            self.get_table_name(model)
        ))
        cursor.execute("DELETE FROM {0}".format(table_name))
        transaction.commit_unless_managed()

    def change_tables(self, old_table_name, new_table_name):
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS {0}".format(old_table_name))
        cursor.execute("ALTER TABLE {0} RENAME TO {1}".format(
            new_table_name,
            old_table_name
        ))
        transaction.commit_unless_managed()

    def vacuum(self, table_name):
        cursor = connection.cursor()
        conn = cursor.db.connection

        old_isolation_level = conn.isolation_level
        conn.set_isolation_level(0)

        cursor.execute("VACUUM VERBOSE ANALYZE {0}".format(table_name))

        conn.set_isolation_level(old_isolation_level)

    def import_data(self, filename, table_name):

        cursor = connection.cursor()

        file_as_stdin = open(filename)
        command = "COPY {0} FROM STDIN CSV DELIMITER ',' QUOTE '\"'".format(
            table_name
        )

        cursor.copy_expert(command, file_as_stdin)
        transaction.commit_unless_managed()

    def get_model_indexes(self, model):
        """ Return a dictionary of CREATE statements with index names as keys """

        return pg_introspection.get_model_indexes(model)

    def get_model_constraints(self, model):
        """ Return a dictionary of ALTER TABLE ADD statements with constraint names as keys """

        return pg_introspection.get_model_constraints(model)

    def apply_model_indexes(self, indexes, table_name=None):
        """ Execute CREATE INDEX statements """

        pg_introspection.apply_model_indexes(indexes, table_name=table_name)

    def apply_model_constraints(self, constraints):

        pg_introspection.apply_model_constraints(constraints)

    def remove_model_constraints(self, model):

        pg_introspection.remove_model_constraints(model)

    def check_model_indexes(self, model, old_indexes):
        """ Assert that the current indexes are the same as old indexes """

        table_name = self.get_table_name(model)
        assert len(self.get_model_indexes(model).keys()) == len(old_indexes.keys()), "There is a discrepancy in indexes in {0}".format(table_name)

    def check_model_constraints(self, model, old_constraints):
        """ Assert that the current constraints are the same as old constraints """

        table_name = self.get_table_name(model)
        assert self.get_model_constraints(model) == old_constraints, "There is a discrepancy in constraints in {0}".format(table_name)

    def get_timestamp(self):
        now = datetime.now()
        # ddmmyyyy_hhmm
        return now.strftime("%d%m%Y_%H%M")

    def handle(self, *args, **kwargs):
        """
        Handle
        """

        infile = args[0]
        suffix = self.get_timestamp()

        old_table_name = self.get_table_name(Group)
        new_table_name = self.get_new_tablename(Group, suffix)

        group_indexes = self.get_model_indexes(Group)
        constraints = dict(
            groups=self.get_model_constraints(Group),
            audience=self.get_model_constraints(Audience),
            by_countries=self.get_model_constraints(TrafficByCountries),
            by_cities=self.get_model_constraints(TrafficByCities)
        )

        logging.basicConfig(level=logging.DEBUG)

        logging.info("Creating temprorary table {0} for importing groups...".format(new_table_name))
        self.create_new_table(Group, new_table_name)

        logging.info('Importing new data into {0}'.format(new_table_name))
        self.import_data(infile, new_table_name)

        logging.info("Applying indexes for {0}...".format(new_table_name))
        self.apply_model_indexes(group_indexes, new_table_name)

        logging.info("Remove constraints for tables that is dependent on Groups...")
        self.remove_model_constraints(Audience)
        self.remove_model_constraints(TrafficByCountries)
        self.remove_model_constraints(TrafficByCities)

        try:
            logging.info("Renaming {0} to {1}".format(new_table_name, old_table_name))
            self.change_tables(old_table_name, new_table_name)

        finally:
            logging.info("Restoring constraints...")
            self.apply_model_constraints(constraints['audience'])
            self.apply_model_constraints(constraints['by_countries'])
            self.apply_model_constraints(constraints['by_cities'])

            logging.info("Checking indexes and constraints...")
            self.check_model_indexes(Group, group_indexes)
            self.check_model_constraints(Audience, constraints['audience'])
            self.check_model_constraints(TrafficByCountries, constraints['by_countries'])
            self.check_model_constraints(TrafficByCities, constraints['by_cities'])

            logging.info("Vacuuming table {0}...".format(old_table_name))
            self.vacuum(old_table_name)
