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
            cliente_socket, cliente_address = server.accept()
            cliente_thread = threading.Thread(target=self.comunicacao_cliente, args=(cliente_address, cliente_socket))
            cliente_thread.start()

    # def comunicacao_cliente(self, cliente_address, cliente_socket):
        
    #     cliente = cliente_socket
    #     menu = ("      MENU      \n1  - Salas disponíveis\n2 - Criar uma nova sala\n3 - Voltar")
    #     cliente.send(menu.encode('utf8'))
    #     resposta = cliente.recv(1024).decode('utf8')
    #     self.mostrar_menu_servidor(resposta)
    #     while True:
    #         msg = cliente_socket.recv(1024).decode("utf8")
    #         print(f'Mensagem: {cliente_address} ==== {msg}')


    def comunicacao_cliente(self, cliente_address, cliente_socket):
        print(f"Cliente conectado: {cliente_address}")
        self.enviar_menu_para_cliente(cliente_socket)  # Envia o menu inicial para o cliente

        while True:
            # Aguarda a resposta do cliente
            resposta_cliente = cliente_socket.recv(1024).decode('utf-8')

            # Lógica para processar a resposta do cliente
            if resposta_cliente == '1':
                self.mostrar_salas_disponiveis()
                cliente_socket.send("Você escolheu a opção 1".encode('utf-8'))
            elif resposta_cliente == '2':
                self.__enviar_msg_cliente("Digite o nome da sala: ", cliente_socket)
                nome_sala = self.__receber_msg_cliente(cliente_socket)
                self.__criar_sala(nome_sala, cliente_address)
                cliente_socket.send("Você escolheu a opção 2".encode('utf-8'))
            else:
                # Mensagem para resposta inválida
                cliente_socket.send("Opção inválida. Tente novamente.".encode('utf-8'))
    
    def __enviar_msg_cliente(self, mensagem, cliente_socket):
        cliente_socket.send(mensagem.encode('utf8'))

    def __receber_msg_cliente(self, cliente_socket):
        msg = cliente_socket.recv(1024).decode('utf8')
        return msg

    def enviar_menu_para_cliente(self, cliente_socket):
        menu = "(      MENU      \n1  - Salas disponíveis\n2 - Criar uma nova sala\n3 - Voltar)"
        cliente_socket.send(menu.encode('utf-8'))
    
    # def pedir_entrada_para_cliente(self, client_socket):
    #     enviar_pedido_entrada = client_socket.send(("Digite uma opção: ").encode('utf8'))
    #     resposta = client_socket.recv(1024).decode('utf8')
    #     return resposta

    # def mostrar_menu_servidor(self, resposta):
    #     if resposta == 1:
    #         self.mostrar_salas_disponiveis()  # Chama a função para mostrar as salas disponíveis
    #     elif resposta == 2:
    #         nome_sala = input('Digite o nome da sala: ')
    #         self.__criar_sala(nome_sala)  # Chama a função para criar uma nova sala

    def mostrar_salas_disponiveis(self):
        print("Salas Disponíveis:")
        salas = self.salas.keys()
        for sala in salas:
            print(sala)

    def __criar_sala(self, nome, cliente_address):
        self.salas.put(nome, cliente_address)
        print(self.salas)

servidor = Server()
servidor.iniciar_servidor()