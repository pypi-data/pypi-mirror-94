#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  _      _  _       _   _  _    _   _
# | |  |  _| _| |_| |_  |_   |  |_| |_|
# |_|  | |_  _|   |  _| |_|  |  |_|   |
#
#  _       _  _   _  _  _      .   _                  _   _   _   _   _  _                       __
# |_| |_  |  | \ |_ |_ |   |_| |   | |/ |  |\/| |\ | | | |_| |_| |_| |_  | | | \  / \    / \/ \/  /
# | | |_| |_ |_/ |_ |  |_| | | | |_| |\ |_ |  | | \| |_| |     | |\   _| | |_|  \/   \/\/  /\ /  /_
# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Audio Team, all rights reserved

from numpy import array_equal, polyfit, sqrt, mean, absolute, log10, arange, power
from glxaudio.AudioConstants import GLXAUDIO
import math
import numpy


def rms_flat(a):
    """
    Return the root mean square of all the elements of *a*, flattened out.
    """
    return sqrt(mean(absolute(a) ** 2))


def linear_to_db(factor):
    """
    Return the level of a field quantity in decibels.

    linear-to-db(x) = log(factor) * 20.0

    :return: log(x) * 20.0
    :rtype: float
    """
    if factor == 0:
        factor = 0.0
    return 20.0 * log10(factor)


def db_to_linear(gain):
    """
    Return the level of a field quantity sample.

    db-to-linear(x) = 10^(gain / 20.0)

    :return: 10^(gain / 20.0)
    :rtype: float
    """
    return 10 ** (gain / 20.0)


def to_percent(value, maximum):
    """compute a percentage"""
    return value * 100 / maximum


def from_percent(value, maximum):
    """compute a value from percentage"""
    return maximum * value / 100


def percent_to_linear(value, maximum):
    """compute a value from percentage"""
    return maximum - (maximum * (value / 100))


def linear_to_percent(value, maximum):
    """compute a value from percentage"""
    return maximum - (maximum * (value / 100))


