# -*- coding: utf8 -*-

""" Base class for updaters """

from collections import namedtuple
import logging

Progress = namedtuple('Progress', ['current', 'all'])

class Updater(object):

    def __init__(self, tracker):
        self.tracker = tracker

    def pre(self):
        self.tracker.step("Pre-updating...")

    def run(self):
        self.tracker.step("Updating...")

    def is_done(self):
        return True

    def post(self):
        self.tracker.step("Post-updating...")

    def get_progress(self):
        return Progress(current=0, all=0)
