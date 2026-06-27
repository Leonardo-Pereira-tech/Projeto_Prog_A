import sys
import os
from tkinter import colorchooser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Model.fig import *;from Model.desenho import *
from View.view import *

class Controlador():
    
    def __init__(self,desenho,view):
        self.desenho = desenho
        self.view = view
        
        self.cor_linha = "black"
        self.cor_fundo = ""

        self.figura_nova = None
        
        canvas = self.view.canvas
        botaoBorda = self.view.coresBorda
        botaoPreencher = self.view.coresPreencher
        botaoApagar = self.view.apagar

        canvas.bind("<ButtonPress-1>", self.iniciar_figura)
        canvas.bind("<B1-Motion>", self.atualizar_figura)
        canvas.bind("<Motion>", self.atualizar_figura)  
        canvas.bind("<ButtonRelease-1>", self.terminar_figura)
        canvas.bind("<ButtonPress-3>", self.finalizar_poligono)
        
        botaoBorda.configure(command=self.escolher_Cor_borda)
        botaoPreencher.configure(command=self.escolher_Cor_preenchimento)
        botaoApagar.configure(command=self.deletar)
        
    def iniciar_figura(self,event):
        x1 ,y1 = event.x, event.y
        figura = self.view.detectarFigura()

        # Caso especial se for um polígono sendo desenhado
        if figura == "Polígono" and isinstance(self.figura_nova, Poligono) and not self.figura_nova.finalizado:
            self.figura_nova.adicionar_ponto(event.x, event.y)
            self.view.redesenhar(self.desenho,self.figura_nova)
            self.figura_nova.desenhar(self.view.canvas)
            return
        
        elif figura == "Retângulo":
            self.figura_nova = Retangulo(x1,y1,x1,y1,self.cor_linha,self.cor_fundo)
        elif figura == "Oval":
            self.figura_nova = Oval(x1,y1,x1,y1,self.cor_linha,self.cor_fundo)
        elif figura == "Linha":
            self.figura_nova = Linha(x1,y1,x1,y1,self.cor_linha)
        elif figura == "Rabisco":
            self.figura_nova = Rabisco(x1,y1,self.cor_linha)
        elif figura == "Círculo":
            self.figura_nova = Circulo(x1,y1,x1,y1,self.cor_linha,self.cor_fundo)
        elif figura == "Polígono":
            self.figura_nova = Poligono(x1, y1, self.cor_linha, self.cor_fundo)
    
    def atualizar_figura(self,event):
        # Esse event.state é para o acaso do mouse estiver se movendo solto (0)
        if event.state == 0 and self.view.detectarFigura() != "Polígono":
            return
        
        if self.figura_nova:
            self.figura_nova.atualizar(event.x, event.y)
            self.view.redesenhar(self.desenho,self.figura_nova)
            self.figura_nova.desenhar(self.view.canvas)
    
    #Aqui é armazenada a figura atual
    def terminar_figura(self, event):

        if self.view.detectarFigura() != "Polígono":
            self.desenho.adicionar_figura(self.figura_nova)
            self.figura_nova = None
    
    #Função para finalizar o polígono
    def finalizar_poligono(self, event):
        
        if self.view.detectarFigura() == "Polígono" and isinstance(self.figura_nova, Poligono):
            self.figura_nova.finalizar()
            self.desenho.adicionar_figura(self.figura_nova)
            self.view.redesenhar(self.desenho,self.figura_nova)
            self.figura_nova = None
    
    def escolher_Cor_borda(self): 
        cor = colorchooser.askcolor(title="Selecionar Cor")
        if cor and cor[1]:
            self.cor_linha = cor[1]
            
    def escolher_Cor_preenchimento(self): 
        cor = colorchooser.askcolor(title="Selecionar Cor para preencher")
        if cor and cor[1]:
            self.cor_fundo = cor[1]
            
    def deletar(self):
        
        self.cor_linha, self.cor_fundo = "black",""
        self.view.canvas.delete("all")
        self.desenho.limpar()
            