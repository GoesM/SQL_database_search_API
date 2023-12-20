import socket
def get_ipv6_address():
    try:
        # 获取主机名
        host_name = socket.gethostname()
        
        # 获取主机名对应的IPv6地址列表
        ipv6_addresses = socket.getaddrinfo(host_name, None, socket.AF_INET6)
        
        # 从列表中提取IPv6地址
        for address_info in ipv6_addresses:
            ipv6_address = address_info[4][0]
            if '%' not in ipv6_address:
                return ipv6_address

    except socket.error as e:
        print(f"Error: {e}")

    return None


#global_ip = '10.130.147.18'
global_ip = '127.0.0.1'
port_num = '5000'
ipv6_ip = get_ipv6_address()
api_ = f'[{ipv6_ip}]:{port_num}'
print(api_)

default_account = 'gsm'
default_key = '123456'