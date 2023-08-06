# -*- coding: utf-8 -*-
"""
App Event Hook
hook the widget event rather than override class event method
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2020-11-02 23:47:53"

try:
    from collections import Iterable
except:
    from collections.abc import Iterable

import six
import inspect
from functools import partial

from Qt import QtCore, QtWidgets, QtGui


class QEventHook(QtCore.QObject):

    __invert_flag = False
    __instance = None
    __hook = {}
    __invert_hook = {}
    __event = None
    __callbacks = None

    @classmethod
    def instance(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = cls(*args, **kwargs)
        return cls.__instance

    def __init__(self):
        if self.__instance:
            raise Exception("This class is a singleton!")
        super(QEventHook, self).__init__()
        self.installEventFilter(self)
        event = QtCore.QEvent(QtCore.QEvent.User)
        QtCore.QCoreApplication.postEvent(self, event)

    def eventFilter(self, receiver, event):
        data = self.__hook.get(receiver)
        if data:
            callbacks = data.get(event.type(), [])
            for callback in callbacks:
                callback = callback.func if isinstance(callback, partial) else callback
                length = len(inspect.getargspec(callback).args)
                count = length - 1 if inspect.ismethod(callback) else length
                args = (event,)
                callback(*args[:count])

        # NOTE invert event hook
        data = self.__invert_hook.get(receiver)
        if data is None and type(receiver).__name__ != "QWindow":
            callbacks = self.__invert_hook.get(event.type(), [])
            for callback in callbacks:
                callback = callback.func if isinstance(callback, partial) else callback
                length = len(inspect.getargspec(callback).args)
                count = length - 1 if inspect.ismethod(callback) else length
                args = (receiver, event)
                callback(*args[:count])

        if receiver is self and event.type() == QtCore.QEvent.User:
            self.removeEventFilter(self)
            app = QtWidgets.QApplication.instance()
            app.installEventFilter(self)
        return super(QEventHook, self).eventFilter(receiver, event)

    def __rrshift__(self, receiver):
        event = self.__event
        events = (
            (event,)
            if isinstance(event, six.string_types) or not isinstance(event, Iterable)
            else event
        )
        for event in events:
            event = getattr(QtCore.QEvent, event) if isinstance(event, str) else event
            if self.__invert_flag:
                self.add_invert_hook(receiver, event, self.__callbacks)
            else:
                self.add_hook(receiver, event, self.__callbacks)
        self.__invert_flag = False
        return receiver

    def __invert__(self):
        self.__invert_flag = True
        return self

    def __call__(self, event, callbacks):
        """__call__ drive add_hook

        https://doc.qt.io/qtforpython/PySide2/QtCore/QEvent.html

        :param event: QEvent Type
        :type event: str | QEvent.Type
        :param callbacks: callable list or callable object
        :type callbacks: callable
        """

        self.__event = event
        self.__callbacks = callbacks
        return self

    def check_callback(self, callback):
        if inspect.ismethod(callback):
            callback = callback.__func__
        if not inspect.isfunction(callback):
            raise TypeError("{!r} is not a Python function".format(callback))

    def add_hook(self, receiver, event, callbacks):
        """add_hook global hook

        https://doc.qt.io/qtforpython/PySide2/QtCore/QEvent.html

        :param receiver: object or widget
        :type receiver: QtCore.QObject
        :param event: QEvent Type , defaults to None
        :type event: str | QEvent.Type
        :param callbacks: callable list or callable object , defaults to None
        :type callbacks: callable
        """

        if not event or not callbacks:
            return
        self.__hook.setdefault(receiver, {})
        self.__hook[receiver].setdefault(event, [])
        callbacks = (
            [c for c in callbacks if six.callable(c)]
            if isinstance(callbacks, list)
            else [callbacks]
        )
        for callback in callbacks:
            self.check_callback(callback)
        self.__hook[receiver][event].extend(callbacks)

    def add_invert_hook(self, receiver, event, callbacks):
        if not event or not callbacks:
            return
        self.__invert_hook.setdefault(receiver, True)
        self.__invert_hook.setdefault(event, [])
        callbacks = (
            [c for c in callbacks if six.callable(c)]
            if isinstance(callbacks, list)
            else [callbacks]
        )
        for callback in callbacks:
            self.check_callback(callback)
        self.__invert_hook[event].extend(callbacks)

    def get_hook(self):
        return self.__hook

    def set_hook(self, hook):
        self.__hook.update(hook)
