import logging
import os
import uuid
from datetime import datetime

import pytz
import zlib

def bytes_to_hex_str(b):
    return "".join(['%02x' % i for i in b])


def check_json(pb):
    """docstring for check_json"""
    if "JSON" in str(type(pb)):
        LOGGER.warning("Using a json message rather than defined protobuf")


class MessageHandler():
    def __init__(self, pb, **kwargs):
        self.pb = pb
        self.kwargs = kwargs
        self._add_meta_data()
        self._setattrs()
        self._add_meta_data()
        check_json(self.pb)

    def list_attrs(self):
        for item in self.pb._fields.items():
            print(item)

    def _setattrs(self):
        [ setattr(self.pb, key, self.kwargs[key]) for key in self.kwargs if hasattr(self.pb, key) ]
        # for key in self.kwargs:
        #     if hasattr(self.pb, key):
        #         setattr(self.pb, key, self.kwargs[key])

    def _add_meta_data(self):
        if not hasattr(self.pb, "_message_data"):
            LOGGER.critical("Protobuff does not have _message_data field this is necessary")
            raise MessageHandlerException("Protobuf does not contain _message_data field")
        self.md = self.pb._message_data
        self.md.iso_date = utcnow().isoformat()
        self.md.environment = messageData.Environment.Value(ENVIRONMENT)
        self.md.sending_service = SENDING_SERVICE
        self.md.uuid = str(uuid.uuid1())
        if not self.md.trace_id:
            self.md.trace_id = trace_id()

    def string_repr(self):
        return self.pb.SerializeToString()

    def compress(self):
        return zlib.compress(self.string_repr(), -1)

    def to_dict(self):
        """docstring for to_json"""
        return {"protobuf": bytes_to_hex_str(self.string_repr())}
