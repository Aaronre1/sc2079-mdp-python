import socket

SOCK = socket.socket()
PORT = 12345
IP = "192.168.1.9"
# server 
def start():
    SOCK.bind((IP,PORT))
    SOCK.listen(5)
    c, addr = SOCK.accept()
    print(f"connected by {addr}")
    while True:
        data = c.recv(1024)
        print(data)
        if not data:
            break
        c.sendall(data)
        
        #c.send(bytearray([0x00,0x00]))
        
       # c.close()
    
    
start()