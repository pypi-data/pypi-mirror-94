import tempfile
from unittest.mock import patch

from PyQt5 import QtCore, QtTest, QtWidgets

from RAI.main_window import CompositeWindow
from RAI.session import Session
from RAI.video import Video

from .fixtures import (
    WAIT_TIME, TOLERANCE,
    TestCaseDefault, PatchWrapper,
    mouse_click, make_random_array
)


class TestVideoButtons(TestCaseDefault):
    """Class for testing the video buttons."""

    def setUp(self):
        super().setUp()

        # Extra patches
        self.patch_wrappers += (
            PatchWrapper(
                "read_image_from_capture", Video,
                return_value=(
                    True,
                    make_random_array(
                        14,
                        self.video.widget_width,
                        self.video.widget_height
                    )
                )
            ),
        )

        # Create window
        self.win = CompositeWindow(self.views, self.videos, parent_session=self.session)

        # Show window
        self.win.show()
        QtTest.QTest.qWait(WAIT_TIME)

    def tearDown(self):

        # Close window
        self.win.close()

        super().tearDown()

    def test_play(self):
        """ Test the PLAY button. """

        # Check that the timer has not started yet
        self.assertFalse(self.win.timer.status_running)

        # Press the PLAY button
        mouse_click(self.win.buttons["Play"], QtCore.QPoint(), QtCore.Qt.LeftButton)

        # Check that the timer has started
        self.assertTrue(self.win.timer.status_running)

        # Wait until the end of the video reading
        QtTest.QTest.qWait(1200 * self.video.duration)

        # Check that the timer has stopped
        self.assertFalse(self.win.timer.status_running)

        # Play button should be disable now
        self.assertFalse(self.win.buttons["Play"].isEnabled())

    def test_stop(self):
        """ Test the STOP button. """

        # Press the PLAY button
        mouse_click(self.win.buttons["Play"], QtCore.QPoint(), QtCore.Qt.LeftButton)

        # Check that the timer has started
        self.assertTrue(self.win.timer.status_running)

        # Wait about half of the video
        waiting_time = 0.5 * self.video.duration  # in s
        QtTest.QTest.qWait(1000. * waiting_time)

        # Press the STOP button
        mouse_click(self.win.buttons["Stop"], QtCore.QPoint(), QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that the timer has stopped
        self.assertFalse(self.win.timer.status_running)

        # Check elapsed time
        self.assertLessEqual(abs(self.win.current_time - waiting_time) / waiting_time, 1.0)

    def test_many_stops(self):
        """ Test the case when the STOP button is pressed several times. """

        # Press the PLAY button
        mouse_click(self.win.buttons["Play"], QtCore.QPoint(), QtCore.Qt.LeftButton)

        # Check that the timer has started
        self.assertTrue(self.win.timer.status_running)

        # Wait about half of the video
        waiting_time = 0.5 * self.video.duration  # in s
        QtTest.QTest.qWait(1000. * waiting_time)

        # Press the STOP button
        mouse_click(self.win.buttons["Stop"], QtCore.QPoint(), QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that the timer has stopped
        self.assertFalse(self.win.timer.status_running)

        # Record current time
        rec_current_time = self.win.current_time

        # Wait again
        QtTest.QTest.qWait(1000. * waiting_time)

        # Press the STOP button
        mouse_click(self.win.buttons["Stop"], QtCore.QPoint(), QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check
        self.assertAlmostEqual(self.win.current_time, rec_current_time)

    def test_reset(self):
        """ Test the RESET button. """

        # Press the PLAY button
        mouse_click(self.win.buttons["Play"], QtCore.QPoint(), QtCore.Qt.LeftButton)

        # Check that the timer has started
        self.assertTrue(self.win.timer.status_running)

        # Wait about half of the video
        waiting_time = 0.5 * self.video.duration  # in s
        QtTest.QTest.qWait(1000. * waiting_time)

        # Press the RESET button
        mouse_click(self.win.buttons["Reset"], QtCore.QPoint(), QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that the timer has stopped
        self.assertFalse(self.win.timer.status_running)

        # Check elapsed time
        self.assertLessEqual(self.win.current_time, TOLERANCE)

        # Check that the slider and the vertical lines have been reset
        for plot in self.win.views['View'].plots:
            self.assertLess(plot.line1.value(), TOLERANCE)
            self.assertLess(plot.line2.value(), TOLERANCE)

        self.assertEqual(self.win.msl.value(), 0)


class TestSessionButtons(TestCaseDefault):
    """Class for testing the session buttons."""

    def setUp(self):
        super().setUp()

        # Extra patches
        self.patch_wrappers += (
            PatchWrapper("save", Session),
            PatchWrapper("load", Session),
            PatchWrapper("exec_", QtWidgets.QFileDialog, return_value=1),  # OK
            PatchWrapper("selectedFiles", QtWidgets.QFileDialog),
        )

        # Create window
        self.win = CompositeWindow(self.views, self.videos, parent_session=self.session)

        # Show window
        self.win.show()
        QtTest.QTest.qWait(WAIT_TIME)

    def tearDown(self):

        # Close window
        self.win.close()

        super().tearDown()

    def load_save_check(self, button_name):
        """Funtion for testing the save and load buttons."""

        # Check that the button is enabled
        self.assertTrue(self.win.buttons[button_name].isEnabled())

        # Choose file to save to.
        with tempfile.NamedTemporaryFile(suffix='.json') as tf:

            # Add return value
            self.get_patch('selectedFiles').mock.return_value = [tf.name]

            # Press the SAVE SESSION button
            mouse_click(self.win.buttons[button_name], QtCore.QPoint(), QtCore.Qt.LeftButton)

            # Save session
            self.win.dlg_save.exec_()
            QtTest.QTest.qWait(WAIT_TIME)

            # Check that save has been called only once and with correct argument
            mock_name = button_name.split()[0].lower()
            self.assertEqual(self.get_patch('selectedFiles').mock.call_count, 1)
            self.assertEqual(self.get_patch(mock_name).mock.call_count, 1)
            self.get_patch(mock_name).mock.assert_called_with(tf.name)

    def test_load(self):
        """ Test the Load Session button. """
        self.load_save_check('Load Session')

    def test_save(self):
        """ Test the Save Session button. """
        self.load_save_check('Save Session')


class TestPlotButtons(TestCaseDefault):
    """Class for testing the plot buttons."""

    def setUp(self):

        super().setUp()

        # Extra patches
        self.patch_wrappers += (
            PatchWrapper("_clear_plots", CompositeWindow),
            PatchWrapper("_remove_plots", CompositeWindow),
            PatchWrapper("_modify_view", CompositeWindow),
            PatchWrapper("exec_", QtWidgets.QFileDialog, return_value=1),
        )
        """
        self.patches[6] = patch.object(CompositeWindow, "_clear_plots")
        self.patches[7] = patch.object(CompositeWindow, "_remove_plots")
        self.patches[8] = patch.object(QtWidgets.QFileDialog, "exec_")
        self.patches[9] = patch.object(CompositeWindow, "_modify_view")
        self.mocked_clear_plots = self.patches[6].start()
        self.mocked_remove_plots = self.patches[7].start()
        self.mocked_exec_ = self.patches[8].start()
        self.mocked_modify_view = self.patches[9].start()

        # Close the dialog with "OK"
        self.mocked_exec_.return_value = 1
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

    def test_add_new_plot(self):
        """ Test the NEW PLOT button. """

        # Check that the button is enabled
        self.assertTrue(self.win.buttons["New Plot"].isEnabled())

        # Press the NEW PLOT button
        mouse_click(self.win.buttons["New Plot"], QtCore.QPoint(), QtCore.Qt.LeftButton)

        QtTest.QTest.qWait(WAIT_TIME)

        # Check that load has been called only once and with correct argument
        self.assertEqual(self.get_patch('_modify_view').mock.call_count, 1)

    def test_clear_plot(self):
        """ Test the CLEAR PLOT button. """

        # Check that the button is enabled
        self.assertTrue(self.win.buttons["Clear Plot"].isEnabled())

        # Press the CLEAR PLOT button
        mouse_click(self.win.buttons["Clear Plot"], QtCore.QPoint(), QtCore.Qt.LeftButton)

        # Check that dialog is open
        self.assertTrue(self.win.check_list.isVisible())
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that the OK button is disabled
        self.assertFalse(self.win.check_list.ok_btn.isEnabled())

        # Check that the correct stream name is shown
        item = self.win.check_list.list_widget.item(0)
        self.assertEqual(item.checkState(), QtCore.Qt.Unchecked)
        QtTest.QTest.qWait(WAIT_TIME)
        item.setCheckState(QtCore.Qt.Checked)
        self.assertEqual(item.checkState(), QtCore.Qt.Checked)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that the OK button is enabled
        self.assertTrue(self.win.check_list.ok_btn.isEnabled())

        # Press the OK button
        mouse_click(self.win.check_list.ok_btn, QtCore.QPoint(), QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that load has been called only once and with correct argument
        self.assertEqual(self.get_patch('_clear_plots').mock.call_count, 1)
        self.get_patch('_clear_plots').mock.assert_called_with([0])

    def test_remove_plot(self):
        """ Test the REMOVE PLOT button. """

        # Check that the button is enabled
        self.assertTrue(self.win.buttons["Remove Plot"].isEnabled())

        # Press the REMOVE PLOT button
        mouse_click(self.win.buttons["Remove Plot"], QtCore.QPoint(), QtCore.Qt.LeftButton)

        # Check that dialog is open
        self.assertTrue(self.win.check_list.isVisible())
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that the OK button is not enabled
        self.assertFalse(self.win.check_list.ok_btn.isEnabled())

        # Check item
        item = self.win.check_list.list_widget.item(0)
        item.setCheckState(QtCore.Qt.Checked)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that the OK button is not enabled
        self.assertTrue(self.win.check_list.ok_btn.isEnabled())

        # Press the OK button
        mouse_click(self.win.check_list.ok_btn, QtCore.QPoint(), QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that load has been called only once and with correct argument
        self.assertEqual(self.get_patch('_remove_plots').mock.call_count, 1)
        self.get_patch('_remove_plots').mock.assert_called_with([0])


class TestWindowButtons(TestCaseDefault):
    """Class for testing the window buttons."""

    def setUp(self):

        super().setUp()

        # Extra patches
        # Extra patches
        self.patch_wrappers += (
            PatchWrapper("_build_new_view", CompositeWindow),
            PatchWrapper("_on_save_view_button_clicked", CompositeWindow),
            PatchWrapper("_on_load_view_button_clicked", CompositeWindow),
            PatchWrapper("_on_rename_view_button_clicked", CompositeWindow),
            PatchWrapper("_on_refresh_btn_clicked", CompositeWindow),
        )
        """
        self.patches[6] = patch.object(CompositeWindow, "_build_new_view")
        self.patches[7] = patch.object(CompositeWindow, "_on_save_view_button_clicked")
        self.patches[8] = patch.object(CompositeWindow, "_on_load_view_button_clicked")
        self.patches[9] = patch.object(CompositeWindow, "_on_rename_view_button_clicked")
        self.patches[10] = patch.object(CompositeWindow, "_on_refresh_btn_clicked")
        self.mocked_build_new_view = self.patches[6].start()
        self.mocked_on_save_view_button_clicked = self.patches[7].start()
        self.mocked_on_load_view_button_clicked = self.patches[8].start()
        self.mocked_on_rename_view_button_clicked = self.patches[9].start()
        self.mocked_on_refresh_btn_clicked = self.patches[10].start()
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

    def test_add_new_view(self):
        """ Test the NEW VIEW button. """

        # Check that the button is enabled
        self.assertTrue(self.win.buttons["New View"].isEnabled())

        # Press the NEW PLOT button
        mouse_click(self.win.buttons["New View"], QtCore.QPoint(), QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check right calls
        self.assertEqual(self.get_patch('_build_new_view').mock.call_count, 1)

    def test_save_view(self):
        """ Test the SAVE VIEW button. """

        # Check that the button is enabled
        self.assertTrue(self.win.buttons["Save Views"].isEnabled())

        # Press the NEW PLOT button
        mouse_click(self.win.buttons["Save Views"], QtCore.QPoint(), QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check right calls
        self.assertEqual(self.get_patch('_on_save_view_button_clicked').mock.call_count, 1)

    def test_load_view(self):
        """ Test the LOAD VIEWS button. """

        # Check that the button is enabled
        self.assertTrue(self.win.buttons["Load Views"].isEnabled())

        # Press the NEW PLOT button
        mouse_click(self.win.buttons["Load Views"], QtCore.QPoint(), QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check right calls
        self.assertEqual(self.get_patch('_on_load_view_button_clicked').mock.call_count, 1)

    def test_rename_view(self):
        """ Test the RENAME VIEW button. """

        # Check that the button is enabled
        self.assertTrue(self.win.buttons["Rename View"].isEnabled())

        # Press the NEW PLOT button
        mouse_click(self.win.buttons["Rename View"], QtCore.QPoint(), QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check right calls
        self.assertEqual(self.get_patch('_on_rename_view_button_clicked').mock.call_count, 1)

    def test_copy_path(self):
        """Test the button copying the file path to the clipboard."""

        # Check that the button is enabled
        self.assertTrue(self.win.buttons["Copy Path"].isEnabled())

        clipboard = QtWidgets.QApplication.clipboard()

        # Clipboard should be empty at start
        clipboard.clear()
        self.assertEqual(clipboard.text(), u'')

        # Press the button
        mouse_click(self.win.buttons["Copy Path"], QtCore.QPoint(), QtCore.Qt.LeftButton)

        # Clipboard should contain the path
        self.assertEqual(clipboard.text(), self.session.sensors_file)

    def test_refresh_sensors_data(self):
        """Test the button refreshing the Sensors data file."""

        # Check that the button is enabled
        self.assertTrue(self.win.buttons["Refresh Data"].isEnabled())

        # Press the button
        mouse_click(self.win.buttons["Refresh Data"], QtCore.QPoint(), QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check right calls
        self.assertEqual(self.get_patch('_on_refresh_btn_clicked').mock.call_count, 1)
