# -*- coding: utf-8 -*-

import logging
import os


class Logger(object):

    def __init__(self):
        self._logger = logging.getLogger("bintray")
        self._logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s:%(levelname)s: %(message)s')
        ch = logging.StreamHandler()
        level = int(os.getenv("BINTRAY_LOGGING_LEVEL", logging.INFO))
        ch.setLevel(level)
        ch.setFormatter(formatter)
        self._logger.addHandler(ch)

    @property
    def logger(self):
        return self._logger
