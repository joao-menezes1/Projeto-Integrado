import socket
import threading
from hashtable import *
import multiprocessing
import dicionario_temas_palavras
from unidecode import unidecode
import random
import re
from lista_circular import *
from fila import *

class Server():
    def __init__(self):
        self.salas = HashTable(size=4)
        self.jogadores = LinkedList()

    def iniciar_servidor(self):
        HOST = '192.168.0.85'
        #HOST = '172.30.224.1'
        PORT = 10000
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (HOST, PORT)

        server.bind(orig)
        server.listen()

        print("Aguardando conexões...")

        while True:
            cliente_socket, cliente_address = server.accept()
            cliente_thread = threading.Thread(target=self.comunicacao_cliente, args=(cliente_socket, cliente_address))
            cliente_thread.start()

    def comunicacao_cliente(self, cliente_socket, cliente_address):
        print(f"Cliente conectado: {cliente_address}")
        self.enviar_menu_para_cliente(cliente_socket)  # Envia o menu inicial para o cliente

        while True:
            # Aguarda a resposta do cliente
            resposta_cliente = self.__receber_msg_cliente(cliente_socket)
            # Lógica para processar a resposta do cliente
            if resposta_cliente == '1':
                self.mostrar_salas_disponiveis(cliente_socket, cliente_address)
            elif resposta_cliente == '2':
                self.__criar_sala(cliente_socket)
                # self.__enviar_msg_cliente('Você entrou na sala:', cliente_socket)
            else:
                # Mensagem para resposta inválida
                cliente_socket.send("Opção inválida. Tente novamente.".encode('utf-8'))
                self.enviar_menu_para_cliente(cliente_socket)
    
    def __enviar_msg_cliente(self, mensagem, cliente_socket):
        cliente_socket.send(mensagem.encode('utf8'))

    def __receber_msg_cliente(self, cliente_socket):
        msg = cliente_socket.recv(1024).decode('utf8')
        return msg
    
    def __enviar_msg_cliente_broadcast(self, mensagem, cliente_socket):
        for cliente in client_socket:
            self.__enviar_msg_cliente(mensagem, cliente)

    def enviar_menu_para_cliente(self, cliente_socket):
        menu = "      MENU      \n1  - Salas disponíveis\n2 - Criar uma nova sala\n\nDigite uma opção:"
        self.__enviar_msg_cliente(menu, cliente_socket)
    
    def mostrar_salas_disponiveis(self, cliente_socket, cliente_address):
        salas = self.salas.keys()
        if len(salas) == 0:
            self.__enviar_msg_cliente('Não existem salas disponíveis!!', cliente_socket)
            self.enviar_menu_para_cliente(cliente_socket)
        else:
            salas_str = ''
            for sala in salas:
                salas_str += (f'-  {sala}\n')
            self.__enviar_msg_cliente(salas_str, cliente_socket)
            self.__enviar_msg_cliente('      MENU      \n\n1  - Entrar em uma sala\n2 - Voltar para o menu principal\n\nDigite uma opção:', cliente_socket)
            resp = self.__receber_msg_cliente(cliente_socket)
            if resp == '1':
                self.__enviar_msg_cliente("Digite a sala que deseja entrar:", cliente_socket)
                resposta = self.__receber_msg_cliente(cliente_socket)
                self.__entrar_na_sala(resposta, cliente_socket)
            else: 
                self.enviar_menu_para_cliente(cliente_socket)

    def __criar_sala(self, cliente_socket):
        self.__enviar_msg_cliente("Digite o nome da sala: ", cliente_socket)
        nome_sala = self.__receber_msg_cliente(cliente_socket)
        self.salas.put(nome_sala, [cliente_socket])
        self.__enviar_msg_cliente('Sala criada', cliente_socket)
        while True:
            self.__iniciar_jogo_sala(nome_sala)
    
    def __entrar_na_sala(self, sala, cliente_socket):
        # semáforos
        lista = self.salas.get(sala)
        if len(lista) < 4:    
            lista.append(f'{cliente_socket}')
            self.salas.put(f'{sala}', lista)
            self.__enviar_msg_cliente('Você entrou na sala', cliente_socket)
            print(self.salas.items())
        else:
            self.__enviar_msg_cliente('A sala desejada esta com lotação máxima.', cliente_socket)
            self.enviar_menu_para_cliente(cliente_socket)

    
    def __iniciar_jogo_sala(self, sala):
        if len(self.salas[f'{sala}']) == 2:
                jogo_sala = self.jogo(sala)

    def jogo(self, sala):
        self._iniciar_jogo(sala)

    def limpar_entrada(self, entrada):
        entrada_sem_acentos = unidecode(entrada)
        entrada_sem_numeros = re.sub(r'\d+', '', entrada_sem_acentos)
        entrada_apenas_letras = re.sub(r'[^a-zA-Z]', '-', entrada_sem_numeros)
        return entrada_apenas_letras

    def __palavra_usuario(self, cliente):
        tema = self.__mostrar_temas()
        self.__enviar_msg_cliente(tema, cliente)
        tema_escolhido = self.__receber_msg_cliente(cliente)
        palavra = self.__buscar_palavra(tema_escolhido)
        return self.limpar_entrada(palavra)

    def __mostrar_temas(self):
        temas = dicionario_temas_palavras.Temas
        tema_escolhido = "      TEMAS      \n\n"
        for tema, array in temas.items():
            tema_escolhido += (f'-  {tema}\n')
        tema_escolhido += ('\n-  Digite o tema:')
        print(type(tema_escolhido))
        return tema_escolhido

    def __buscar_palavra(self, tema_escolhido):
        palavras_tema = dicionario_temas_palavras.Temas.get(tema_escolhido)
        palavra_aleatoria_escolhida = random.choice(palavras_tema)
        return palavra_aleatoria_escolhida

    def letras(self, letra, array_palavra_jogo, palavra):
        for i, let in enumerate(palavra):
            if letra == let:
                array_palavra_jogo[i] = letra
        palavra_letras = (' '.join(array_palavra_jogo))
        return palavra_letras
    
    def adicionar_jogadores_a_lista(self, lista_jogadores):
        for i in range(len(lista_jogadores)):
            self.jogadores.insert(lista_jogadores[i], (i+1))
    
    def passar_a_vez_jogador(self):
        self.jogadores.advance()
    
    def enviar_status_jogo(self, status, clientes):
        self.__enviar_msg_cliente_broadcast(status, clientes)


    def _iniciar_jogo(self, lista_jogadores):
        self.adicionar_jogadores_a_lista(lista_jogadores)
        tentativas_maximas = 6
        palavra = list(self.__palavra_usuario(self.jogadores.element(0)).upper())
        array_palavra_jogo = ['_'] * len(palavra)
        fila_letras_erradas = Fila()
        tentativas = 0
        jogador = self.jogadores.element(0)
        palavra_rasurada = ''
        status = (f'{palavra_rasurada}\nLetras erradas: {fila_letras_erradas}\nTentativas restantes: {tentativas_maximas - tentativas}')

        while '_' in array_palavra_jogo and tentativas < tentativas_maximas:
            self.__enviar_msg_cliente('Digite uma letra: ', jogador)
            self.__receber_msg_cliente(jogador)
            entrada_limpa = self.limpar_entrada(entrada_usuario.upper())

            if len(entrada_limpa) != 1:
                self.__enviar_msg_cliente('Por favor, digite apenas uma letra.', jogador)
                continue

            letra = entrada_limpa

            if fila_letras_erradas.busca(letra) or letra in array_palavra_jogo:
                self.__enviar_msg_cliente('Você já tentou essa letra. Tente outra.', jogador)
                continue

            elif letra in palavra:
                palavra_rasurada = self.letras(letra, array_palavra_jogo, palavra)
                self.__enviar_msg_cliente(palavra_rasurada, jogador)
                jogador = self.jogadores.advance()
                self.enviar_status_jogo()

            else:
                tentativas += 1
                fila_letras_erradas.enfileirar(letra)
                self.__enviar_msg_cliente(f'Letras erradas: {fila_letras_erradas}', jogador)
                self.__enviar_msg_cliente(f'Tentativas restantes: {tentativas_maximas - tentativas}', jogador)

        if '_' not in array_palavra_jogo:
            self.__enviar_msg_cliente(f'Parabéns! Você acertou a palavra.', jogador)
        else:
            print(f'Você perdeu! A palavra era: {" ".join(palavra)}', jogador)


servidor = Server()
servidor.iniciar_servidor()




    # def __requisicao_para_comecar_o_jogo(self, sala):
    #     jogadores_sala = self.salas[f'{sala}']
    #     for jogador in jogadores_sala:
    #         self.__enviar_msg_cliente('O jogo está pronto para começar.\n\nDigite s/"sim" e n/"não":', jogador)
    #         resposta = self.__receber_msg_cliente(jogador)


# COMENTARIOS

    # def comunicacao_cliente(self, cliente_address, cliente_socket):
        
    #     cliente = cliente_socket
    #     menu = ("      MENU      \n1  - Salas disponíveis\n2 - Criar uma nova sala\n3 - Voltar")
    #     cliente.send(menu.encode('utf8'))
    #     resposta = cliente.recv(1024).decode('utf8')
    #     self.mostrar_menu_servidor(resposta)
    #     while True:
    #         msg = cliente_socket.recv(1024).decode("utf8")
    #         print(f'Mensagem: {cliente_address} ==== {msg}')

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