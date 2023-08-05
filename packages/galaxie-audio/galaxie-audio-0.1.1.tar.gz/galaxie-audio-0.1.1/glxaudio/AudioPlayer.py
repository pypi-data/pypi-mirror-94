#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Radio Team, all rights reserved

import pyaudio
import time
import wave
from glxaudio.Audio import Audio
from glxaudio.AudioUtils import sec2time
from glxviewer import viewer


class AudioPLayer(Audio):
    def __init__(self):
        Audio.__init__(self)

        self.duration_start = None
        self.verbose = True
        self.is_detached = None

        self.set_chunk_size(512)
        self.set_is_detached(True)

        self.create_audio()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def callback(self, _, frame_count, __, ___):
        # Display
        if self.get_verbose():
            viewer.flush_infos(
                column_1=str(sec2time(time.time() - self.get_duration_start())),
                status_text="PLAY",
                status_text_color="GREEN",
                status_symbol=">",
                prompt=True,
            )

        data = self.get_wave().readframes(frame_count)

        flag = pyaudio.paContinue

        # if self.get_wave().getnframes() == self.get_wave().tell():
        #     flag = pyaudio.paComplete

        return data, flag

    def play_detached(self, output_device_index=None):
        """
        PLay a sound over a callback, in a detached Thread.

        That is done automatically by PyAudio.

        :return: Time it have take for play the audio file
        :rtype: int
        """
        # instantiate PyAudio via self.get_new_audio()
        if output_device_index is None:
            output_device_index = self.get_sysdefault_id()

        self.set_stream(
            self.get_audio().open(
                format=self.get_format(),
                channels=self.get_channels(),
                rate=self.get_rate(),
                output=True,
                output_device_index=output_device_index,
                stream_callback=self.callback,
            )
        )

        # start the stream
        self.set_duration_start()
        self.stream_start()

        # wait for stream to finish
        if self.get_debug():
            viewer.flush_infos(
                column_1=self.__class__.__name__ + str(":"),
                column_2="play " + str(self.get_wave_path()),
            )
        while self.get_stream().is_active():
            pass

        if self.get_verbose():
            viewer.flush_a_new_line()

        # Close Stream Pyaudio and Wave
        self.stream_close()

        return time.time() - self.get_duration_start()

    def play_normal(self, output_device_index=None):
        """
        Play a sound.

        :return: Time it have take for play the audio file
        :rtype: int
        """
        if output_device_index is None:
            output_device_index = self.get_sysdefault_id()

        self.set_stream(
            self.get_audio().open(
                format=self.get_format(),
                channels=self.get_channels(),
                rate=self.get_rate(),
                output=True,
                output_device_index=output_device_index,
            )
        )
        self.stream_start()
        self.set_duration_start()
        if self.get_debug():
            viewer.flush_infos(
                column_1=self.__class__.__name__ + str(":"), column_2="play"
            )

        data = self.get_wave().readframes(self.get_chunk_size())

        while len(data) > 0:
            if len(data) > 0:
                self.get_stream().write(data)
            else:
                pass
            data = self.get_wave().readframes(self.get_chunk_size())
            # Display
            if self.get_verbose():
                # /tmp/tmpRqQsrP Wav,16 bit int,Mono,16KHz,29K
                viewer.flush_infos(
                    column_1=str(sec2time(time.time() - self.get_duration_start())),
                    status_text="PLAY",
                    status_text_color="GREEN",
                    status_symbol=">",
                    prompt=True,
                )

        if self.get_verbose():
            viewer.flush_a_new_line()

        if self.get_debug():
            viewer.flush_infos(
                column_1=self.__class__.__name__ + str(":"), column_2="stop"
            )
            viewer.flush_a_new_line()
        # Close Stream Pyaudio and Wave
        self.stream_close()

        return time.time() - self.get_duration_start()

    def play(self, filename=None, output_device_index=None):
        """
        Wrapper function for play in detached thread or not.

        If you let filename=None and have all ready set a ``wave_path`` with AudioPlayer.set_wave_path(), the function
        will use AudioPlayer.get_wave_path() as file. It permit to call it function without parameter.

        See: AudioPlayer.set_is_detached() for have influence on the choose

        :param filename: a file path
        :type filename: str
        :param output_device_index: a  index id as returned by pyaudio or None for get the sysdefault id
        :type output_device_index: int or None
        """
        if self.get_wave_path() is not None and filename is None:
            filename = self.get_wave_path()

        # Set the path
        self.set_wave_path(filename)

        # Store the wave object
        self.set_wave(wave.open(self.get_wave_path(), "rb"))

        # Set the format
        self.set_format(pyaudio.get_format_from_width(self.get_wave().getsampwidth()))
        # self.set_format(GLXAUDIO.FORMAT_FLOAT32)

        # Set the channel number
        self.set_channels(self.get_wave().getnchannels())

        # Set the Frame Rate
        self.set_rate(self.get_wave().getframerate())

        self.get_wave_informations(filename)

        if self.get_is_detached():
            if self.get_debug():
                viewer.flush_infos(
                    column_1=self.__class__.__name__ + str(":"),
                    column_2="detached mode is enable",
                )
            duration = self.play_detached(output_device_index=output_device_index)
        else:
            if self.get_debug():
                viewer.flush_infos(
                    column_1=self.__class__.__name__ + str(":"),
                    column_2="detached mode is disable",
                )
            duration = self.play_normal(output_device_index=output_device_index)

        self.close_pyaudio()
        self.close_wave()
        return duration

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

    def set_is_detached(self, value):
        """
        Set the Player will play sound on a detached thread.

        Note: In call back no debug information's are available

        Default True

        :param value: False for disable
        :type value: bool
        :raise TypeError: when ``value`` is not a bool type
        """
        # Exit as soon of possible
        if type(value) != bool:
            raise TypeError("'value' must be a bool type")

        # make the job in case
        if self.get_is_detached() != bool(value):
            self.is_detached = bool(value)

    def get_is_detached(self):
        """
        Return the number of channels as set by Audio.set_channel()

        :return: False is disable, True if enable
        :rtype: bool
        """
        return self.is_detached
