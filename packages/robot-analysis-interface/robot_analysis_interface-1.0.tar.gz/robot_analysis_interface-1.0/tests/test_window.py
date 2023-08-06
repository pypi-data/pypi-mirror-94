from copy import deepcopy
import json
import random
from unittest.mock import patch

from PyQt5 import QtTest, QtCore

from RAI.main_window import CompositeWindow
from RAI.plotting import Plot
from RAI.session import Session
from RAI.table import SelectionTable
from RAI.video import Video

from .fixtures import (
    WAIT_TIME, TOLERANCE,
    TestCaseDefault, PatchWrapper,
    FAKE_FRAME, mouse_click,
)


class TestWindow(TestCaseDefault):
    """Class for testing the Window."""

    def setUp(self):
        super().setUp()

        # Extra patches
        self.patch_wrappers += (
            PatchWrapper("read_image_from_capture", Video, return_value=(True, FAKE_FRAME)),
            PatchWrapper("_get_color_from_curve", Plot, return_value=0),
            PatchWrapper("update_data", SelectionTable),
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

    def test_sync_all_wrt_time(self):
        """Test the synchronization of all widgets."""

        # New time value (float rounded to 2 decimal places) for random video duration
        time = round(random.uniform(0.1, self.video.duration), 2)

        # Call synchronization
        self.win._sync_all_wrt_time(time)

        # Check that Plots have been updated
        for plot in self.win.views['View'].plots:
            self.assertLess(abs(plot.line1.value() - time), TOLERANCE)
            self.assertLess(abs(plot.line2.value() - time), TOLERANCE)

        # Check that an update of the frames has been called
        count_theo = 2 * len(self.videos)
        self.assertEqual(self.get_patch('get_closest_frame').mock.call_count, count_theo)

        # Check that the table has been updated
        count_theo = 1
        self.assertEqual(self.get_patch('update_data').mock.call_count, count_theo)

        # Check that the slider has been updated
        rel_err = abs(self.win.msl.value() - time) / time
        # Precision given by the number of steps of the slider (+ buffer)
        precision = (2 + 1) * 1 / self.win.msl.steps_per_seconds
        self.assertLess(rel_err, precision)

        # Check that LineEdit has been updated
        self.assertEqual(self.win.time_line_edit.value(), time)

        # Check that start_time has been updated
        self.assertLess(abs(self.win.current_time - time), TOLERANCE)

    def test_add_new_plot(self):
        """Check that we can add a new empty plot."""

        # Initial plot layout
        nrows = self.win.views['View'].vertical_layout_plots_scroll.count()

        # Add new plot
        self.win._on_new_plot_button_clicked()
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that layout has increased
        nrows_new = self.win.views['View'].vertical_layout_plots_scroll.count()
        self.assertEqual(nrows_new, nrows + 1)
        QtTest.QTest.qWait(WAIT_TIME)

        # New Plot should be empty
        new_plot = self.win.views['View'].plots[nrows_new - 1]
        self.assertEqual(new_plot.x_data, {})
        self.assertEqual(new_plot.y_data, {})
        self.assertEqual(new_plot.streams, [])

    def test_remove_plot(self):
        """Check that we can remove a plot."""

        # Initial values
        nrows = self.win.views['View'].vertical_layout_plots_scroll.count()
        deleted_plot = self.win.views['View'].plots[0]
        survivor_plot = self.win.views['View'].plots[1]

        # Remove plot
        self.win._remove_plots([0])
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that layout has decreased
        nrows_new = self.win.views['View'].vertical_layout_plots_scroll.count()
        self.assertEqual(nrows_new, nrows - 1)

        # Check that the remaining plot has changed position
        self.assertNotEqual(deleted_plot, self.win.views['View'].plots[0])
        self.assertEqual(survivor_plot, self.win.views['View'].plots[0])

    def test_serialize(self):
        """Test the serialization of a Window."""

        # Serialize window
        dictionary = self.win.serialize()

        # Check that the dictionary is not empty
        self.assertGreater(len(dictionary), 0)

        # The dictionary should have at least some fundamental elements
        elements = ['title', 'window_size', 'plot_size', 'serial_version']

        for x in elements:
            self.assertIsNotNone(dictionary[x])

    def test_deserialize(self):
        """Test the deserialization of a Window."""

        from RAI.session import RAIEncoder

        # Serialize window
        dictionary = json.loads(json.dumps(self.win, sort_keys=True, indent=4, cls=RAIEncoder))
        QtTest.QTest.qWait(WAIT_TIME)

        new_session = Session()
        new_session.sensors_data = self.session.sensors_data
        new_session.sensors_file = self.session.sensors_file
        loaded_win = CompositeWindow.deserialize(dictionary, self.videos, new_session)

        # The dictionary should have at least some fundamental elements
        elements = ['title', 'width', 'height',
                    'layout_horizontal_spacing', 'layout_vertical_spacing']

        for elem in elements:
            self.assertEqual(getattr(self.win, elem), getattr(loaded_win, elem))

        # Close and delete
        loaded_win.close()

    def test_refresh_sensors_data(self):
        """Check that everything gets updated when we refresh the sensors data."""

        with patch.object(Session, 'refresh_sensors_data') as mocked_refresh_sensors_data, \
                patch.object(Plot, '_update_stream') as mocked_update_stream:

            self.win._on_refresh_btn_clicked()
            QtTest.QTest.qWait(WAIT_TIME)

            self.assertEqual(mocked_refresh_sensors_data.call_count, 1)
            self.assertEqual(mocked_update_stream.call_count, len(self.views['View']))

    def test_splitter_resize(self):
        """Check that videos are resized properly when moving the splitter."""

        # set opaque resizing as false to visualize splitter working
        self.win.main_splitter.setOpaqueResize(False)

        # Get initial sizes of the widgets around the splitter (list)
        init_videos_width = self.win.vertical_widget_videos.geometry().width()
        sizes = self.win.main_splitter.sizes()

        # By how much the sizes will changes
        size_delta = random.randint(1, 100)  # in pixels

        # Increase plots
        self.win.main_splitter.setSizes([sizes[0] + size_delta, sizes[1] - size_delta])
        self.assertEqual(self.win.vertical_widget_videos.geometry().width(),
                         init_videos_width - size_delta)

        # Increase videos
        self.win.main_splitter.setSizes([sizes[0] - size_delta, sizes[1] + size_delta])
        self.assertEqual(self.win.vertical_widget_videos.geometry().width(),
                         init_videos_width + size_delta)

    def test_frame_resize(self):
        """Test if the video frame is resized correctly during a resizeEvent of the window."""

        # initial size of window and video image
        init_win_size = self.win.size()
        init_image_size = self.video.image_widget.image.size()

        win_size_delta = random.randint(50, 500)  # in pixels

        # Resize window 1: decreasing width
        self.win.resize(init_win_size.width() - win_size_delta, init_win_size.height())
        # wait for the size update
        QtTest.QTest.qWait(WAIT_TIME)

        # check 1: video image size decreases
        resized_video_image = self.video.image_widget.image.size()
        self.assertLess(resized_video_image.width(), init_image_size.width())

        # Resize window 2: decreasing height
        self.win.resize(init_win_size.width() - win_size_delta,
                        init_win_size.height() - win_size_delta)
        QtTest.QTest.qWait(WAIT_TIME)

        # check 2: video image no size change
        self.assertEqual(self.video.image_widget.image.size(), resized_video_image)

        # Resize window 3: increase both height and width
        self.win.resize(init_win_size.width() + win_size_delta,
                        init_win_size.height() + win_size_delta)
        QtTest.QTest.qWait(WAIT_TIME)

        # check 3: video image size increases
        self.assertGreater(self.video.image_widget.image.size().width(), init_image_size.width())


class TestWindowNoVideo(TestCaseDefault):
    """Class to test the window without videos."""

    def setUp(self):

        super().setUp()

        # Create window
        self.win = CompositeWindow(self.views, None, parent_session=self.session)

        # Show window
        self.win.show()
        QtTest.QTest.qWait(WAIT_TIME)

    def test_no_video(self):
        """Test a Window without Video."""

        # Check that the window is visible
        self.assertTrue(self.win.isVisible())
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that the dimensions are correct
        self.assertEqual(self.win.layout_horizontal_spacing, 3)
        self.assertEqual(self.win.layout_vertical_spacing, 2)

        # Check that there is no Video buttons
        self.assertFalse('Play' in self.win.buttons.keys())
        self.assertFalse('Stop' in self.win.buttons.keys())
        self.assertFalse('Reset' in self.win.buttons.keys())

        # Check that there is no slider
        self.assertFalse(hasattr(self.win, 'msl'))

    def tearDown(self):

        # Close window
        self.win.close()

        super().tearDown()


class TestWindowVideoOffset(TestCaseDefault):
    """Class testing functionalities relative to the video offsets."""

    def setUp(self):
        super().setUp()

        # Extra patches
        self.patch_wrappers += (
            PatchWrapper("read_image_from_capture", Video, return_value=(True, FAKE_FRAME)),
            PatchWrapper("_update_offset", Video),
        )

        # Add second video to compare offsets and sync them
        video2 = deepcopy(self.video)
        video2.name = "Copied video"
        video2.duration = self.video.duration * 2  # second video twice as long
        video2.num_frames = 11
        self.videos.append(video2)

        # Create window
        self.win = CompositeWindow(self.views, self.videos, parent_session=self.session)

        # Show window
        self.win.show()
        QtTest.QTest.qWait(WAIT_TIME)

    def test_enter_offset(self):
        """Test entering an offset value."""

        # SpinBox to specify offset
        spin_box = self.win.time_offset_boxes[self.video]

        # Initially must be 0
        self.assertAlmostEqual(spin_box.value(), 0.0)
        self.assertEqual(self.get_patch('_update_offset').mock.call_count, 0)

        # Input negative value: cannot go below - max_time
        spin_box.setValue(-2 * self.session.sensors_data.max_time)
        self.assertAlmostEqual(spin_box.value(), -self.session.sensors_data.max_time)
        self.assertEqual(self.get_patch('_update_offset').mock.call_count, 1)

        # Input number larger than video duration : should become the video duration
        spin_box.setValue(5 * self.video.duration)
        self.assertAlmostEqual(spin_box.value(), self.video.duration)
        self.assertEqual(self.get_patch('_update_offset').mock.call_count, 2)
        self.get_patch('_update_offset').mock.assert_called_with(
            self.video.duration, self.win.current_time)

        # That should work
        new_offset_val = random.uniform(-self.session.sensors_data.max_time, self.video.duration)
        spin_box.setValue(new_offset_val)
        self.assertAlmostEqual(spin_box.value(), round(new_offset_val, 3))
        self.assertEqual(self.get_patch('_update_offset').mock.call_count, 3)
        self.get_patch('_update_offset').mock.assert_called_with(
            round(new_offset_val, 3), self.win.current_time)

        # Check that timer is stopped when offset it set
        self.assertFalse(self.win.timer.status_running)
        self.win.timer.start()
        self.assertTrue(self.win.timer.status_running)
        QtTest.QTest.qWait(1000)

        spin_box.setValue(1.0)
        self.assertFalse(self.win.timer.status_running)

    def test_sync_offset(self):
        """Test synchronizing the offsets between different videos."""

        self.patch_wrappers += (
            PatchWrapper("_on_offset_changed", CompositeWindow),
        )

        # SpinBoxes to specify offset
        spin_box0 = self.win.time_offset_boxes[self.videos[0]]
        spin_box1 = self.win.time_offset_boxes[self.videos[1]]

        # Sync button
        sync_btn = self.win.sync_offset_buttons[self.videos[0]]

        # Set offsets
        val1 = random.uniform(-self.session.sensors_data.max_time, self.video.duration)
        spin_box0.setValue(val1)
        self.assertEqual(self.get_patch('_on_offset_changed').mock.call_count, 1)
        self.get_patch('_on_offset_changed').mock.assert_called_with(round(val1, 3), self.videos[0])
        QtTest.QTest.qWait(WAIT_TIME)

        val2 = random.uniform(-self.session.sensors_data.max_time, self.video.duration)
        spin_box1.setValue(val2)
        self.assertEqual(self.get_patch('_on_offset_changed').mock.call_count, 2)
        self.get_patch('_on_offset_changed').mock.assert_called_with(round(val2, 3), self.videos[1])
        QtTest.QTest.qWait(WAIT_TIME)

        # Set up offset for video 0 and sync all others
        self.videos[0].offset = val1
        mouse_click(sync_btn, QtCore.QPoint(), QtCore.Qt.LeftButton)
        QtTest.QTest.qWait(WAIT_TIME)

        # Only one more call on the second video
        self.assertEqual(self.get_patch('_on_offset_changed').mock.call_count, 3)
        self.get_patch('_on_offset_changed').mock.assert_called_with(round(val1, 3), self.videos[1])

    def test_compute_video_playing_time(self):
        """Test the computation of the video playing time."""

        # Stop offset patch
        self.get_patch('_update_offset').stop()

        # SpinBoxes to specify offsets
        spin_box0 = self.win.time_offset_boxes[self.videos[0]]
        spin_box1 = self.win.time_offset_boxes[self.videos[1]]

        # Case 1
        # First, it should be the duration of the first video (because it is shorter)
        self.assertAlmostEqual(self.win.min_duration, self.videos[0].duration)
        mouse_click(self.win.buttons["Play"], QtCore.QPoint(), QtCore.Qt.LeftButton)  # play video
        QtTest.QTest.qWait(1200 * self.win.min_duration)
        self.assertAlmostEqual(self.win.min_duration, 0)
        self.assertFalse(self.win.buttons["Play"].isEnabled())

        # Reset - min_duration back to original value and Play button enabled
        mouse_click(self.win.buttons["Reset"], QtCore.QPoint(), QtCore.Qt.LeftButton)
        self.assertAlmostEqual(self.win.min_duration, self.videos[0].duration)
        self.assertTrue(self.win.buttons["Play"].isEnabled())

        # Case 2: Offset Video 2 by 1 second and Video 1 by 0: nothing should change
        QtTest.QTest.qWait(WAIT_TIME)
        spin_box0.setValue(0.0)
        # Setting offset 1.0 since random minimum duration is 1.0 seconds (Video 2 min. duration will be 2.0 seconds)
        spin_box1.setValue(1.0)
        self.assertAlmostEqual(self.win.min_duration, self.videos[0].duration)
        mouse_click(self.win.buttons["Play"], QtCore.QPoint(), QtCore.Qt.LeftButton)  # play video
        QtTest.QTest.qWait(1200 * self.win.min_duration)
        self.assertAlmostEqual(self.win.min_duration, 0)
        self.assertFalse(self.win.buttons["Play"].isEnabled())

        # Case 3: Offset Video 1 by 1 second and Video 2 by 0: 1 second less in the video 1 reading
        QtTest.QTest.qWait(WAIT_TIME)
        mouse_click(self.win.buttons["Reset"], QtCore.QPoint(), QtCore.Qt.LeftButton)
        # Setting offset 1.0 since random minimum duration is 1.0 seconds
        spin_box0.setValue(1.0)
        spin_box1.setValue(0.0)
        self.assertAlmostEqual(self.win.min_duration, self.videos[0].duration - 1.0)
        mouse_click(self.win.buttons["Play"], QtCore.QPoint(), QtCore.Qt.LeftButton)  # play video
        QtTest.QTest.qWait(1200 * self.win.min_duration)
        self.assertAlmostEqual(self.win.min_duration, 0)
        self.assertFalse(self.win.buttons["Play"].isEnabled())

        # Case 4: Offset Video 1 by -1 second and Video 2 by 0
        QtTest.QTest.qWait(WAIT_TIME)
        mouse_click(self.win.buttons["Reset"], QtCore.QPoint(), QtCore.Qt.LeftButton)
        spin_box0.setValue(-1.0)
        spin_box1.setValue(0.0)
        self.assertAlmostEqual(self.win.min_duration, self.videos[0].duration + 1.0)
        mouse_click(self.win.buttons["Play"], QtCore.QPoint(), QtCore.Qt.LeftButton)  # play video
        QtTest.QTest.qWait(1200 * self.win.min_duration)
        self.assertAlmostEqual(self.win.min_duration, 0)
        self.assertFalse(self.win.buttons["Play"].isEnabled())

        # Case 5: Offset Video 1 by -(Video 1 random duration + 1) and Video 2 by 0 (can read video 2 fully)
        QtTest.QTest.qWait(WAIT_TIME)
        mouse_click(self.win.buttons["Reset"], QtCore.QPoint(), QtCore.Qt.LeftButton)
        spin_box0.setValue(-(self.videos[0].duration + 1))
        spin_box1.setValue(0.0)
        self.assertAlmostEqual(self.win.min_duration, self.videos[1].duration)
        mouse_click(self.win.buttons["Play"], QtCore.QPoint(), QtCore.Qt.LeftButton)  # play video
        QtTest.QTest.qWait(1200 * self.win.min_duration)
        self.assertAlmostEqual(self.win.min_duration, 0)
        self.assertFalse(self.win.buttons["Play"].isEnabled())

    def tearDown(self):

        # Close window
        self.win.close()

        super().tearDown()
