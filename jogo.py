import numpy as np
from tkinter import *

class GameInterface:
    def __init__(self):
        self.janela = Tk()
        self.janela.title("Jogo da Velha")
        self.botoes = np.zeros((3, 3), dtype=object)
        self.jogador_atual = "X"

        for i in range(3):
            for j in range(3):
                self.botoes[i][j] = Button(self.janela, text=" ", width=10, height=4,
                                           command=lambda i=i, j=j: self.cliq(i, j))
                self.botoes[i][j].grid(row=i, column=j)

        self.janela.mainloop()

    def cliq(self, i, j):
        if self.botoes[i][j]['text'] != " ":
            return
        
        self.botoes[i][j]['text'] = self.jogador_atual

        if self.vitoria():
            print(f"Jogador {self.jogador_atual} ganhou!")
            self.desabilitar_botoes()
            self.janela.after(1000, self.reiniciar_jogo)
            return

        if self.tabuleiro_cheio():
            print("Empate!")
            self.janela.after(1500, self.reiniciar_jogo)
            return

        self.jogador_atual = "O" if self.jogador_atual == "X" else "X"

    def vitoria(self):
        for i in range(3):  # linha
            if all(self.botoes[i][j]['text'] == self.botoes[i][0]['text'] and self.botoes[i][0]['text'] != " " for j in range(3)):
                return True

        for j in range(3):  # coluna
            if all(self.botoes[i][j]['text'] == self.botoes[0][j]['text'] and self.botoes[0][j]['text'] != " " for i in range(3)):
                return True

        if (self.botoes[0][0]['text'] == self.botoes[1][1]['text'] == self.botoes[2][2]['text']) and self.botoes[0][0]['text'] != " ":
            return True

        if (self.botoes[0][2]['text'] == self.botoes[1][1]['text'] == self.botoes[2][0]['text']) and self.botoes[2][0]['text'] != " ":
            return True

        return False

    def tabuleiro_cheio(self):
        return all(self.botoes[i][j]['text'] != " " for i in range(3) for j in range(3))

    def desabilitar_botoes(self):
        for i in range(3):
            for j in range(3):
                self.botoes[i][j]['state'] = 'disabled'

    def reiniciar_jogo(self):
        for i in range(3):
            for j in range(3):
                self.botoes[i][j]['text'] = " "
                self.botoes[i][j]['state'] = 'normal'
        self.jogador_atual = "X"

interface = GameInterface()
