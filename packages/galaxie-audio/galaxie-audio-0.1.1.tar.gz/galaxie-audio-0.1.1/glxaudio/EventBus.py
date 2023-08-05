#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Curses Team, all rights reserved


class EventBusClient(object):
    """
    :Description:

    The :class:`EventBusClient <GLXCurses.EventBusClient.EventBusClient>` object is The bus it interconnect Widget
    :class:`Application <GLXCurses.Application.Application>` is a special case where the
    :func:`Application.dispatch() <GLXCurses.Application.Application.dispatch()>` rewrite the
    :func:`EventBusClient.dispatch() <GLXCurses.EventBusClient.EventBusClient.dispatch()>`.
    """

    def __init__(self):
        self.__events_list = dict()
        self.application = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @property
    def events_list(self):
        return self.__events_list

    def set_application(self, application=None):
        """
        Set a Galaxie Curses Application

        :param application: a Galaxie-Curses Application
        :type application: GLXCurses.application
        """
        # Exit as soon of possible, bad day today ...
        if application is not None:
            if not hasattr(application, "active_window_id") and not hasattr(
                    application, "main_window"
            ):
                raise TypeError("'application' must be a GLXCurses.application type")

        # make the job in case
        if self.get_application() != application:
            self.application = application

    def get_application(self):
        """
        Get the Galaxie-Curses Application as set by set_application()

        :return: a Galaxie-Curses Application or None is not set
        :rtype: Galaxie-Curses Application or None
        """
        return self.application

    def emit(self, detailed_signal, data=None):
        """
        Every Object emit signal in direction to the Application.

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param data: additional parameters arg1, arg2
        :type data: dict
        """
        # If args is still None replace it by a empty list
        if data is None:
            data = dict()

        # Emit inside the Mainloop
        self.get_application().emit(detailed_signal, data)

    def connect(self, detailed_signal, handler, args=None):
        """
        The connect() method adds a function or method (handler) to the end of the event list
        for the named detailed_signal but before the default class signal handler.
        An optional set of parameters may be specified after the handler parameter.
        These will all be passed to the signal handler when invoked.

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param handler: a function handler
        :type handler: handler
        :param args: additional parameters arg1, arg2
        :type args: list
        """
        if args is None:
            args = list()

        if type(detailed_signal) != str:
            raise TypeError("'detailed_signal' must be a str type")

        if type(args) != list:
            raise TypeError("'args' must be a list type")

        if detailed_signal not in self.events_list:
            self.events_list[detailed_signal] = list()

        self.events_list[detailed_signal].append(handler)

        if args:
            self.events_list[detailed_signal].append(args)

    def disconnect(self, detailed_signal, handler):
        """
        The disconnect() method removes the signal handler with the specified handler
        from the list of signal handlers for the object.

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param handler: a function handler
        :type handler: handler
        """
        if detailed_signal in self.events_list:
            self.events_list[detailed_signal].remove(handler)

    def events_flush(self, detailed_signal, args=None):
        if args is None:
            args = []

        if detailed_signal in self.events_list:
            for handler in self.events_list[detailed_signal]:
                handler(self, detailed_signal, args)

    def events_dispatch(self, detailed_signal, args=None):
        """
        Inform every children or child about a event and execute a eventual callback

        :param detailed_signal: a string containing the signal name
        :type detailed_signal: str
        :param args: additional parameters arg1, arg2
        :type args: list
        """

        # If args is still None replace it by a empty list
        if args is None:
            args = []

        # Flush internal event
        self.events_flush(detailed_signal, args)

    def get_events_list(self):
        """
        Return teh event list

        :return: the event list under a dictionary
        :rtype: dict
        """
        return self.events_list
