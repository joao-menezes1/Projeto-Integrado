import dicionarios
import random


class jogo:
    def  menu():
        print("      MENU      \n1  - Iniciar jogo....")
        input('Digite a sua opção: ')
    
    def mostrar_temas():
        temas = dicionarios.Temas
        for tema, array in temas.items():
            if tema != 'None':
                print(tema + '\n')

    def buscar_palavra():
        for k in range(len(dicionarios.Temas)):
            print(dicionarios.Temas)


print(jogo.mostrar_temas())

# v = dicionarios.Temas
# print(v['frutas'][1])