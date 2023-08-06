import random

import numpy
from PyQt5 import QtGui, QtTest
import qimage2ndarray

from RAI.main_window import CompositeWindow
from RAI.video import Video

from .fixtures import (
    WAIT_TIME,
    TestCaseDefault, PatchWrapper,
    make_random_array
)


class TestVideo(TestCaseDefault):
    """Class for testing the Video."""

    def my_side_effect_time(self, *args):
        """Returns a random array using the first argument as a seed."""

        # Keeping argument as float since fps is randomly chosen (not 1.0)
        seed = args[0]
        # frame index should be in the range 0 to number of frames
        self.video.frame_index = min(
            max(0, int(seed / self.video.duration * self.video.num_frames)),
            self.video.num_frames - 1
        )
        return make_random_array(
            self.video.frame_index,
            self.video.widget_width,
            self.video.widget_height
        )

    def setUp(self):
        super().setUp()

        # List of mock images read from the capture
        self.img_list = [
            (True, make_random_array(seed, self.video.widget_width, self.video.widget_height))
            for seed in range(self.video.num_frames)
        ]

        # Extra patches
        self.patch_wrappers += (
            PatchWrapper(
                "read_image_from_capture",
                Video,
                side_effect=lambda: self.img_list[self.video.frame_index + 1]),
        )

        # Adding side effet
        self.get_patch('get_closest_frame').mock.side_effect = self.my_side_effect_time

        # Check video call
        self.get_patch('_fill_video_info').mock.assert_called_with()
        self.assertEqual(self.get_patch('_fill_video_info').mock.call_count, 1)

        # Create window
        self.win = CompositeWindow(self.views, self.videos, parent_session=self.session)

        # Show window
        self.win.show()
        QtTest.QTest.qWait(WAIT_TIME)

    def tearDown(self):

        # Close window
        self.win.close()

        super().tearDown()

    def test_wrong_format(self):
        """Testing that the correct exception is thrown if the video has not the correct format."""

        filename = 'my_bad_video.mov'
        with self.assertRaisesRegex(TypeError, "Cannot load video*"):
            _ = Video(filename)

    def test_video_prepare(self):
        """Test initialization of the video."""

        # Check initial frame
        img_theo = make_random_array(0, self.video.widget_width, self.video.widget_height)
        pixmap_check = self.video.image_widget.image
        pixmap_check = pixmap_check.convertToFormat(QtGui.QImage.Format_RGB32)
        pixmap_check = Video._scale_image(
            pixmap_check, self.video.widget_width, self.video.widget_height)
        img_check = qimage2ndarray.rgb_view(pixmap_check)

        numpy.testing.assert_array_equal(img_check, img_theo)

    def test_video_update_video_to_next_frame(self):
        """Test the video playing capability of the window."""

        # Start the time
        self.win.timer.start()

        # Wait until the full video has been played
        # We reduce wait time to avoid rendering next frame
        QtTest.QTest.qWait(950 * self.video.duration)
        self.win.timer.stop()

        # Assertions
        # Right number of calls is (total frames - 1) as one initial frame is used for rendering during app start
        self.assertEqual(self.get_patch('read_image_from_capture').mock.call_count,
                         self.video.num_frames - 1)

        # Check last frame
        pixmap_check = self.video.image_widget.image
        pixmap_check = pixmap_check.convertToFormat(QtGui.QImage.Format_RGB32)
        pixmap_check = Video._scale_image(
            pixmap_check, self.video.widget_width, self.video.widget_height)
        img_check = qimage2ndarray.rgb_view(pixmap_check)

        numpy.testing.assert_array_equal(img_check, self.img_list[-1][1])

        # Reset and add negative offset
        self.win.msl.setValue(0.0)
        self.win.msl.sliderReleased.emit()
        self.assertAlmostEqual(self.win.current_time, 0.0)
        offset = -2.0

        self.video._update_offset(offset, self.win.current_time)

        # Play for 2 seconds, nothing should happen
        self.win.timer.start()
        QtTest.QTest.qWait(2000)
        self.win.timer.stop()
        self.assertEqual(self.get_patch('read_image_from_capture').mock.call_count,
                         self.video.num_frames - 1)

    def test_video_update_offset(self):
        """Test the behavior of the video when the offset is modified."""

        self.assertAlmostEqual(self.win.current_time, 0.0)
        self.assertAlmostEqual(self.video.offset, 0.0)
        self.assertEqual(self.video.frame_index, 0)

        # No offset Initial frame
        pixmap_check = self.video.image_widget.image
        pixmap_check = pixmap_check.convertToFormat(QtGui.QImage.Format_RGB32)
        pixmap_check = Video._scale_image(
            pixmap_check, self.video.widget_width, self.video.widget_height)
        img_check = qimage2ndarray.rgb_view(pixmap_check)
        numpy.testing.assert_array_equal(img_check, self.img_list[self.video.frame_index][1])
        # Update offset by about 2 seconds
        offset = 2.1
        # Calculate frame number(should be in range 0 to number of frames) to check locally
        frame_number = min(max(0, int((offset / self.video.duration) * self.video.num_frames)),
                           self.video.num_frames - 1)

        self.video._update_offset(offset, self.win.current_time)
        QtTest.QTest.qWait(WAIT_TIME)

        self.assertAlmostEqual(self.win.current_time, 0.0)
        self.assertAlmostEqual(self.video.offset, offset)
        self.assertEqual(self.video.frame_index, frame_number)
        # Check image
        pixmap_check = self.video.image_widget.image
        pixmap_check = pixmap_check.convertToFormat(QtGui.QImage.Format_RGB32)
        pixmap_check = Video._scale_image(
            pixmap_check, self.video.widget_width, self.video.widget_height)
        img_check = qimage2ndarray.rgb_view(pixmap_check)
        numpy.testing.assert_array_equal(img_check, self.img_list[self.video.frame_index][1])

        # Update offset to negative value - frame index should be 0
        offset = -1.0
        frame_number = min(max(0, int(self.win.current_time + offset / self.video.duration * self.video.num_frames)),
                           self.video.num_frames - 1)

        self.video._update_offset(offset, self.win.current_time)
        QtTest.QTest.qWait(WAIT_TIME)

        self.assertAlmostEqual(self.win.current_time, 0.0)
        self.assertAlmostEqual(self.video.offset, offset)
        self.assertEqual(self.video.frame_index, frame_number)

    def test_video_update_to_given_time(self):
        """Test the painting capability when the video is updated to a specific time."""

        get_frame_call = 1
        self.assertEqual(self.get_patch('get_closest_frame').mock.call_count, get_frame_call)
        self.assertEqual(self.video.frame_index, 0)

        # Update the image to a random time of the movie
        time = random.randint(0, self.video.duration)
        # Update frame as per random time and offset
        frame_number = min(max(0, int(time / self.video.duration *
                                      self.video.num_frames)), self.video.num_frames - 1)
        # No offset
        self.assertAlmostEqual(self.video.offset, 0.0)
        self.win.msl.setValue(time)
        self.win.msl.sliderReleased.emit()
        # update get closest frame call count
        get_frame_call += 1

        # Check number of calls
        self.assertEqual(self.get_patch('get_closest_frame').mock.call_count, get_frame_call)
        self.assertEqual(self.video.frame_index, frame_number)

        # Check current frame using frame number since fps varies randomly
        img_theo = make_random_array(
            frame_number, self.video.widget_width, self.video.widget_height)
        pixmap_check = self.video.image_widget.image
        pixmap_check = pixmap_check.convertToFormat(QtGui.QImage.Format_RGB32)
        img_check = qimage2ndarray.rgb_view(pixmap_check)

        numpy.testing.assert_array_equal(img_check, img_theo)
        # offset list: positive, too much positive, negative, too much negative
        offsets = [1.0, 10.0, -2.0, -10.0]
        for offset in offsets:
            self.assertAlmostEqual(self.win.current_time, time)
            self.video._update_offset(offset, self.win.current_time)
            # update get closest frame call count and frame number since initial time is randomly chosen
            get_frame_call += 1
            time_offset = time + offset
            frame_number = min(max(0, int(time_offset / self.video.duration * self.video.num_frames)),
                               self.video.num_frames - 1)

            # Check number of calls and index
            self.assertEqual(self.get_patch('get_closest_frame').mock.call_count, get_frame_call)
            self.assertEqual(self.video.frame_index, frame_number)

    def test_serialize(self):
        """Test the serialization of a Video."""

        # Serialize video
        dictionary = self.video.serialize()

        # Check that the dictionary is not empty
        self.assertGreater(len(dictionary), 0)

        # The dictionary should have at least some fundamental elements
        elements = ['filename', 'name', 'widget_width', 'widget_height', 'serial_version', 'offset']
        for x in elements:
            self.assertTrue(x in dictionary)

    def test_deserialize(self):
        """Test the deserialization of a Video."""

        # Serialize video
        dictionary = self.video.serialize()

        loaded_video = Video.deserialize(dictionary)

        # The dictionary should have at least some fundamental elements
        elements = ['filename', 'name', 'id_number', 'offset']
        for elem in elements:
            self.assertEqual(getattr(self.video, elem), getattr(loaded_video, elem))
