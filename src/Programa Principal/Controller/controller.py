import sys
import os
from tkinter import colorchooser

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Model.fig import *;from Model.desenho import *
from View.view import *
from Controller.FerramentaState import *

class Controlador():
    
    def __init__(self,desenho,view):
        self.desenho = desenho
        self.view = view
        
        self.cor_linha = "black"
        self.cor_fundo = ""

        self.figura_nova = None
        
        self.ferramenta = FerramentaRetangulo()
        
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
        
        self.menu.bind("<<ComboboxSelected>>", self.mudarFerramenta)
        
    def iniciar_figura(self,event):
        self.ferramenta.click(self,event)
    
    def atualizar_figura(self,event):
        self.ferramenta.arrastar(self,event)
    
    #Aqui é armazenada a figura atual
    def terminar_figura(self, event):
        self.ferramenta.soltar(self, event)
    
    #Função para finalizar o polígono
    def finalizar_poligono(self, event):
        self.ferramenta.botaoDireito(self, event) 
    
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
    
    def mudarFerramenta(self,event = None):
        nome = self.view.detectarFigura()
        if nome == "Retângulo":
            self.ferramenta = FerramentaRetangulo()
        elif nome == "Linha":
            self.ferramenta = FerramentaLinha()
        elif nome == "Polígono":
            self.ferramenta = FerramentaPoligono()
        elif nome == "Rabisco":
            self.ferramenta = FerramentaRabisco()
        elif nome == "Oval":
            self.ferramenta = FerramentaOval()
        elif nome == "Círculo":
            self.ferramenta = FerramentaCirculo()
        
