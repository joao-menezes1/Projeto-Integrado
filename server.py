import socket
import threading

class server():

    def iniciar_servidor(self):
        HOST = '192.168.0.85'
        PORT = 10000
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (HOST, PORT)

        server.bind(orig)

        server.listen()

        print("Aguardando conexões...")

        while True:
            client_socket, client_address = server.accept()
            client_thread = threading.Thread(target=self.comunicacao_cliente, args=(client_address, client_socket))
            client_thread.start()
    
    def comunicacao_cliente(self, cliente_address, cliente_socket):
        print(f"Cliente conectado: {cliente_address}")
        while True:
            msg = cliente_socket.recv(1024).decode("utf8")
            print(f'Mensagem: {cliente_address} ==== {msg}')
    
    def criar_sala(self):
        
        



server = server()
server.iniciar_servidor()