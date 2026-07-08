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
        controlador.figura_nova = Retangulo(x1,y1,x1,y1,controlador.cor_linha,controlador.cor_fundo,controlador.espessura_linha)

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
        controlador.figura_nova = Linha(x1,y1,x1,y1,controlador.cor_linha,controlador.espessura_linha)
    
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
            controlador.figura_nova = Poligono(event.x, event.y, controlador.cor_linha, controlador.cor_fundo,controlador.espessura_linha)
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
        controlador.figura_nova = Rabisco(event.x, event.y, controlador.cor_linha,controlador.espessura_linha)
    
    def arrastar(self, controlador, event):
        if controlador.figura_nova:
            controlador.figura_nova.atualizar(event.x,event.y)
            controlador.view.redesenhar(controlador.desenho, controlador.figura_nova)
    
    def soltar(self, controlador, event):
        controlador.desenho.adicionar_figura(controlador.figura_nova)
        controlador.figura_nova = None
        
class FerramentaCirculo(FerramentaState):
    
    def click(self, controlador, event):
        controlador.figura_nova = Circulo(event.x, event.y, event.x, event.y, controlador.cor_linha, controlador.cor_fundo,controlador.espessura_linha)
        
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
        controlador.figura_nova = Oval(x1, y1, x1, y1, controlador.cor_linha, controlador.cor_fundo,controlador.espessura_linha)

    def arrastar(self, controlador, event):
        if controlador.figura_nova:
            controlador.figura_nova.atualizar(event.x, event.y)
            controlador.view.redesenhar(controlador.desenho, controlador.figura_nova)
            controlador.figura_nova.desenhar(controlador.view.canvas)

    def soltar(self, controlador, event):
        if controlador.figura_nova:
            controlador.desenho.adicionar_figura(controlador.figura_nova)
            controlador.figura_nova = None
            
class FerramentaSelecionar(FerramentaState):
    def click(self, controlador, event):
        if controlador.figura_selecionada:
            controlador.figura_selecionada.selecionada = False
            
        controlador.figura_selecionada = controlador.desenho.selecionar_figura(event.x,event.y)

        if controlador.figura_selecionada:
            controlador.figura_selecionada.selecionada = True
            controlador.clickX = event.x
            controlador.clickY = event.y
            controlador.view.canvas.focus_set()

        controlador.view.redesenhar(controlador.desenho, None)

    def arrastar(self, controlador, event):
        if controlador.figura_selecionada and (controlador.clickX != None and controlador.clickY != None): # Sistema não dar erro quando parar de selecionar
            deltaX = event.x - controlador.clickX # atualizar em tempo real e garantir que não vai deformar a figura
            deltaY = event.y - controlador.clickY
            
            controlador.figura_selecionada.mover(deltaX,deltaY) # Definição no model para mexer
            controlador.clickX = event.x
            controlador.clickY = event.y

            controlador.view.redesenhar(controlador.desenho,None) #Atualizar o canvas com a mudança
            
    def soltar(self, controlador, event):
        controlador.clickX = None # Reset no valor quando parar de soltar (E fazer com que pare de seguir o mouse)
        controlador.clickY = None 