'''
View
====

This module provides a :py:class:`View` class that organizes Plots into Views.

:author: Jean-Claude Passy <jean-claude.passy@tuebingen.mpg.de>
'''


from PyQt5 import QtGui, QtCore, QtWidgets
from .serial import Serializable
from .utils import _build_common_widget


class View(Serializable, QtCore.QObject):
    """ This class allows the user to create and save a layout of Plots.

    :param plots: View plots.
    :type plots: list(:py:class:`Plot<RAI.plotting.Plot>`)
    """

    serial_version = '1.0'

    def __init__(self, plots=None, name='View'):

        super().__init__()

        self.plots = plots or []
        self.name = name

    def build(self, width, height, parent=None):
        """ Build widgets to display View.

        :param width: width of a Plot.
        :type width: int
        :param height: height of a Plot.
        :type height: int
        """

        # Initialize attributes
        self.plot_width = width
        self.plot_height = height
        self.parent = parent

        # Build ScrollArea
        self.scroll_area_plots = QtWidgets.QScrollArea(self.parent)
        self.scroll_area_plots.setWidgetResizable(True)
        self.scroll_area_plots_widget_contents = QtWidgets.QWidget(self.scroll_area_plots)
        self.scroll_area_plots_widget_contents.setGeometry(QtCore.QRect(0, 0, 380, 247))
        self.scroll_area_plots.setWidget(self.scroll_area_plots_widget_contents)

        self.vertical_widget_plots = QtWidgets.QWidget(self.parent)
        self.vertical_layout_plots = QtWidgets.QVBoxLayout(self.vertical_widget_plots)
        self.vertical_layout_plots.addWidget(self.scroll_area_plots)
        self.vertical_layout_plots_scroll = QtWidgets.QVBoxLayout(
            self.scroll_area_plots_widget_contents)

        # Insert Plot widget
        for plot in self.plots:
            plot_widget = _build_common_widget(self.parent, 1, 2, plot.widget1, plot.widget2,
                                               stretch_columns=[2, 1])
            plot_widget.setMinimumSize(self.plot_width, self.plot_height)
            self.vertical_layout_plots_scroll.addWidget(plot_widget)

        # Install event filter
        self.scroll_area_plots.verticalScrollBar().installEventFilter(self)

    def eventFilter(self, obj, event):

        # Deactivate wheel events because they mess things up with Plots
        if event.type() == QtCore.QEvent.Wheel:
            return True

        return False

    def deleteLater(self):
        """Deleting plots to avoid Seg fault"""
        for plot in self.plots:
            plot.deleteLater()
        super().deleteLater()

    def serialize(self):

        super().serialize()

        return {"name": self.name,
                "plots": self.plots,
                "serial_version": self.serial_version
                }

    @staticmethod
    def deserialize(dictionary, *args, **kwargs):

        assert(len(args) >= 1)  # we need the plots
        plots = args[0]

        dictionary.pop("serial_version")
        dictionary.pop("plots")

        return View(plots, **dictionary)
