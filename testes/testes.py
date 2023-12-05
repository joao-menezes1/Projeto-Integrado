import multiprocessing

def minha_funcao(numero):
    print(f'Número: {numero}')

if __name__ == "__main__":
    # Criação de um processo
    processo = multiprocessing.Process(target=minha_funcao, args=(10,))
    
    # Inicia o processo
    processo.start()
    
    # Espera o processo terminar
    processo.join()