#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Radio Team, all rights reserved
import shutil
import numpy
import sys
import os
from GLXAudio.Audio import Audio
from GLXAudio.AudioConstants import GLXAUDIO


class AudioSpectrogram(Audio):
    def __init__(self, output_device_index=None):
        Audio.__init__(self)
        if output_device_index is None:
            self.output_device_index = self.get_sysdefault_id()
        else:
            self.output_device_index = output_device_index

        self.set_format(GLXAUDIO.FORMAT_INT16)
        self.set_rate(22050)
        self.set_channels(1)
        self.set_chunk_size(int(self.get_rate() * 0.030))

        self.colors_gradient = list()
        self.colors = 30, 34, 35, 91, 93, 97
        # http://www.remycorthesy.fr/montpellier/symboles-codes-caracteres-ascii-iso.htm
        self.chars = " ░▒▓\t▓▒░"
        # self.chars = ' ·•+†‡\t‡†+•·'
        # self.chars = ' ·•+|‖\t‖|+•·'
        # self.chars = ' ·•׀|t\‖|׀•·'
        # self.chars = ' :%#\t#%:'
        # self.chars = ' ·•ǀ|‖\t‖|ǀ•·'
        self.boost = 0.001
        self.nband_param = 4

    def __enter__(self):
        """Open the microphone stream."""
        self.set_stream(
            self.create_audio().open(
                format=self.get_format(),
                channels=self.get_channels(),
                rate=self.get_rate(),
                input=True,
                input_device_index=self.output_device_index,
                frames_per_buffer=self.get_chunk_size(),
            )
        )

        for bg, fg in zip(self.colors, self.colors[1:]):
            for char in self.chars:
                if char == "\t":
                    bg, fg = fg, bg
                else:
                    self.colors_gradient.append(
                        "\x1b[{};{}m{}".format(fg, bg + 10, char)
                    )

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stream_close()

    def color(self, x):
        """
        Given 0 <= x <= 1 (input is clamped), return a string of ANSI
        escape sequences representing a colors_gradient color.
        """
        x = max(0.0, min(1.0, x))
        return self.colors_gradient[int(x * (len(self.colors_gradient) - 1))]

    def listen(self):
        """Listen for one buffer of audio and print a colors_gradient."""
        block_string = self.get_stream().read(
            self.get_chunk_size(), exception_on_overflow=False
        )
        # block = numpy.fromstring(block_string, dtype=self.get_dtype()) / self.get_base_ten_signed_max_value()
        block = numpy.fromstring(block_string, dtype=self.get_dtype())

        nbands = self.nband_param * shutil.get_terminal_size()[0]
        fft = abs(numpy.fft.fft(block, n=nbands))

        pos, neg = numpy.split(fft, 2)
        bands = (pos + neg[::-1]) / float(nbands) * self.boost

        line = (self.color(x) for x in bands[: shutil.get_terminal_size()[0]])

        sys.stdout.write("".join(line) + "\x1b[0m")
        # sys.stdout.write('\auto_gain_control_queue_size')
        sys.stdout.flush()


if __name__ == "__main__":
    # Do a basic screen clear.
    os.system("clear")
    # Turn the cursor off to look prettier... ;o)
    os.system("setterm -cursor off")

    spectrogram = AudioSpectrogram()
    try:
        while True:
            spectrogram.listen()
    except KeyboardInterrupt:
        if bool(spectrogram.get_stream()):
            spectrogram.get_stream().stop_stream()
            spectrogram.get_stream().close()
        if bool(spectrogram.get_audio()):
            spectrogram.get_audio().terminate()
        sys.exit(0)

    # with AudioSpectrogram() as spectrogram:
    #     try:
    #         while True:
    #             spectrogram.listen()
    #     except KeyboardInterrupt:
    #         if bool(spectrogram.get_stream()):
    #             spectrogram.get_stream().stop_stream()
    #             spectrogram.get_stream().close()
    #         if bool(spectrogram.get_audio()):
    #             spectrogram.get_audio().terminate()
    #         sys.exit(0)
