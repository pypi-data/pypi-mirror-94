#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Radio Team, all rights reserved

import pyaudio
import time
import numpy as np
import sys
import os
import array

# Require when you haven't GLXRadio as default Package
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))

from glxviewer import viewer
from glxaudio.Audio import Audio
from glxaudio.AudioUtils import sec2time
from glxaudio.RingBuffer import RingBuffer


class AudioSWHear(Audio):
    """
    The AudioSWHear class is made to provide access to continuously recorded
    (and mathematically processed) microphone data.

    Original: https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/
    """

    def __init__(self, input_device_index=None, start_streaming=False):
        """fire up the AudioSWHear class."""
        Audio.__init__(self)
        if input_device_index is None:
            input_device_index = self.get_sysdefault_id()

        self.set_format(pyaudio.paInt16)
        # number of data points to read at a time
        self.set_chunk_size(4096)
        # time resolution of the recording device (Hz)
        self.set_rate(44100)
        # that is a one track object normally
        self.set_channels(1)

        # for tape recording (continuous "tape" of recent audio)
        self.tape_length = 3  # seconds
        self.start_duration = time.time()

        # self.tape = np.empty(self.rate * self.tape_length) * np.nan

        self.ring_buffer_capacity = int(
            self.get_rate() * self.tape_length / self.get_chunk_size()
        )
        self.tape = RingBuffer(
            self.ring_buffer_capacity, dtype=self.get_dtype(), allow_overwrite=True
        )

        if start_streaming:
            # start the PyAudio class
            self.create_audio()
            self.stream_create(input_device_index=input_device_index)
            self.stream_start()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_all()

    # LOWEST LEVEL AUDIO ACCESS
    # pure access to microphone and stream operations
    # keep math, plotting, FFT, etc out of here.
    def stream_read(self):
        """return values for a single chunk"""
        # data = np.fromstring(self.get_stream().read(self.get_chunk_size(),
        #                                             exception_on_overflow=False),
        #                      dtype=self.get_dtype()
        #                      )
        if self.get_stream() is not None:
            block_string = self.get_stream().read(
                self.get_chunk_size(), exception_on_overflow=False
            )
            block = np.fromstring(block_string, dtype=self.get_dtype())

            # print(data)
            return block
        else:
            return None

    def stream_create(self, input_device_index=None):
        """connect to the audio device"""
        self.close_pyaudio()
        self.stream_close()
        self.create_audio()
        self.set_stream(
            self.get_audio().open(
                format=self.get_format(),
                channels=self.get_channels(),
                rate=self.get_rate(),
                input=True,
                input_device_index=input_device_index,
                frames_per_buffer=self.get_chunk_size(),
            )
        )

    # TAPE METHODS
    # tape is like a circular magnetic ribbon of tape that's continously
    # recorded and recorded over in a loop. self.tape contains this data.
    # the newest data is always at the end. Don't modify data on the type,
    # but rather do math on it (like FFT) as you read from it.

    def tape_add(self):
        """add a single chunk to the tape."""
        # self.tape[:-self.get_frames_per_buffer()] = self.tape[self.get_frames_per_buffer():]
        # self.tape[-self.get_frames_per_buffer():] = self.stream_read()
        self.tape.appendleft(np.mean(self.stream_read()))

    def tape_flush(self):
        """completely fill tape with new data."""

        reads_in_tape = int(self.get_rate() * self.tape_length / self.get_chunk_size())

        if self.get_debug():
            viewer.flush_infos(
                column_1=self.__class__.__name__ + str(":"),
                column_2=" -- flushing %d s tape with %dx%.2f ms reads"
                         % (
                             self.tape_length,
                             reads_in_tape,
                             self.get_chunk_size() / self.get_rate(),
                         ),
            )

        for i in range(reads_in_tape):
            self.tape_add()

    def tape_forever(self, plotSec=None):

        # t1 = 0
        #
        # if plotSec is None:
        #     plotSec = 0.01
        try:
            self.start_duration = time.time()
            is_full_time = self.start_duration
            while True:
                self.tape_add()
                self.do_something(is_full_time)
                if not self.tape.is_full:
                    is_full_time = time.time()

                # if (time.time() - t1) > plotSec:
                #     t1 = time.time()

        except KeyboardInterrupt:
            return

    def do_something(self, is_full_time):
        """do something with what's in the tape."""
        maxi = np.array(self.stream_read())
        viewer.flush_infos(
            status_text_color="WHITE",
            status_text="TAPE",
            column_1=str(self.get_db_from_chunk(maxi))
                     + "dBFS, "
                     + str(sec2time(time.time() - self.start_duration)),
            column_2=str(sec2time(is_full_time - self.start_duration))
                     + "                                     ",
            prompt=-1,
        )
