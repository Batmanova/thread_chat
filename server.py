import socket
import threading

stop = False
thread_sum = 0

def root_mode():
    while True:
        received, addr = sock.recvfrom(8192)
        if received == b'close':
            break
        elif received == b'show_logs':
            with open("log.txt", 'r') as log_file:
                for line in log_file:
                    print(line)
        elif received == b'clean_logs':
            with open("log.txt", 'wb') as log_file:
                pass
        elif received == b'clean_clients':
            global addresses, passwords, connections
            addresses = {}
            passwords = {}
            connections = []
        elif received == b'EXIT' or received == b'Exit' or received == b'exit':
            sock.sendto('exit root mode'.encode('utf-8'), addr)
            break

class Scan(threading.Thread):
    def __init__(self):
        global thread_sum
        threading.Thread.__init__(self, name="scan")
        thread_sum += 1

    def run(self):
        global stop, thread_sum
        while not stop:
            for i in range(1024, 65536, thread_sum):
                try:
                    sock.bind(('', i))
                    sock.listen(1)
                    port = i
                except BaseException:
                    with open("log.txt", "w") as file:
                        file.write("connecting error")
        print('connected: ', port)

def client(address):
    nickname = addresses[address]
    while True:
          global connections
          received, addr = sock.recvfrom(8192)
          print(addr)
          if addr != address:
              continue
          else:
              print(received)
              if not received:
                  break
              if received == b'EXIT' or received == b'Exit' or received == b'exit':
                  print('Exit')
                  connections.remove(addr)
                  sock.sendto('exit'.encode('utf-8'), addr)
                  break
              elif received == b'root_mode' or received == b'ROOT_MODE':
                  root_mode(True)
              else:
                  for conn in connections:
                      #if conn != addr: #чтобы было видно что работает
                          msg = nickname + ' said: '.encode('utf-8') + received
                          sock.sendto(msg, conn)
    sock.close()


addresses = {}
passwords = {}
connections = []
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
port = 9090
try:
    sock.bind(('', port))
    sock.listen(1)
except BaseException:
    scanner1 = Scan()
    scanner1.start()
    scanner2 = Scan()
    scanner2.start()

n = 0
while True:
    received, addr = sock.recvfrom(8192)
    if addr in addresses.keys() and addr not in connections:
        sock.sendto('Enter the password'.encode('utf-8'), addr)
        data, addr = sock.recvfrom(8192)
        if not data:
            break
        if data == passwords[addresses.get(addr)]:
            sock.sendto('Welcome'.encode('utf-8'), addr)
            connections.append(addr)
        else:
            sock.sendto('Wrong password'.encode('utf-8'), addr)
            continue
    #elif addr not in addresses.values():
    else:
        sock.sendto('Hi! Write your nickname'.encode('utf-8'), addr)
        data_name, addr = sock.recvfrom(8192)
        addresses[addr] = data_name
        sock.sendto('Write your password'.encode('utf-8'), addr)
        data_pass, addr = sock.recvfrom(8192)
        passwords[addr] = data_pass
        sock.sendto('Welcome! Write your first message'.encode('utf-8'), addr)
        connections.append(addr)
        n += 1
    client = threading.Thread(target=client, name=str(n), args=[addr])
    client.start()