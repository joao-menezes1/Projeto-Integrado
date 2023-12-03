import socket 

HOST = '192.168.0.85'
PORT = 10000

server = (HOST, PORT)

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cliente.connect(server)

while True:
    msg_servidor = cliente.recv(1024).decode('utf8')
    print(msg_servidor)
    msg = str(input("mensagem: "))
    cliente.send(msg.encode('utf8'))