import numpy as np
from PyQt5 import QtCore, QtTest

from RAI.plotting import Plot
from RAI.main_window import CompositeWindow
from RAI.session import Session

from .fixtures import (
    WAIT_TIME, TestCaseDefault, PatchWrapper,
    mouse_click, generate_random_path
)


class TestTable(TestCaseDefault):
    """Class for testing the Table."""

    def setUp(self):

        super().setUp()

        # Extra patches
        self.patch_wrappers += (
            PatchWrapper("_add_stream", Plot),
            PatchWrapper("_remove_stream", Plot),
        )
        """
        self.patches[8] = patch.object(Plot, "_add_stream")
        self.mocked_add_stream = self.patches[8].start()
        self.patches[9] = patch.object(Plot, "_remove_stream")
        self.mocked_remove_stream = self.patches[9].start()
        """

        # Create window
        self.win = CompositeWindow(self.views, self.videos, parent_session=self.session)

        # Show window
        self.win.show()
        QtTest.QTest.qWait(WAIT_TIME)

    def tearDown(self):

        # Close window
        self.win.close()

        super().tearDown()

    def test_create_table(self):
        """Test the creation of the selection table."""

        # Check that table is open
        self.assertTrue(self.win.selection_table.isVisible())
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that the correct stream name is shown
        item = self.win.selection_table.item(0, 0)
        self.assertTrue(item.text() == self.session.sensors_data.fields[0])

    def test_cancel_selection(self):
        """Check that the plot goes back to its initial state when pressing the Cancel button."""

        # Get item and click on it
        item = self.win.selection_table.item(0, 0)
        self.win.selection_table.itemClicked.emit(item)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that the dialog opened
        self.assertTrue(self.win.selection_table.check_list.isVisible())

        # Check that the OK button is disabled
        self.assertFalse(self.win.selection_table.check_list.ok_btn.isEnabled())

        # Get plot and uncheck it
        item = self.win.selection_table.check_list.list_widget.item(0)
        self.assertEqual(item.checkState(), QtCore.Qt.Checked)
        QtTest.QTest.qWait(WAIT_TIME)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.assertEqual(item.checkState(), QtCore.Qt.Unchecked)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that remove_stream has been called
        self.assertEqual(self.get_patch('_remove_stream').mock.call_count, 1)

        # Check that the OK button is enabled
        self.assertTrue(self.win.selection_table.check_list.ok_btn.isEnabled())

        # Check it again
        item.setCheckState(QtCore.Qt.Checked)
        self.assertEqual(item.checkState(), QtCore.Qt.Checked)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that _add_stream has been called
        self.assertEqual(self.get_patch('_add_stream').mock.call_count, 3)

        # Uncheck it again (that's the last time, promise...)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.assertEqual(item.checkState(), QtCore.Qt.Unchecked)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that remove_stream has been called
        self.assertEqual(self.get_patch('_remove_stream').mock.call_count, 2)

        # Press Cancel button
        mouse_click(self.win.selection_table.check_list.cancel_btn,
                    QtCore.QPoint(), QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that _add_stream has been called
        self.assertEqual(self.get_patch('_add_stream').mock.call_count, 4)

    def test_confirm_selection(self):
        """Check that everything is correctly updated when pressing the OK button."""

        # Get item and click on it
        item = self.win.selection_table.item(0, 0)
        self.win.selection_table.itemClicked.emit(item)

        # Check that the dialog opened
        self.assertTrue(self.win.selection_table.check_list.isVisible())

        # Get plot and uncheck it
        item = self.win.selection_table.check_list.list_widget.item(0)
        self.assertEqual(item.checkState(), QtCore.Qt.Checked)
        QtTest.QTest.qWait(WAIT_TIME)
        item.setCheckState(QtCore.Qt.Unchecked)
        self.assertEqual(item.checkState(), QtCore.Qt.Unchecked)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that remove_stream has been called
        self.assertEqual(self.get_patch('_remove_stream').mock.call_count, 1)

        # Press OK button
        mouse_click(
            self.win.selection_table.check_list.ok_btn,
            QtCore.QPoint(), QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(WAIT_TIME)

    def test_update_data(self):
        """Check that the plot is updated correctly when dragging the plot lines."""

        # Check initial plot list
        item = self.win.selection_table.item(0, 1)
        x, y = self.session.sensors_data.get_streams('stream')
        val = '%6.6e' % np.interp(x[0], x, y)
        self.assertEqual(item.text(), val)

        # Drag line
        new_value = 1.4
        line = self.win.views['View'].plots[0].line1
        line.setValue(new_value)
        line.sigPositionChangeFinished.emit(line)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check new plot list
        item = self.win.selection_table.item(0, 1)
        val = '%6.6e' % np.interp(new_value, x, y)
        self.assertEqual(item.text(), val)

    def test_search_bar(self):
        """Test the Search bar."""

        # Check that the search bar is initially empty
        self.assertTrue(self.win.search_edit.text() == '')

        # Set regular expression that should show the stream
        self.win.search_edit.setText('st')
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that the row is shown
        self.assertFalse(self.win.selection_table.isRowHidden(0))

        # Set regular expression that should hide the stream
        self.win.search_edit.setText('a')
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that the row is shown
        self.assertTrue(self.win.selection_table.isRowHidden(0))

        # Empty the search bar
        self.win.search_edit.setText('')
        QtTest.QTest.qWait(WAIT_TIME)

        # Everything should be shown
        self.assertFalse(self.win.selection_table.isRowHidden(0))

    def test_widget_width(self):
        """Test that the path name does not impact the width of the widgets."""

        def get_width_of_widgets_in_column(window):

            res = []
            for i in range(window.layout_horizontal_spacing):
                res.append(window.layout.itemAtPosition(i, 0).widget().width())
            return res

        widget_widths = get_width_of_widgets_in_column(self.win)

        # Create a second session with same data but a much longer path
        session2 = Session()

        instance = self.get_patch('RAI.sensors.SensorsData').mock.return_value

        # Session
        session2.sensors_data = instance
        session2.sensors_file = generate_random_path()

        # Window
        win2 = CompositeWindow(self.views, self.videos, parent_session=session2)

        # Show window
        win2.show()
        QtTest.QTest.qWait(WAIT_TIME)

        # Widths of the second window should be the same
        widget_widths2 = get_width_of_widgets_in_column(win2)
        self.assertListEqual(widget_widths, widget_widths2)

        # Close window #2
        win2.close()
        QtTest.QTest.qWait(WAIT_TIME)
