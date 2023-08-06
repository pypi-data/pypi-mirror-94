'''
Fixtures
========

This module provides utility fixtures for unit testing of the framework.

:author: Jean-Claude Passy <jean-claude.passy@tuebingen.mpg.de>
'''

from contextlib import suppress
import os
import random
import string
from unittest import TestCase
from unittest.mock import patch, MagicMock

import numpy
from PyQt5 import QtGui, QtCore, QtTest, QtWidgets
from pyqtgraph.graphicsItems.LegendItem import LegendItem

from RAI.video import Video
from RAI.main_window import CompositeWindow
from RAI.session import Session
from RAI.utils import get_app


def make_random_array(seed, width, height):
    """ Create a random RGB array according to a given seed.

    :param seed: seed for the random generator.
    :type seed: int
    :param width: width of the array
    :type width: int
    :param height: height of the array
    :type height: int
    """

    # Seed can now be negative if video offset is negative
    prng = numpy.random.RandomState(max(0, seed))

    # Build RGB image
    img = prng.randint(0, 256, size=(width, height, 3))
    img = numpy.array(img, dtype='uint8')
    return img


# Constants for fake plots
MAX_TIME = 10
FAKE_X = numpy.arange(0, MAX_TIME, 0.1)
FAKE_Y = FAKE_X ** 2

# Constants for fake videos
VIDEO_SIZE = 100  # heigh and width in pixels
FAKE_FRAME = make_random_array(
    41, VIDEO_SIZE, VIDEO_SIZE
)
# Additional constants
WAIT_TIME = 1000  # Process waiting time (in ms)
TOLERANCE = 1e-6  # Tolerance for some assertion checks


class PatchWrapper:
    """Class representing and manipulating a patch.

    :param str name: Name of the method or the class to patch
    :param object obj: If any, object to patch
    :param object return_value: Mock return value
    :param fun side_effect: Mock side effects
    :param str prefix: Prefix used to differentiate patches
    """

    def __init__(self, name, obj=None, return_value=None, side_effect=None, prefix=None):

        # Create patch
        if not obj:
            self.patcher = patch(name)
        else:
            self.patcher = patch.object(obj, name)

        self.name = prefix + '_' + name if prefix else name

        # Start patch
        self.mock = self.patcher.start()

        # Define return value and/or side_effect:
        if return_value is not None:
            self.mock.return_value = return_value
        if side_effect is not None:
            self.mock.side_effect = side_effect

    def stop(self):
        """Stop a patch."""
        with suppress(RuntimeError):  # in case patch has already been stopped
            self.patcher.stop()


class MockedTestCase(TestCase):
    """TestCase for which classes and functions are mocked."""

    def setUp(self):
        # Create patches
        self.patch_wrappers = ()

    def tearDown(self):
        # Stop patchers
        for p in self.patch_wrappers:
            p.stop()

    def get_patch(self, name):
        """Returns a PatchWrapper instance by name."""

        for p in self.patch_wrappers:
            if p.name == name:
                return p
        raise ValueError(f"No PatchWrapper with name {name}")


class TestCaseDefault(MockedTestCase):
    """Default TestClass used in most tests."""

    def setUp(self):
        super().setUp()

        # Get QApplication
        self.app = get_app()

        # Create patches
        super().setUp()
        self.patch_wrappers += (
            PatchWrapper(
                'RAI.sensors.SensorsData',
                return_value=MagicMock(
                    fields=['stream'],
                    max_time=10,
                    get_streams=lambda s: (FAKE_X, FAKE_Y)
                )
            ),
            PatchWrapper("_fill_video_info", Video),
            PatchWrapper("get_closest_frame", Video, FAKE_FRAME),
            PatchWrapper("_resize_video", Video),
            PatchWrapper("_resize_current_video", CompositeWindow),
            PatchWrapper("removeItem", LegendItem, prefix='legend'),
            PatchWrapper("addItem", LegendItem),
        )

        # Session
        self.session = Session()
        self.session.sensors_data = self.get_patch('RAI.sensors.SensorsData').mock.return_value
        self.session.sensors_file = 'Fake Sensors'

        # View
        self.views = {}
        self.views['View'] = {0: ['stream'], 1: ['stream']}

        # Video
        self.video = Video('video.mp4')
        self.video.num_frames = 6
        # Setting random video duration and fps
        self.video.duration = random.randint(1, 10)
        self.video.fps = self.video.num_frames / self.video.duration
        self.video.widget_height = VIDEO_SIZE
        self.video.widget_width = VIDEO_SIZE
        self.video.frame_index = 0
        self.video.offset = 0.0
        self.videos = [self.video]

    def tearDown(self):

        super().tearDown()
        self.app.deleteLater()
        QtTest.QTest.qWait(WAIT_TIME)


