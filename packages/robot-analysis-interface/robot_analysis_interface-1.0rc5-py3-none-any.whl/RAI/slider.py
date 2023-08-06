'''
Slider
======

This module provides a slider that controls plots and videos.

:author: Jean-Claude Passy <jean-claude.passy@tuebingen.mpg.de>
'''


from PyQt5 import QtCore, QtWidgets

from .utils import signals_blocked


class FloatSlider(QtWidgets.QSlider):
    """
    This class provides a slider that handles floats.

    :param float duration: Duration of the video in seconds.
    """

    # Number of steps per second
    steps_per_seconds = 10

    def __init__(self, duration, *args):

        super().__init__(*args)

        self._max_int = int(duration * self.steps_per_seconds)
        self.setRange(0, self._max_int)
        self.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.setTickInterval(self.maximum() / 10)  # ticks every 10%
        self.setValue(0)

    def value(self):
        return float(super().value()) / self.steps_per_seconds

    def setValue(self, value):
        super().setValue(int(value * self.steps_per_seconds))

    def update_slider(self, val):
        """
        Update the slider to new position.

        :param int value: new value for the slider
        """

        with signals_blocked(self):
            self.setValue(val)

    def mousePressEvent(self, event):

        # Send a signal to the main_window, which then will update the plots/videos
        if event.button() == QtCore.Qt.LeftButton:
            super().mousePressEvent(event)
            self.sliderReleased.emit()
