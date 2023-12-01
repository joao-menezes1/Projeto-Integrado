import dicionario_temas_palavras
from unidecode import unidecode
import random
import re
from fila import *

class Jogo:
    # ... (código anterior)

    def limpar_entrada(self, entrada):
        entrada_sem_acentos = unidecode(entrada)
        entrada_sem_numeros = re.sub(r'\d+', '', entrada_sem_acentos)
        entrada_apenas_letras = re.sub(r'[^a-zA-Z]', '', entrada_sem_numeros)
        return entrada_apenas_letras

    def __menu(self):
        print("      MENU      \n1  - Iniciar jogo....")
        return input('Digite a sua opção: ')

    def __palavra_usuario(self):
        tema = self.__mostrar_temas()
        palavra = self.__buscar_palavra(tema)
        return self.limpar_entrada(palavra)

    def __mostrar_temas(self):
        temas = dicionario_temas_palavras.Temas
        print("      TEMAS      \n")
        for tema, array in temas.items():
            if tema != 'None':
                print("- ", tema)

        tema_escolhido = input("Digite o tema escolhido: ")
        return tema_escolhido

    def __buscar_palavra(self, tema_escolhido):
        palavras_tema = dicionario_temas_palavras.Temas.get(tema_escolhido)
        palavra_aleatoria_escolhida = random.choice(palavras_tema)
        return palavra_aleatoria_escolhida

    def letras(self, letra, array_palavra_jogo, palavra):
        for i, let in enumerate(palavra):
            if letra == let:
                array_palavra_jogo[i] = letra
        print(' '.join(array_palavra_jogo))

    def _iniciar_jogo(self):
        tentativas_maximas = 6
        palavra = list(self.__palavra_usuario().upper())
        array_palavra_jogo = ['_'] * len(palavra)
        fila_letras_erradas = Fila()
        tentativas = 0

        while '_' in array_palavra_jogo and tentativas < tentativas_maximas:
            entrada_usuario = input('Digite uma letra: ')
            entrada_limpa = self.limpar_entrada(entrada_usuario.upper())

            if len(entrada_limpa) != 1:
                print('Por favor, digite apenas uma letra.')
                continue

            letra = entrada_limpa

            if fila_letras_erradas.busca(letra) or letra in array_palavra_jogo:
                print('Você já tentou essa letra. Tente outra.')

            elif letra in palavra:
                self.letras(letra, array_palavra_jogo, palavra)

            else:
                tentativas += 1
                fila_letras_erradas.enfileirar(letra)
                print(f'Letras erradas: {fila_letras_erradas}')
                print(f'Tentativas restantes: {tentativas_maximas - tentativas}')

        if '_' not in array_palavra_jogo:
            print('Parabéns! Você acertou a palavra.')
        else:
            print(f'Você perdeu! A palavra era: {" ".join(palavra)}')

# Criando uma instância do jogo
jogo_instancia = Jogo()
jogo_instancia._iniciar_jogo()
