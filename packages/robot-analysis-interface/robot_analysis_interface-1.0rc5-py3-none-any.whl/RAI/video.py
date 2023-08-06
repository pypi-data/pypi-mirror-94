'''
Video
=====

This module provides a :py:class:`Video` class used to display videos on a MainWindow.

:author: Jean-Claude Passy <jean-claude.passy@tuebingen.mpg.de>
'''

from pathlib import Path

import cv2
from packaging import version
from PyQt5 import QtGui, QtCore, QtWidgets

from .serial import Serializable

# OpenCV API is different between 2.x and 3.x
if version.parse(cv2.__version__) < version.parse("3"):
    cv2.CAP_PROP_FRAME_COUNT = cv2.cv.CV_CAP_PROP_FRAME_COUNT
    cv2.CAP_PROP_FRAME_WIDTH = cv2.cv.CV_CAP_PROP_FRAME_WIDTH
    cv2.CAP_PROP_FRAME_HEIGHT = cv2.cv.CV_CAP_PROP_FRAME_HEIGHT
    cv2.CAP_PROP_FPS = cv2.cv.CV_CAP_PROP_FPS
    cv2.CAP_PROP_POS_FRAMES = cv2.cv.CV_CAP_PROP_POS_FRAMES


class Video(Serializable):
    """
    This class provides access to the video to be displayed.

    :param str videoname: Name of the video file.
    :param str name: Name tag of the container.
    :param float offset: Offset between the video and the sensors in seconds (must be > 0)
    """

    serial_version = '1.2'

    # Only .mp4 can be read for now.
    accepted_formats = ['.mp4']

    def __init__(self, filename=None, name='Video', offset=0.0,
                 parent_session=None, parent_window=None, **kwargs):

        ext = Path(filename).suffix
        if ext not in self.accepted_formats:
            raise TypeError(
                f'Cannot load video {filename}. Format must be among {self.accepted_formats}.'
            )

        self.filename = filename
        self.name = name
        self.offset = max(offset, 0.0)
        self.parent_session = parent_session
        self.parent_window = parent_window
        self._fill_video_info()

        # Parameters to be set during the window initialization.
        # Size of the displayed image
        self.widget_width = None
        self.widget_height = None

        # ID number in the GridLayout.
        self.id_number = None
        if 'id_number' in kwargs:
            self.id_number = kwargs['id_number']

    def _fill_video_info(self):
        """Get information about the video using OpenCV, and fill the instance accordingly."""

        # Add root path if needed
        if self.parent_session is not None:
            filename = Path(self.parent_session.root_path) / self.filename
        else:
            filename = Path(self.filename)

        self.capture = cv2.VideoCapture(str(filename))
        if not self.capture.isOpened():
            raise NameError('Cannot initialize video capture from video ' + self.name)

        self.num_frames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.fps = self.capture.get(cv2.CAP_PROP_FPS)
        self.duration = self.num_frames / self.fps

        self.frame_index = 0  # Initially, point at the first frame
        self.video_img = None  # Current frame as read from the video

    @property
    def aspect_ratio(self):
        """Returns the aspect ratio of the frames."""
        return self.widget_width / self.widget_height

    def _prepare(self):
        """Prepare Video widget to be used in class <CompositeWindow>."""

        # Widget to contain the video
        self.image_widget = _ImageWidget(parent_video=self, parent=self.parent_window)

        # Initialization
        self._update_video_to_given_time(0.0)

    def _update_offset(self, offset, current_time):
        """Update the offset of the video and render current frame accordingly."""

        self.offset = offset

        # Update frame (current time stays the same, but frame changes because of the offset change)
        self._update_video_to_given_time(current_time)

    def update_video_to_next_frame(self, time):
        """Update video to the next frame.

        :param float time: time in seconds which the video should be updated to.
        """

        # If the offset is negative and there is no frame
        # corresponding to this part of the sensors,
        # do nothing
        if time + self.offset < 0:
            return

        if self.frame_index < self.num_frames:

            rec, img = self.read_image_from_capture()

            # Update frame_index
            self.frame_index += 1

            # The above should work perfectly. However, sometimes,
            # one cannot read the last frames
            if not rec:
                assert self.frame_index > int(0.95 * self.num_frames)
                img = self.get_closest_frame(self.duration)

            # Update video image
            self.video_img = Video.array_to_qimage(img)

            # Update widget image
            self.image_widget.set_image(self.video_img, self.widget_width, self.widget_height)

    def _update_video_to_given_time(self, time):
        """
        Update video to a specific time.

        :param float time: time in seconds which the video should be updated to.
        """

        # Update video image
        img = self.get_closest_frame(time + self.offset)
        self.video_img = Video.array_to_qimage(img)

        # Update widget image
        self.image_widget.set_image(self.video_img, self.widget_width, self.widget_height)

    def get_closest_frame(self, time):
        """
        Return the closest frame to a given time.

        :param float time: time in seconds which the video should be updated to.
        :returns: closest frame to time.
        :rtype: ``numpy.array``
        """

        # Cannot go below 0 or above the number of frames
        frame_number = min(max(0, int(time / self.duration * self.num_frames)), self.num_frames)
        self.capture.set(int(cv2.CAP_PROP_POS_FRAMES), frame_number)
        rec, img = self.read_image_from_capture()

        # The above should work perfectly. However, sometimes,
        # one cannot read the last frames
        # This is a hacky way to make sure that we get a frame that OpenCV can read.
        while not rec:
            frame_number -= 1
            self.capture.set(int(cv2.CAP_PROP_POS_FRAMES), frame_number)
            rec, img = self.read_image_from_capture()

        self.frame_index = frame_number
        return img

    def read_image_from_capture(self):
        """
        Read the frame from the video capture and return the RGB image.

        :returns: a tuple that contains:
            * a flag that is True if the reading was successful
            * the video frame
        :rtype: tuple(bool,numpy.array)
        """
        rec, img = self.capture.read()
        if rec:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return rec, img

    def _resize_video(self, width, height, ratio=QtCore.Qt.KeepAspectRatio):
        """
        Resize video frame.

        :param int width: new width
        :param int height: new height
        """

        # Update attributes
        self.widget_width = width
        self.widget_height = height

        # Just scale image
        self.image_widget.set_image(self.video_img, self.widget_width, self.widget_height)

    @ staticmethod
    def array_to_qimage(array):
        """
        Convert a numpy array to a Qimage.

        :param numpy.array array: input array
        :param int width: desired width of the image
        :param int height: desired height of the image
        :returns: output image.
        :rtype: ``QImage``
        """

        h, w, bpc = array.shape
        bpl = bpc * w
        image = QtGui.QImage(array.data, w, h, bpl, QtGui.QImage.Format_RGB888)

        return image

    @staticmethod
    def _scale_image(image, width, height, ratio=QtCore.Qt.KeepAspectRatio):
        """Scale QImage.

        :param QImage image: image to scale
        :param int width: desired width of the image
        :param int height: desired height of the image
        :returns: output image
        :rtype: ``QImage``
        """

        if (width is not None) and (height is not None):
            image = image.scaled(width, height, ratio)
        return image

    def serialize(self):

        super().serialize()

        return {
            "filename": self.filename,
            "name": self.name,
            "widget_width": self.widget_width,
            "widget_height": self.widget_height,
            "id_number": self.id_number,
            "serial_version": self.serial_version,
            "offset": self.offset
        }

    @staticmethod
    def deserialize(dictionary, *args, **kwargs):

        # Backwards compatibility
        if dictionary["serial_version"] == '1.0':
            dictionary["filename"] = dictionary.pop("videoname")

        dictionary.pop("serial_version")
        # TODO: Can I remove that?
        dictionary.pop('widget_height')  # temporary until resizeEvent is fixed
        dictionary.pop('widget_width')  # temporary until resizeEvent is fixed
        return Video(**dictionary)


class _ImageWidget(QtWidgets.QWidget):
    """This class represents the image widget used to display a video."""

    # Now the widget needs to know about the parent video in case of a resizing event.
    # May be there is a better way, I'll think about it in the resizing story
    def __init__(self, parent_video=None, parent=None):
        super().__init__(parent)
        self.image = None
        self.parent_video = parent_video
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def set_image(self, image, width, height):
        self.image = Video._scale_image(image, width, height, QtCore.Qt.KeepAspectRatio)
        sz = self.image.size()
        self.setMinimumSize(sz)
        self.update()

    def paintEvent(self, event):
        # change width of image widget as per video widget
        # and change height as per aspect ratio
        width = event.rect().size().width()
        self.image = Video._scale_image(
            self.parent_video.video_img, width,
            width / self.parent_video.aspect_ratio)
        sz = self.image.size()
        self.setMinimumSize(sz)

        qp = QtGui.QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0, 0), self.image)
        qp.end()
