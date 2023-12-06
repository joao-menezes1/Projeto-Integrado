import dicionario_temas_palavras
from unidecode import unidecode
import random
import re
from lista_circular import *
from fila import *
from funcoes_compartilhadas import *

class Jogo():

    def __init__(self):
        self.jogadores = LinkedList()
        def_compartilha = Compartilha()


    def limpar_entrada(self, entrada):
        entrada_sem_acentos = unidecode(entrada)
        entrada_sem_numeros = re.sub(r'\d+', '', entrada_sem_acentos)
        entrada_apenas_letras = re.sub(r'[^a-zA-Z]', '', entrada_sem_numeros)
        return entrada_apenas_letras

    def __palavra_usuario(self, cliente):
        tema = self.__mostrar_temas()
        def_compartilha.__enviar_msg_cliente(tema, cliente)
        tema_escolhido = def_compartilha.__receber_msg_cliente(cliente)
        palavra = self.__buscar_palavra(tema_escolhido)
        return self.limpar_entrada(palavra)

    def __mostrar_temas(self):
        temas = dicionario_temas_palavras.Temas
        tema_escolhido = ("      TEMAS      \n")
        for tema, array in temas.items():
            tema_escolhido += ('-  ', tema,'\n')
        tema_escolhido + ('-  Digite o tema:')
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
        def_compartilha.__enviar_msg_cliente_broadcast(status, clientes)


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
            def_compartilha.__enviar_msg_cliente('Digite uma letra: ', jogador)
            def_compartilha.__receber_msg_cliente(jogador)
            entrada_limpa = self.limpar_entrada(entrada_usuario.upper())

            if len(entrada_limpa) != 1:
                def_compartilha.__enviar_msg_cliente('Por favor, digite apenas uma letra.', jogador)
                continue

            letra = entrada_limpa

            if fila_letras_erradas.busca(letra) or letra in array_palavra_jogo:
                def_compartilha.__enviar_msg_cliente('Você já tentou essa letra. Tente outra.', jogador)
                continue

            elif letra in palavra:
                palavra_rasurada = self.letras(letra, array_palavra_jogo, palavra)
                def_compartilha.__enviar_msg_cliente(palavra_rasurada, jogador)
                jogador = self.jogadores.advance()
                self.enviar_status_jogo()

            else:
                tentativas += 1
                fila_letras_erradas.enfileirar(letra)
                def_compartilha.__enviar_msg_cliente(f'Letras erradas: {fila_letras_erradas}')
                def_compartilha.__enviar_msg_cliente(f'Tentativas restantes: {tentativas_maximas - tentativas}')

        if '_' not in array_palavra_jogo:
            print('Parabéns! Você acertou a palavra.')
        else:
            print(f'Você perdeu! A palavra era: {" ".join(palavra)}')