#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Radio Team, all rights reserved

import audioop
import contextlib
import os
import sys
import wave

import numpy as np
from numpy import negative

from glxaudio.AudioConstants import GLXAUDIO
from glxaudio.AudioInterfaces import AudioInterfaces
from glxaudio.AudioUtils import get_format_to_dtype
from glxaudio.AudioUtils import get_format_to_human_view
from glxaudio.AudioUtils import get_quantification
from glxaudio.AudioUtils import linear_to_db
from glxaudio.AudioUtils import sizeof
from glxaudio.Object import Object
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


try:
    with ignore_stderr():
        import pyaudio
except ImportError:
    raise AttributeError("Could not find PyAudio check installation")

from distutils.version import LooseVersion

if LooseVersion(pyaudio.__version__) < LooseVersion("0.2.11"):
    raise AttributeError(
        "PyAudio 0.2.11 or later is required (found version {})".format(
            pyaudio.__version__
        )
    )

from glxaudio.EventBus import EventBusClient


class Audio(Object, AudioInterfaces, EventBusClient):
    def __init__(self):
        Object.__init__(self)
        AudioInterfaces.__init__(self)
        EventBusClient.__init__(self)

        self.format = None
        self.rate = None
        self.channels = None
        self.base_ten_signed_max_value = None
        self.base_ten_signed_min_value = None
        self.frame_min_amplitude = None
        self.frame_max_amplitude = None
        self.chunk_size = None
        # self.chunk = None
        self.stream = None
        self.dtype = None
        self.sample_width = None
        self.wave = None
        self.wave_path = None
        self.audio = None
        self.application = None
        self.support_galaxie_curses = None

        if self.get_debug() and self.get_debug_level() > 2:
            viewer.flush_infos(
                column_1=self.__class__.__name__ + str(":"),
                column_2="PyAudio {0}, PortAudio {1} ".format(
                    pyaudio.__version__, pyaudio.get_portaudio_version()
                ),
            )

    def stream_close(self):
        """ Close the stream"""
        # Close stream
        if type(self.get_stream()) == pyaudio.Stream:
            # Stop
            if self.get_debug() and self.get_debug_level() > 2:
                viewer.flush_infos(
                    column_1=self.__class__.__name__ + str(":"),
                    column_2="stop " + str(self.get_stream())[1:-1],
                )

            self.get_stream().stop_stream()

        # Close
        if self.get_debug() and self.get_debug_level() > 2:
            viewer.flush_infos(
                column_1=self.__class__.__name__ + str(":"),
                column_2="close " + str(self.get_stream())[1:-1],
            )

    def stream_start(self):
        """start a stream"""
        if type(self.get_stream()) == pyaudio.Stream:
            self.get_stream().start_stream()

        if self.get_debug():
            if type(self.get_stream()) == pyaudio.Stream:
                if self.get_stream().is_active():
                    viewer.flush_infos(
                        column_1=self.__class__.__name__ + str(":"),
                        column_2="start " + str(self.get_stream())[1:-1],
                    )

    def stream_stop(self):
        """stop a stream"""
        if type(self.get_stream()) == pyaudio.Stream:
            self.get_stream().stop_stream()

        if self.get_debug():
            if type(self.get_stream()) == pyaudio.Stream:
                if not self.get_stream().is_active():
                    viewer.flush_infos(
                        column_1=self.__class__.__name__ + str(":"),
                        column_2="stop " + str(self.get_stream())[1:-1],
                    )

    def close_wave(self):
        # Close Wave
        if (
                type(self.get_wave()) == wave.Wave_read
                or type(self.get_wave()) == wave.Wave_write
        ):
            if self.get_debug() and self.get_debug_level() > 2:
                viewer.flush_infos(
                    column_1=self.__class__.__name__ + str(":"),
                    column_2="close " + str(self.get_wave())[1:-1],
                )
            self.get_wave().close()

    def close_pyaudio(self):
        # Close pyaudio
        if type(self.get_audio()) == pyaudio.PyAudio:

            if self.get_debug() and self.get_debug_level() > 2:
                viewer.flush_infos(
                    column_1=self.__class__.__name__ + str(":"),
                    column_2="close " + str(self.get_audio())[1:-1],
                )
            self.get_audio().terminate()

    def close_all(self):
        self.stream_close()
        self.close_wave()
        self.close_pyaudio()

    def create_audio(self):
        with ignore_stderr():
            # instantiate PyAudio only here and never where else
            self.audio = pyaudio.PyAudio()
            if type(self.get_audio()) == pyaudio.PyAudio:

                if self.get_debug() and self.get_debug_level() > 2:
                    viewer.flush_infos(
                        column_1=self.__class__.__name__ + str(":"),
                        column_2="create " + str(self.get_audio())[1:-1],
                    )

        return self.audio

    def get_audio(self):
        return self.audio

    def set_format(self, audio_format):
        """
        Set the PaSampleFormat Sample Formats

        valid GLXAUDIO.AUDIO_FORMATS:
         * GLXAUDIO.FORMAT_FLOAT32 for 32 bit float
         * GLXAUDIO.AUDIO_FORMAT_INT32 for 32 bit int
         * GLXAUDIO.AUDIO_FORMAT_INT24 for 24 bit int
         * GLXAUDIO.AUDIO_FORMAT_INT16 for 16 bit int
         * GLXAUDIO.AUDIO_FORMAT_INT8 for 8 bit int
         * GLXAUDIO.AUDIO_FORMAT_UINT8 for 8 bit unsigned int
         * GLXAUDIO.AUDIO_FORMAT_CUSTOM for a custom data format

        :param audio_format: Sampling size and format. PaSampleFormat Sample Formats contain in GLXAUDIO.AUDIO_FORMATS
        :type audio_format: int
        :raise TypeError: when "audio_format" argument is not a valid int contain on GLXAUDIO.AUDIO_FORMATS
        """
        # Exit as soon of possible
        if audio_format not in GLXAUDIO.FORMATS:
            raise TypeError("'audio_format' must be a valid GLXAUDIO.AUDIO_FORMATS")

        # make the job in case
        if self.get_format() != audio_format:
            self.format = audio_format

        neg, pos, amplitude = get_quantification(get_format_to_dtype(audio_format))
        if self.base_ten_signed_min_value != neg:
            self.base_ten_signed_min_value = neg
        if self.base_ten_signed_max_value != pos:
            self.base_ten_signed_max_value = pos
        if self.frame_min_amplitude != 0:
            self.frame_min_amplitude = 0
        if self.frame_max_amplitude != amplitude:
            self.frame_max_amplitude = amplitude

        # paFloat32 = 1
        # 32 bit float
        if audio_format == GLXAUDIO.FORMAT_FLOAT32:
            self.set_dtype(np.float32)
            self.set_sample_width(pyaudio.get_sample_size(audio_format))

        # paInt32 = 2
        # 32 bit int
        if audio_format == GLXAUDIO.FORMAT_INT32:
            self.set_dtype(np.int32)
            self.set_sample_width(pyaudio.get_sample_size(audio_format))

        # paInt24 = 4
        # 24 bit int
        if audio_format == GLXAUDIO.FORMAT_INT24:
            self.set_dtype(np.int32)
            self.set_sample_width(pyaudio.get_sample_size(audio_format))

        # paInt16 = 8
        #: 16 bit int
        if audio_format == GLXAUDIO.FORMAT_INT16:
            self.set_dtype(np.int16)
            self.set_sample_width(pyaudio.get_sample_size(audio_format))

        # paInt8 = 16
        # #: 8 bit int
        if audio_format == GLXAUDIO.FORMAT_INT8:
            self.set_dtype(np.int8)
            self.set_sample_width(pyaudio.get_sample_size(audio_format))

        # paUInt8 = 32
        #: 8 bit unsigned int
        if audio_format == GLXAUDIO.FORMAT_UINT8:
            self.set_dtype(np.uint8)
            self.set_sample_width(pyaudio.get_sample_size(audio_format))

        if audio_format == GLXAUDIO.FORMAT_CUSTOM:
            self.set_dtype(np.int32)
            self.set_sample_width(4)

    def get_format(self):
        """
        Get the PaSampleFormat Sample Formats

        :return: a valid GLXAUDIO.AUDIO_FORMATS
        :rtype: int
        """
        return self.format

    def set_sample_width(self, sample_width=2):
        """
        Set the sample width to ``sample_width`` bytes

        Default 2

        :param sample_width: The desired sample width in bytes (1, 2, 3, or 4)
        :rtype: int
        """
        if sample_width not in [1, 2, 3, 4]:
            raise TypeError("'sample_width' must be a 1, 2, 3 or 4")

        # make the job in case
        if self.get_sample_width() != sample_width:
            self.sample_width = sample_width

    def get_sample_width(self):
        """
        Returns sample width in bytes.

        :return: sample width in bytes
        :rtype: int
        """
        return self.sample_width

    def set_dtype(self, dtype=np.int16):
        """
        numpy dtype to use, see Audio.set_format()


        :param dtype: numpy dtype
        :type dtype: dtype
        :raise TypeError: when ``dtype`` argument is not a numpy.uint8, numpy.int8, \
        numpy.int16, numpy.int32, numpy.float32
        """
        # Exit as soon of possible
        if dtype not in [np.uint8, np.int8, np.int16, np.int32, np.float32]:
            raise TypeError(
                "'dtype' must be a numpy.uint8, numpy.int8, numpy.int16, numpy.int32, numpy.float32 type"
            )

        # make the job in case
        if self.get_dtype() != dtype:
            self.dtype = dtype

    def get_dtype(self):
        """
        Return the numpy dtype to use, as impose by Audio.set_format()

        :return: numpy dtype
        :rtype: numpy.uint8 or numpy.int8 or numpy.int16 or numpy.int32 or numpy.float32
        """
        return self.dtype

    def set_channels(self, channels):
        """
        Set the number of channel of the audio to play or record, depends of audio you want.

        Generally that set to 1 for Mono and 2 for Stereo.

        :param channels: Number of channels
        :type channels: int
        """
        # Exit as soon of possible
        if type(channels) != int:
            raise TypeError("'channels' must be a int type")

        # make the job in case
        if self.get_channels() != channels:
            self.channels = channels

    def get_channels(self):
        """
        Return the number of channels as set by Audio.set_channel()

        :return: channels number
        :rtype: int
        """
        return self.channels

    def set_rate(self, rate):
        """
        Set Sample rate.

        A commonly seen measure of sampling is S/s, which stands for "samples per second".
        As an example, 1 MS/s is one million samples per second.

        :param rate: The sample rate like 8000 11025 16000 22050 32000 37800 44056 44100 47250 48000 in Hz
        :type rate: int
        """
        # Exit as soon of possible
        if type(rate) != int:
            raise TypeError("'rate' must be a int type")

        # make the job in case
        if self.get_rate() != rate:
            self.rate = rate

    def get_rate(self):
        """
        Return the Sampling rate as set by Audio.set_rate()

        :return: The sample rate like 8000 11025 16000 22050 32000 37800 44056 44100 47250 48000 in Hz
        :rtype: int
        """
        return self.rate

    def set_base_ten_signed_max_value(self, max_value=None):
        """
        The max frame is generally the ``pos`` value impose by the audio format.

        See Audio.set_format() for more details.

        Here few examples:

        # Code in 8 bits = 2 puissant 8
         (neg, -128), (pos, 127), (amplitude, 48)

        # Code in 16 bits = 2 puissant 16
         (neg, -32768), (pos, 32767), (amplitude, 96)

        # Code in 20 bits = 2 puissant 20
         (neg, -524288), (pos, 524287), (amplitude, 120)

        # Code in 24 bits = 2 puissant 24
         (neg, -8388608), (pos, 8388607), (amplitude, 144)

        # Code in 32 bits = 2 puissant 32
         (neg, -2147483648), (pos, 2147483647), (amplitude, 192)

        :param max_value: the max value of Base-ten signed range (per sample)
        :type max_value: int
        """
        # Exit as soon of possible
        if type(max_value) != int:
            raise TypeError("'max_frame_value' must be a int type")

        # make the job in case
        if self.get_base_ten_signed_max_value() != max_value:
            self.base_ten_signed_max_value = max_value

    def get_base_ten_signed_max_value(self):
        """
        Return Base-ten signed range (per sample) as impose by Audio.set_format()

        See: Audio.set_frame_max_value()

        :return: something like 32767 for 16bit audio format (per sample)
        :rtype: int
        """
        return self.base_ten_signed_max_value

    def set_base_ten_signed_min_value(self, min_value=None):
        """
        The max frame is generally the ``neg`` value impose by the audio format.

        See Audio.set_format() for more details.

        Here few examples:

        # Code in 8 bits = 2 puissant 8
         (neg, -128), (pos, 127), (amplitude, 48)

        # Code in 16 bits = 2 puissant 16
         (neg, -32768), (pos, 32767), (amplitude, 96)

        # Code in 20 bits = 2 puissant 20
         (neg, -524288), (pos, 524287), (amplitude, 120)

        # Code in 24 bits = 2 puissant 24
         (neg, -8388608), (pos, 8388607), (amplitude, 144)

        # Code in 32 bits = 2 puissant 32
         (neg, -2147483648), (pos, 2147483647), (amplitude, 192)

        :param min_value: The max frame as impose by Audio.set_format() (per sample)
        :type min_value: int
        """
        # Exit as soon of possible
        if type(min_value) != int:
            raise TypeError("'min_value' must be a int type")

        # make the job in case
        if self.get_base_ten_signed_min_value() != min_value:
            self.base_ten_signed_min_value = min_value

    def get_base_ten_signed_min_value(self):
        """
        Return Base-ten signed range (per sample) impose by Audio.set_format()

        See: Audio.set_frame_min_value()

        :return: something like -32768 for 16bit audio format (per sample)
        :rtype: int
        """
        return self.base_ten_signed_min_value

    def set_chunk_size(self, chunk_size):
        """
        Specifies the number of frames per buffer.

        :param chunk_size: Block size.
        :type chunk_size: int
        """
        # Exit as soon of possible
        if type(chunk_size) != int:
            raise TypeError("'chunk_size' must be a int type")

        # make the job in case
        if self.get_chunk_size() != chunk_size:
            self.chunk_size = chunk_size

    def get_chunk_size(self):
        """
        Return the ``chunk_size`` as set by Audio.set_frames_per_buffer()

        :return: Block size.
        :rtype: int
        """
        return self.chunk_size

    def set_stream(self, stream):
        """
        Set the stream, that permit to store a pyaudio.Stream

        :param stream: Pyaudio Stream
        :type stream: pyaudio.Stream
        """
        if not isinstance(stream, pyaudio.Stream):
            raise TypeError("'stream' must be a pyaudio.Stream instance")

        if self.get_stream() != stream:
            self.stream = stream

            if type(self.get_stream()) == pyaudio.Stream:
                if self.get_debug() and self.get_debug_level() > 2:
                    viewer.flush_infos(
                        column_1=self.__class__.__name__ + str(":"),
                        column_2="create " + str(self.get_stream())[1:-1],
                    )

    def get_stream(self):
        """
        Return the stream, as store by Audio.set_stream()

        :return: PyAudio Stream
        :rtype: pyaudio.Stream
        """
        return self.stream

    def set_wave(self, wav):
        """
        Store a ``wave`` object as return by wave.open() .

        It function is call by AudioPlayer.get_wave_setting()

        :param wav: A wave object
        :type wav: wave.Wave_read or wave.Wave_write
        :raise TypeError: when ``wav`` argument is not a :py:data:`wave`
        """
        # exit as soon of possible
        if not isinstance(wav, wave.Wave_write) and not isinstance(wav, wave.Wave_read):
            raise TypeError("'wav' must be a valid wave.Wave_read or  wave.Wave_read ")

        # make the job in case
        if self.get_wave() != wav:
            self.wave = wav
            if (
                    type(self.get_wave()) == wave.Wave_write
                    or type(self.get_wave()) == wave.Wave_read
            ):

                if self.get_debug() and self.get_debug_level() > 2:
                    viewer.flush_infos(
                        column_1=self.__class__.__name__ + str(":"),
                        column_2="create " + str(self.get_wave())[1:-1],
                    )

    def get_wave(self):
        """
        Get wave object as set by AudioPlayer.set_wave()

        :return: A wav object
        :rtype: wave.Wave_read or wave.Wave_write
        """
        return self.wave

    def set_wave_path(self, file_path=None):
        """
        Set the path of the audio fileq to read.

        Default: None

        When you use it function the file existence and require permission's will be tested.

        In case of trouble that raise a error. Typically test file existence and read access

        See: AudioPlayer.get_file_path() for get back the value

        :param file_path: The Queue Size
        :type file_path: str
        :raise TypeError: when ``wave_path`` argument is not a :py:data:`string`
        :raise IOError: when ``wave_path`` does not exist
        :raise IOError: when ``wave_path`` is not file
        :raise IOError: when ``wave_path`` can't be read
        """
        # Exit as soon of possible
        if type(file_path) != str:
            raise TypeError("'wave_path' must be a str type")

        if not os.path.exists(os.path.realpath(file_path)):
            raise FileNotFoundError("'wave_path' does not exist")

        if not os.access(os.path.realpath(file_path), os.R_OK):
            raise IOError("'%s' can't be read" % file_path)

        if not os.path.isfile(os.path.realpath(file_path)):
            raise IOError("'wave_path' must be a file")

        # make the job in case
        if self.get_wave_path() != os.path.realpath(file_path):
            self.wave_path = os.path.realpath(file_path)

    def get_wave_path(self):
        return self.wave_path

    def get_wave_informations(self, filename):
        # Debug information
        if self.get_debug() and self.get_debug_level() > 1:
            sample_format = get_format_to_human_view(self.get_format())

            viewer.flush_infos(
                column_1=self.__class__.__name__ + ":",
                column_2="file: " + str(filename),
            )
            viewer.flush_infos(
                column_1=self.__class__.__name__ + ":",
                column_2="format: "
                         + str(sample_format)
                         + ", size: "
                         + sizeof(os.path.getsize(filename)),
            )
            viewer.flush_infos(
                column_1=self.__class__.__name__ + ":",
                column_2="rate: "
                         + str(self.get_rate())
                         + "Hz"
                         + ", length: "
                         + str(self.get_wave().getnframes()),
            )
            viewer.flush_infos(
                column_1=self.__class__.__name__ + ":",
                column_2="channels: "
                         + str(self.get_channels())
                         + ", sample width: "
                         + str(self.get_wave().getsampwidth()),
            )

    def get_db_from_chunk(self, data_chunk):
        """
        Return a value in Decibel, with quantification

        Note that is dB from calculation, not true SPL meter, consider that as dB value of a peak meter.

        Example:
         * for a 16bit int format the amplitude can go as high as 32767.
         * if you have a wave that peaks at 14731

         amplitude = 14731 / 32767 = 0.44
         dB = 20 * log10(0.44) = -7.13

         amplitude = 14731 / 32767 = 0,449568163
         dB = 20 * log10(0.44) = -6.93

         Equations in log base 10:

         linear-to-db(x) = log(x) * 20
         db-to-linear(x) = 10^(x / 20)

        :param data_chunk: a Array with value inside
        :type data_chunk: numpy.array
        :return: dB from calculation
        :rtype: float
        """
        # peaks = float(max(data_chunk))
        # np.amax(data_chunk)

        # maximum = np.abs(np.amax(data_chunk)).astype(self.get_dtype())
        # maximum = self.get_average_intensities_from_chunk(data_chunk)
        maximum = np.abs(audioop.avg(data_chunk, self.get_sample_width())).astype(
            self.get_dtype()
        )
        max_allowed = np.abs(self.get_base_ten_signed_max_value()).astype(
            self.get_dtype()
        )
        peak = maximum / max_allowed

        if maximum <= 0:
            return float(
                "{:0.2f}".format(
                    negative(linear_to_db(self.get_base_ten_signed_max_value()))
                )
            )
        else:
            return float("{:0.2f}".format(linear_to_db(peak)))

    def get_average_intensities_from_chunk(self, data_chunk, sample_width=None):
        """
        Gets average audio intensity of your mic sound. You can use it to get
        average intensities while you're talking and/or silent. The average
        is the avg of the 20% largest intensities recorded.

        :rtype: float
        """

        if sample_width is None:
            sample_width = self.get_sample_width()

        return np.sqrt(
            np.abs(audioop.avg(data_chunk, sample_width)).astype(self.get_dtype())
        ).astype(self.get_dtype())
