import socket
import threading
from hashtable import *

class Server:
    def __init__(self):
        self.salas = HashTable(size=4)
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
        cliente = cliente_socket
        menu = ("      MENU      \n1  - Salas disponíveis\n2 - Criar uma nova sala\n3 - Voltar")
        cliente.send(menu.encode('utf8'))
        resposta = cliente.recv(1024).decode('utf8')
        self.mostrar_menu_servidor(resposta)
        while True:
            msg = cliente_socket.recv(1024).decode("utf8")
            print(f'Mensagem: {cliente_address} ==== {msg}')

    def mostrar_menu_servidor(self, resposta):
        if resposta == 1:
            self.mostrar_salas_disponiveis()  # Chama a função para mostrar as salas disponíveis
        elif resposta == 2:
            nome_sala = input('Digite o nome da sala: ')
            self.__criar_sala(nome_sala)  # Chama a função para criar uma nova sala

    def mostrar_salas_disponiveis(self):
        print("Salas Disponíveis:")
        salas = self.salas.keys()
        for sala in salas:
            print(sala)

    def __criar_sala(self, nome, client_address):
        self.salas.put(nome, client_address)
        print(self.salas)

servidor = Server()
servidor.iniciar_servidor()