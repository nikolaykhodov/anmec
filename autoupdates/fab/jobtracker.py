# -*- coding: utf-8 -*-

from urllib import urlencode
from datetime import datetime
from multiprocessing import Pool
import logging
import hashlib
import urllib2


class JobTracker(object):

    def __init__(self, url):
        self.url = url
        # Dirty hack to make notification request to tracker in background
        self.pool = Pool(1)

    def _get_timestamp(self):
        now = datetime.now()
        # ddmmyyyy_hhmm
        return now.strftime("%d%m%Y_%H%M%S")

    def _notify(self, **kwargs):
        url = self.url + '?' + urlencode(kwargs)
        try:
            urllib2.urlopen(url).read()
        except Exception, ex:
            print(ex)

    def start(self, name):
        self.taskId = hashlib.sha1(self._get_timestamp() + name).hexdigest()
        self._notify(
            taskId=self.taskId,
            name=name,
            action='start'
        )

    def step(self, message, *args):
        """
        Notify tracker about current action
        """
        if args is not None:
            message = message % args
        logging.info(message)

        self._notify(
            taskId=self.taskId,
            action="step",
            message=message
        )

    def progress(self, progress):
        """
        Notify tracker about progress.
        Arguments:
            -- taskId - id of taskes returned by start()
            -- progress - named tuple with two field: current and all
        """

        if progress is not None:
            self._notify(
                taskId=self.taskId,
                action="progress",
                progress="{0}/{1}".format(progress.current, progress.all)
            )

    def finish(self):

        self._notify(
            taskId=self.taskId,
            action="finish"
        )
