import socket 
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address  = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

clients = []
nicknames = []
print("Server is running")

def remove(connection):
    if connection in clients:
        clients.remove(connection)

def broadcast(message,connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message.encode("utf-8"))
            except:
                remove(client)


def clientThread(conn,nickname):
    conn.send("welcome to this chatroom!".encode("utf-8"))
    while True:
        try:
            message = conn.recv(2048).decode("utf-8")
            if message:
                print("<"+ nickname[0] + "> " + message)
                # message_to_send = "<"+ nickname[0] + "> " + message
                broadcast(message, conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)


while True:
    conn,addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')

    clients.append(conn)
    nicknames.append(nickname)
    message = "{} joined this server!".format(nickname)

    print(addr[0]+" connected")
    print(message)

    broadcast(message,conn)

    new_thread = Thread(target= clientThread,args = (conn,addr))
    new_thread.start()

