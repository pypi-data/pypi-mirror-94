from pathlib import Path
import random
import tempfile

import json
import numpy as np
import pkg_resources
from PyQt5 import QtTest

from RAI.main_window import CompositeWindow
from RAI.sensors import SensorsData
from RAI.session import Session
from RAI.utils import get_app
from RAI.video import Video

from .fixtures import WAIT_TIME, MockedTestCase, PatchWrapper


class TestSession(MockedTestCase):
    """Class for testing a Session."""

    def run(self, *args, **kwargs):
        # Create temporary dir for the session file
        with tempfile.TemporaryDirectory() as tf:
            self.session_file = Path(tf) / 'Session.json'
            return super().run(*args, **kwargs)

    def setUp(self):
        super().setUp()

        # Get QApplication
        self.app = get_app()

        self.sensors_file = pkg_resources.resource_filename('RAI', 'resources/d00300')
        self.videos_list = [
            pkg_resources.resource_filename('RAI', 'resources/solo.mp4'),
            pkg_resources.resource_filename('RAI', 'resources/bolt.mp4')
        ]
        self.views_data = {}
        self.views_data['View'] = {0: ['LF_z', 'momrate_ref__a'], 1: ['momrate_ref__a'], 2: []}

        self.session = Session(self.sensors_file, self.videos_list, self.views_data)

    def tearDown(self):
        super().tearDown()

        # Close window and delete app
        self.session.window.close()
        self.app.deleteLater()
        QtTest.QTest.qWait(WAIT_TIME)

    def test_unicity(self):
        """Check the unicity of each session."""

        session2 = Session(self.sensors_file, self.videos_list, self.views_data)
        self.assertNotEqual(self.session.ID, session2.ID)

        # Close window
        session2.window.close()
        QtTest.QTest.qWait(WAIT_TIME)

    def test_launch(self):
        """Check that a window is created and visible when the session is launched."""

        # Launch session
        self.session.launch(start_qt_loop=False)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check that a window exists and is visible
        self.assertTrue(hasattr(self.session, 'window'))
        self.assertIsNotNone(self.session.window)
        self.assertTrue(self.session.window.isVisible())

    def test_refresh_sensors_data(self):
        """Check that the Sensors Data is correctly refreshed."""

        # Here we will:
        #  1- take a stream from the current sensors_file
        #  2- modify it
        #  3- save it in a new file and reload the SensorsData object
        #  4- check that the values of this field have changed

        # Step 1
        random_field = random.choice(list(self.session.sensors_data.fields))
        xold, yold = self.session.sensors_data.get_streams(["time", random_field])

        # Step 2
        random_float = random.uniform(0.0, 1e3)
        random_int = random.randint(1, 100)

        x = xold + [random_float] * random_int
        y = yold + [random_float ** 2.0] * random_int
        fields = {
            'time': 0,
            random_field: 1
        }
        units = {
            'time': 's',
            random_field: 'whatever'
        }
        data = [x, y]
        metadata = {'robot': 'R2D2'}
        dict_data = {
            'fields': fields,
            'units': units,
            'data': data,
            'metadata': metadata
        }

        # Step 3
        with tempfile.NamedTemporaryFile("w+b", suffix=".npy") as new_sensors:

            np.save(new_sensors.name, dict_data)
            self.session.sensors_file = new_sensors.name

            # Reload
            self.session.refresh_sensors_data()

            # Step 4
            x_new, y_new = self.session.sensors_data.get_streams(["time", random_field])
            self.assertEqual(len(x_new), len(xold) + random_int)
            self.assertEqual(len(y_new), len(x_new))

            for i in range(random_int):
                self.assertAlmostEqual(x_new[-i - 1], random_float)
                self.assertAlmostEqual(y_new[-i - 1], random_float ** 2.0)

    def test_serialization(self):
        """Test the serialization of a Session."""

        # Extra patches
        self.patch_wrappers += (
            PatchWrapper("serialize", SensorsData, prefix='sensor'),
            PatchWrapper("serialize", Video, prefix='video'),
            PatchWrapper("serialize", CompositeWindow, prefix='window'),
        )

        # Save session
        self.session.save(self.session_file)

        # Check that the file is not empty
        session_file_path = Path(self.session_file)
        self.assertTrue(session_file_path.is_file())
        self.assertGreater(session_file_path.stat().st_size, 0)
        QtTest.QTest.qWait(WAIT_TIME)

        # Check the correct number of calls
        self.assertEqual(self.get_patch('sensor_serialize').mock.call_count, 1)
        self.assertEqual(self.get_patch('video_serialize').mock.call_count, len(self.videos_list))
        self.assertEqual(self.get_patch('window_serialize').mock.call_count, 1)

        # The file should have at least some fundamental elements
        elements = ['ID', 'creation_time', 'framework_version', 'root_path']

        with open(self.session_file) as data_file:
            data = json.load(data_file)
            for x in elements:
                self.assertIsNotNone(data[x])

    def test_deserialization(self):
        """ Test the deserialization of a Session. """

        # Extra patches
        self.patch_wrappers += (
            PatchWrapper("deserialize", SensorsData, prefix='sensor'),
            PatchWrapper("deserialize", Video, prefix='video'),
            PatchWrapper("deserialize", CompositeWindow, prefix='window'),
        )

        # Save session
        self.session.save(self.session_file)

        # Rebuild session
        session2 = Session.load(self.session_file)

        # Check the correct number of calls
        self.assertEqual(self.get_patch('sensor_deserialize').mock.call_count, 1)
        self.assertEqual(self.get_patch('video_deserialize').mock.call_count, len(self.videos_list))
        self.assertEqual(self.get_patch('window_deserialize').mock.call_count, 1)

        # Two sessions are identical if some elements for each class are equal
        session_elements = ['ID', 'creation_time', 'root_path']
        for elem in session_elements:
            self.assertEqual(getattr(self.session, elem), getattr(session2, elem))

        # Close window
        session2.window.close()
