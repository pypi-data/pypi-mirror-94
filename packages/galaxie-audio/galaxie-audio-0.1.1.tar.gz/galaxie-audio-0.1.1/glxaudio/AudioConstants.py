#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Audio Team, all rights reserved

# Inspired by: http://code.activestate.com/recipes/65207-constants-in-python/?in=user-97991


class Constants(object):
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const(%s)" % name)
        self.__dict__[name] = value

    def __getattr__(self, name):
        if name not in self.__dict__:
            raise self.ConstError("No attribute %s exist" % name)
        return self.__dict__[name]


#############################
# Variables
#############################

GLXAUDIO = Constants()


#### PortAudio ####
##### PaSampleFormat Sample Formats #####

# paFloat32 = 1
# 32 bit float
GLXAUDIO.FORMAT_FLOAT32 = 1

# paInt32 = 2
# 32 bit int
GLXAUDIO.FORMAT_INT32 = 2

# paInt24 = 4
# 24 bit int
GLXAUDIO.FORMAT_INT24 = 4

# paInt16 = 8
#: 16 bit int
GLXAUDIO.FORMAT_INT16 = 8

# paInt8 = 16
# #: 8 bit int
GLXAUDIO.FORMAT_INT8 = 16

# paUInt8 = 32
#: 8 bit unsigned int
GLXAUDIO.FORMAT_UINT8 = 32

# paCustomFormat = 65536
# #: a custom data format
GLXAUDIO.FORMAT_CUSTOM = 65536

GLXAUDIO.FORMATS = [
    GLXAUDIO.FORMAT_FLOAT32,
    GLXAUDIO.FORMAT_INT32,
    GLXAUDIO.FORMAT_INT24,
    GLXAUDIO.FORMAT_INT16,
    GLXAUDIO.FORMAT_INT8,
    GLXAUDIO.FORMAT_UINT8,
    GLXAUDIO.FORMAT_CUSTOM,
]

GLXAUDIO.COMMON_SAMPLE_RATES = [
    8000,
    11025,
    16000,
    22050,
    32000,
    37800,
    40056,
    44100,
    47250,
    48000,
    50000,
    50400,
    64000,
    88200,
    96000,
    176400,
    192000,
    352800,
    2822400,
    5644800,
    11289600,
    22579200,
]
