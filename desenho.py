
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
        if figura:
            indice = self.figuras.index(figura)
            if indice < len(self.figuras)-1:
                self.figuras[indice], self.figuras[indice+1] = (
                    self.figuras[indice+1],
                    self.figuras[indice]
                )
            

    def mover_atras(self, figura):
        if(figura):
            indice = self.figuras.index(figura)
            if indice > 0:
                self.figuras[indice], self.figuras[indice-1] = (
                    self.figuras[indice-1],
                    self.figuras[indice]
                )
            

    def mover_topo(self, figura):
        if(figura):
            self.figuras.remove(figura)
            self.figuras.append(figura)
            

    def mover_fundo(self, figura):
        if(figura):
            self.figuras.remove(figura)
            self.figuras.insert(0, figura)
            
    
    def Copiar(self, figura):
        if figura:
            return figura.copiar()
        
    def colar(self, figura):
        if figura:
            nova = figura.copiar()
            nova.mover(20,20)
            self.adicionar_figura(nova)
            return nova

    def apagar_desenho(self,figura):
        if figura:
            self.figuras.remove(figura)
            figura = None
            return figura
