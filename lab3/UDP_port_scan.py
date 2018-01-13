import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

dst_ip = "172.16.143.136"
src_port = 20349
# dst_port = 45
dst_port = 500
dst_timeout = 10


def udp_scan(dst_ip, dst_port, dst_timeout):
    udp_scan_resp = sr1(IP(dst=dst_ip)/UDP(dport=dst_port),
                        timeout=dst_timeout)
    print udp_scan_resp
    if ( not udp_scan_resp):
        retrans = []
        for count in range(0, 3):
            retrans.append(
                sr1(IP(dst=dst_ip)/UDP(dport=dst_port), timeout=dst_timeout))
        for item in retrans:
            if (item):
                udp_scan(dst_ip, dst_port, dst_timeout)
        return "Open|Filtered"
    elif (udp_scan_resp.haslayer(UDP)):
        return "Open"
    elif(udp_scan_resp.haslayer(ICMP)):
        if(int(udp_scan_resp.getlayer(ICMP).type) == 3 and int(udp_scan_resp.getlayer(ICMP).code) == 3):
            return "Closed"
        elif(int(udp_scan_resp.getlayer(ICMP).type) == 3 and int(udp_scan_resp.getlayer(ICMP).code) in [1, 2, 9, 10, 13]):
            return "Filtered"

if __name__ == '__main__':
    print udp_scan(dst_ip, dst_port, dst_timeout)
