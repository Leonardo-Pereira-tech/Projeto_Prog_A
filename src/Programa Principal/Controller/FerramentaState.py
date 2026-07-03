import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Model.fig import *;from Model.desenho import *
from View.view import *
from Controller.controller import *
from abc import ABC, abstractmethod

class FerramentaState(ABC):
    
    @abstractmethod
    def click(self,controlador,event):
        pass
    
    @abstractmethod
    def arrastar(self,controlador,event):
        pass
    
    @abstractmethod
    def soltar(self,controlador,event):
        pass
    
class FerramentaRetangulo(FerramentaState):
    
    def click(self,controlador,event):
        x1,y1 = event.x, event.y
        controlador.figura_nova = Retangulo(x1,y1,x1,y1,controlador.cor_linha,controlador.cor_fundo)

    def arrastar(self,controlador,event):
        if controlador.figura_nova:
            controlador.figura_nova.atualizar(event.x,event.y)
            controlador.view.redesenhar(controlador.desenho, controlador.figura_nova)
            
    def soltar(self,controlador,event):
        if controlador.figura_nova:
            controlador.desenho.adicionar_figura(controlador.figura_nova)
            controlador.figura_nova = None
            
class FerramentaLinha(FerramentaState):
    
    def click(self,controlador,event):
        x1,y1 = event.x,event.y
        controlador.figura_nova = Linha(x1,y1,x1,y1,controlador.cor_linha)
    
    def arrastar(self,controlador,event):
        if controlador.figura_nova:
            
            controlador.figura_nova.atualizar(event.x,event.y)
            controlador.view.redesenhar(controlador.desenho, controlador.figura_nova)
            
    def soltar(self,controlador,event):
        controlador.desenho.adicionar_figura(controlador.figura_nova)
        controlador.figura_nova = None

class FerramentaPoligono(FerramentaState):
    
    def click(self, controlador, event):
        if not controlador.figura_nova:
            controlador.figura_nova = Poligono(event.x, event.y, controlador.cor_linha, controlador.cor_fundo)
        else:
            controlador.figura_nova.adicionar_ponto(event.x,event.y)
            controlador.view.redesenhar(controlador.desenho, controlador.figura_nova)
    def arrastar(self, controlador, event):
        if controlador.figura_nova:

            controlador.figura_nova.atualizar(event.x,event.y)
            controlador.view.redesenhar(controlador.desenho, controlador.figura_nova)
            
    def soltar(self, controlador, event):
        pass
    
    def botaoDireito(self, controlador, event):
        controlador.figura_nova.finalizar()
        controlador.desenho.adicionar_figura(controlador.figura_nova)
        controlador.view.redesenhar(controlador.desenho, controlador.figura_nova)
        controlador.figura_nova = None

class FerramentaRabisco(FerramentaState):
    
    def click(self, controlador, event):
        controlador.figura_nova = Rabisco(event.x, event.y, controlador.cor_linha)
    
    def arrastar(self, controlador, event):
        if controlador.figura_nova:
            controlador.figura_nova.atualizar(event.x,event.y)
            controlador.view.redesenhar(controlador.desenho, controlador.figura_nova)
    
    def soltar(self, controlador, event):
        controlador.desenho.adicionar_figura(controlador.figura_nova)
        controlador.figura_nova = None
        
class FerramentaCirculo(FerramentaState):
    
    def click(self, controlador, event):
        controlador.figura_nova = Circulo(event.x, event.y, event.x, event.y, controlador.cor_linha, controlador.cor_fundo)
        
    def arrastar(self, controlador, event):
        if controlador.figura_nova:
            controlador.figura_nova.atualizar(event.x,event.y)
            controlador.view.redesenhar(controlador.desenho, controlador.figura_nova)
    def soltar(self, controlador, event):
        
        controlador.desenho.adicionar_figura(controlador.figura_nova)
        controlador.figura_nova = None
        
class FerramentaOval(FerramentaState):
    def click(self, controlador, event):
        x1, y1 = event.x, event.y
        controlador.figura_nova = Oval(x1, y1, x1, y1, controlador.cor_linha, controlador.cor_fundo)

    def arrastar(self, controlador, event):
        if controlador.figura_nova:
            controlador.figura_nova.atualizar(event.x, event.y)
            controlador.view.redesenhar(controlador.desenho, controlador.figura_nova)
            controlador.figura_nova.desenhar(controlador.view.canvas)

    def soltar(self, controlador, event):
        if controlador.figura_nova:
            controlador.desenho.adicionar_figura(controlador.figura_nova)
            controlador.figura_nova = None
            

