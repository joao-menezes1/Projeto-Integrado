import socket 

HOST = '192.168.0.85'
PORT = 10000

server = (HOST, PORT)

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect(server)

while True:
    msg = input("mensagem: ")
    cliente.send(f"{msg.encode('utf8')}")