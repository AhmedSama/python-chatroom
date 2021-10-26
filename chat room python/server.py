import socket
import threading
import pygame
from ClientClass import Client


class ServerSocket():
    def __init__(self):

        try:
            self.socket = socket.socket()
            self.client = []
            self.ID_Maker = 0
        except Exception as e:
            print(e)

    def start(self, port):
        print(f"Server Started at Port {port}")
        try:
            self.socket.bind(("127.0.0.1", port))
            self.socket.listen(2)
        except Exception as e:
            print(e)
        while True:
            try:
                client, ip = self.socket.accept()
                print(f"new client connected...")
                self.HandleClient(client)
                clientThread = threading.Thread(
                    target=self.HandleRECV, args=(client))
                clientThread.start()
            except Exception as e:
                print(e)

    def HandleClient(self, client):
        c = Client(client, self.ID_Maker)
        self.ID_Maker += 1
        self.client.append(c)

    def HandleRECV(self, client):
        while True:
            try:
                msg = client.recv(1024)
                print(msg.decode())
                self.Broadcast(client, msg.decode())
            except Exception as e:
                # TODO  remove the client from the list and handle disconnection and sendall msg about disconnected one
                print(e)

    def Broadcast(self, c, msg):
        for client in self.client:
            try:
                if client.clientSocket != c:
                    client.clientSocket.send(msg)
            except Exception as e:
                print(e)

    def SendAll(self, msg):
        for client in self.client:
            try:
                client.clientSocket.send(msg)
            except Exception as e:
                print(e)


# Variabls
server = socket.socket()
port = 9876

rooms = {}
id_maker = 0
max_rooms = 5
clientIDES = 0


# Functions

def createRoom(client):
    rooms[clientIDES] = Room(clientIDES,10)
    rooms[clientIDES].Add(Client(client,-1))

def HandleClient(client):

    while True:
        try:
            msg = client.clientSocket.recv(1024)
            HandleMSG(client, msg)
            # Broadcast(client, msg)
        except Exception as e:
            disconnect(client)
            print("connection closed from "+str(client.ID))
            break


def disconnect(c):
    for i in rooms:
        for index,client in enumerate(rooms[i].clients) :
            if client.clientSocket == c.clientSocket:
                del rooms[i].clients[index].clientSocket
                break


def HandleMSG(client, msg):
    msg = msg.decode()
    msgIdentifier = msg.split(",")[0]
    if(msgIdentifier == "msg"):
        Broadcast(client, msg)
    elif msgIdentifier == "create":
        createRoom(client)
        # id = int(msg.split(",")[1])
        # if(id in range(max_rooms)):
        #     rooms[id].Add(client)
        #     sendTo(client.clientSocket, "enter,yes")
    elif msgIdentifier == "join":
        id = int(msg.split(",")[1])
        if(id in range(max_rooms)):
            rooms[id].Add(client)
def Broadcast(c, msg):
    id = int(msg.split(",")[1])
    try:
        for client in rooms[id].clients:
            if c != client.clientSocket:
                sendTo(client.clientSocket, msg)

    except Exception as e:
        print(e)


def sendTo(client, msg):
    try:
        client.send(msg.encode())
    except Exception as e:
        print(e)


# room class

class Room:
    def __init__(self, id_, max_users):
        self.id = id_
        self.max = max_users
        self.msgs = []
        self.clients = []
        self.idIndex = 0

    def Add(self, user):
        user.ID = self.MakeID()
        self.clients.append(user)

    def MakeID(self):
        if self.idIndex <= self.max:
            currentID = self.idIndex
            self.idIndex += 1
            return currentID
        return -1


# Listening on main Thread
try:
    # making rooms
    clientIDES = "id,"+clientIDES
    server.bind(("127.0.0.1", port))
    server.listen(2)
    print(f"server started at port {port}")
    while True:
        client, ip = server.accept()
        print("new client connected...")
        c = Client(client, -1)
        clientThread = threading.Thread(target=HandleClient, args=(c,))
        clientThread.start()
except Exception as e:
    print(e)
