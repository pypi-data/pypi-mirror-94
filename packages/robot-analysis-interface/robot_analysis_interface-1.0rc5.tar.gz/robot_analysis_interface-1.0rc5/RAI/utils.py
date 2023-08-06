'''
Utils
=====

This module provides utility functions for the RAI.

:author: Jean-Claude Passy <jean-claude.passy@tuebingen.mpg.de>
'''

from contextlib import contextmanager
from pathlib import Path
import sys

import cv2
import numpy as np
from PyQt5 import QtWidgets

from .video import Video


def show_video(video, frame_folder=None):
    """
    Play the video in a separate OpenCV window.

    :param :py:class:`Video<RAI.video.Video>` video: Video to be displayed.
    :param str frame_folder: folder where to save frames
    """

    if not isinstance(video, Video):
        TypeError("Expected argument of type Video, instead got %s." % type(video))

    # By default, save all frames in the cwd
    frame_folder = frame_folder or Path('.')

    # Set pointer to first frame
    frame_number = 0
    video.capture.set(int(cv2.CAP_PROP_POS_FRAMES), frame_number)
    rec = 0

    # Show all the frames
    print("Press q to stop video, SPACE to save frame")
    while not rec and frame_number < video.num_frames:
        ret, frame = video.capture.read()
        if not ret:
            break

        # Allow interactive resizing
        cv2.namedWindow(video.name, cv2.WINDOW_NORMAL)

        # Show frame
        cv2.imshow(video.name, frame)

        # Save frame or quit
        time_between_frames = int(1000.0 / video.fps)  # in ms
        rec = _check_for_command(time_between_frames, frame, frame_number, frame_folder)
        frame_number += 1

    # Last command before closing the window
    print("Press q to close window, SPACE to save the last frame")
    while _check_for_command(0, frame, frame_number, frame_folder) == 0:
        pass

    cv2.destroyAllWindows()


def _check_for_command(time, frame, frame_number, frame_folder):
    """
    Check for command sent by the user.

    :param int time: time in ms to wait for user's command
    :param numpy.array frame: current frame
    :param int frame_number: number of the frame
    :param Path frame_folder: where to save the frame
    """

    key = cv2.waitKey(time)
    c = chr(key & 255)

    if c == 'q':
        return -1
    if c == ' ':
        filename = str(frame_folder / f"frame{frame_number:04d}.jpg")
        cv2.imwrite(filename, frame)
        print("Saved frame to " + filename)
    return 0


def get_app():
    """
    Return either the QtWidgets.QApplication that is already running, or a newly created one.

    :returns: the only running QtWidgets.QApplication
    :rtype: ``QtWidgets.QApplication``
    """

    # Do not use Qtwidgets.qApp! (empty static wrapper that cannot return None)
    # See http://stackoverflow.com/questions/40400954/qapp-versus-qapplication-instance

    global app  # unclear why this is needed, but a segfault is thrown otherwise
    app = QtWidgets.QApplication.instance()

    if app is None:
        app = QtWidgets.QApplication(sys.argv)

    # Change app style, otherwise checkboxes are not shown
    app.setStyle(QtWidgets.QStyleFactory.create('Plastique'))
    return app


def _build_common_widget(parent, nrow, ncol, *args, **kwargs):
    """
    Generate a QGridLayout widget made out of several widgets passed by *args.

    :param int nrow: number of rows of the widget.
    :param int ncol: number of columns of the widget.
    :returns: common widget
    :rtype: ``QWidget``
    """

    # Check size and number of widgets match
    if not (nrow * ncol == len(args)):
        raise RuntimeError("Trying to put %i widgets in a GridLayout with %i cells."
                           % (len(args), nrow * ncol))

    common_widget = QtWidgets.QWidget(parent)
    common_layout = QtWidgets.QGridLayout(common_widget)
    common_layout.setHorizontalSpacing(nrow)
    common_layout.setVerticalSpacing(ncol)

    # Set stretch factors
    if "stretch_columns" in kwargs:
        for col in range(ncol):
            common_layout.setColumnStretch(col, kwargs["stretch_columns"][col])

    for i in range(0, nrow):
        for j in range(0, ncol):
            index = j + i * ncol
            common_layout.addWidget(args[index], i, j)

    return common_widget


def _remove_widget_from_gridlayout(layout, row, col):
    """
    Remove item and widget from layout.

    :param QtWidgets.QGridLayout layout: layout
    :param int row: row number of the widget to delete
    :param int col: column number of the widget to delete
    """

    if layout.itemAtPosition(row, col) is not None:
        widget = layout.itemAtPosition(row, col).widget()
        layout.removeWidget(widget)
        widget.setParent(None)
        widget.deleteLater()


@contextmanager
def signals_blocked(obj):
    """Context manager for blocking signals of an object."""

    obj.blockSignals(True)
    yield
    obj.blockSignals(False)


def are_zeros_and_ones(x):
    """
    Check if the values in the array are only 0s and 1s.

    :param numpy.array x: array of floats
    """

    rtol = 1e-9
    atol = 1e-9
    are_zeros = np.isclose(x, np.zeros(len(x)), rtol=rtol, atol=atol)
    are_ones = np.isclose(x, np.ones(len(x)), rtol=rtol, atol=atol)

    return np.logical_or(are_zeros, are_ones).all()
