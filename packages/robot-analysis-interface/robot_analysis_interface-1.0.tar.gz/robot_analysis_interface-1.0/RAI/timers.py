'''
Timers
======

This module provides a :py:class:`DoubleTimer` class
needed to play videos and update plots synchronously.

:author: Jean-Claude Passy <jean-claude.passy@tuebingen.mpg.de>
'''

from PyQt5 import QtCore


class DoubleTimer(object):
    """
    This class provides timers to synchronize plots and videos.
    It is made out of a continuous timer of type :py:class:`QtCore.QTimer`
    and an elapsed timer of type :py:class:`QtCore.QElapsedTimer`.

    :param int timeout: timeout in ms of the continuous timer.
    """

    def __init__(self, timeout=30):

        self.repeat_timer = QtCore.QTimer()
        self.elapse_timer = QtCore.QElapsedTimer()
        self.timeout = timeout
        self.status_running = False

    def start(self):
        """Start the DoubleTimer."""

        if not self.status_running:
            self.repeat_timer.start(self.timeout)
            self.elapse_timer.start()
            self.status_running = True

    def stop(self):
        """Stop the DoubleTimer."""

        if self.status_running:
            self.repeat_timer.stop()
            self.status_running = False
