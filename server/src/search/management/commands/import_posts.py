# -*- coding: utf-8 -*-

"""
Import groups data
"""

from django.core.management.base import BaseCommand
from django.db import connection
from django.db import transaction
from search.models import Post
from datetime import datetime

import logging


class Command(BaseCommand):

    args = '<CSV with raw posts data>>'
    help = "Import posts"

    def get_table_name(self, model):
        return model._meta.db_table

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
        command = "COPY {0}(post_id, date, likes, reposts, comments, text, attachments) FROM STDIN CSV DELIMITER ',' QUOTE '\"'".format(
            table_name
        )

        cursor.copy_expert(command, file_as_stdin)
        transaction.commit_unless_managed()

    def compute_ratio(self, table_name):
        cursor = connection.cursor()

        command = "UPDATE {0} SET repost_like_ratio=CAST(100.0 * reposts / likes AS integer) WHERE likes > 0 AND repost_like_ratio IS NULL".format(
            table_name
        )
        cursor.execute(command)

        transaction.commit_unless_managed()

    def get_timestamp(self):
        now = datetime.now()
        # ddmmyyyy_hhmm
        return now.strftime("%d%m%Y_%H%M")

    def handle(self, *args, **kwargs):
        """
        Handle
        """

        infile = args[0]
        old_table_name = self.get_table_name(Post)

        logging.basicConfig(level=logging.DEBUG)

        logging.info('Importing new data into {0}'.format(old_table_name))
        self.import_data(infile, old_table_name)

        logging.info("Vacuuming table {0}...".format(old_table_name))
        self.vacuum(old_table_name)

        logging.info("Computing reposts to likes ratio for imported posts...")
        self.compute_ratio(old_table_name)
