import random

import numpy
from PyQt5 import QtTest, QtCore
from pyqtgraph.graphicsItems.PlotItem import PlotItem

from RAI.main_window import CompositeWindow
from RAI.plotting import Plot
from RAI.table import SelectionTable

from .fixtures import (
    WAIT_TIME, TOLERANCE,
    TestCaseDefault, PatchWrapper,
    mouse_drag, mouse_move
)


class TestPlot(TestCaseDefault):
    """Class for testing the Plot."""

    def setUp(self):
        super().setUp()

        # Extra patches
        self.patch_wrappers += (
            PatchWrapper("plot", PlotItem),
            PatchWrapper("removeItem", PlotItem, prefix='plot'),
            PatchWrapper("update_data", SelectionTable),
            PatchWrapper("_get_color_from_curve", Plot, return_value=0),
        )

        # Create window
        self.win = CompositeWindow(self.views, self.videos, parent_session=self.session)

        # Current view
        self.current_view = self.win.get_current_view()

        # Show window
        self.win.show()
        QtTest.QTest.qWait(WAIT_TIME)

    def tearDown(self):

        # Close window
        self.win.close()

        super().tearDown()

    def test_add_stream(self):
        """ Test adding a stream to a Plot. """

        self.patch_wrappers += (
            PatchWrapper('RAI.plotting.are_zeros_and_ones', return_value=True),
        )

        # Check that plot has been called at the beginning
        count_theo = 2 * len(self.current_view.plots) * len(self.session.sensors_data.fields)
        self.assertEqual(self.get_patch('plot').mock.call_count, count_theo)

        # Check that data for the new stream does not exist
        new_stream = 'new_stream'
        plot = self.current_view.plots[0]
        self.assertFalse(new_stream in plot.x_data.keys())
        self.assertFalse(new_stream in plot.y_data.keys())
        self.assertFalse(new_stream in plot.streams)
        self.assertFalse(new_stream in plot.curves.keys())

        # Add stream to plot
        plot._add_stream(*self.session.sensors_data.get_streams(new_stream), new_stream)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that there is a new stream plotted
        self.assertEqual(self.get_patch('plot').mock.call_count, count_theo + 2)
        self.assertTrue(new_stream in plot.x_data.keys())
        self.assertTrue(new_stream in plot.y_data.keys())
        self.assertTrue(new_stream in plot.streams)
        self.assertTrue(new_stream in plot.curves.keys())
        self.assertEqual(type(plot.curves[new_stream]), tuple)
        self.assertEqual(len(plot.curves[new_stream]), 2)
        self.assertEqual(self.get_patch('RAI.plotting.are_zeros_and_ones').mock.call_count, 1)

        # Check that legend has been updated
        count_theo = len(self.current_view.plots) * len(self.session.sensors_data.fields) + 1
        self.assertEqual(self.get_patch('addItem').mock.call_count, count_theo)

    def test_remove_stream(self):
        """ Test removing a stream from a Plot. """

        # Check that data for the old stream exists
        old_stream = self.get_patch('RAI.sensors.SensorsData').mock.return_value.fields[0]
        plot = self.current_view.plots[0]
        self.assertTrue(old_stream in plot.x_data.keys())
        self.assertTrue(old_stream in plot.y_data.keys())
        self.assertTrue(old_stream in plot.streams)
        self.assertTrue(old_stream in plot.curves.keys())
        self.assertEqual(type(plot.curves[old_stream]), tuple)
        self.assertEqual(len(plot.curves[old_stream]), 2)

        # Remove stream from plot
        old_streams = list(plot.streams)
        plot._remove_stream(old_stream)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that the old stream has been removed
        self.assertEqual(self.get_patch('plot_removeItem').mock.call_count, 2)
        self.assertFalse(old_stream in plot.x_data.keys())
        self.assertFalse(old_stream in plot.y_data.keys())
        self.assertFalse(old_stream in plot.streams)
        self.assertFalse(old_stream in plot.curves.keys())

        # Check that the other streams are still there
        old_streams.remove(old_stream)
        self.assertEqual(sorted(plot.streams), sorted(old_streams))

        # Check that legend has been updated
        self.assertEqual(self.get_patch('legend_removeItem').mock.call_count, 1)

    def test_clear_plot(self):
        """Test clearing a plot."""

        # Clear plot 1
        fields = list(self.session.sensors_data.fields)
        self.win._clear_plots([0])
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that both streams been removed
        self.assertEqual(self.get_patch('plot_removeItem').mock.call_count, 2 * len(fields))
        QtTest.QTest.qWait(WAIT_TIME)

    def test_update(self):
        """Test that plots/videos/attributes are updated correctly when the line of a plot moves."""

        self.assertEqual(self.get_patch('update_data').mock.call_count, 0)

        # Drag line to random video duration (avoid division by zero)
        new_value = random.randint(1, self.video.duration)
        line = self.current_view.plots[0].line1
        line.setValue(new_value)
        line.sigPositionChangeFinished.emit(line)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that plots have been updated
        for plot in self.current_view.plots:
            self.assertEqual(plot.line1.value(), new_value)
            self.assertEqual(plot.line2.value(), new_value)

        # Check that slider has been updated
        rel_err = abs(self.win.msl.value() - new_value) / new_value
        self.assertLess(rel_err, TOLERANCE)

        # Check that table has been updated
        self.assertEqual(self.get_patch('update_data').mock.call_count, 1)

    def test_serialize(self):
        """ Test the serialization of a Plot. """

        # Serialize plot
        dictionary = self.current_view.plots[0].serialize()

        # Check that the dictionary is not empty
        self.assertGreater(len(dictionary), 0)

        # The dictionary should have at least some fundamental elements
        elements = ['streams', 'name', 'plot_type', 'x_label', 'y_label',
                    'x_units', 'y_units', 'include_vertical_lines', 'serial_version']

        for x in elements:
            self.assertIsNotNone(dictionary[x])

    def test_deserialize(self):
        """ Test the deserialization of a Plot. """

        # Serialize plot
        dictionary = self.current_view.plots[0].serialize()

        # Load plot
        loaded_plot = Plot.deserialize(dictionary, self.session.sensors_data)

        # Check that the dictionary is not empty
        self.assertIsNotNone(dictionary)

        # The dictionary should have at least some fundamental elements
        elements = ['name', 'plot_type', 'x_data', 'y_data', 'x_label', 'y_label',
                    'x_units', 'y_units', 'include_vertical_lines', 'id_number']

        for elem in elements:
            a = getattr(self.current_view.plots[0], elem)
            b = getattr(loaded_plot, elem)
            try:
                self.assertEqual(a, b)
            except ValueError:  # We are dealing with a dict which values are arrays
                for stream in a:
                    numpy.testing.assert_array_equal(a[stream], b[stream])


