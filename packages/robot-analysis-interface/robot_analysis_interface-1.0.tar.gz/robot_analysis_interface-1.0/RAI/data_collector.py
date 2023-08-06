'''
Data Collector
==============

This module provides a :py:class:`DataCollector` class containing information
from the sensors. It provides an API to collect data stream and to access the
stored data.

:author1: Maximilien Naveau <maximilien.naveau@tuebingen.mpg.de>
:author2: Jean-Claude Passy <jean-claude.passy@tuebingen.mpg.de>
'''

import struct
import os.path
from copy import deepcopy
import numpy as np
import pickle
from sys import maxsize

try:
    import pinocchio as se3
    from pinocchio.rpy import matrixToRpy

    USE_PINOCCHIO = True
except ImportError:
    USE_PINOCCHIO = False


class DataCollector(object):
    """
    This class manages data.
    It can read and dump data from a file.
    It stores data on the fly.
    """

    def __init__(self):

        # a list of list representing the data
        self.data = []
        # the list of the fields names
        self.fields = {}
        # the units of each field
        self.units = {}
        # a bunch of data that one may save (date, controller name, ...)
        self.metadata = {}
        # some metadata from the d-file loading
        self.arg_max = 0
        self.reduce_x_axis = True

    def get_streams(self, fields):
        """ Return a list containing the data from the elements in `fields`.

        :param fields: Desired stream fields.
        :type fields: str or list(str)
        :returns: Data from the elements in `fields`
        :rtype: list(list(``float``))
        """

        if isinstance(fields, str):
            return self._get_one_stream(fields)
        else:
            return [self._get_one_stream(field) for field in fields]

    def _get_one_stream(self, field):
        """ Return the list containing the information corresponding to
        the string `field`.

        :param field: Desired stream field.
        :type field: str
        """

        if not isinstance(field, str):
            raise TypeError(
                "field should be a string, " +
                "instead got {} of type {}.".format(field, type(field)))

        if field in self.fields:
            return self.data[self.fields[field]]

        raise KeyError(field + ' is not a valid sensor input.')

    def get_all_streams(self):
        """ Return a list of list array containing the data from the all
        elements in the sensors file.

        :return: the list of all the fields
        """

        return self.data

    def get_units(self, fields):
        """ Return a list of numpy array containing the units all elements in
        `fields`.

        :param fields: Profiles for which the units are required.
        :type fields: str or list(str)
        :return: Units from the elements in `fields`
        :rtype: list(``numpy.array``)
        """

        if isinstance(fields, str):
            return self._get_one_unit(fields)
        else:
            return [self._get_one_unit(field) for field in fields]

    def _get_one_unit(self, field):
        """ Return the units of `field`.

        :param field: Profile for which the units are required.
        :type field: str
        :return: one unit
        """

        if not isinstance(field, str):
            raise TypeError(
                "data should be a string, " +
                "instead got {} of type {}.".format(field, type(field)))

        if field in self.fields:
            return self.units[field]

        raise KeyError(field + ' is not a valid sensor input.')

    def get_all_units(self):
        """ Return a list of numpy array containing the units all elements in
        the sensors file.

        :return: the list of units stored
        """

        return self.get_units(sorted(self.fields.keys()))

    def add_variable(self, data, field, unit):
        """
        Append a single float or int to a stream of data.

        :param data: the float or int to add
        :param field: the name of the stream
        :param unit: the unit associated to the data
        """

        if not isinstance(data, (float, int, bool, np.ndarray)):
            raise TypeError(
                "data should be a float, an int, or a bool, " +
                ", instead got {} of type {}.".format(data, type(data)))

        if not isinstance(field, str):
            raise TypeError(
                "field should be a string, instead got {} of type {}."
                .format(field, type(field)))

        if not isinstance(unit, str):
            raise TypeError(
                "unit should be a string, instead got {} of type {}."
                .format(unit, type(unit)))

        if isinstance(data, (bool, int, np.ndarray)):
            data = float(data)

        if field not in self.fields:
            self.data.append([])
            self.fields[field] = len(self.data) - 1
            self.units[field] = unit

        self.data[self.fields[field]].append(float(data))

        assert len(self.data) == len(self.fields) == len(self.units)

    def add_vector(self, data_vec, field_vec, unit_vec):
        """
        Append each element of the vector to a different stream of data.

        :param data_vec: the vector to add
        :param field_vec: the names of the streams to add the data
        :param unit_vec: the units of all the vector elements
        """
        if not (self._vector_size(data_vec) == len(field_vec) == len(unit_vec)):
            raise ValueError("All input lists must have the same size. " +
                             "Instead got sized {}, {}, and {}".format(
                                 self._vector_size(data_vec),
                                 len(field_vec), len(unit_vec)))

        if isinstance(data_vec, np.ndarray):
            data_col_vec = data_vec.reshape(data_vec.size, 1)
        else:
            data_col_vec = data_vec

        for i in range(len(field_vec)):
            if not isinstance(field_vec[i], str):
                raise TypeError(
                    "fields should be a string, instead got {} of type {}."
                    .format(field_vec[i], type(field_vec[i])))

            if not isinstance(unit_vec[i], str):
                raise TypeError(
                    "units should be a string, instead got {} of type {}."
                    .format(unit_vec[i], type(unit_vec[i])))

            self.add_variable(data_col_vec[i], field_vec[i], unit_vec[i])

    def add_vector_3d(self, data_vec, field, unit):
        """
        Append a 3d vector to 3 streams of data with the names append by [x,y,z]

        :param data_vec: the 3d vector
        :param field: the basename.
        :param unit: the unit of all 3 streams
        """

        if not self._vector_size(data_vec) == 3:
            raise ValueError("data_vec should be a 3D vector, instead got {}"
                             .format(data_vec))

        if not isinstance(field, str):
            raise TypeError(
                "field should be a string, instead got {} of type {}."
                .format(field, type(field)))

        if not isinstance(unit, str):
            raise TypeError(
                "unit should be a string, instead got {} of type {}."
                .format(unit, type(unit)))

        field_vec = [field + "_x", field + "_y", field + "_z"]
        unit_vec = 3 * [unit]
        self.add_vector(data_vec, field_vec, unit_vec)

    def add_quaternion(self, quaternion, field):
        """
        Append a quaternion to 4 streams of data with the names [qw, qx, qy, qz]

        :param quaternion: the quaternion to add
        :param field: the name of the basename for teh quaternion
        """

        field_vec = [field + "_qx", field + "_qy", field + "_qz", field + "_qw"]
        unit_vec = ["-", "-", "-", "-"]
        if USE_PINOCCHIO:
            if isinstance(quaternion, (np.ndarray, list, se3.Quaternion)):
                self.add_vector(quaternion, field_vec, unit_vec)
            else:
                raise TypeError("wrong type, expected a Quaternion," +
                                " a list or a ndarray. Instead got type {}"
                                .format(quaternion))
        else:
            if isinstance(quaternion, (np.ndarray, list)):
                self.add_vector(quaternion, field_vec, unit_vec)
            else:
                raise TypeError("wrong type, expected a list or a ndarray" +
                                ". Instead got type {}".format(quaternion))

    def add_rpy(self, rot, field):
        """
        Append a roll, pitch, yaw vector based on quaternion, rotation matrix or
        quaternion

        :param rot: the rotation to be converted to rpy
        :param field: the basename of the rotation
        """

        if isinstance(rot, (np.ndarray, list)) and self._vector_size(rot) == 3:
            self.add_vector(
                rot, [field + "_roll", field + "_pitch", field + "_yaw"],
                ["rad", "rad", "rad"])
        elif USE_PINOCCHIO:
            if isinstance(rot, se3.Quaternion):
                self.add_rpy(rot.matrix(), field)
            elif isinstance(rot, np.ndarray) and self._vector_size(rot) == 4:
                self.add_rpy(se3.Quaternion(float(rot[3]), float(rot[0]),
                                            float(rot[1]), float(rot[2])), field)
            elif isinstance(rot, np.ndarray) and rot.shape == (3, 3):
                self.add_rpy(matrixToRpy(rot), field)
            else:
                if isinstance(rot, np.ndarray):
                    shape = rot.shape
                else:
                    shape = None
                raise TypeError(
                    'Cannot convert vector of shape \'' + str(shape) + '\' ' +
                    'to rpy. Type has to be either\n' +
                    '    - se3.Quaternion\n' +
                    '    - numpy.ndarray of size (4, 1): [qx, qy, qz, qw]\n' +
                    '    - numpy.ndarray of size (3, 3): a rotation matrix\n' +
                    '    - se3.Quaternion\n' +
                    'Instead got type {}'.format(rot))
        else:
            raise ValueError('The given vector must be a roll pitch yaw ' +
                             'vector')

    def add_se3(self, m, field):
        """
        If Pinocchio is installed, append a SE3 to the streams.

        :param m: an se3.SE3 object
        :param field: the basename of the SE3 to add
        """

        if USE_PINOCCHIO:
            self.add_vector_3d(m.translation, field, "m")
            self.add_quaternion(se3.Quaternion(m.rotation), field)
        else:
            raise ImportError('Without the Pinocchio library this method ' +
                              'is not implemented')

    def add_matrix(self, mat, field, unit):
        """
        Append a matrix to the streams.

        :param mat: the matrix
        :param field: the basename of the matrix
        :param unit: the unit of the matrix elements
        """

        if not isinstance(field, str):
            raise TypeError(
                "field should be a string, instead got {} of type {}."
                .format(field, type(field)))

        if not isinstance(unit, str):
            raise TypeError(
                "unit should be a string, instead got {} of type {}."
                .format(unit, type(unit)))

        if not isinstance(mat, np.matrix):
            raise TypeError(
                "field should be a string, instead got {} of type {}."
                .format(mat, type(mat)))

        for i in range(mat.shape[0]):
            for j in range(mat.shape[1]):
                self.add_variable(mat[i, j], field + "_" +
                                  str(i) + "_" + str(j), unit)

    def to_dictionary(self):
        """
        Return a dictionary containing the the data
        it is used to dump the data

        :return: a dict
        """

        return {
            'fields': self.fields,
            'units': self.units,
            'data': self.data,
            'metadata': self.metadata
        }

    def from_dictionary(self, dictionary):
        """
        Parse the loaded dictionary from a data file

        :param dictionary: the dictionary to parse
        """

        self._check_data_dictionary(dictionary)
        self.metadata = deepcopy(dictionary['metadata'])
        self.fields = deepcopy(dictionary['fields'])
        self.units = deepcopy(dictionary['units'])
        self.data = deepcopy(dictionary['data'])

    def dump(self, filename):
        """
        Dump the data in as a dictionary in the filename using pickle

        :param str filename: the path to the file
        """

        if not len(self.data):
            raise ValueError("No data to dump, the file would be empty")

        # check the size of each column, they have to be equal.
        try:
            for i in range(1, len(self.data)):
                assert len(self.data[i - 1]) == len(self.data[i])
        except AssertionError:
            raise ValueError("Data ill formed, " +
                             "all stream must have the same length")

        _, ext = os.path.splitext(filename)
        if not ext == ".pkl":
            filename = filename + ".pkl"

        with open(filename, "wb") as f:
            pickle.dump(self.to_dictionary(), f)

    def dump_compressed(self, filename):
        """
        Dump the data in as a compressed format using numpy.savez_compressed

        :param filename: the filename to dump the data
        """

        DataCollector.dump_npz(filename, [self], ['data'])

    @staticmethod
    def dump_npz(filename, list_data_collector, list_zip_names=None):
        """
        Dump a list of DataCollector in a zip folder with numpy.savez_compressed

        :param filename: the name of the file to dump the data
        :param list_data_collector: the list of the DataCollector objects
        :param list_zip_names: the list of names in the zipped folder
        """

        if not isinstance(filename, str):
            raise TypeError("filename should be of type string or basestring" +
                            ". Instead got {} of type {}"
                            .format(filename, type(filename)))

        if not all(isinstance(data_collector, DataCollector)
                   for data_collector in list_data_collector):
            raise TypeError("list_data_collector must be a list of " +
                            "DataCollector. Instead got types {}"
                            .format([type(data) for data in list_data_collector]
                                    ))
        if list_zip_names is not None:
            assert all(isinstance(zip_name, str) for zip_name in list_zip_names)
            assert len(list_zip_names) == len(list_data_collector)
        else:
            list_zip_names = []
            max_nb_file = str(len(str(len(list_data_collector))))
            for i, data_collector in enumerate(list_data_collector):
                list_zip_names.append(
                    str("data{:" + max_nb_file + "d}").format(i))

        path, ext = os.path.splitext(filename)
        if not ext == ".npz":
            filename = filename + ".npz"

        data_to_dump = {}
        for data_collector, zip_name in zip(list_data_collector, list_zip_names):
            data_to_dump[zip_name] = data_collector.to_dictionary()

        np.savez_compressed(filename, **data_to_dump)

    def load(self, filename, reduce_dfile_x_axis=True):
        """
        Load the file from filename

        :param filename: the root path to the file
        """
        load_functions = {
            '.pkl': lambda data_file:
                self.from_dictionary(pickle.load(data_file)),
            '.npy': lambda data_file:
                self.from_dictionary(self._parse_npy(data_file)),
            '.npz': lambda data_file:
                self.from_dictionary(self._parse_npz_file(data_file)),
            '': lambda data_file:  # default is d-file
                self.from_dictionary(self._parse_d_file(data_file,
                                                        reduce_dfile_x_axis))
        }
        if os.path.isfile(filename):
            _, fileext = os.path.splitext(filename)
            if fileext not in ['.pkl', '.npy', '.npz']:
                fileext = ''
            error_message = ('Cannot load file ' + filename + ' as SensorsData\n' +
                             'The parser manages files from SL and with the ' +
                             'extension .pkl, .npy, .npz')
            try:
                with open(filename, 'rb') as data_file:
                    load_functions[fileext](data_file)
            except ValueError as e:
                error_message = ("ValueError: an error has been detected while " +
                                 "loading the data file, \'" + e.message + "\'\n" +
                                 error_message)
                raise RuntimeError(error_message)

        elif os.path.isdir(filename):
            self.from_dictionary(self._parse_dg_folder(filename))
        else:
            raise ValueError('The path is not a file or directory.')

        self.sanity_check()

    @staticmethod
    def _parse_dg_folder(data_folder):
        """
        parse from dynamic graph folder

        :param data_folder: the root path to the last folder in dynamic graph folder
        :type data_folder: str
        """
        data = {'metadata': {}, 'fields': {}, 'units': {}, 'data': []}

        # get the time limits
        file_data = {}
        stop_time = maxsize
        for file in os.listdir(data_folder):
            name, _ = os.path.splitext(file)
            file_data[name] = np.loadtxt(os.path.join(data_folder, file))
            stop_time = min(stop_time, len(file_data[name]))

        # fill data
        index = 0
        for file in os.listdir(data_folder):
            name, _ = os.path.splitext(file)
            if len(file_data[name][:]) == 0:
                continue

            for i in range(1, len(file_data[name][0])):
                data['fields'][name + '/' + str(i)] = index
                index += 1
                data['units'][name + '/' + str(i)] = '_'
                data['data'].append(file_data[name][:stop_time, i])

        data['fields']["time"] = index
        data['units']["time"] = ["millisec"]
        data['data'].append(np.arange(0.0, stop_time, 1.0).tolist())
        index += 1
        return data

    @staticmethod
    def _parse_d_file(data_file, reduce_x_axis=True):
        """
        Parse a SL d-file

        :param filename: the root path to the file
        :type filename: str
        """

        # Header
        data = {'metadata': {}, 'fields': {}, 'units': {}, 'data': []}
        temp = data_file.readline().split()

        cols = int(temp[1])
        rows = int(temp[2])
        data['metadata']['frequency'] = float(temp[3])

        # Fields and units
        temp = data_file.readline().decode().split()

        for i in range(cols):
            data['fields'][temp[2 * i]] = i
            data['units'][temp[2 * i]] = temp[2 * i + 1]

        # full data
        full_data = np.array(struct.unpack(
            '>' + 'f' * cols * rows, data_file.read(4 * cols * rows))
        ).reshape(rows, cols).transpose()

        # There might be a bunch of 0's at the end of the array `time`.
        # So we crop the data here by default
        time = full_data[data['fields']['time']]
        data['metadata']['arg_max'] = time.argmax()
        data['metadata']['reduce_x_axis'] = reduce_x_axis
        if reduce_x_axis:
            for i in range(len(data['fields'])):
                data['data'].append(full_data[i, :data['metadata']['arg_max'] + 1].tolist())
        else:
            for i in range(len(data['fields'])):
                data['data'].append(full_data[i].tolist())
        return data

    @staticmethod
    def _parse_npy(data_file):
        try:
            data = np.load(data_file, allow_pickle=False).all()
        except ValueError:
            data = np.load(data_file, allow_pickle=True).all()
        return data

    @staticmethod
    def _parse_npz_file(data_file):
        """
        Parse the zip folder loaded via numpy.load from a npz file

        :param data_file: object return by "open(filename)"
        """

        def _parse_data_dictionary(file_dictionary):
            # deal with all the data from the different files
            idn = 0
            for filezip in file_dictionary:
                data_dictionary = file_dictionary[filezip].all()
                # first deal with the frequency
                data['metadata'][filezip] = {}
                # copy the metadata separately for each file
                data['metadata'][filezip] = deepcopy(data_dictionary['metadata'])
                # accumulate the data changing the field of the fields
                for i, field in enumerate(data_dictionary['fields']):
                    data['fields'][str(filezip + "/" + field)] = idn + i
                    data['units'][str(filezip + "/" + field)] = (
                        data_dictionary['units'][field])
                    data['data'] += [data_dictionary["data"][
                        data_dictionary["fields"][field]]]
                idn += len(data_dictionary['fields'])
            # get the time field
            assert "time" not in data['fields']
            data['fields']["time"] = idn
            data['units']["time"] = ["s"]
            time_field_name = file_dictionary.files[0] + "/time"
            data['data'] += [data['data'][data['fields'][time_field_name]]]
            return data

        data = {'metadata': {}, 'fields': {}, 'units': {}, 'data': []}
        try:
            with np.load(data_file, allow_pickle=False) as file_dictionary:
                data = _parse_data_dictionary(file_dictionary)
        except ValueError:
            with np.load(data_file, allow_pickle=True) as file_dictionary:
                data = _parse_data_dictionary(file_dictionary)

        return data

    def _check_data_dictionary(self, dictionary):
        """
        Check if the dictionary from the loaded file has the correct fields

        :param dictionary: the dictionary to test
        """
        if 'fields' not in dictionary:
            raise ValueError('fields has to be in the read dictionary')
        if 'units' not in dictionary:
            raise ValueError('units has to be in the read dictionary')
        if 'data' not in dictionary:
            raise ValueError('data has to be in the read dictionary')
        if 'metadata' not in dictionary:
            raise ValueError('metadata has to be in the file read')

    def _vector_size(self, vec):
        """
        simple utility that return either the size of a numpy.ndarray
        or the length of a list accordingly

        :param vec: input vector, could be a list or a vector
        """

        if USE_PINOCCHIO:
            assert isinstance(vec, (list, dict, np.ndarray, se3.Quaternion))
        else:
            assert isinstance(vec, (list, dict, np.ndarray))

        if isinstance(vec, np.ndarray):
            return vec.size
        else:
            return len(vec)

    def sanity_check(self):
        """
        Do a couple of assertion on the object to verify its sanity
        """
        assert isinstance(self.fields, dict)
        for stream in self.data:
            for value in stream:
                assert isinstance(value, float)

        n = len(self.fields)
        all_ids = self.fields.values()

        assert len(all_ids) == n
        assert set(all_ids) == set(range(n))
