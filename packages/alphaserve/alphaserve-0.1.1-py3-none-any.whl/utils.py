import socket
import urllib

def get_public_ip():
    """Returns the public ip of this client\nParams: none\npublic_ip"""
    ip = urllib.urlopen("https://api.ipify.org").read()
    return ip

def get_local_ip():
    """Returns the local ip of this client\nParams: none\nlocal_ip"""
    return([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect(("192.168.1.0", 6666))
    s.close()
    return s.getsockname()[0]
    
def get_broadcast_address(ip=get_local_ip()):
    """Returns the local broadcast address of the network\nParams: [ip=local_ip]\nget_broad_addr"""
    import re
    return "".join(re.split(r'(\.|/)', ip)[0:-1])+"255"

def send_udp_message(msg, ip=get_broadcast_address(ip=get_local_ip()), port=7777):
    """Sends a UDP message [msg] to the [ip] on [port]\nParams: msg, [ip=local_broadcast], [port=7777]\nsend_udp"""
    if len(msg) <= 0:
        return 0

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    result = udp.sendto(bytes(msg, "utf-8"), (ip, port))
    return result

def recv_udp_message(length, ip="0.0.0.0", port=7777):
    """Receives a UDP message of the given [length] on [ip]:[port]\nParams: length, [ip=local_broadcast], [port=7777]\nrecv_udp"""
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        udp.bind((str(ip), port))
    except Exception as e:
        print("Failed to bind socket... [{}:{}]".format(ip, port))
        print(e)
        return None
    msg = udp.recvfrom(length)
    if len(msg) > 0:
        return msg
    else:
        return None
