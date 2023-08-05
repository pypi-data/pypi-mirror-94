#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Radio Team, all rights reserved

import os
import sys
import contextlib
from glxviewer import viewer


@contextlib.contextmanager
def ignore_stderr():
    devnull = os.open(os.path.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)


with ignore_stderr():
    import pyaudio


class AudioInterfaces(object):
    def __init__(self):
        self.a = 1

        with ignore_stderr():
            p = pyaudio.PyAudio()
        self.sysdefault_id = None
        for i in range(p.get_device_count()):
            dev = p.get_device_info_by_index(i)
            if dev["name"] == "jack":
                self.sysdefault_id = i
                continue
            elif dev["name"] == "pulse":
                self.sysdefault_id = i
                continue

    def get_sysdefault_id(self):
        return self.sysdefault_id

    @staticmethod
    def print_interfaces(only_default=False):
        with ignore_stderr():
            p = pyaudio.PyAudio()

        for i in range(p.get_device_count()):
            dev = p.get_device_info_by_index(i)
            if only_default:
                # Presentation verbal ++
                if dev["name"] == "pulse":
                    viewer.flush_infos(
                        status_text="INIT",
                        status_text_color="WHITE",
                        status_symbol=">",
                        column_1=str(i) + ", " + str(dev["name"]),
                    )
                    viewer.flush_infos(
                        status_text="INIT",
                        status_text_color="WHITE",
                        column_2="SampleRate:" + str(dev["defaultSampleRate"]),
                    )
                    viewer.flush_infos(
                        status_text="INIT",
                        status_text_color="WHITE",
                        column_2="maxOutputChannels:" + str(dev["maxOutputChannels"]),
                    )
                    viewer.flush_infos(
                        status_text="INIT",
                        status_text_color="WHITE",
                        column_2="maxInputChannels:" + str(dev["maxInputChannels"]),
                    )
            else:
                # Presentation verbal ++
                if dev["name"] == "sysdefault":
                    viewer.flush_infos(
                        status_text="INIT",
                        status_text_color="WHITE",
                        status_symbol=">",
                        column_1=str(i) + ", " + str(dev["name"]),
                    )
                else:
                    viewer.flush_infos(
                        status_text="INIT",
                        status_text_color="WHITE",
                        column_1=str(i) + ", " + str(dev["name"]),
                    )

                viewer.flush_infos(
                    status_text="INIT",
                    status_text_color="WHITE",
                    column_2="SampleRate:" + str(dev["defaultSampleRate"]),
                )
                viewer.flush_infos(
                    status_text="INIT",
                    status_text_color="WHITE",
                    column_2="maxOutputChannels:" + str(dev["maxOutputChannels"]),
                )
                viewer.flush_infos(
                    status_text="INIT",
                    status_text_color="WHITE",
                    column_2="maxInputChannels:" + str(dev["maxInputChannels"]),
                )

        p.terminate()
