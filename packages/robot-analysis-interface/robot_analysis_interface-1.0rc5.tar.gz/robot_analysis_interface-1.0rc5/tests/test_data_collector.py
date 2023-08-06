"""
Author: Maximilien Naveau  Max Planck Institute for Intelligent System
Tubingen 2017
publication : (None)

This file contains tests for the DataCollector class.
(see file RAI/data_collector.py)

"""

from pathlib import Path
import pickle
import tempfile
from unittest import TestCase

import pkg_resources
import numpy as np

from RAI.data_collector import DataCollector

from .fixtures import create_dummy_data, TOLERANCE

try:
    import pinocchio as se3
    USE_PINOCCHIO = True
except ImportError:
    USE_PINOCCHIO = False


def eye(n):
    """
    Returns a square diagonal matrix with 1s on the diagonal.
    :param int n: Linear dimension of the matrix
    """
    return np.matrix(np.eye(n), np.double)


def rand(n):
    """
    Returns a matrix filled with random values.
    :param int or list(int) n: Dimensions of the matrix. If int, the matrix is a vector.
    """
    array = np.random.rand(n, 1) if isinstance(n, int) else np.random.rand(n[0], n[1])
    return np.matrix(array, np.double)


def isapprox(a, b, epsilon=TOLERANCE):
    if "np" in a.__class__.__dict__:
        a = a.np
    if "np" in b.__class__.__dict__:
        b = b.np
    if isinstance(a, (np.ndarray, list)) and isinstance(b, (np.ndarray, list)):
        return np.allclose(a, b, epsilon)
    return abs(a - b) < epsilon


