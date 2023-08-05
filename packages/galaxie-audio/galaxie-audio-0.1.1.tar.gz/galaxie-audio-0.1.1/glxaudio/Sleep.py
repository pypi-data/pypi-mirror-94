#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Radio Team, all rights reserved

import time
from glxaudio.Object import Object
from glxviewer import Viewer
from glxaudio.AudioUtils import sec2time


class Sleep(Object):
    """
    A class it wait, like time.sleep() but more advanced.

    Why do that ? that because it's easy to do
    """

    def __init__(self):
        Object.__init__(self)

        self.duration_start = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.duration_start = None

    def sleep(self, sleep_time):
        sleep_time = float(sleep_time)
        self.set_duration_start()
        # duration_end = self.get_duration_start()

        while True:
            duration_end = time.time()
            if (duration_end - self.get_duration_start()) >= sleep_time:
                break
            if self.verbose:
                viewer.flush_infos(
                    status_text="WAIT",
                    status_text_color="CYAN",
                    column_1=str(sec2time(duration_end - self.get_duration_start())),
                    prompt=True,
                )
            # duration_end = time.time()
        if self.get_verbose():
            viewer.flush_a_new_line()

    def set_duration_start(self):
        """
        Internally store time, for can report status during a play.
        """
        self.duration_start = time.time()

    def get_duration_start(self):
        """
        Get the time when play sound has start. It's use internally for report statistic's

        :return: Unix time
        :rtype: int
        """
        return self.duration_start
