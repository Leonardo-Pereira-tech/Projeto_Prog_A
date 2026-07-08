
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
            
    