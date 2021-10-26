import socket
import threading
from time import sleep


# Variabls
c = socket.socket()
port = 9876
clientList = []
rooms = {}
id_ = None
max_rooms = 5

# functions


def MyStrip(word):
    newWord = ""
    for letter in word:
        if(letter) == " ":
            continue
        newWord = newWord + letter
    return newWord

def HandleSEND():
    while True:
        try:
            msg = input("Enter msg : ")
            msg = "msg,"+str(id_)+","+msg
            c.send(msg.encode())
        except Exception as e:
            print(e)


def HandleRECV():

    while True:
        try:
            msg = c.recv(1024)
            HandleMSG(msg)
            # Broadcast(client, msg)
        except Exception as e:
            print(e)


def HandleMSG(msg):
    msg = msg.decode()
    msgIdentifier = msg.split(",")[0]
    if(msgIdentifier == "enter"):
        print(msg)
        sendThread = threading.Thread(target=HandleSEND)
        sendThread.start()

    if(msgIdentifier == "msg"):
        print(msg.split(",")[2])
    if(msgIdentifier == "id"):
        print(msg.split(",")[1])


# connect to the server
try:
    c.connect(("127.0.0.1", port))
    clientThread = threading.Thread(target=HandleRECV)
    clientThread.start()
    sleep(1)
    print("usage : ")
    print("\t-send (create) to create room")
    print("\t-send (join) to join a room")
    print("")
    command = input(" >> ")
    command = MyStrip(command.lower())
    if command  == "create":
        msg = "create,"
        msg = msg+"room"
    elif command == "join":
        msg = input("Enter your room ID : ")
        msg = "join,"+msg
    # id = int(msg)
    # msg = "room,"+msg
    c.send(msg.encode())
except Exception as e:
    print(e)
