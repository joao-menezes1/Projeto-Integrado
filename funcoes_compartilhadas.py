class Compartilha:
    
    def __enviar_msg_cliente(self, mensagem, cliente_socket):
        cliente_socket.send(mensagem.encode('utf8'))

    def __receber_msg_cliente(self, cliente_socket):
        msg = cliente_socket.recv(1024).decode('utf8')
        return msg
    
    def __enviar_msg_cliente_broadcast(self, mensagem, cliente_socket):
        for cliente in client_socket:
            self.__enviar_msg_cliente(mensagem, cliente)