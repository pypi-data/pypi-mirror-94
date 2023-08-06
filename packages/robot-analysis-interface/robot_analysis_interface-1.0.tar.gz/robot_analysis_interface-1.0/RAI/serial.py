'''
Serial
======

This module provides a mother class for recursive (de)serialization.

:author: Jean-Claude Passy <jean-claude.passy@tuebingen.mpg.de>
'''


class Serializable(object):
    """This base class is inherited from by classes which need to be serialized."""

    serial_version = None

    def serialize(self):
        """
        Serialize the object.

        :returns: serialized object
        :rtype: dict
        """

        # Check that the version has been set in the child class.
        assert(self.serial_version is not None)

    @staticmethod
    def deserialize(dictionary, *args, **kwargs):
        """
        Deserialization function.

        :param dict dictionary: dictionary containing the information for deserialization.
        :returns: deserialized object
        :rtype: object
        """

        raise NotImplementedError("Deserialize method not implemented.")
