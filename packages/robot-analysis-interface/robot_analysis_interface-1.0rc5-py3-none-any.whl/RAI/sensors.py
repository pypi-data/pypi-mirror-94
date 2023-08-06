'''
Sensors
=======

This module provides a :py:class:`SensorsData` class containing information from the sensors.

:author: Jean-Claude Passy <jean-claude.passy@tuebingen.mpg.de>
'''

import os

from .data_collector import DataCollector
from .serial import Serializable


class SensorsData(Serializable, DataCollector):
    """
    This class reads, stores, and provides access to the data from a sensors file.

    :param str filename: Name of the sensors file.
    :param str name: Name tag of the container.
    :param bool reduce_x_axis: whether we should crop the profiles and remove the 0s at the end of the array `time`.
    :param parent_session: A reference to the managing class.
    :type parent_session: :py:class:`Session<RAI.session.Session>`
    """

    serial_version = '1.0'

    def __init__(self, filename, name='Sensors',
                 reduce_x_axis=True, parent_session=None):

        super().__init__()
        self.reduce_x_axis = reduce_x_axis
        self.filename = filename
        self.name = name
        self.parent_session = parent_session

        # Add root path if needed
        if self.parent_session is not None:
            filename = os.path.join(self.parent_session.root_path, filename)

        try:
            self.load(filename, self.reduce_x_axis)
        except (IOError, AttributeError) as e:
            raise RuntimeError(
                'Cannot load file %s as SensorsData' % self.filename,
                e.message)

        self.max_time = max(self.get_streams("time"))

    def serialize(self):

        super().serialize()

        return {
            "filename": self.filename,
            "name": self.name,
            "serial_version": self.serial_version,
            "arg_max": self.arg_max,
            "reduce_x_axis": self.reduce_x_axis
        }

    @staticmethod
    def deserialize(dictionary, *args, **kwargs):

        dictionary.pop("serial_version")
        dictionary.pop("arg_max")

        return SensorsData(**dictionary)
