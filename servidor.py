import socket
import hashtable
import threading
import random

HOST = '192.168.0.85'
PORT = 10000

print('=== Servidor ===')

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
orig = (HOST, PORT)

udp.bind(orig)

while True:
    frutas = hashtable.dicionario['frutas']
    fruta = frutas[random.randint(0, len(frutas))]
    msg, cliente = udp.recvfrom(1024)
    print('Recebi de', cliente, 'a mensagem', msg.decode(encoding="utf-8"))
    resposta = fruta
    udp.sendto(resposta.encode(), cliente)

    # posiçoes = ['b',"a","n","a","n","a"]
    # resultado = ' '.join(posiçoes)

    # for i in range (len(fruta.slip())):
    #     if msg == fruta[i]:
    #         posiçoes.append(fruta[i])
    #     else:
    #         posiçoes.append('_')
    