class TestPlotRegion(TestCaseDefault):
    """Class for testing plot regions."""

    def setUp(self):
        super().setUp()

        # Create window
        self.win = CompositeWindow(self.views, self.videos, parent_session=self.session)

        # Current view
        self.current_view = self.win.get_current_view()

        # Show window
        self.win.show()
        QtTest.QTest.qWait(WAIT_TIME)

    def tearDown(self):

        # Close window
        self.win.close()

        super().tearDown()

    def test_mouse_event(self):

        # Make zoomed-in region bigger so we can more easily click on it
        plot = self.current_view.plots[0]
        plot.lr.setRegion((3, 7))

        # Get the center of the pyqtgraph widget
        pg_widget = self.current_view.plots[0].widget1
        pg_geometry = pg_widget.frameGeometry()
        pg_local_pos = QtCore.QPoint(pg_geometry.x() + pg_geometry.width() / 2,
                                     pg_geometry.y() + pg_geometry.height() / 2)

        # Get the PyQt widget at this location
        qt_widget = pg_widget.childAt(pg_local_pos)

        # Get the center of the PyQt widget
        qt_geometry = qt_widget.frameGeometry()
        qt_local_pos = QtCore.QPoint(qt_geometry.x() + qt_geometry.width() / 2,
                                     qt_geometry.y() + qt_geometry.height() / 2)

        # Move mouse to the widget
        QtTest.QTest.qWait(WAIT_TIME)
        mouse_move(qt_widget, qt_local_pos)

        # Prepare mouse drag event
        npixels_drag = 70  # for how many pixels do we drag the blue region?
        new_qt_local_pos = QtCore.QPoint(qt_local_pos.x() + npixels_drag, qt_local_pos.y())
        vb = plot.plot_item1.getViewBox()  # plot view box
        vb_x_size = vb.size().width()
        x_range = vb.state['viewRange'][0]  # range on the x-axis
        delta_x = x_range[1] - x_range[0]
        length_drag = delta_x * npixels_drag / vb_x_size

        # Initial position of zoomed-in region
        init_pos_lr = plot.lr.getRegion()

        # Move the region
        QtTest.QTest.qWait(WAIT_TIME)
        mouse_drag(qt_widget, qt_local_pos, new_qt_local_pos, QtCore.Qt.LeftButton)

        # Final position of zoomed-in region
        end_pos_lr = plot.lr.getRegion()

        # Check that the slider has moved to the right as expected, and not increased in size
        QtTest.QTest.qWait(WAIT_TIME)

        dx1 = init_pos_lr[1] - init_pos_lr[0]
        dx2 = end_pos_lr[1] - end_pos_lr[0]
        self.assertLess(abs(end_pos_lr[0] - init_pos_lr[0] - length_drag) / length_drag, TOLERANCE)
        self.assertLess(abs(dx2 - dx1) / dx1, TOLERANCE)


class TestPlotNoVideo(TestCaseDefault):
    """Class for testing plot time/line update without video."""

    def setUp(self):
        super().setUp()

        # Extra patches
        self.patch_wrappers += (
            PatchWrapper("update_data", SelectionTable),
        )

        # Create window
        self.win_plot = CompositeWindow(self.views, parent_session=self.session)

        # Current view
        self.current_view = self.win_plot.get_current_view()

        # Show window
        self.win_plot.show()
        QtTest.QTest.qWait(WAIT_TIME)

    def tearDown(self):
        # Close window
        self.win_plot.close()

        super().tearDown()

    def test_update(self):
        """Test that plots/attributes are updated correctly when the line of a plot moves."""

        self.assertEqual(self.get_patch('update_data').mock.call_count, 0)

        # Drag line to random video duration (avoid division by zero)
        new_value = random.randint(1, self.video.duration)
        line = self.current_view.plots[0].line1
        line.setValue(new_value)
        line.sigPositionChangeFinished.emit(line)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that plots have been updated
        for plot in self.current_view.plots:
            self.assertEqual(plot.line1.value(), new_value)
            self.assertEqual(plot.line2.value(), new_value)

        # Check that table has been updated
        self.assertEqual(self.get_patch('update_data').mock.call_count, 1)
