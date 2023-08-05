#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Radio Team, all rights reserved

# inspired by : https://stackoverflow.com/questions/18406570/python-record-audio-on-detected-sound
# inspired by : https://stackoverflow.com/questions/892199/detect-record-audio-in-python
# Inspired by : https://www.dk0tu.de/users/DL5BBN/Python_Amateur_Radio_Programs/
# Inspired by : https://www.swharden.com/wp/2016-07-19-realtime-audio-visualization-in-python/}

from glxaudio.Audio import Audio
from glxaudio.AudioUtils import get_format_to_dtype
from glxaudio.AudioUtils import clamp
from glxaudio.AudioUtils import sec2time
from glxaudio.AudioUtils import linear_to_db
from glxaudio.AudioConstants import GLXAUDIO
from glxviewer import viewer

from array import array
from struct import pack
from numpy import negative, abs, amax, amin

import copy
import wave
import time
import sys


class AudioRecorder(Audio):
    def __init__(self):
        Audio.__init__(self)

        self.threshold = None
        self.normalize_minus_one_db = None
        self.trim_to_append = None
        self.timeout_length = None
        self.duration_start = None
        self.verbose = True

        # set default value
        self.set_format(GLXAUDIO.FORMAT_INT16)
        self.set_channels(2)
        self.set_chunk_size(2048)
        self.set_rate(16000)
        self.set_trim_to_append(self.get_rate() / 10)

        self.set_timeout_length(3)

        # After that we set the threshold
        self.set_threshold(5)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_all()

    def is_silent(self, data_chunk):
        """ Returns 'True' if below the 'silent' threshold """
        return bool(max(data_chunk) < self.get_threshold())

    def normalize_minus_dot_one_db(self, data_all, dbfs=0.1):
        """
        Normalize a array to -0.1dB

        Standard" (non-dynamic) audio normalization algorithm applies the same constant amount of gain to all samples
        in ``data_all``

        :param dbfs: neg dBFS
        :rtype dbfs: float or int
        :param data_all: array from data you want normalize
        :type data_all: array
        :return: normalized array
        :rtype: array
        :raise TypeError: when ``value`` is not a bool type
        """
        # Inspired by: https://github.com/lordmulder/DynamicAudioNormalizer

        # Start
        # Exit as soon of possible
        if type(data_all) != array:
            raise TypeError("'data_all' must be a array type")

        # On debug we flush something
        if self.get_debug():
            viewer.flush_infos(
                column_1=self.__class__.__name__ + str(":"), column_2="normalize start"
            )

        # Variables
        signal_to_quantization_noise_ratio = 6.02 * get_format_to_dtype(
            self.get_format()
        )
        frame_db = (
                self.get_base_ten_signed_max_value() / signal_to_quantization_noise_ratio
        )
        frame_minus_dot_one_db = int(frame_db * dbfs)
        data_all_max = max(abs(i) for i in data_all)

        # On debug we flush something
        if self.get_debug():
            if self.get_debug_level() > 1:
                viewer.flush_infos(
                    column_1=self.__class__.__name__ + str(":"),
                    column_2="normalize SQNR "
                             + str(signal_to_quantization_noise_ratio)
                             + "dB, "
                             + "1dB = "
                             + str(int(frame_db))
                             + "frame(s), "
                             + "0.1dB = "
                             + str(frame_minus_dot_one_db)
                             + "frame(s), ",
                )

        try:
            # calculate how mush the value should be multiply
            normalize_factor = float(
                self.get_base_ten_signed_max_value() / data_all_max
            )

            # on debug we flush something
            # if self.get_debug():
            #     viewer.flush_infos(
            #         column_1=self.__class__.__name__ + str(':'),
            #         column_2='normalize max found ' + str(int(self.get_db_from_chunk(array('h', [data_all_max])))) + 'dB' +
            #                  ', factor ' + str(normalize_factor)
            #     )

            value_to_return = array("h")
            count = 1

            for i in data_all:
                # prevent a OverflowError: signed short integer is less than minimum
                value_to_append = clamp(
                    value=int((i * normalize_factor) - frame_minus_dot_one_db),
                    smallest=self.base_ten_signed_min_value,
                    largest=self.base_ten_signed_max_value,
                )
                # append the value
                value_to_return.append(value_to_append)
                count += 1
                # This not a debug this, that is a true display
                if self.get_verbose() and self.get_verbose_level() == 2:
                    viewer.flush_infos(
                        status_text="WORK",
                        status_text_color="YELLOW",
                        column_1="normalize elements "
                                 + str("%0.2f" % ((count * 100) / len(data_all)))
                                 + "%          ",
                        prompt=-1,
                    )

            # Stop
            # On debug we flush something
            if self.get_debug():
                viewer.flush_infos(
                    column_1=self.__class__.__name__ + str(":"),
                    column_2="normalize stop",
                )

            # Normal return
            return value_to_return

        # Troubles
        except ZeroDivisionError:
            # we flush something in case
            if self.get_debug():
                viewer.flush_infos(
                    column_1=self.__class__.__name__ + str(":"),
                    column_2="normalize nothing have been normalize due to a ZeroDivisionError",
                )
                viewer.flush_infos(
                    column_1=self.__class__.__name__ + str(":"),
                    column_2="normalize stop",
                )
            # Return untouched value
            return data_all

        except ValueError:
            # we flush something in case
            if self.get_debug():
                viewer.flush_infos(
                    column_1=self.__class__.__name__ + str(":"),
                    column_2="normalize nothing have been normalize due to a ValueError",
                )
                viewer.flush_infos(
                    column_1=self.__class__.__name__ + str(":"),
                    column_2="normalize stop",
                )
            # Return untouched value
            return data_all

    def trim(self, data_all, attack=0.115, release=0.650, release_knee=0.2):
        """
        Trim data_all found silence's start/stop and return a data_all without they silence.

        In addition it prepend a certain amount of time in sec (estimate via frame rate) via ``attack`` parameter.

        ``release`` will append a certain amount of time in sec (estimate via frame rate).

        Both ``attack`` and ``release`` are estimated by use ``threshold`` (see: set_threshold() and getet_threshold())
        the ``release`` is special case where nobody like have a message cut hardly in center of the message. For that
        a attenuation factor call 'knee' will be apply to ``threshold`` during the release phase calculation.

        :param data_all: a record
        :type data_all: array
        :param attack: time to prepend in second , it use as factor of frame rate setting.
        :type attack: int or float
        :param release: time to append in second , it use as factor of frame rate setting.
        :type release: int or float
        :param release_knee:  threshold factor, use during the release. 0.2 will consider to reduse of 20% of the \
        actual threshold during the release phase.
        :type release_knee: int or float
        :return: deep copy operation on arbitrary Python objects
        :rtype: array
        :raise TypeError: when ``data_all`` is not a array type
        :raise TypeError: when ``attack`` is not a int or float type
        :raise TypeError: when ``release`` is not a int or float type
        :raise TypeError: when ``release_knee`` is not a int or float type
        """
        # Exit as soon of possible
        # It should have a really good reason to work :)
        if type(data_all) != array:
            raise TypeError("'data_all' must be a array type")

        if type(attack) != int and type(attack) != float:
            raise TypeError("'attack' must be a int or float type")

        if type(release) != int and type(release) != float:
            raise TypeError("'release' must be a int or float type")

        if type(release_knee) != int and type(release_knee) != float:
            raise TypeError("'release_knee' must be a int or float type")

        # Start
        trim_from = 0
        trim_to = len(data_all) - 1

        # On debug we flush something
        if self.get_debug():
            if self.get_debug_level() > 1:
                viewer.flush_infos(
                    column_1=self.__class__.__name__ + str(":"), column_2="trim start"
                )
            viewer.flush_infos(
                column_1=self.__class__.__name__ + str(":"),
                column_2="trim searching start",
            )

        # From
        for i, b in enumerate(data_all):
            if abs(b) > self.get_threshold():
                trim_from = max(0, i - int(attack * self.get_rate()))
                # trim_from -= int(attack * self.get_rate())

                if self.get_debug():
                    viewer.flush_infos(
                        column_1=self.__class__.__name__ + str(":"),
                        column_2="trim found start at "
                                 + str(sec2time(int(trim_from / self.get_rate()), 3)),
                    )
                break

        # To
        count = 1
        for i, b in enumerate(reversed(data_all)):
            if abs(b) > self.get_threshold() * release_knee:
                trim_to = min(
                    len(data_all) - 1,
                    len(data_all) - 1 - i + int(release * self.get_rate()),
                )
                # trim_to += int(release * self.get_rate())
                if self.get_debug():
                    viewer.flush_infos(
                        column_1=self.__class__.__name__ + str(":"),
                        column_2="trim found end at  "
                                 + str(
                            sec2time(
                                int(
                                    (len(data_all) / self.get_rate())
                                    - (count / self.get_rate())
                                )
                            )
                        ),
                    )
                    viewer.flush_infos(
                        column_1=self.__class__.__name__ + str(":"),
                        column_2="trim found end at  "
                                 + str(sec2time(int(trim_to / self.get_rate()))),
                    )
                break
            count += 1

        # End of trim on debug mode we flush something
        if self.get_debug():
            if self.get_debug_level() > 1:
                viewer.flush_infos(
                    column_1=self.__class__.__name__ + str(":"), column_2="trim stop"
                )

        return copy.deepcopy(data_all[int(trim_from): int((trim_to + 1))])

    def read_next_chunk(self):
        next_chunk = array(
            "h",
            self.get_stream().read(self.get_chunk_size(), exception_on_overflow=False),
        )

        if sys.byteorder == "big":
            next_chunk.byteswap()

        return next_chunk

    def record(self, input_device_index=None):
        """
        Record a word or words from the microphone and return the data as an array of signed shorts.

        :return: the recoded file on array form
        :rtype: array.array
        """

        if input_device_index is None:
            input_device_index = self.get_sysdefault_id()

        self.set_stream(
            self.create_audio().open(
                format=self.get_format(),
                channels=self.get_channels(),
                rate=self.get_rate(),
                input=True,
                input_device_index=input_device_index,
                frames_per_buffer=self.get_chunk_size(),
            )
        )

        self.get_stream().start_stream()

        silent_chunks_counter = 0
        audio_started = False
        data_all = array("h")

        self.set_duration_start()

        if self.get_debug():
            viewer.flush_infos(
                column_1=self.__class__.__name__ + str(":"),
                column_2="waiting for audio signal ...",
            )

        while self.get_stream().is_active():
            data_chunk = self.read_next_chunk()
            data_all.extend(data_chunk)

            if not audio_started:

                # We display something, this is not a exercise !!!
                if self.get_verbose():
                    mic = "%0.2f" % (self.get_db_from_chunk(data_chunk))
                    viewer.flush_infos(
                        status_text="WAIT",
                        status_text_color="WHITE2",
                        column_1=str(mic) + "dBFS, sample(s)" + str(max(data_chunk)),
                        prompt=True,
                    )

            if audio_started:
                if self.get_verbose():
                    viewer.flush_infos(
                        column_1=str(sec2time(time.time() - self.get_duration_start())),
                        status_text="REC",
                        status_text_color="RED",
                        status_symbol="<",
                        prompt=True,
                    )

                # LA
                if max(data_chunk) < self.get_threshold() * 0.5:
                    silent_chunks_counter += 1
                    if silent_chunks_counter > self.get_timeout_length():
                        # break
                        self.get_stream().stop_stream()
                else:
                    silent_chunks_counter = 0

            elif not self.is_silent(data_chunk):
                if self.get_debug() and self.get_debug_level() > 1:
                    viewer.flush_infos(
                        column_1=self.__class__.__name__ + str(":"),
                        column_2="record start",
                    )

                audio_started = True
                self.set_duration_start()

        if self.get_verbose():
            viewer.flush_a_new_line()

        if self.get_debug() and self.get_debug_level() > 1:
            viewer.flush_infos(
                column_1=self.__class__.__name__ + str(":"), column_2="record stop"
            )

        # we trim before normalize as threshold applies to un-normalized wave (as well as is_silent() function)
        data_all = self.trim(data_all)
        data_all = self.normalize_minus_dot_one_db(data_all)

        return data_all

    def record_to_file(self, filename=None, input_device_index=None):
        """
        Wrapper function for record in detached thread or not.

        If you let filename=None and have all ready set a ``wave_path`` with AudioPlayer.set_wave_path(), the function
        will use AudioPlayer.get_wave_path() as file. It permit to call it function without parameter.

        See: AudioPlayer.set_is_detached() for have influence on the choose

        :param filename: a destination file path
        :type filename: str
        :param input_device_index: a  index id as returned by arecord -L or None for get the sysdefault id
        :type input_device_index: int or None
        """
        if self.get_wave_path() is not None and filename is None:
            filename = self.get_wave_path()

        if filename is not None:
            self.set_wave_path(filename)

        if self.get_debug():
            viewer.flush_infos(
                column_1="AudioRecorder: record "
                         + str(self.get_wave_path())
                         + " in normal mode"
            )
        data = self.record(input_device_index=input_device_index)

        data = pack("<" + ("h" * len(data)), *data)

        # Debug information's
        if self.get_debug():
            viewer.flush_infos(
                column_1=self.__class__.__name__ + str(":"), column_2="save file"
            )

        self.set_wave_path(filename)

        self.set_wave(wave.open(self.get_wave_path(), "wb"))

        self.get_wave().setnchannels(self.get_channels())
        self.get_wave().setsampwidth(self.get_sample_width())
        self.get_wave().setframerate(self.get_rate())
        self.get_wave().writeframes(data)

        self.get_wave_informations(self.get_wave_path())

        # Close everything
        self.stream_close()

    def set_threshold(self, threshold=10):
        """
        Set the noise gate Threshold

        :param threshold: noise gates attenuate signals that register below the threshold in percentage
        :type threshold: int or float
        :raise TypeError: when "threshold" argument is not a :py:data:`int` or :py:data:`float`
        """
        # Exit as soon of possible
        if type(threshold) != int and type(threshold) != float:
            raise TypeError("'threshold' must be a int or float type")

        new = self.get_base_ten_signed_max_value() * threshold / 100

        if self.get_threshold() != new:
            self.threshold = new

        max_allowed = abs(self.get_base_ten_signed_max_value()).astype(self.get_dtype())
        peak = self.get_threshold() / max_allowed

        if self.get_threshold() <= 0:
            display = float(
                "{:0.2f}".format(
                    negative(linear_to_db(self.get_base_ten_signed_max_value()))
                )
            )
        else:
            display = float("{:0.2f}".format(linear_to_db(peak)))

        if self.get_debug():
            viewer.flush_infos(
                column_1=self.__class__.__name__ + str(":"),
                column_2="threshold "
                         + str(display)
                         + "dBFS, "
                         + str(self.get_threshold())
                         + " sample(s)",
            )

    def get_threshold(self):
        """
        Get the noise gate Threshold

        :return: noise gates attenuate signals that register below the threshold
        :rtype: int
        """
        return self.threshold

    def set_threshold_db(self, threshold=-54):
        """
        Set the noise gate Threshold

        :param threshold: noise gates attenuate signals that register below the threshold in percentage
        :type threshold: int or float
        :raise TypeError: when "threshold" argument is not a :py:data:`int` or :py:data:`float`
        """
        # Exit as soon of possible
        if type(threshold) != int and type(threshold) != float:
            raise TypeError("'threshold' must be a int or float type")

        # make the job in case
        threshold = abs(threshold)
        # 6dB set
        threshold = int((threshold * 6) * self.frame_max_amplitude - 1)
        threshold = self.base_ten_signed_max_value - clamp(
            value=threshold, smallest=0, largest=self.get_base_ten_signed_max_value()
        )
        if self.get_debug():
            viewer.flush_infos(
                column_2="AudioRecorder: max frame: "
                         + str(self.base_ten_signed_max_value)
                         + ", "
                         + "threshold: "
                         + str(threshold)
            )

        if self.get_threshold() != threshold:
            self.threshold = threshold

    def set_trim_to_append(self, trim_to_append):
        """
        A number of frame to prepend and append during the trim frunction call

        :param trim_to_append: Maximal recording time in sec
        :type trim_to_append: int or float
        """
        # Exit as soon of possible
        if type(trim_to_append) != int and type(trim_to_append) != float:
            raise TypeError("'trim_to_append' must be a int or float type")

        # make the job in case
        if self.get_trim_to_append() != int(trim_to_append):
            self.trim_to_append = int(trim_to_append)

    def get_trim_to_append(self):
        """
        Return the timeout_length as set by AudioRecorder.set_timeout_length()

        :return: Maximal recording time in sec.
        :rtype: int or float
        """
        return self.trim_to_append

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

    def set_timeout_length(self, timeout_length):
        """
        The time when automatically stop the recording.

        Note when the timeout can be disable

        :param timeout_length: Maximal recording time in sec
        :type timeout_length: int or float
        """
        # Exit as soon of possible
        if type(timeout_length) != int and type(timeout_length) != float:
            raise TypeError("'timeout_length' must be a int or float type")

        # make the job in case
        if (
                self.get_timeout_length()
                != timeout_length * self.get_rate() / self.get_chunk_size()
        ):
            self.timeout_length = (
                    timeout_length * self.get_rate() / self.get_chunk_size()
            )

    def get_timeout_length(self):
        """
        Return the timeout_length as set by AudioRecorder.set_timeout_length()

        :return: Maximal recording time in sec.
        :rtype: int or float
        """
        return self.timeout_length
