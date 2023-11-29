import dicionario_temas_palavras
import random


class jogo:
    def  __menu(self):
        print("      MENU      \n1  - Iniciar jogo....")
        input('Digite a sua opção: ')
    
    def __palavra_usuario(self):
        tema = self.__mostrar_temas()
        palavra = self.__buscar_palavra(tema)
        print(palavra)


    def __mostrar_temas(self):
        temas = dicionario_temas_palavras.Temas
        print("      TEMAS      \n")
        for tema, array in temas.items():
            if tema != 'None':
                print("- ",tema)
        
        Tema_escolhido = input("Digite o tema escolhido: ")
        return Tema_escolhido


    def __buscar_palavra(self, Tema_escolhido):
        Palavras_tema = dicionario_temas_palavras.Temas.get(Tema_escolhido)
        Palavra_aleatoria_escolhida = Palavras_tema[random.randint(0, 11)]

        return Palavra_aleatoria_escolhida
    
    def letras(self, letra, array_palavra_jogo, palavra):
        for let in array_palavra_jogo:
            if letra != let:
                array_palavra_jogo[let] = '_'
        print(array_palavra_jogo)

        
    def __iniciar_jogo(self):
        menu = self.__menu()
        palavra = self.__palavra_usuario()
        print("Palavra já escolhida")
        array_letras_escolhidas = []
        letra = input('Digite uma letra: ')
        array_palavra_jogo = palavra.slipt()
        self.letras(letra, array_palavra_jogo, palavra)
        







        

