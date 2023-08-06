'''
Session
=======

This module provides a :py:class:`Session` class to handle an analysis session.

:author: Jean-Claude Passy <jean-claude.passy@tuebingen.mpg.de>
'''


import os
import json
from time import asctime
import uuid

from .main_window import CompositeWindow
from .sensors import SensorsData
from .serial import Serializable
from .utils import get_app
from .version import __version__ as framework_version
from .video import Video


class Session(Serializable):
    """
    This class handles the creation of the CompositeWindow and of the necessary instances.
    It also offers the capability to save and load the current state of the analysis session.

    :param str sensors_file: Name of the Sensors file
    :param list(str) video_files: Name of the videos to include
    :param dict view_data: Data describing the Plots and the View
    """

    serial_version = '1.1'
    framework_version = framework_version

    def __init__(self, sensors_file=None, video_files=None, views_data=None):

        self.ID = uuid.uuid1().hex
        self.creation_time = asctime()

        # Paths are relative with respect to the location of the sensors file
        if sensors_file is not None:
            self.root_path, self.sensors_file = os.path.split(os.path.abspath(sensors_file))
        else:
            self.root_path = None
            self.sensors_file = None

        self.video_files = []
        if video_files is not None:
            for filename in video_files:
                rel_path = os.path.relpath(filename, self.root_path)
                self.video_files.append(rel_path)

        # Add an empty View in case None is provided by the user
        empty_view = {
            'Empty View': {0: []}
        }
        views_data = views_data or empty_view

        if self.sensors_file or self.video_files:
            self._prepare(views_data)

    def _prepare(self, views_data):
        """Prepare the session."""

        # Get QApplication
        app = get_app()

        # Build sensors data
        if self.sensors_file is not None:
            self.sensors_data = SensorsData(self.sensors_file, parent_session=self)

        # Build videos
        self.videos = []
        for video in self.video_files:
            self.videos.append(Video(video, parent_session=self))

        # Build window
        self.window = CompositeWindow(views_data, self.videos, parent_session=self)

    def refresh_sensors_data(self):
        """Refresh the sensors data."""

        assert self.sensors_file is not None, \
            'Sensors file path is None, cannot refresh.'

        self.sensors_data = SensorsData(self.sensors_file, parent_session=self)

    def launch(self, start_qt_loop=True):
        """
        Launch the session.

        :param bool start_qt_loop: start the Qt loop for events input by the user?
        """

        # potential utility to kill the app with normal crtl+c
        # https://stackoverflow.com/questions/4938723/what-is-the-correct-way-to-make-my-pyqt-application-quit-when-killed-from-the-co

        # Get QApplication
        app = get_app()

        # Show window
        self.window.show()

        # Start Qt loop
        if start_qt_loop:
            app.exec_()

    def save(self, session_file):
        """
        Write a JSON file that contains the session data necessary for restart.

        :param str session_file: session file
        :returns: saved session filename
        :rtype: str
        """

        session_file = os.path.abspath(session_file)

        with open(session_file, 'w') as f:
            json.dump(self, f, sort_keys=True, indent=4, cls=RAIEncoder)

    def serialize(self):

        super().serialize()

        return {
            "ID": self.ID,
            "creation_time": self.creation_time,
            "root_path": self.root_path,
            "sensors_data": self.sensors_data,
            "videos": self.videos,
            "window": self.window,
            "serial_version": self.serial_version,
            "framework_version": self.framework_version
        }

    @staticmethod
    def load(session_file):
        """
        Deserialize JSON file and restart session.

        :param str session_file: session file
        :returns: loaded session
        :rtype: Session
        """

        session_file = os.path.abspath(session_file)

        with open(session_file) as data_file:
            data = json.load(data_file)

        # Call deserialize and return session
        return Session.deserialize(data)

    @staticmethod
    def deserialize(dictionary, *args, **kwargs):

        # Get QApplication
        app = get_app()

        # Build session
        session = Session()

        # Some arguments to copy
        for elem in ["ID", "creation_time"]:
            setattr(session, elem, dictionary[elem])

        # Need to specify parent_session for root_path
        if dictionary["serial_version"] > '1.0':
            elem = "root_path"
            setattr(session, elem, dictionary[elem])
            dictionary['sensors_data']['parent_session'] = session
            for one_dict in dictionary['videos']:
                one_dict['parent_session'] = session

        # Build sensors data
        if dictionary['sensors_data'] is not None:
            session.sensors_data = SensorsData.deserialize(dictionary['sensors_data'],)
            setattr(session, 'sensors_file', dictionary['sensors_data']['filename'])

        # Build videos
        session.videos = []
        if dictionary['videos'] is not None:
            setattr(session, 'video_files', [video.videoname for video in session.videos])
            for one_dict in dictionary['videos']:
                session.videos.append(Video.deserialize(one_dict))

        # Build window
        session.window = CompositeWindow.deserialize(dictionary['window'], session.videos, session)

        return session


class RAIEncoder(json.JSONEncoder):
    """JSON encoder for data structures."""

    def default(self, o):
        if issubclass(type(o), Serializable):
            return o.serialize()
        return
