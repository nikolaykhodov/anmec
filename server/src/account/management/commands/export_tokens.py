# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from account.models import Account
import sys


class Command(BaseCommand):

    args = '<output file> [vk|fb|twitter]'
    help = "Import user tokens"

    def handle(self, *args, **kwargs):

        if len(args) < 1:
            print("You should specify an output file name")
            sys.exit()

        tokens = Account.objects.all().values_list('vk_token')
        content = ''
        for token in tokens:
            content += "{0}\n".format(token[0])

        outfile = open(args[0], 'w+')
        outfile.write(content)
        outfile.close()