class TestDataCollector(TestCase):
    """Class for testing the Data Collector."""

    def setUp(self):
        self.dc = DataCollector()

    def tearDown(self):
        self.dc.sanity_check()

    def test_get_streams(self):
        """ Test accessing the streams."""

        self.dc.from_dictionary(create_dummy_data())
        data = create_dummy_data()
        self.assertEqual(self.dc.get_streams('time'), data['data'][0])
        self.assertEqual(self.dc.get_streams('x'), data['data'][1])
        self.assertEqual(self.dc.get_streams('y'), data['data'][2])
        self.assertEqual(self.dc.get_streams('z'), data['data'][3])
        self.assertEqual(self.dc.get_streams(['time', 'x']),
                         [data['data'][0], data['data'][1]])
        self.assertEqual(self.dc.get_streams(['y', 'z']),
                         [data['data'][2], data['data'][3]])

    def test_get_one_stream(self):
        """Test accessing one stream."""

        self.dc.from_dictionary(create_dummy_data())
        data = create_dummy_data()
        self.assertEqual(self.dc._get_one_stream('time'), data['data'][0])
        self.assertEqual(self.dc._get_one_stream('x'), data['data'][1])
        self.assertEqual(self.dc._get_one_stream('y'), data['data'][2])
        self.assertEqual(self.dc._get_one_stream('z'), data['data'][3])

    def test_get_all_streams(self):
        """Test accessing all stream."""

        self.dc.from_dictionary(create_dummy_data())
        data = create_dummy_data()
        self.assertEqual(self.dc.get_all_streams(), data['data'])

    def test_get_units(self):
        """Test accessing units."""

        self.dc.from_dictionary(create_dummy_data())
        self.assertEqual(self.dc.get_units('time'), 's')
        self.assertEqual(self.dc.get_units('x'), 'm')
        self.assertEqual(self.dc.get_units('y'), 'm')
        self.assertEqual(self.dc.get_units('z'), 'm')
        self.assertEqual(self.dc.get_units(['time', 'x']),
                         ['s', 'm'])
        self.assertEqual(self.dc.get_units(['y', 'z']),
                         ['m', 'm'])

    def test_get_one_unit(self):
        """Test accessing one unit."""

        self.dc.from_dictionary(create_dummy_data())
        self.assertEqual(self.dc._get_one_unit('time'), 's')
        self.assertEqual(self.dc._get_one_unit('x'), 'm')
        self.assertEqual(self.dc._get_one_unit('y'), 'm')
        self.assertEqual(self.dc._get_one_unit('z'), 'm')

    def test_get_all_units(self):
        """Test accessing all units."""

        self.dc.from_dictionary(create_dummy_data())
        self.assertEqual(self.dc.get_all_units(), ['s', 'm', 'm', 'm'])

    def test_add_variable(self):
        """Test adding a variable."""

        # the initialization call the update function internally
        self.dc.add_variable(np.matrix([[1.0]]), "time", "s")
        self.assertEqual(len(self.dc.data), 1)
        self.assertEqual(len(self.dc.fields), 1)
        self.assertEqual(len(self.dc.units), 1)
        self.assertEqual(self.dc.data[0], [1.0])
        self.assertEqual(self.dc.fields["time"], 0)
        self.assertEqual(self.dc.units["time"], "s")
        #
        self.dc.add_variable(np.matrix([[2.0]]), "time", "s")
        self.assertEqual(len(self.dc.data), 1)
        self.assertEqual(len(self.dc.fields), 1)
        self.assertEqual(len(self.dc.units), 1)
        self.assertEqual(self.dc.data[0], [1.0, 2.0])
        self.assertEqual(self.dc.fields["time"], 0)
        self.assertEqual(self.dc.units["time"], "s")
        #
        self.dc.add_variable(np.matrix([[6]]), "my_field_name",
                             "my_unit_name")
        self.assertEqual(len(self.dc.data), 2)
        self.assertEqual(len(self.dc.fields), 2)
        self.assertEqual(len(self.dc.units), 2)
        self.assertEqual(self.dc.data[1], [6])
        self.assertEqual(self.dc.fields["my_field_name"], 1)
        self.assertEqual(self.dc.units["my_field_name"], "my_unit_name")

    def test_add_vector(self):
        """Test adding a vector."""

        # the initialization call the update function internally
        fields = ["a", "b", "c", "d"]
        units = ["s", "m", "rad", "hz"]
        data = np.matrix([[1.0, 2.0, 3.0, 4.0]])

        self.dc.add_vector(data, fields, units)
        self.dc.add_vector(data, fields, units)
        self.dc.add_vector(data, fields, units)
        self.dc.add_vector(data, fields, units)
        self.assertEqual(len(self.dc.data), 4)
        self.assertEqual(len(self.dc.fields), 4)
        self.assertEqual(len(self.dc.units), 4)

        np.testing.assert_array_almost_equal(
            self.dc.data, np.hstack((data.T, data.T, data.T, data.T)).tolist())
        self.assertEqual(self.dc.fields,
                         {"a": 0, "b": 1, "c": 2, "d": 3})
        self.assertEqual(self.dc.units,
                         {"a": "s", "b": "m", "c": "rad", "d": "hz"})

    def test_add_vector_3d(self):
        """Test adding a 3D vector [x, y, z]."""

        self.dc.add_vector_3d(np.matrix([[1.0, 2.0, 3.0]]).T, "a", "m")
        self.dc.add_vector_3d(np.matrix([[4.0, 5.0, 6.0]]).T, "b", "rad")
        self.dc.add_vector_3d(np.matrix([[7.0, 8.0, 9.0]]).T, "c", "J")
        self.dc.add_vector_3d(np.matrix([[10.0, 11.0, 12.0]]).T, "d", "hz")
        self.assertEqual(len(self.dc.data), 4 * 3)
        self.assertEqual(len(self.dc.fields), 4 * 3)
        self.assertEqual(len(self.dc.units), 4 * 3)

        np.testing.assert_array_almost_equal(self.dc.data,
                                             np.matrix(np.arange(1.0, 13.0, 1.0)).T)
        self.assertEqual(self.dc.fields["a_x"], 0)
        self.assertEqual(self.dc.fields["a_y"], 1)
        self.assertEqual(self.dc.fields["a_z"], 2)
        self.assertEqual(self.dc.fields["b_x"], 3)
        self.assertEqual(self.dc.fields["b_y"], 4)
        self.assertEqual(self.dc.fields["b_z"], 5)
        self.assertEqual(self.dc.fields["c_x"], 6)
        self.assertEqual(self.dc.fields["c_y"], 7)
        self.assertEqual(self.dc.fields["c_z"], 8)
        self.assertEqual(self.dc.fields["d_x"], 9)
        self.assertEqual(self.dc.fields["d_y"], 10)
        self.assertEqual(self.dc.fields["d_z"], 11)
        self.assertEqual(self.dc.units["a_x"], "m")
        self.assertEqual(self.dc.units["a_y"], "m")
        self.assertEqual(self.dc.units["a_z"], "m")
        self.assertEqual(self.dc.units["b_x"], "rad")
        self.assertEqual(self.dc.units["b_y"], "rad")
        self.assertEqual(self.dc.units["b_z"], "rad")
        self.assertEqual(self.dc.units["c_x"], "J")
        self.assertEqual(self.dc.units["c_y"], "J")
        self.assertEqual(self.dc.units["c_z"], "J")
        self.assertEqual(self.dc.units["d_x"], "hz")
        self.assertEqual(self.dc.units["d_y"], "hz")
        self.assertEqual(self.dc.units["d_z"], "hz")

    def random_quat(self):
        """
        Create a random quaternion.
        :return: a quaternion or a simple 4D vector
        """

        if USE_PINOCCHIO:
            vec = rand(4)
            return se3.Quaternion(
                float(vec[3]), float(vec[0]), float(vec[1]), float(vec[2]))
        else:
            return rand(4)

    def test_add_quaternion(self):
        """Test adding a quaternion [qx, qy, qz, qw]."""

        q0 = self.random_quat()
        q1 = self.random_quat()
        q2 = self.random_quat()

        self.dc.add_quaternion(q0, "a")
        self.dc.add_quaternion(q1, "b")
        self.dc.add_quaternion(q2, "c")
        self.assertEqual(len(self.dc.data), 3 * 4)
        self.assertEqual(len(self.dc.fields), 3 * 4)
        self.assertEqual(len(self.dc.units), 3 * 4)

        if USE_PINOCCHIO:
            np.testing.assert_array_almost_equal(self.dc.data,
                                                 np.vstack((q0.coeffs(), q1.coeffs(), q2.coeffs())).tolist())
        else:
            np.testing.assert_array_almost_equal(
                self.dc.data, np.vstack((q0, q1, q2)).tolist())
        self.assertEqual(self.dc.fields["a_qx"], 0)
        self.assertEqual(self.dc.fields["a_qy"], 1)
        self.assertEqual(self.dc.fields["a_qz"], 2)
        self.assertEqual(self.dc.fields["a_qw"], 3)
        self.assertEqual(self.dc.fields["b_qx"], 4)
        self.assertEqual(self.dc.fields["b_qy"], 5)
        self.assertEqual(self.dc.fields["b_qz"], 6)
        self.assertEqual(self.dc.fields["b_qw"], 7)
        self.assertEqual(self.dc.fields["c_qx"], 8)
        self.assertEqual(self.dc.fields["c_qy"], 9)
        self.assertEqual(self.dc.fields["c_qz"], 10)
        self.assertEqual(self.dc.fields["c_qw"], 11)
        self.assertEqual(self.dc.units["a_qx"], "-")
        self.assertEqual(self.dc.units["a_qy"], "-")
        self.assertEqual(self.dc.units["a_qz"], "-")
        self.assertEqual(self.dc.units["a_qw"], "-")
        self.assertEqual(self.dc.units["b_qx"], "-")
        self.assertEqual(self.dc.units["b_qy"], "-")
        self.assertEqual(self.dc.units["b_qz"], "-")
        self.assertEqual(self.dc.units["b_qw"], "-")
        self.assertEqual(self.dc.units["c_qx"], "-")
        self.assertEqual(self.dc.units["c_qy"], "-")
        self.assertEqual(self.dc.units["c_qz"], "-")
        self.assertEqual(self.dc.units["c_qw"], "-")

    def test_add_rpy(self):
        """Test adding a Roll Pitch Yaw rotation [r, p, y]."""

        if USE_PINOCCHIO:
            q = self.random_quat()
            self.dc.add_rpy(q, "q")
            self.dc.add_rpy(q.coeffs(), "qcoeffs")
            self.dc.add_rpy(np.identity(3), "mat")
        self.dc.add_rpy(rand(3), "vec")
        self.dc.add_rpy([0.0, 1.0, 2.0], "list")

    def test_add_se3(self):
        """Test adding a SE3 object [x, y, z, qx, qy, qz, qw]."""

        if USE_PINOCCHIO:
            se3_i = se3.SE3.Identity()
            self.dc.add_se3(se3_i, "identity")
            self.assertEqual(len(self.dc.data), 4 + 3)
            self.assertEqual(len(self.dc.fields), 4 + 3)
            self.assertEqual(len(self.dc.units), 4 + 3)
            np.testing.assert_array_almost_equal(self.dc.data,
                                                 [[0.0], [0.0], [0.0], [0.0], [0.0], [0.0], [1.0]])

    def test_add_matrix(self):
        """Test adding a matrix [ij]."""

        mat = eye(3)
        self.dc.add_matrix(mat, "I3", "-")
        self.assertEqual(len(self.dc.data), 9)
        self.assertEqual(len(self.dc.fields), 9)
        self.assertEqual(len(self.dc.units), 9)
        np.testing.assert_array_almost_equal(self.dc.data,
                                             [[1.0], [0.0], [0.0], [0.0], [1.0], [0.0], [0.0], [0.0], [1.0]])
        self.assertEqual(self.dc.fields["I3_0_0"], 0)
        self.assertEqual(self.dc.fields["I3_0_1"], 1)
        self.assertEqual(self.dc.fields["I3_0_2"], 2)
        self.assertEqual(self.dc.fields["I3_1_0"], 3)
        self.assertEqual(self.dc.fields["I3_1_1"], 4)
        self.assertEqual(self.dc.fields["I3_1_2"], 5)
        self.assertEqual(self.dc.fields["I3_2_0"], 6)
        self.assertEqual(self.dc.fields["I3_2_1"], 7)
        self.assertEqual(self.dc.fields["I3_2_2"], 8)

    def test_from_dictionary(self):
        """Test parsing of a dictionary."""

        self.dc.from_dictionary(create_dummy_data())
        self.assertEqual(len(self.dc.data), 4)
        self.assertEqual(len(self.dc.fields), 4)
        self.assertEqual(len(self.dc.units), 4)
        np.testing.assert_array_almost_equal(
            self.dc.data,
            np.vstack(
                (range(0, 11), range(10, 21), range(20, 31), range(30, 41))
            ).tolist()
        )
        self.assertEqual(self.dc.fields["time"], 0)
        self.assertEqual(self.dc.fields["x"], 1)
        self.assertEqual(self.dc.fields["y"], 2)
        self.assertEqual(self.dc.fields["z"], 3)
        self.assertEqual(self.dc.metadata["robot"], "athena")

    def test_to_dictionary(self):
        """Test the conversion to a dictionary."""

        self.dc.from_dictionary(create_dummy_data())
        self.assertEqual(self.dc.to_dictionary(), create_dummy_data())

    def test_dump_and_reload(self):
        """Test dumping a bunch of data and read them back with pkl and npz format."""

        # collect a bush of data
        self.dc.metadata["robot"] = "athena"
        mat = eye(3)
        self.dc.add_matrix(mat, "I3", "-")
        self.dc.add_matrix(mat, "I3", "-")
        self.dc.add_matrix(mat, "I3", "-")
        self.dc.add_matrix(mat, "I3", "-")
        self.dc.add_matrix(mat, "I3", "-")
        self.dc.add_matrix(mat, "I3", "-")
        self.dc.add_matrix(mat, "I3", "-")
        self.dc.add_matrix(mat, "I3", "-")

        # dump the data
        with tempfile.NamedTemporaryFile("w+b", suffix=".pkl") as pklfile:
            self.dc.dump(pklfile.name)

            # read back
            self.dc.load(pklfile.name)
            self.assertEqual(len(self.dc.data), 9)
            self.assertEqual(len(self.dc.fields), 9)
            self.assertEqual(len(self.dc.units), 9)
            eye_vec = 8 * [[1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]]
            np.testing.assert_array_almost_equal(self.dc.data,
                                                 np.matrix(eye_vec).T.tolist())
            self.assertEqual(self.dc.fields["I3_0_0"], 0)
            self.assertEqual(self.dc.fields["I3_0_1"], 1)
            self.assertEqual(self.dc.fields["I3_0_2"], 2)
            self.assertEqual(self.dc.fields["I3_1_0"], 3)
            self.assertEqual(self.dc.fields["I3_1_1"], 4)
            self.assertEqual(self.dc.fields["I3_1_2"], 5)
            self.assertEqual(self.dc.fields["I3_2_0"], 6)
            self.assertEqual(self.dc.fields["I3_2_1"], 7)
            self.assertEqual(self.dc.fields["I3_2_2"], 8)
            self.assertEqual(self.dc.metadata["robot"], "athena")

            # test the npz format
            data0 = DataCollector()
            data1 = DataCollector()
            data0.from_dictionary(create_dummy_data())
            data1.from_dictionary(create_dummy_data())

        # dump the file
        with tempfile.NamedTemporaryFile("w+b", suffix=".npz") as npzfile:
            DataCollector.dump_npz(npzfile.name, [data0, data1], ['data0', 'data1'])

            data_tmp = DataCollector()
            data_tmp.load(npzfile.name)

    def test_dump(self):
        """Test dumping simple data in the pkl and npz formats."""

        # pkl format
        # load some simple data
        data = DataCollector()
        data.from_dictionary(create_dummy_data())

        # dump the data
        with tempfile.NamedTemporaryFile("w+b", suffix=".pkl") as pklfile:
            data.dump(pklfile.name)

            # load back the data
            with open(pklfile.name, "rb") as datafile:
                dumped = pickle.load(datafile)
                self.assertEqual(dumped, create_dummy_data())

        # npz format from single data object
        # dump the data
        with tempfile.NamedTemporaryFile("w+b", suffix=".npz") as npzsinglefile:
            data.dump_compressed(npzsinglefile.name)

            # load back the data
            with open(npzsinglefile.name, "rb") as datafile:
                files = np.load(datafile, allow_pickle=True)
                for filedata in files:
                    data_loaded = files[filedata].all()
                    self.assertEqual(data_loaded, create_dummy_data())

        # npz format from multiple data object
        # load a couple of data
        data0 = DataCollector()
        data1 = DataCollector()
        data0.from_dictionary(create_dummy_data())
        data1.from_dictionary(create_dummy_data())
        # dump the data

        with tempfile.NamedTemporaryFile("w+b", suffix=".npz") as npzfile:
            DataCollector.dump_npz(npzfile.name, [data0, data1], ['data0', 'data1'])

            with open(npzfile.name, "rb") as datafile:
                files = np.load(datafile, allow_pickle=True)
                for filedata in files:
                    data_loaded = files[filedata].all()
                    self.assertEqual(data_loaded, create_dummy_data())

    def test_loading_data(self):
        """Test loading npy, pkl, npz, and d-file files."""

        dfile_name = pkg_resources.resource_filename('RAI', 'resources/d00300')

        # create the temporary files
        with tempfile.NamedTemporaryFile("w+b", suffix=".npy") as npy, \
                tempfile.NamedTemporaryFile("w+b", suffix=".npz") as npz, \
                tempfile.NamedTemporaryFile("w+b", suffix=".npz") as npz, \
                tempfile.NamedTemporaryFile("w+b", suffix=".pkl") as pkl, \
                tempfile.NamedTemporaryFile(suffix='.ext') as dfile_tmp:

            # create a copy of the d-file with a dummy extension
            with open(dfile_name, 'rb') as f1:
                with open(dfile_tmp.name, 'wb') as f2:
                    f2.write(f1.read())

            # dump data on the files
            data_test = create_dummy_data()
            np.save(npy.name, create_dummy_data())
            np.savez(npz.name, data0=create_dummy_data(), data1=create_dummy_data())
            pickle.dump(create_dummy_data(), pkl)

            # execute all the opening procedure
            # npy
            data_tmp = DataCollector()
            data_tmp.load(npy.name)
            self.assertEqual(data_tmp.to_dictionary(), create_dummy_data())

            # npz
            data_tmp = DataCollector()
            data_tmp.load(npz.name)
            self.assertEqual(data_tmp.get_streams("time"),
                             data_test["data"][0])
            self.assertEqual(data_tmp.get_streams("data0/time"),
                             data_test["data"][0])
            self.assertEqual(data_tmp.get_streams("data0/x"),
                             data_test["data"][1])
            self.assertEqual(data_tmp.get_streams("data0/y"),
                             data_test["data"][2])
            self.assertEqual(data_tmp.get_streams("data0/z"),
                             data_test["data"][3])
            self.assertEqual(data_tmp.get_streams("data1/time"),
                             data_test["data"][0])
            self.assertEqual(data_tmp.get_streams("data1/x"),
                             data_test["data"][1])
            self.assertEqual(data_tmp.get_streams("data1/y"),
                             data_test["data"][2])
            self.assertEqual(data_tmp.get_streams("data1/z"),
                             data_test["data"][3])

            # pkl
            data_tmp = DataCollector()
            pkl.seek(0)
            data_tmp.load(pkl.name)
            self.assertEqual(data_tmp.to_dictionary(), create_dummy_data())

            # d-file
            data_tmp = DataCollector()
            data_tmp.load(dfile_name)
            np.testing.assert_array_almost_equal(data_tmp.get_streams('time'),
                                                 np.arange(0.0, 4.889, 0.002))

            # d-file with dummy extension
            data_tmp = DataCollector()
            data_tmp.load(dfile_tmp.name)
            np.testing.assert_array_almost_equal(data_tmp.get_streams('time'),
                                                 np.arange(0.0, 4.889, 0.002))

    def test_dg_parser(self):
        """Test loading a folder."""

        with tempfile.TemporaryDirectory() as empty_dir:
            dg_folder_path = Path(empty_dir).absolute()

            data_0 = np.concatenate(
                (np.arange(0, 5, 1).reshape([5, 1]), np.random.rand(5, 3)), axis=1)
            data_1 = np.concatenate(
                (np.arange(0, 4, 1).reshape([4, 1]), np.random.rand(4, 4)), axis=1)

            np.savetxt(Path(dg_folder_path) / "data_0.dat", data_0)
            np.savetxt(Path(dg_folder_path) / "data_1.dat", data_1)

            data_tmp = DataCollector()
            data_tmp.load(dg_folder_path)

            # test
            np.testing.assert_almost_equal(
                np.array(data_tmp.get_streams("data_0/1")), data_0[:4, 1])
            np.testing.assert_almost_equal(
                np.array(data_tmp.get_streams("data_0/2")), data_0[:4, 2])
            np.testing.assert_almost_equal(
                np.array(data_tmp.get_streams("data_0/3")), data_0[:4, 3])

            np.testing.assert_almost_equal(np.array(data_tmp.get_streams("data_1/1")), data_1[:, 1])
            np.testing.assert_almost_equal(np.array(data_tmp.get_streams("data_1/2")), data_1[:, 2])
            np.testing.assert_almost_equal(np.array(data_tmp.get_streams("data_1/3")), data_1[:, 3])
            np.testing.assert_almost_equal(np.array(data_tmp.get_streams("data_1/4")), data_1[:, 4])
