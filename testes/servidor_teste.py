import socket
import threading
import time
from hashtable import HashTable

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

            verifica_conexao_thread = threading.Thread(target=self.verificar_conexao, args=(cliente_socket, cliente_address))
            verifica_conexao_thread.start()

    def comunicacao_cliente(self, cliente_address, cliente_socket):
        print(f"Cliente conectado: {cliente_address}")
        self.enviar_menu_para_cliente(cliente_socket)  # Envia o menu inicial para o cliente

        while True:
            resposta_cliente = self.__receber_msg_cliente(cliente_socket)

            if resposta_cliente == '1':
                self.mostrar_salas_disponiveis(cliente_socket)
                cliente_socket.send("Você escolheu a opção 1".encode('utf-8'))
            elif resposta_cliente == '2':
                self.__enviar_msg_cliente("Digite o nome da sala: ", cliente_socket)
                nome_sala = self.__receber_msg_cliente(cliente_socket)
                self.__criar_sala(nome_sala, cliente_address)
                cliente_socket.send("Você escolheu a opção 2".encode('utf-8'))
            else:
                cliente_socket.send("Opção inválida. Tente novamente.".encode('utf-8'))
    
    def __enviar_msg_cliente(self, mensagem, cliente_socket):
        cliente_socket.send(mensagem.encode('utf8'))

    def __receber_msg_cliente(self, cliente_socket):
        msg = cliente_socket.recv(1024).decode('utf8')
        return msg

    def enviar_menu_para_cliente(self, cliente_socket):
        menu = "      MENU      \n1  - Salas disponíveis\n2 - Criar uma nova sala\n3 - Voltar"
        self.__enviar_msg_cliente(menu, cliente_socket)
    
    def mostrar_salas_disponiveis(self, cliente_socket):
        salas = self.salas.keys()
        salas_str = ''
        for sala in salas:
            salas_str += (f'-  {sala}\n')
        self.__enviar_msg_cliente(salas_str, cliente_socket)

    def __criar_sala(self, nome, cliente_address):
        self.salas.put(nome, cliente_address)
        print(self.salas)

    def verificar_conexao(self, cliente_socket, cliente_address):
        while True:
            # Envia um sinal de verificação para o cliente
            self.__enviar_msg_cliente("check_connection", cliente_socket)
            time.sleep(5)  # Aguarda 5 segundos
            if self.__receber_msg_cliente(cliente_socket) != 'connection_ok':
                encerrar_conexao = cliente_socket.close()

servidor = Server()
servidor.iniciar_servidor()
