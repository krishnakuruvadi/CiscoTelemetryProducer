from proto_files.telemetry_pb2 import Telemetry

class CiscoTelemetry:
    def __init__(self, node_id, subscription, encoding_path, collection_id, start_time, msg_timestamp, end_time):
        self.obj = Telemetry()
        self.obj.node_id_str = node_id
        self.obj.subscription_id_str = subscription
        self.obj.encoding_path = encoding_path
        self.obj.collection_id = collection_id
        self.obj.collection_start_time = start_time
        self.obj.msg_timestamp = msg_timestamp
        self.obj.collection_end_time = end_time

