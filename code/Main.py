from .KafkaProducerWrapper import KafkaProducerWrapper
from .CiscoTelemetry import CiscoTelemetry
from .CiscoInterface import CiscoInterface
import threading
import time
import datetime


def create_interface_proto(row):
    intface = CiscoInterface(row["Interface"], row["NetIntIndex"], row["Capacity"], row["NetIntOperStatus"], row["NetIntAdminStatus"], row["NetInt::PhysAddress"]):
    if row["IPAddress"] is not None:
        intface.set_ip(row["IPAddress"], row["NetIntNetMask"])

def push_interface_data(database, kafkaConn, node, topic, sleep_time, num_times):
    print("Send interfaces of node:" + node)
    sqlConn = SqliteConn()
    sqlConn.create_connection(database)
    start_time = datetime.datetime.now()
    interfaces_data = []
    for row in sqlConn.select_rows_from_table("NetIntInterfaces", '''Node="''' + node + '''"'''):
        interface_data = create_interface_proto(row)
        interfaces_data.append(interface_data)
    while num_times > 0:
        num_times = num_times -1
        telemetry_header = CiscoTelemetry(node, topic, encoding_path, collection_id, start_time, datetime.datetime.now(), datetime.datetime.now())
        telemetry_header.set_gpbkv(interfaces_data)
        time.sleep(sleep_time)


def main():
    topic = "interfaces"
    #Open connection to kafka
    kafkaConn = KafkaProducerWrapper(bootstrap_servers=['localhost:9092'], topic=topic)
    kafkaConn.setup()

    # Open database file and read all interfaces
    database = r"../test/resources/2node_plan.db"
    sqlConn = SqliteConn()
    sqlConn.create_connection(database)
    thread_list = []
    nodes = []
    for row in sqlConn.select_rows_from_table("Nodes"):
        nodes.append(row["Name"])
    sqlConn.close()
    for node in nodes:
        thread = threading.Thread(target = push_interface_data, args = (database, kafkaConn, node, topic, 5, 2))
        thread_list.append(thread)
    for th in thread_list:
        th.join()
    

        


if __name__ == '__main__':
    main()
