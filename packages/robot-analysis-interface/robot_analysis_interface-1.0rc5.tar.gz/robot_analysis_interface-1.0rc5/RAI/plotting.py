'''
Plotting
========

This module provides a :py:class:`Plot` class containing the information about a plot to display in the CompositeWindow.

:author: Jean-Claude Passy <jean-claude.passy@tuebingen.mpg.de>
'''

from contextlib import suppress

from PyQt5 import QtCore
from PyQt5.QtGui import QColor
import pyqtgraph as pg

from .serial import Serializable
from .utils import are_zeros_and_ones


class Plot(Serializable, QtCore.QObject):
    """This class provides access to the plot to be displayed.

    :param dict x: x-axis data
    :param dict y: y-axis data
    :param list(str) streams: names of the streams plotted
    :param str name: Name tag of the plot
    :param str plot_type: Type of plot. Only PyQtGraph is supported for the moment
    :param str x_label: x-axis label
    :param str y_label: y-axis label
    :param str x_units: x-axis units
    :param str y_units: y-axis units
    :param bool include_vertical_lines: if True, add vertical lines that will be connected to the videos
    """

    serial_version = '1.0'
    line_updated_signal = QtCore.pyqtSignal(float)

    # Dictionary of colors counting how many times each has been used (initially 0)
    colors = {
        0: (QColor(255, 0, 0), 0),  # red
        1: (QColor(0, 255, 0), 0),  # green
        2: (QColor(0, 0, 255), 0),  # blue
        3: (QColor(0, 255, 255), 0),  # cyan
        4: (QColor(255, 0, 255), 0),  # magenta
        5: (QColor(255, 127, 36), 0),  # chocolate
    }

    # Set up background/foreground colors
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')

    def __init__(self, x_data=None, y_data=None, streams=None,
                 name='Plot', plot_type='PyQtGraph',
                 x_label='time', y_label='Streams', x_units='s', y_units='',
                 include_vertical_lines=True, parent=None,
                 **kwargs):

        super().__init__(parent)

        self.name = name
        self.plot_type = plot_type

        self.x_data = x_data or {}
        self.y_data = y_data or {}
        self.streams = streams or []

        self.x_label = x_label
        self.y_label = y_label
        self.x_units = x_units
        self.y_units = y_units

        self.include_vertical_lines = include_vertical_lines

        # ID number in the GridLayout.
        self.id_number = None
        if 'id_number' in kwargs:
            self.id_number = kwargs['id_number']

        # Check that x_/ y_data and streams have the same length.
        assert (len(self.x_data) == len(self.y_data)), \
            'x/y data do not have the same length (%s != %s).' % (
                len(self.x_data), len(self.y_data))
        assert (len(self.x_data) == len(self.streams)), \
            'x_data and streams do not have the same length (%s != %s).' % (
                len(self.x_data), len(self.streams))

    def deleteLater(self):

        # Close PlotItems
        with suppress(AttributeError):
            self.plot_item1.close()
        with suppress(AttributeError):
            self.plot_item2.close()
        super().deleteLater()

    def _prepare(self, parent):
        """Prepare Widgets/PlotIteams/LinearRegionItems."""

        # First create empty plot
        self.widget1 = pg.GraphicsLayoutWidget(parent)

        self.plot_item1 = self.widget1.addPlot()
        self.plot_item1.setLabel('bottom', self.x_label, units=self.x_units)
        self.plot_item1.setLabel('left', self.y_label, units=self.y_units)
        self.lr = pg.LinearRegionItem([1.0, 2.0])

        # Set up color of the lines
        self.lr.lines[0].setPen(pg.mkPen('l', width=2))
        self.lr.lines[1].setPen(pg.mkPen('l', width=2))
        self.lr.lines[0].setHoverPen(pg.mkPen('r', width=2))
        self.lr.lines[1].setHoverPen(pg.mkPen('r', width=2))

        self.lr.setZValue(-10)
        self.plot_item1.addItem(self.lr)

        self.widget2 = pg.GraphicsLayoutWidget(parent)
        self.plot_item2 = self.widget2.addPlot()
        self.plot_item2.setLabel('bottom', self.x_label, units=self.x_units)

        # Connect both panels
        self.lr.sigRegionChanged.connect(self._update_zoom_plot)
        self.plot_item2.sigXRangeChanged.connect(self._update_main_plot)
        self._update_zoom_plot()

        if self.include_vertical_lines:
            self.line1 = self.plot_item1.addLine(0.0, pen=pg.mkPen('k', width=2),
                                                 hoverPen=pg.mkPen('r', width=2), movable=True)
            self.line2 = self.plot_item2.addLine(0.0, pen=pg.mkPen('k', width=2),
                                                 hoverPen=pg.mkPen('r', width=2), movable=True)

            # Connect signals
            self.line1.sigPositionChangeFinished.connect(self._line_updated)
            self.line2.sigPositionChangeFinished.connect(self._line_updated)

        # Add legend and hide it if there is no stream to plot
        self.legend = pg.LegendItem(offset=(450, 150))
        self.legend.setParentItem(self.plot_item1)
        if len(self.streams) == 0:
            self.legend.setVisible(False)

        # Add streams if needed
        self.curves = {}
        for stream in self.streams:
            self._add_stream(self.x_data[stream], self.y_data[stream], stream)

        # Show grids
        self.plot_item1.showGrid(x=True, y=True, alpha=0.35)
        self.plot_item2.showGrid(x=True, y=True, alpha=0.75)

    def _update_zoom_plot(self):
        """Update zoomed-in plot when moving the slider on the main plot."""

        self.plot_item2.setXRange(*self.lr.getRegion(), padding=0)

    def _update_main_plot(self):
        """Update slider on the main plot when resizing zoomed-in plot."""

        self.lr.setRegion(self.plot_item2.getViewBox().viewRange()[0])

    def _line_updated(self, source):
        """
        Send signal to MainWindow that a line has been moved.

        :param pg.InfiniteLine source: Updated line
        """

        # New value
        val = source.value()

        # Send signal to main window
        self.line_updated_signal.emit(val)

    def _update_vertical_lines(self, val):
        """
        Update the vertical lines to new position.

        :param float value: x-value at which to draw line
        """

        # First disconnect signals to avoid infinite calls
        self.line1.sigPositionChangeFinished.disconnect(self._line_updated)
        self.line2.sigPositionChangeFinished.disconnect(self._line_updated)

        # Update plots
        self.line2.setValue(val)
        self.line1.setValue(val)

        # Reconnect
        self.line1.sigPositionChangeFinished.connect(self._line_updated)
        self.line2.sigPositionChangeFinished.connect(self._line_updated)

    def serialize(self):

        super().serialize()

        return {
            "streams": self.streams,
            "name": self.name,
            "plot_type": self.plot_type,
            "x_label": self.x_label,
            "y_label": self.y_label,
            "x_units": self.x_units,
            "y_units": self.y_units,
            "include_vertical_lines": self.include_vertical_lines,
            "id_number": self.id_number,
            "serial_version": self.serial_version
        }

    @staticmethod
    def deserialize(dictionary, *args, **kwargs):

        assert(len(args) >= 1)  # we need the sensors data
        sensors_data = args[0]

        # Get streams data
        x, y = {}, {}

        for stream in dictionary['streams']:
            x1, y1 = sensors_data.get_streams(['time', stream])
            x[stream] = x1
            y[stream] = y1

        dictionary.pop("serial_version")
        return Plot(x, y, **dictionary)

    def _add_stream(self, x, y, stream, update_legend=True):
        """
        Add stream to the plot.

        :param numpy.array x: x-data
        :param numpy.array y: y-data
        :param str stream: stream to add
        """

        # Add data and stream in lists (not to do if the plot is being prepared)
        if stream not in self.streams:
            self.x_data[stream] = x
            self.y_data[stream] = y
            self.streams.append(stream)

        # Find which color to use
        color_id = self._get_next_available_color()
        color = self.colors[color_id][0]

        # Plot stream

        # The rendering becomes very slow if we render "booleans" (i.e. 0s and 1s)
        # because of the connecting lines between points
        # In case we try to plot such stream, we use a scattered plot instead.
        plot_kwargs = {}
        if are_zeros_and_ones(y):
            plot_kwargs['pen'] = None
            plot_kwargs['symbolBrush'] = color
            plot_kwargs['symbolSize'] = 5
            plot_kwargs['symbolPen'] = None
        else:
            plot_kwargs['pen'] = pg.mkPen(color, width=2)

        c1 = self.plot_item1.plot(x, y, name=stream, **plot_kwargs)
        c2 = self.plot_item2.plot(x, y, **plot_kwargs)
        self.curves[stream] = (c1, c2)

        # Add color count
        self.colors[color_id] = (self.colors[color_id][0], self.colors[color_id][1] + 1)

        # Add item to legend
        # Make legend visible in case it was not
        if update_legend:
            self.legend.addItem(c1, stream)
            if not self.legend.isVisible():
                self.legend.setVisible(True)

    def _remove_stream(self, stream, update_legend=True):
        """
        Remove stream from plot.

        :param stream: stream to add
        :type stream: str
        """

        # Stream should be present
        assert stream in self.streams, \
            "Cannot find stream {} to remove.".format(stream)

        # Curves to remove
        (c1, c2) = self.curves[stream]

        # Find color
        color_id = self._get_color_from_curve(c1)

        # Remove curves
        self.plot_item1.removeItem(c1)
        self.plot_item2.removeItem(c2)
        self.curves.pop(stream)

        # Remove data
        self.x_data.pop(stream)
        self.y_data.pop(stream)

        # Remove stream from list of streams
        self.streams.remove(stream)

        # Remove color count
        self.colors[color_id] = (self.colors[color_id][0], self.colors[color_id][1] - 1)

        # Remove item from legend
        # Hide legend in case there is no stream to display
        if update_legend:
            self.legend.removeItem(stream)
            if len(self.legend.items) == 0:
                self.legend.setVisible(False)

    def _update_stream(self, x, y, stream):
        """
        Update plots when data has been refreshed.

        :param numpy.array x: new x-data
        :param numpy.array y: new y-data
        :param str stream: name of the stream to update
        """

        # Remove old data
        self._remove_stream(stream, update_legend=False)

        # Add new data
        self._add_stream(x, y, stream, update_legend=False)

    def _get_next_available_color(self):
        """
        Find the color to use.

        :returns Index of the color to use
        :rtype int
        """

        # Loop through all the colors and find which one has been used the least
        indices = [0]
        min_val = self.colors[0][1]

        count = 1
        while count < len(self.colors):
            if self.colors[count] == min_val:
                indices.append[count]
            elif self.colors[count][1] < min_val:
                indices = [count]
                min_val = self.colors[count][1]
            else:
                pass
            count += 1

        return min(indices)

    def _get_color_from_curve(self, curve):
        """
        Find the color of a curve.

        :param curve: Curve
        :type curve: :py:class:`<pyqtgraph.graphicsItems.PlotItem>`
        :returns Index of the color
        :rtype int
        """

        try:
            color = curve.opts.get('pen').color()
        except AttributeError:  # this is a boolean field
            color = curve.opts.get('symbolBrush')

        color_id = 0
        while color_id < len(self.colors) - 1:
            if color.__eq__(self.colors[color_id][0]):
                break
            color_id += 1

        return color_id
