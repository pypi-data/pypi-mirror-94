from PyQt5 import QtTest

from RAI.main_window import CompositeWindow

from .fixtures import (
    WAIT_TIME, TOLERANCE,
    TestCaseDefault, PatchWrapper
)


class TestSlider(TestCaseDefault):
    """Class for testing the Slider."""

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

    def test_slider_size(self):
        """Test the min/max values of the slider."""

        # Assertions
        # Initial state of the slider.
        self.assertEqual(self.win.msl.value(), 0.0)

        # Min value should be 0.0
        self.win.msl.setValue(-10.0)
        self.win.msl.sliderReleased.emit()
        QtTest.QTest.qWait(WAIT_TIME)
        self.assertEqual(self.win.msl.value(), 0.0)

        # Max value should be the duration of the video
        self.win.msl.setValue(7.0 * self.video.duration)
        self.win.msl.sliderReleased.emit()
        QtTest.QTest.qWait(WAIT_TIME)
        rel_err = abs(self.win.msl.value() - self.video.duration) / self.video.duration
        self.assertLess(rel_err, TOLERANCE)

        # Check number of calls
        count_theo = 2
        self.assertEqual(self.get_patch('_sync_all_wrt_time').mock.call_count, count_theo)

    def test_update(self):
        """Test that plots/videos/attributes are updated correctly when the slider moves."""

        # Are the lines and start_time updated correctly?
        time = 0.41 * self.video.duration
        self.win.msl.setValue(time)
        self.win.msl.sliderReleased.emit()
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that the timer has been stopped
        self.assertFalse(self.win.timer.status_running)

        # Check that the table has been updated
        count_theo = 1
        self.assertEqual(self.get_patch('_sync_all_wrt_time').mock.call_count, count_theo)