def key_press(widget, key, modifier=QtCore.Qt.NoModifier, text='', autorep=False, count=1):
    """Key press event.

    :param widget: target widget.
    :type widget: QtWidgets.QWidget
    :param modifier: keyboard modifier.
    :type modifier: QtCore.Qt.KeyboardModifiers
    :param text: unicode text generated by the key.
    :type text: QString
    :param autorep: whether the event comes from an auto-repeating key.
    :type autorep: bool
    :param count: number of keys involved in the event.
    :type count: int
    """

    app = get_app()
    event = QtGui.QKeyEvent(QtCore.QEvent.KeyPress, key, modifier, text, autorep, count)
    app.sendEvent(widget, event)


def mouse_press(widget, point, button, buttons=QtCore.Qt.NoButton, modifier=QtCore.Qt.NoModifier):
    """Mouse press event.

    :param widget: target widget.
    :type widget: QtWidgets.QWidget
    :param point: position of the mouse.
    :type point: QtCore.QPoint
    :param button: button to press.
    :type button: QtCore.Qt.MouseButton
    :param buttons: buttons pressed at the time of the event.
    :type buttons: QtCore.Qt.MouseButton
    :param modifier: keyboard modifier.
    :type modifier: QtCore.Qt.KeyboardModifiers
    """

    app = get_app()
    event = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress, point, button, buttons, modifier)
    app.sendEvent(widget, event)


def mouse_release(widget, point, button, buttons=QtCore.Qt.NoButton, modifier=QtCore.Qt.NoModifier):
    """Mouse release event.QtWidgets.QWidget

    :param widget: target widget.
    :type widget: QtWidgets.QWidget
    :param point: position of the mouse.
    :type point: QtCore.QPoint
    :param button: button to release.
    :type button: QtCore.Qt.MouseButton
    :param buttons: buttons pressed at the time of the event.
    :type buttons: QtCore.Qt.MouseButton
    :param modifier: keyboard modifier.
    :type modifier: QtCore.Qt.KeyboardModifiers
    """

    # For difference between QTest and QMouseEvent in the mouse drag case,
    # see https://atlas.is.localnet/confluence/display/SW/PyQt

    app = get_app()
    event = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonRelease, point, button, buttons, modifier)
    app.sendEvent(widget, event)


def mouse_move(widget, point, buttons=QtCore.Qt.NoButton, modifier=QtCore.Qt.NoModifier):
    """Mouse move event handler.

    :param widget: target widget.
    :type widget: QtWidgets.QWidget
    :param point: position of the mouse.
    :type point: QtCore.QPoint
    :param buttons: buttons pressed at the time of the event.
    :type buttons: QtCore.Qt.MouseButtons
    :param modifier: keyboard modifier.
    :type modifier: QtCore.Qt.KeyboardModifiers
    """

    app = get_app()
    event = QtGui.QMouseEvent(QtCore.QEvent.MouseMove, point, QtCore.Qt.NoButton, buttons, modifier)
    app.sendEvent(widget, event)

    # Physically move the mouse (not strictly necessary but it is nice if we can visualize it).
    QtTest.QTest.mouseMove(widget, point)


