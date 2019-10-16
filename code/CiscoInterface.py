from proto_files.im_cmd_info_pb2 import im_cmd_info, im_cmd_info_KEYS, im_cmd_mac_addr_st
import re
from ipaddress import IPv4Network

class CiscoInterface:
    def __init__(self, intf_name, if_index, speed, state, line_state, mac_addr):
        self.keys = im_cmd_info_KEYS()
        self.keys.interface_name = intf_name

        self.obj = im_cmd_info()
        self.obj.interface_handle = intf_name
        self.obj.interface_type = self.get_type(intf_name)
        self.obj.if_index = if_index
        self.obj.mtu = 1514
        self.obj.speed = speed
        self.obj.state = self.set_state(state, line_state)
        self.obj.line_state = self.set_state(state, line_state)
        self.obj.burned_in_address = im_cmd_mac_addr_st()
        self.obj.burned_in_address.address = self.set_burned_in_address(mac_addr)

    def get_type(self, intf_name):
        match = re.search("/d", intf_name)
        if match is not None:
            return intf_name[0:match.start()]
        else:
            return intf_name

    def set_state(self, state, line_state):
        if state == "up":
            return "im-state-up"
        else:
            if line_state == "down":
                return "im-state-admindown"
            else:
                return "im-state-down"

    def set_burned_in_address(self, mac_addr):
        tel_rep = mac_addr.replace(":","")
        tel_rep = tel_rep[0:4] + ":" + tel_rep[4:8] + ":" + tel_rep[8:12]
        return tel_rep
    
    def set_ip(ip, mask):
        self.obj.im_cmd_ip_info_st.ip_address = ip
        self.obj.im_cmd_ip_info_st.subnet_mask_length = IPv4Network("0.0.0.0/"+mask).prefixlen
