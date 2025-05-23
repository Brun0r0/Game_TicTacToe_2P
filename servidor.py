from comum import Jogador
from tkinter import *
import socket
import numpy as np
import sys

#tipos de mensagem e formato
# 0 - pedido do servidor para o cliente, qual posição do tabuleiro ele deseja preencher
    ### Requisição: 1 byte para id de operação
    ### Resposta : 1 byte para posicao jogada no tabuleiro
# 1 - iniciador, indica o ID do jogador
    ### Requisição: 1 byte para id de operação
    ###             1 byte para posicao jogada no tabuleiro
# 2 - vencedor do jogo
    ### Requisição: 1 byte para id de operação
    ###             1 byte para identificar vencedor (valor 2 para empate)
# 3 - atualização de tabuleiro
    ### Requisição: 1 byte para id de operação
    ###             1 byte para posicao jogada no tabuleiro
# 4 - mensagem de erro - 1 byte para código, 1 byte para tamanho da mensagem, mensagem
    ### Requisição: 1 byte para id de operação
    ###             1 byte para tamanho da mensagem
    ###             mensagem
    
def verificaVitoria(tabuleiro):
    for i in range(3):
        #linhas
        if(tabuleiro[3*i] == tabuleiro[(3*i)+1] and tabuleiro[3*i] == tabuleiro[(3*i)+2] and tabuleiro[3*i] != -1):
            return True
        #colunas
        if(tabuleiro[i] == tabuleiro[i+3] and tabuleiro[i] == tabuleiro[i+6] and tabuleiro[i] != -1):
            return True
    #diagonais
    if(tabuleiro[0] == tabuleiro[4] and tabuleiro[4] == tabuleiro[8] and tabuleiro[4] != -1):
        return True
    if(tabuleiro[2] == tabuleiro[4] and tabuleiro[4] == tabuleiro[6] and tabuleiro[4] != -1):
        return True
    
    return False

def main():

    socket_conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    endereco = ('',50000)
    socket_conexao.bind(endereco)
    socket_conexao.listen(2)
    jogadores = []

    while len(jogadores) < 2:
        socket_jogador, _ = socket_conexao.accept()
        j = Jogador(socket_jogador)
        jogadores.append(j)

    # enviar uma mensagem dizendo o ID do jogador
    for i in range(2):
        msg = int.to_bytes(1,1,'big') + int.to_bytes(i,1,'big')
        jogadores[i].socket.send(msg)   

    #Tabuleiro vazio
    tabuleiro = np.full(9, -1)

    jogoTerminado = False
    jogadorAtual = 0
    cont = 0
    resultado = -1


    while(jogoTerminado == False):

        msg = int.to_bytes(0, 1, 'big')
        jogadores[jogadorAtual].socket.send(msg)

        jogada = int(int.from_bytes(jogadores[jogadorAtual].socket.recv(1), 'big'))

        tabuleiro[jogada] = jogadorAtual

        cont = cont+1

        jogoTerminado = verificaVitoria(tabuleiro)

        if(jogoTerminado):
            resultado = jogadorAtual
        elif(cont == 9):
            resultado = 2

        if(resultado != -1):
            msg = int.to_bytes(2, 1, 'big') + int.to_bytes(resultado, 1, 'big')
            jogadores[jogadorAtual].socket.send(msg)
            jogadores[(jogadorAtual+1)%2].socket.send(msg)
        else:
            jogadorAtual = (jogadorAtual + 1)%2

            #Mensagem para outro jogador informando posição ja preenchida
            msg = int.to_bytes(3, 1, 'big') + int.to_bytes(jogada, 1, 'big')
            jogadores[jogadorAtual].socket.send(msg)
                
            
if __name__ == '__main__':
    main()