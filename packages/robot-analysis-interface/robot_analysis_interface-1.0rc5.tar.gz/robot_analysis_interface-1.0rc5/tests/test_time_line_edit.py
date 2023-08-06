import random

from PyQt5 import QtTest, QtCore

from RAI.main_window import CompositeWindow

from .fixtures import (
    WAIT_TIME, TestCaseDefault, PatchWrapper,
    key_press
)


class TestTimeLineEdit(TestCaseDefault):
    """Class for testing the Timeline Edit."""

    def setUp(self):

        super().setUp()

        # Extra patches
        self.patch_wrappers += (
            PatchWrapper("_sync_all_wrt_time", CompositeWindow),
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

    def test_update_time(self):
        """Test that plots/videos/attributes are updated correctly when the user inputs a time."""

        # New time value
        time = random.uniform(0, 10)

        # Enter time in LineEdit
        self.win.time_line_edit.setValue(time)
        QtTest.QTest.qWait(WAIT_TIME)

        # Press Enter
        key_press(self.win.time_line_edit, QtCore.Qt.Key_Return)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check number of calls
        self.assertEqual(self.get_patch('_sync_all_wrt_time').mock.call_count, 1)
        self.assertAlmostEqual(
            self.get_patch('_sync_all_wrt_time').mock.call_args[0][0],
            time,
            places=3
        )
