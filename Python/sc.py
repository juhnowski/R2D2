import socket
import threading
import socketserver

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024).decode("utf-8")
        cur_thread = threading.current_thread()
        response = str(cur_thread.name) + ":" + str(data)
        self.request.send(str.encode(response))

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.send(message)
        response = sock.recv(1024)
        print("Received: "+ str(response))
    finally:
        sock.close()

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "127.0.0.1", 9001
    ip=HOST
    port = PORT
    data = "start"
    print("Available command: +f1,-f1,+f2,-f2,i,stop")
    while data != "stop":
        data = input()
        if (len(data)>0):
            client(ip, port, str.encode(data))
        else:
            print ("Null string is unavailable to send")
    

