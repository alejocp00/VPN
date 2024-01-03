import socket
import struct


class UDP:
    def __init__(self):
        # UDP Header
        self.VERSION_OFF     = 0
        self.IHL_OFF         = self.VERSION_OFF
        self.DSCP_OFF        = self.IHL_OFF + 1
        self.ECN_OFF         = self.DSCP_OFF
        self.LENGTH_OFF      = self.DSCP_OFF + 1
        self.ID_OFF          = self.LENGTH_OFF + 2
        self.FLAGS_OFF       = self.ID_OFF + 2
        self.OFF_OFF         = self.FLAGS_OFF
        self.TTL_OFF         = self.OFF_OFF + 2
        self.PROTOCOL_OFF    = self.TTL_OFF + 1
        self.IP_CHECKSUM_OFF = self.PROTOCOL_OFF + 1
        self.SRC_IP_OFF      = self.IP_CHECKSUM_OFF + 2
        self.DEST_IP_OFF     = self.SRC_IP_OFF + 4
        self.SRC_PORT_OFF    = self.DEST_IP_OFF + 4
        self.DEST_PORT_OFF   = self.SRC_PORT_OFF + 2
        self.UDP_LEN_OFF     = self.DEST_PORT_OFF + 2
        self.UDP_CHECKSUM_OFF= self.UDP_LEN_OFF + 2
        self.DATA_OFF        = self.UDP_CHECKSUM_OFF + 2

        self.IP_PACKET_OFF   = self.VERSION_OFF
        self.UDP_PACKET_OFF  = self.SRC_PORT_OFF

        self.socket = None
        self.src_addr = None

    def parse(self,data):
        packet = {}
        packet['version']       = data[self.VERSION_OFF] >> 4
        packet['IHL']           = data[self.IHL_OFF] & 0x0F
        packet['DSCP']          = data[self.DSCP_OFF] >> 2
        packet['ECN']           = data[self.ECN_OFF] & 0x03
        packet['length']        = (data[self.LENGTH_OFF] << 8) + data[self.LENGTH_OFF + 1]
        packet['Identification']= (data[self.ID_OFF] << 8) + data[self.ID_OFF + 1]
        packet['Flags']         = data[self.FLAGS_OFF] >> 5
        packet['Offset']        = ((data[self.OFF_OFF] & 0b11111) << 8) + data[self.OFF_OFF + 1]
        packet['TTL']           = data[self.TTL_OFF]
        packet['Protocol']      = data[self.PROTOCOL_OFF]
        packet['Checksum']      = (data[self.IP_CHECKSUM_OFF] << 8) + data[self.IP_CHECKSUM_OFF + 1]
        packet['src_ip']        = '.'.join(map(str, [data[x] for x in range(self.SRC_IP_OFF, self.SRC_IP_OFF + 4)]))
        packet['dest_ip']       = '.'.join(map(str, [data[x] for x in range(self.DEST_IP_OFF, self.DEST_IP_OFF + 4)]))
        packet['src_port']      = (data[self.SRC_PORT_OFF] << 8) + data[self.SRC_PORT_OFF + 1]
        packet['dest_port']     = (data[self.DEST_PORT_OFF] << 8) + data[self.DEST_PORT_OFF + 1]
        packet['udp_length']    = (data[self.UDP_LEN_OFF] << 8) + data[self.UDP_LEN_OFF + 1]
        packet['UDP_checksum']  = (data[self.UDP_CHECKSUM_OFF] << 8) + data[self.UDP_CHECKSUM_OFF + 1]
        packet['data']          = ''.join(map(chr, [data[self.DATA_OFF + x] for x in range(0, packet['udp_length'] - 8)]))

        return packet

    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
        return self.socket
    
    def udp_bind(self,src_addr):
        self.socket.bind(src_addr)
        self.src_addr = src_addr

    def udp_send(self,data, dest_addr):

        #Generate pseudo header
        src_ip, dest_ip = self.ip2int(self.src_addr[0]), self.ip2int(dest_addr[0])
        src_ip = struct.pack('!4B', *src_ip)
        dest_ip = struct.pack('!4B', *dest_ip)

        zero = 0

        protocol = socket.IPPROTO_UDP 

        #Check the type of data
        try:
            data = data.encode()
        except AttributeError:
            pass

        src_port = self.src_addr[1]
        dest_port = dest_addr[1]

        data_len = len(data)
        
        udp_length = 8 + data_len

        checksum = 0
        pseudo_header = struct.pack('!BBH', zero, protocol, udp_length)
        pseudo_header = src_ip + dest_ip + pseudo_header
        udp_header = struct.pack('!4H', src_port, dest_port, udp_length, checksum)
        checksum = self.checksum_func(pseudo_header + udp_header + data)
        udp_header = struct.pack('!4H', src_port, dest_port, udp_length, checksum)
        
        self.socket.sendto(udp_header + data, dest_addr)

    def checksum_func(self,data):
        checksum = 0
        data_len = len(data)
        if (data_len % 2):
            data_len += 1
            data += struct.pack('!B', 0)
        
        for i in range(0, data_len, 2):
            w = (data[i] << 8) + (data[i + 1])
            checksum += w

        checksum = (checksum >> 16) + (checksum & 0xFFFF)
        checksum = ~checksum & 0xFFFF
        return checksum

    def ip2int(self,ip_addr):
        if ip_addr == 'localhost':
            ip_addr = '127.0.0.1'

        return [int(x) for x in ip_addr.split('.')]

    def udp_recv(self, size):
        zero = 0
        protocol = 17
        data=None
        while True:
            data, src_addr = self.socket.recvfrom(size)

            packet = self.parse(data)
            ip_addr = struct.pack('!8B', *[data[x] for x in range(self.SRC_IP_OFF, self.SRC_IP_OFF + 8)])
            udp_psuedo = struct.pack('!BB5H', zero, protocol, packet['udp_length'], packet['src_port'], packet['dest_port'], packet['udp_length'], 0)
            
            verify = self.verify_checksum(ip_addr + udp_psuedo + packet['data'].encode(), packet['UDP_checksum'])
            print(packet['data'])
            print(src_addr)
            print(verify)
            print(packet['UDP_checksum'])
            if verify == 0xFFFF:
                print(packet['data'])
                return data, src_addr
            else:
                print('Checksum Error!Packet is discarded')
                return "",""   ##############cambiar aqui segun lo que sea necesario

    def verify_checksum(self,data, checksum):
        data_len = len(data)
        if (data_len % 2) == 1:
            data_len += 1
            data += struct.pack('!B', 0)
        
        for i in range(0, data_len, 2):
            w = (data[i] << 8) + (data[i + 1])
            checksum += w
            checksum = (checksum >> 16) + (checksum & 0xFFFF)

        return checksum
    
    def close(self):
        self.socket.close()
        