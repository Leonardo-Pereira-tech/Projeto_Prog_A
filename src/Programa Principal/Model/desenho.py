
from abc import ABC, abstractmethod
from tkinter import *


class Desenho():
    
    def __init__(self):
        self.figuras = []
    
    def adicionar_figura(self,figura):
        self.figuras.append(figura)
    
    def limpar(self):
        self.figuras.clear()

    def obter_figuras(self):
        return self.figuras
    
    def selecionar_figura(self,x, y):
        for figura in reversed(self.figuras):
            if figura.contem(x,y):
                return figura
    
    def mover_frente(self, figura):
        indice = self.figuras.index(figura)
        if indice < len(self.figuras)-1:
            self.figuras[indice], self.figuras[indice+1] = (
                self.figuras[indice+1],
                self.figuras[indice]
            )

    def mover_atras(self, figura):
        indice = self.figuras.index(figura)
        if indice > 0:
            self.figuras[indice], self.figuras[indice-1] = (
                self.figuras[indice-1],
                self.figuras[indice]
            )

    def mover_topo(self, figura):
        self.figuras.remove(figura)
        self.figuras.append(figura)

    def mover_fundo(self, figura):
        self.figuras.remove(figura)
        self.figuras.insert(0, figura)