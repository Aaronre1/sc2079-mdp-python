from server import ImageServer
import socket

if __name__ == '__main__':
    ip =  socket.gethostbyname(socket.gethostname())
    port = 12345
    with ImageServer(ip, port) as s:
        client, addr = s.accept()
        while True:
            data = client.recv(1024)
            
            # get file path from data
            # process image
            # return result
    
    print(ip)