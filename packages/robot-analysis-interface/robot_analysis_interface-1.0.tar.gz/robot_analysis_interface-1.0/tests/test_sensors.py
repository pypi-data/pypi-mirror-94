from unittest import TestCase

import numpy
import pkg_resources

from RAI.sensors import SensorsData


class SensorFileMixin:
    """Mixin for testing a sensors file."""

    filename = None

    def setUp(self):
        self.assertIsNotNone(self.filename)
        self.sensors_data = SensorsData(self.filename)
        self.assertIsNotNone(self.sensors_data)

    def test_read(self):
        """Test if one can read the data from a sensors file."""

        time = self.sensors_data.get_streams('time')
        self.assertIsInstance(time, list)
        self.assertGreater(len(time), 0)

        time_units = self.sensors_data.get_units('time')
        self.assertIsInstance(time_units, str)
        self.assertEqual(time_units, 's')

        time2 = self.sensors_data.get_streams(['time', 'time'])
        self.assertIsInstance(time2, list)
        self.assertEqual(len(time2), 2)

        time_units2 = self.sensors_data.get_units(['time', 'time'])
        self.assertIsInstance(time_units2, list)

    def test_serialize(self):
        """Test the serialization of a SensorsData."""

        # Serialize SensorsData
        dictionary = self.sensors_data.serialize()

        # Check that the dictionary is not empty
        self.assertGreater(len(dictionary), 0)

        # The dictionary should have at least some fundamental elements
        elements = ['filename', 'reduce_x_axis', 'serial_version']
        for x in elements:
            self.assertIsNotNone(dictionary[x])

    def test_deserialize(self):
        """Test the deserialization of a SensorsData."""

        # Serialize SensorsData
        dictionary = self.sensors_data.serialize()

        # Load SensorsData
        loaded_sensors_data = SensorsData.deserialize(dictionary)

        # The dictionary should have at least some fundamental elements
        elements = ['filename', 'name', 'reduce_x_axis', 'arg_max', 'fields', 'units']

        for elem in elements:
            try:
                self.assertEqual(getattr(self.sensors_data, elem),
                                 getattr(loaded_sensors_data, elem))
            except AttributeError:
                for a, b in zip(getattr(self.sensors_data, elem),
                                getattr(loaded_sensors_data, elem)):
                    self.assertListEqual(a, b)

        # Check that the data are the same (some values are NaN)
        elem = 'data'
        for a, b in zip(getattr(self.sensors_data, elem),
                        getattr(loaded_sensors_data, elem)):
            numpy.testing.assert_array_equal(a, b)


class TestSensorsDFile(SensorFileMixin, TestCase):
    """Class for testing the Sensors D File."""

    filename = pkg_resources.resource_filename(
        'RAI', 'resources/d00300')


class TestSensorsPickle(SensorFileMixin, TestCase):
    """Class for testing the Sensors D File."""

    filename = pkg_resources.resource_filename(
        'RAI', 'resources/jviereck_hopper/traj.pkl')
