import socket
import sys
import numpy as np
from comum import Jogador 

def printarTabuleiro(tabuleiro):
    for i in range(9):
        if(tabuleiro[i] == 0):
            print('| X |', end='')
        elif(tabuleiro[i] == 1):
            print('| O |', end='')
        else:
            print('|', i, '|', end='')
        if((i+1)%3==0):
            print()

def main():
     
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1',50000))

    j = Jogador(sock)
    
    msg = j.socket.recv(2)
    if not msg:
        print('Erro - desconexão')
        sys.exit(-1)

    codigo = int.from_bytes(msg[0:1], 'big')
    id = int.from_bytes(msg[1:2], 'big')
    j.id = id
    print(f"Conectado como jogador {j.id}")

    #Inciciando Tabuleiro vazio
    tabuleiro = np.full(9, -1)

    partidaEncerrada = False
    
    while not partidaEncerrada:

        msg = j.socket.recv(1)
        if not msg:
            print('Desconexão')
            sys.exit(-1)

        codigo = int.from_bytes(msg, 'big')

        match codigo:
            #Escolher uma posição para jogar
            case 0:
                printarTabuleiro(tabuleiro)
                while(True):
                    try:
                        posicao = int(input("Escolha a posicao que deseja jogar: "))
                        if(tabuleiro[posicao] == -1 and (posicao >= 0) and (posicao <= 8)):
                            break
                    except:
                        print("Entrada inválida")
                
                tabuleiro[posicao] = j.id
                msg = int.to_bytes(posicao, 1, 'big')
                j.socket.send(msg)

            #case 1: Iniciador

            #Informa o vencedor do jogo
            case 2:
                vencedorJogo = int.from_bytes(j.socket.recv(1), 'big')
                print()
                if(vencedorJogo == 2):
                    print("------")
                    print("Empate")
                    print("------")
                elif(vencedorJogo == j.id):
                    print("---gg-izi---")
                    print('Você venceu')
                    print("-----------")
                else:
                    print("---loser---")
                    print('Você perdeu')
                    print("-----------")
                partidaEncerrada = True
            
            #Atualizar tabuleiro
            case 3:
                posicao = int.from_bytes(j.socket.recv(1), 'big')
                tabuleiro[posicao] = (j.id + 1)%2

            #Mensagem de erro
            case 4:
                tam = int.from_bytes(j.socket.recv(1), 'big')
                mensagem = j.socket.recv(tam).decode()
                print('Mensagem do servidor: ', mensagem)

    
if __name__ == '__main__':
    main()