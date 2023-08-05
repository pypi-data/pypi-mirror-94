#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Radio Team, all rights reserved


class Object(object):
    def __init__(self):
        self.verbose = True
        self.verbose_level = 0
        self.debug = False
        self.debug_level = 0

    def set_verbose(self, verbose):
        """
        Set if the verbose information's display on the screen.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param verbose: True is verbose mode is enable, False for disable it.
        :type verbose: bool
        :raise TypeError: when "verbose" argument is not a :py:data:`bool`
        """
        # Exit as soon of possible
        if type(verbose) != bool:
            raise TypeError("'verbose' must be a bool type")

        # make the job in case
        if self.get_verbose() != bool(verbose):
            self.verbose = bool(verbose)

    def get_verbose(self):
        """
        Get if the verbose information's is display to the screen.

        :return: True if verbose mode is enable, False for disable it.
        :rtype: bool
        """
        return bool(self.verbose)

    def set_verbose_level(self, verbose_level):
        """
        Set the verbose level of information'ss display on the screen.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param verbose_level: The Debug level to set
        :type verbose_level: int
        :raise TypeError: when "verbose_level" argument is not a :py:data:`int`
        """
        # Exit as soon of possible
        if type(verbose_level) != int:
            raise TypeError("'verbose_level' must be a int type")

        # make the job in case
        if self.get_verbose_level() != verbose_level:
            self.verbose_level = verbose_level

    def get_verbose_level(self):
        """
        Get the verbose information's level to display on the screen.

        Range: 0 to 3

        See: Object.set_verbose_level() for more information's about effect of ``debug_level``

        :return: The debug level as set with MorseDecoder.set_debug_level()
        :rtype: int
        """
        return self.verbose_level

    def set_debug(self, debug):
        """
        Set the debugging level of information'ss display on the screen.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param debug: True is debugging mode is enable, False for disable it.
        :type debug: bool
        :raise TypeError: when "debug" argument is not a :py:data:`bool`
        """
        # Exit as soon of possible
        if type(debug) != bool:
            raise TypeError("'debug' must be a bool type")

        # make the job in case
        if self.get_debug() != bool(debug):
            self.debug = bool(debug)

    def get_debug(self):
        """
        Get the debugging information's level to display on the screen.

        :return: True if debugging mode is enable, False for disable it.
        :rtype: bool
        """
        return bool(self.debug)

    def set_debug_level(self, debug_level):
        """
        Set the debugging level of information'ss display on the screen.

        Generally it highly stress the console and is here for future maintenance of that Application.

        Enjoy future dev it found it function ;)

        :param debug_level: The Debug level to set
        :type debug_level: int
        :raise TypeError: when "debug_level" argument is not a :py:data:`int`
        """
        # Exit as soon of possible
        if type(debug_level) != int:
            raise TypeError("'debug_level' must be a int type")

        # make the job in case
        if self.get_debug_level() != debug_level:
            self.debug_level = debug_level

    def get_debug_level(self):
        """
        Get the debugging information's level to display on the screen.

        Range: 0 to 3

        See: MorseDecoder.set_debug_level() for more information's about effect of ``debug_level``

        :return: The debug level as set with MorseDecoder.set_debug_level()
        :rtype: int
        """
        return self.debug_level
