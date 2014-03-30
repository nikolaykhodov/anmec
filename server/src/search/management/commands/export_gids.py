# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from search.models import Group
import sys


class Command(BaseCommand):

    args = '<output file> [top]'
    help = "Import analytics"

    def handle(self, *args, **kwargs):

        print(args)
        if len(args) < 1:
            print("You should specify an output file name and how many groups")
            sys.exit()

        need_top_group_ids = len(args) >= 2 and args[1] == 'top'

        if need_top_group_ids:
            groups = Group.objects.order_by('-members_count').filter(is_closed=0)[:settings.UPDATING_POSTS_TOP_GROUPS]
        else:
            groups = Group.objects.all()

        gids = list(groups.values_list('gid'))
        content = ""

        for gid in gids:
            content += "{0}\n".format(gid[0])

        outfile = open(args[0], 'w+')
        outfile.write(content)
        outfile.close()
