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
    
    def tirarLados(self, controlador, event):
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
        if controlador.figura_nova:
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
class FerramentaPoligonoRegular(FerramentaState):
    def click(self, controlador, event):
        clickCtrl = bool(event.state & 0x0004) #detecta se o shift foi pressionado
        if not controlador.figura_nova:
            controlador.figura_nova = PoligonosRegulares(event.x,event.y, controlador.cor_linha,controlador.cor_fundo,controlador.espessura_linha)
        elif(clickCtrl):
            controlador.figura_nova.tirar_lado()
            controlador.view.redesenhar(controlador.desenho, controlador.figura_nova)
        else:
            controlador.figura_nova.adicionar_lado()
            controlador.view.redesenhar(controlador.desenho, controlador.figura_nova)
        
    def arrastar(self, controlador, event):
        if controlador.figura_nova:
            controlador.figura_nova.atualizar(event.x,event.y)
            controlador.view.redesenhar(controlador.desenho, controlador.figura_nova)
    def soltar(self,controlador, event):
        pass
    def botaoDireito(self,controlador, event):
        if controlador.figura_nova:
            controlador.figura_nova.finalizar()
            controlador.desenho.adicionar_figura(controlador.figura_nova)
            controlador.view.redesenhar(controlador.desenho, controlador.figura_nova)
            controlador.figura_nova = None
   
    
    
            
class FerramentaSelecionar(FerramentaState):
    def click(self, controlador, event):
        clickCtrl = bool(event.state & 0x0004) #detecta se o shift foi pressionado
        figuraSelecionada = controlador.desenho.selecionar_figura(event.x,event.y) #Descobre qual figura foi selecionada
        if not clickCtrl:
            if figuraSelecionada is None or figuraSelecionada not in controlador.figuras_selecionadas: # para não resetar o quadrado e mover apenas uma figura
                for figura in controlador.figuras_selecionadas:
                    figura.selecionada = False 
                controlador.figuras_selecionadas = []

        if figuraSelecionada:
            if clickCtrl and figuraSelecionada in controlador.figuras_selecionadas: #Saber que so irá alterar as figuras selecionadas
                figuraSelecionada.selecionada = False
                controlador.figuras_selecionadas.remove(figuraSelecionada)
            
            else:
                figuraSelecionada.selecionada = True
                if figuraSelecionada not in controlador.figuras_selecionadas: #Saber se está implementando mais figuras além das que ja foram selecionadas
                    controlador.figuras_selecionadas.append(figuraSelecionada)
                
            controlador.clickX = event.x
            controlador.clickY = event.y
            controlador.caixa_selecao = False # Caso clicou em uma figura não aciona a caixa
            controlador.view.canvas.focus_set()

        else:
            controlador.clickX = event.x
            controlador.clickY = event.y
            controlador.caixa_selecao = True # clicou na figura, aciona a caixa

        controlador.view.redesenhar(controlador.desenho, None)

    def arrastar(self, controlador, event):
        if not controlador.caixa_selecao:
            if controlador.clickX != None and controlador.clickY != None: # Sistema não dar erro quando parar de selecionar
                deltaX = event.x - controlador.clickX # atualizar em tempo real e garantir que não vai deformar a figura
                deltaY = event.y - controlador.clickY

                for figuras in controlador.figuras_selecionadas:
                    if figuras:
                        figuras.mover(deltaX,deltaY) # Definição no model para mexer

                controlador.clickX = event.x
                controlador.clickY = event.y
            controlador.view.redesenhar(controlador.desenho,None) # Não fazer a figura dar um teleporte, e sim atualizar o movimento flúido
        else:
            controlador.view.redesenhar(controlador.desenho,None) # Não lembro para o que servia, apagando ele funciona, mas antes sem isso o retângulo não aparecia
       
            if controlador.retangulo_selecao is not None:
                controlador.view.canvas.delete(controlador.retangulo_selecao) # Apaga o retangulo antigo, quando já fora criado
    
            controlador.retangulo_selecao = controlador.view.canvas.create_rectangle(controlador.clickX,controlador.clickY,event.x,event.y,dash=(4,4),outline='blue',fill="") # criador visual do retângulo
             
    def soltar(self, controlador, event):
        if controlador.caixa_selecao:
            x_min = min(controlador.clickX, event.x) # Esses métodos são para identificar as bordas e posteriormente saber se as figuras estão dentro 
            x_max = max(controlador.clickX, event.x)
            y_min = min(controlador.clickY, event.y)
            y_max = max(controlador.clickY, event.y)

            for figura in controlador.desenho.obter_figuras():
                figX, figY = figura.obter_pontos() # Método novo do fig para capturar os pontos das figuras(Rabisco e polígono tive que colocar como se fosse matriz)
                if x_min <= figX <= x_max and y_min <= figY <= y_max: # compara as tuplas e vê se estão dentro do quadrado <---- Bem aqui o comentario do max e min
                    figura.selecionada = True

                    if figura not in controlador.figuras_selecionadas:
                        controlador.figuras_selecionadas.append(figura)

            if controlador.retangulo_selecao is not None:
                controlador.view.canvas.delete(controlador.retangulo_selecao)
                controlador.retangulo_selecao = None
            
        controlador.clickX = None # Reset no valor quando parar de soltar (E fazer com que pare de seguir o mouse)
        controlador.clickY = None
        controlador.caixa_selecao = False
        controlador.view.canvas.focus_set()
        controlador.view.redesenhar(controlador.desenho,None) # Mostra as figuras selecionadas