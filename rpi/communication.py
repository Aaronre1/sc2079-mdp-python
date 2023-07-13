import socket

SOCK = socket.socket()
PORT = 12345
IP = "192.168.1.9"


def send(message):
    SOCK.connect(IP, PORT)
    SOCK.send(message)
    SOCK.close()
    
def open_socket(ip):
    address = (ip, PORT)
    conn = socket.socket()
    conn.bind(address)
    conn.listen(1)
    print(conn)
    return conn
    

ip = '192.168.1.1'
conn = open_socket(ip)
while True:
    client = conn.accept()[0]
    data = client.recv(1024)
    print(data)
    client.sendall(b'PONG')
    client.close()
    if not data:
        break
conn.close()    
    