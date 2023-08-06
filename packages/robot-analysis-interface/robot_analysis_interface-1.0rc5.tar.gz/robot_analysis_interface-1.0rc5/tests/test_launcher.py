import contextlib
from itertools import product
import os
from pathlib import Path
import shutil
import tempfile

import numpy as np
import pkg_resources

from RAI.launcher import launcher as rai_launcher

from .fixtures import TestCaseDefault


@contextlib.contextmanager
def chdir(path):
    """Context manager for changing directory."""
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)


class TestLauncher(TestCaseDefault):
    """Class for testing the launcher."""

    def setUp(self):
        super().setUp()

        # Session file
        self.session_file = Path(
            pkg_resources.resource_filename('RAI', 'resources/session_demo.json')
        )

        # Folder with test resources
        self.test_resources_path = Path(__file__).parent / 'resources'

        # do not display the window for the unit test
        self.launcher_extra_args = ['--no-window']

    def test_no_data(self):
        """Launcher smoke test without data."""

        # No session file
        with self.assertRaises(ValueError):
            rai_launcher(self.launcher_extra_args)

        # with session(global path) file
        self.launcher_extra_args += [
            '--session=' + str(self.session_file.absolute())
        ]
        with self.assertRaises(ValueError):
            rai_launcher(self.launcher_extra_args)

        # with session(local path) file
        self.launcher_extra_args += [
            '--session=' + str(self.session_file.relative_to(Path.cwd()))
        ]
        with self.assertRaises(ValueError):
            rai_launcher(self.launcher_extra_args)

    def test_no_data_auto_discovery_dfile(self):
        """Test auto discovering a d-file."""

        dfile_path = Path(__file__).parent / 'resources'

        with tempfile.TemporaryDirectory() as td:
            with open(Path(td) / 'd0000', 'wb') as f:
                shutil.copy2(
                    pkg_resources.resource_filename('RAI', 'resources/d00300'),
                    f.name
                )
            with chdir(Path(td)):
                data_tmp = rai_launcher(self.launcher_extra_args)

        # Checks
        np.testing.assert_array_almost_equal(
            data_tmp.sensors_data.get_streams('time'),
            np.arange(0.0, 4.889, 0.002)
        )

    def test_no_data_auto_discovery_dg_folder(self):
        """Test auto discovering a folder."""

        with tempfile.TemporaryDirectory() as td:
            resources = Path(td) / 'resources'
            shutil.copytree(
                self.test_resources_path,
                resources
            )
            with chdir(Path(resources)):
                data_tmp = rai_launcher(self.launcher_extra_args)

            # Checks
            data_0 = np.loadtxt(Path(resources) / '2019-09-12_04-03-17/data_0.dat')
            data_1 = np.loadtxt(Path(resources) / '2019-09-12_04-03-17/data_1.dat')

            np.testing.assert_almost_equal(
                np.array(data_tmp.sensors_data.get_streams("data_0/1")), data_0[:4, 1])
            np.testing.assert_almost_equal(
                np.array(data_tmp.sensors_data.get_streams("data_0/2")), data_0[:4, 2])
            np.testing.assert_almost_equal(
                np.array(data_tmp.sensors_data.get_streams("data_0/3")), data_0[:4, 3])

            np.testing.assert_almost_equal(
                np.array(data_tmp.sensors_data.get_streams("data_1/1")), data_1[:, 1])
            np.testing.assert_almost_equal(
                np.array(data_tmp.sensors_data.get_streams("data_1/2")), data_1[:, 2])
            np.testing.assert_almost_equal(
                np.array(data_tmp.sensors_data.get_streams("data_1/3")), data_1[:, 3])
            np.testing.assert_almost_equal(
                np.array(data_tmp.sensors_data.get_streams("data_1/4")), data_1[:, 4])

    def launch_and_check_session(self, file_or_folder):
        """Helper to lauch and assert a session."""

        # Loop through all the combinations with data and session
        data_args = [
            '--data=' + str(file_or_folder.absolute()),
            '--data=' + str(file_or_folder.relative_to(Path.cwd())),
        ]
        session_args = [
            '--session=' + str(self.session_file.absolute()),
            '--session=' + str(self.session_file.relative_to(Path.cwd()))
        ]
        all_args = [[x] for x in data_args]
        all_args += [list(x) for x in product(data_args, session_args)]

        for a in all_args:
            self.launcher_extra_args += a
            my_test_session = rai_launcher(self.launcher_extra_args)

            # Checks
            if any('session' in _ for _ in self.launcher_extra_args):
                self.assertEqual(my_test_session.ID, "5b55bfcab80a11e78330f48c50c559b3")
            self.assertEqual(my_test_session.sensors_file, file_or_folder.name)
            self.assertEqual(my_test_session.root_path, str(file_or_folder.parent.absolute()))

    def test_with_data_global(self):
        """Launcher smoke test with data."""
        dfile = Path(pkg_resources.resource_filename('RAI', 'resources/d00300'))
        self.launch_and_check_session(dfile)

    def test_with_folder(self):
        """Launcher smoke test with folder."""
        folder = self.test_resources_path / '2019-08-12_02-03-19'
        self.launch_and_check_session(folder)