def get_quantification(code):
    """
    C’est la seconde phase de la numérisation. Après avoir découpé le signal continu en échantillons,
    il va falloir les mesurer et leur donner une valeur numérique en fonction de leur amplitude.

    Pour cela, on définit un intervalle de ``N`` valeurs destiné à couvrir l’ensemble des valeurs possibles.

    Ce nombre ``N`` est codé en binaire sur 8-16-20 ou 24 bits suivant la résolution du convertisseur A/N.
    L’amplitude de chaque échantillon est alors représentée par un nombre entier.

    Codage sur 8 bits = 2 puissance 8 = 256 valeurs possibles

    Codage sur 16 bits = 2 puissance 16 = 65536 valeurs possibles

    Codage sur 20 bits = 2 puissance 20 = 1.048.576 valeurs possibles

    Codage sur 24 bits = 2 puissance 24 = 16.777.216 valeurs possibles.

    :param code: Codage en binaire 8-16-20-24 ou 32 bits, suivant la résolution du convertiseur A/N
    :type code: int
    :return: for a 16bit code: neg=-32768, pos=32767, amplitude=96
    :rtype: int, int, int
    """
    # http://www.audio-maniac.com/?page_id=35
    # Exit as soon of possible
    if type(code) != int:
        raise TypeError("'code' must be a int type")

    # make the job in case
    neg = int((0 - (2 ** code) // 2))
    pos = int(((2 ** code) // 2) - 1)

    # (6 dB/bit)
    amplitude = int(code * 6)

    # return something
    return neg, pos, amplitude


def get_format_to_dtype(pa_sample_format):
    """
    Return a Coding bits for a PaSampleFormat to numpy dtype.

    :param pa_sample_format: A PaSampleFormat constant.
    :rtype pa_sample_format: int
    :return: Coding bits like 8, 16, 24, or 32
    :rtype: int
    :raises TypeError: for invalid `format`
    """
    # Exit as soon of possible
    if pa_sample_format not in GLXAUDIO.FORMATS:
        raise TypeError("Invalid format: %d" % pa_sample_format)
    # In case make the job
    # GLXAUDIO.FORMAT_FLOAT32,
    if pa_sample_format == GLXAUDIO.FORMAT_FLOAT32:
        return 32
    # GLXAUDIO.FORMAT_INT32,
    elif pa_sample_format == GLXAUDIO.FORMAT_INT32:
        return 32
    # GLXAUDIO.FORMAT_INT24,
    elif pa_sample_format == GLXAUDIO.FORMAT_INT24:
        return 24
    # GLXAUDIO.FORMAT_INT16,
    elif pa_sample_format == GLXAUDIO.FORMAT_INT16:
        return 16
    # GLXAUDIO.FORMAT_INT8,
    elif pa_sample_format == GLXAUDIO.FORMAT_INT8:
        return 8
    # GLXAUDIO.FORMAT_UINT8,
    elif pa_sample_format == GLXAUDIO.FORMAT_UINT8:
        return 8
    elif pa_sample_format == GLXAUDIO.FORMAT_CUSTOM:
        return 65536


def get_format_to_human_view(pa_sample_format):
    """
    Return a human readable string of a PaSampleFormat.

    :param pa_sample_format: A PaSampleFormat constant.
    :rtype pa_sample_format: int
    :return: for GLXAUDIO.AUDIO_FORMAT_INT16 return '16 bit int'
    :rtype: str
    :raises TypeError: for invalid `pa_sample_format`
    """
    # Exit as soon of possible
    if pa_sample_format not in GLXAUDIO.FORMATS:
        raise TypeError("Invalid format: %d" % pa_sample_format)

    # In case make the job
    if pa_sample_format == GLXAUDIO.FORMAT_FLOAT32:
        pa_sample_format = str("32 bit float")

    elif pa_sample_format == GLXAUDIO.FORMAT_INT32:
        pa_sample_format = str("32 bit int")

    elif pa_sample_format == GLXAUDIO.FORMAT_INT24:
        pa_sample_format = str("24 bit int")

    elif pa_sample_format == GLXAUDIO.FORMAT_INT16:
        pa_sample_format = str("16 bit int")

    elif pa_sample_format == GLXAUDIO.FORMAT_INT8:
        pa_sample_format = str("8 bit int")

    elif pa_sample_format == GLXAUDIO.FORMAT_UINT8:
        pa_sample_format = str("8 bit unsigned int")

    elif pa_sample_format == GLXAUDIO.FORMAT_CUSTOM:
        pa_sample_format = str("Custom")

    return pa_sample_format


def clamp(value=None, smallest=None, largest=None):
    """
    Back ``value`` inside ``smallest`` and ``largest`` value range.

    :param value: The value it have to be clamped
    :param smallest: The lower value
    :param largest: The upper value
    :type value: int or float
    :type value: int or float
    :return: The clamped value it depend of parameters value type, int or float will be preserve.
    :rtype: int or float
    """
    # Try to exit as soon of possible
    if type(value) != int and type(value) != float:
        raise TypeError(">value< must be a int or float type")

    if type(smallest) != int and type(smallest) != float:
        raise TypeError(">smallest< must be a int or float type")

    if type(largest) != int and type(largest) != float:
        raise TypeError(">largest< must be a int or float type")

    # make the job
    if type(value) == int:
        if value < smallest:
            value = smallest
        elif value > largest:
            value = largest
        return int(value)
    elif type(value) == float:
        if value < smallest:
            value = smallest
        elif value > largest:
            value = largest
        return float(value)


def sec2time(sec, n_msec=3):
    """
    Convert seconds to 'D days, HH:MM:SS.FFF'

    By: Lee
     Source: https://stackoverflow.com/questions/775049/how-do-i-convert-seconds-to-hours-minutes-and-seconds

    Example:
     $ sec2time(10, 3)
     Out: '00:00:10.000'

     $ sec2time(1234567.8910, 0)
     Out: '14 days, 06:56:07'

     $ sec2time(1234567.8910, 4)
     Out: '14 days, 06:56:07.8910'

     $ sec2time([12, 345678.9], 3)
     Out: ['00:00:12.000', '4 days, 00:01:18.900']

    :param sec:
    :param n_msec:
    :return:
    """
    if hasattr(sec, "__len__"):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if n_msec > 0:
        pattern = "%%02d:%%02d:%%0%d.%df" % (n_msec + 3, n_msec)
    else:
        pattern = r"%02d:%02d:%02d"
    if d == 0:
        return pattern % (h, m, s)
    return ("%d days, " + pattern) % (d, h, m, s)


def sizeof(num):
    suffix = ["", "K", "M", "G", "T", "P", "E", "Z"]
    i = 0 if num < 1 else int(math.log(num, 1024)) + 1
    v = num / math.pow(1024, i)
    v, i = (v, i) if v > 0.5 else (v * 1024, (i - 1 if i else 0))

    return str(str(int(round(v, 0))) + suffix[i])


def get_scale(minimal, maximum, division):

    return numpy.linspace(minimal, maximum, division)
