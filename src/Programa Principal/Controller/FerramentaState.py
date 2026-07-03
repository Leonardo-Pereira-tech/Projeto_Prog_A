import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Model.fig import *;from Model.desenho import *
from View.view import *
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
        self.controlador = controlador
        x1,y1 = event.x, event.y
        self.controlador.figura_nova = Retangulo(x1,y1,x1,y1,self.controlador.cor_linha,self.controlador.cor_fundo)

    def arrastar(self,controlador,event):
        self.controlador = controlador
        if self.controlador.figura_nova:
            self.controlador.figura_nova.atualizar(event.x,event.y)
            self.controlador.figura_nova.redesenhar(self.controlador.view.canvas,self.controlador.figura_nova)
            
    def soltar(self,controlador,event):
        self.controlador = controlador
        if controlador.figura_nova:
            self.controlador.desenho.adicionar_figura(self.controlador.figura_nova)
            self.controlador.figura_nova = None
            
class FerramentaLinha(FerramentaState):
    
    def click(self,controlador,event):
        self.controlador = controlador
        x1,y1 = event.x,event.y
        self.controlador.figura_nova = Linha(x1,y1,x1,y1,self.controlador.cor_linha)
    
    def arrastar(self,controlador,event):
        self.controlador = controlador
        
        if self.controlador.figura_nova:
            self.controlador.figura_nova.atualizar(event.x,event.y)
            self.controlador.figura_nova.redesenhar(self.controlador.view.canvas,self.controlador.figura_nova)
            
    def soltar(self,controlador,event):
        self.controlador = controlador
        if controlador.figura_nova:
            self.controlador.desenho.adicionar_figura(self.controlador.figura_nova)
            self.controlador.figura_nova = None