def mouse_click(widget, point, button, buttons=QtCore.Qt.NoButton, modifier=QtCore.Qt.NoModifier):
    """Mouse click event.

    :param widget: target widget.
    :type widget: QtWidgets.QWidget
    :param point: position of the mouse.
    :type point: QtCore.QPoint
    :param button: button to click.
    :type button: QtCore.Qt.MouseButton
    :param buttons: buttons pressed at the time of the event.
    :type buttons: QtCore.Qt.MouseButtons
    :param modifier: keyboard modifier.
    :type modifier: QtCore.Qt.KeyboardModifiers
    """

    mouse_move(widget, point, buttons, modifier)
    mouse_press(widget, point, button, buttons, modifier)
    mouse_release(widget, point, button, button, modifier)


def mouse_drag(widget, start, end, button, buttons=QtCore.Qt.NoButton, modifier=QtCore.Qt.NoModifier):
    """Mouse drag event.

    :param widget: target widget.
    :type widget: QtWidgets.QWidget
    :param start: start position of the mouse.
    :type start: QtCore.QPoint
    :param end: end position of the mouse.
    :type end: QtCore.QPoint
    :param button: button to press.
    :type button: QtCore.Qt.MouseButton
    :param buttons: buttons pressed at the time of the event.
    :type buttons: QtCore.Qt.MouseButtons
    :param modifier: keyboard modifier.
    :type modifier: QtCore.Qt.KeyboardModifiers
    """

    mouse_move(widget, start, buttons, modifier)
    mouse_press(widget, start, button, buttons, modifier)
    mouse_move(widget, end, button, modifier)
    mouse_release(widget, end, button, button, modifier)


def widgets_at(point):
    """Return all widgets at a given position.

    :param point: position.
    :type point: QtCore.QPoint
    :returns list of widgets at given position.
    :rtype list(QtWidgets.QWidget)
    """

    widgets = []
    widget_at = QtWidgets.qApp.widgetAt(point)

    while widget_at:
        widgets.append(widget_at)

        # Make widget invisible to MouseEvents
        widget_at.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        widget_at = QtWidgets.qApp.widgetAt(point)

    # Restore attribute
    for widget in widgets:
        widget.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, False)

    return widgets


def widgets_under_mouse():
    """Return all widgets under the mouse.

    :returns list of widgets under the mouse.
    :rtype list(QtWidgets.QWidget)
    """

    point = QtGui.QCursor.pos()
    return widgets_at(point)


def window_widgets(window):
    """Return all widgets for a given window.
    :param window: window of interest
    :type window: QtWidgets.QMainWindow
    :returns widgets of a given window
    :rtype list(QtWidgets.QWidget)
    """

    # Take central widget of the window and its layout
    cen_wid = window.centralWidget()
    layout = cen_wid.layout()

    return [layout.itemAt(i).widget() for i in range(layout.count())]


def widget_has_item(widget, item_name):
    """Check if a widget has a given item.
    :param widget: widget of interest
    :type widget: ``Widget``
    :param item_name: name of the searched item
    :type item_name: str
    :returns True or False
    :rtype bool
    """

    # Loop through all the items that belong to the widget
    for item in widget.items():
        if item_name == item.__class__.__name__:
            return True

    return False


def create_dummy_data():
    """
    Create dummy data.
    :return: some simple data
    :rtype: dict
    """

    fields = {"time": 0, "x": 1, "y": 2, "z": 3}
    units = {"time": "s", "x": "m", "y": "m", "z": "m"}
    data = [
        [float(x) for x in range(0, 11)],
        [float(x) for x in range(10, 21)],
        [float(x) for x in range(20, 31)],
        [float(x) for x in range(30, 41)]
    ]
    metadata = {'robot': 'athena'}
    return {
        'fields': fields,
        'units': units,
        'data': data,
        'metadata': metadata
    }


def generate_random_path(nb_folders=None):
    """Generate a random path."""

    nb_folders = nb_folders if nb_folders else random.randint(1, 10)
    path = ""
    for _ in range(nb_folders):
        path = os.path.join(path, generate_random_string())
    return path


def generate_random_string():
    """Generate a random string of random length using upper/lower case letters and digits."""

    length = random.randint(5, 64)
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
