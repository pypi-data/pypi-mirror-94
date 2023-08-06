import socket

def get_local_ip():
    ip = '<host-name>'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 53))
        ip = s.getsockname()[0]
        s.close()
    except:
        ip = socket.gethostname()
    return ip

if __name__ == '__main__':
    print(get_local_ip())