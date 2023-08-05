from __future__ import absolute_import

import warnings
import datetime as dt

import six
import jsonpickle.pickler
import jsonpickle.unpickler
import bson.binary
import pymongo.son_manipulator

# override the default pickler/unpickler to better handle some types


class Pickler(jsonpickle.pickler.Pickler):
    def _flatten(self, obj):
        if isinstance(obj, dt.datetime) and not obj.utcoffset():
            # naive datetimes or UTC datetimes can be stored directly
            return obj
        if six.PY3 and isinstance(obj, bytes):
            return obj
        return super(Pickler, self)._flatten(obj)


class Unpickler(jsonpickle.unpickler.Unpickler):
    def _restore(self, obj):
        restored = super(Unpickler, self)._restore(obj)
        if isinstance(restored, bson.binary.Binary):
            msg = "Binary objects are deprecated"
            warnings.warn(msg, DeprecationWarning)
            return bytes(restored)
        return restored


class SONManipulator(pymongo.son_manipulator.SONManipulator):
    """
    PyMongo provides a hook for custom types. Invoke SONManipulator.install
    on the target database to enable.
    """

    pickler = Pickler()
    unpickler = Unpickler()

    @classmethod
    def install(cls, db):
        db.add_son_manipulator(cls())

    def transform_incoming(self, son, collection):
        return self.pickler.flatten(son)

    def transform_outgoing(self, son, collection):
        return self.unpickler.restore(son)


def encode(value):
    return Pickler().flatten(value)


def decode(value):
    return Unpickler().restore(value)
