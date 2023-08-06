import socket

class Server:
    def StartServer(self, ip, port):
        self.ip = ip
        self.port = port
        self.clients = []
        self.addrs = []
        self.on = False
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.on = True
        try:
            self.server.bind((ip, port))
        except Exception as e:
            print(e)
        while self.on == True:
            self.server.listen()
    def CloseServer(self):
        self.on = False
        self.server.close()
    def GetServerIp(self):
        return self.ip
    def GetServerPort(self):
        return self.port
    def AcceptClient(self):
        client, addr = self.server.accept()
        self.clients.append(client)
        self.addrs.append(addr)
    def GetClientAddr(self, client):
        number = self.clients.index(client)
        return self.addrs[number]
    def GetAddrClient(self, addr):
        number = self.addrs.index(client)
        return self.clients[number]
    def GetAllClients(self):
        return self.clients
    def PrintAllClients(self):
        for i in self.clients:
            print(i)
    def GetAllAddrs(self):
        return self.addrs
    def PrintAllAddrs(self):
        for i in self.addrs:
            print(i)
class Client():
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def Connect(self, ip, port):
        try:
            self.client.connect((ip, port))
            self.client.recv(1024)
        except Exception as e:
            print(e)