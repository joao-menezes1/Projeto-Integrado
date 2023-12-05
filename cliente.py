import socket
import threading

class Cliente:
    def __init__(self):
        self.cliente = None

    def iniciar_cliente(self):
        HOST = '192.168.0.85'
        # HOST = '172.30.224.1'
        PORT = 10000

        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((HOST, PORT))

        self.receber_mensagens_servidor()

    def receber_mensagens_servidor(self):
        while True:
            msg_servidor = self.cliente.recv(1024).decode('utf8')
            print(msg_servidor)
            if ':' in msg_servidor:
                resposta = input("mensagem: ")
                self.enviar_mensagem(resposta)

    def enviar_mensagem(self, msg):
        self.cliente.send(msg.encode('utf8'))


cliente = Cliente()
cliente.iniciar_cliente()



# COMENTARIOS

    # def verificar_conexao(self):
    #     while True:
    #         # Aqui, você pode implementar a lógica para verificar a conexão com o servidor
    #         # Por exemplo, você pode enviar um sinal periódico para o servidor para confirmar a conexão
    #         pass