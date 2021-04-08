import socket

def begin():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    host = input("host: ")
    try:
        port = int(input("port: "))
        sock.connect((host, port))
    except ConnectionRefusedError:
        print("Could not connect, will use another host and port")
        sock.connect(('localhost', 9090))
    except ValueError:
        print("Could not connect, will use another host and port")
        sock.connect(('localhost', 9090))
    #work(sock)

# def work(sock):
#     while True:
#         st = input()
#         sock.send(st.encode())
#         data = sock.recv(8192)
#         print(data)
#         if data == b'exit':
#             sock.close()
#             begin()
#
# begin()

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto('Connect'.encode('utf-8'), ('', 9090))
d = client.recvfrom(1024)
reply = d[0]
addr = d[1]
print (reply.decode('utf-8'))
while True:
     msg = input('Enter message to send: ')
     client.sendto(msg.encode('utf-8'), ('', 9090))
     d = client.recvfrom(1024)
     reply = d[0]
     addr = d[1]
     print (reply.decode('utf-8'))
     if reply == b'exit':
         client.close()
         begin()
client.close()