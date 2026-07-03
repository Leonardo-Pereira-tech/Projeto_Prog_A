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
        
        self.ferramenta_atual = FerramentaRetangulo()

        canvas = self.view.canvas
        botaoBorda = self.view.coresBorda
        botaoPreencher = self.view.coresPreencher
        botaoApagar = self.view.apagar

        canvas.bind("<ButtonPress-1>", self.clickMouse)
        canvas.bind("<B1-Motion>", self.arrastarMouse)
        canvas.bind("<Motion>", self.arrastarMouse)  
        canvas.bind("<ButtonRelease-1>", self.soltarMouse)
        canvas.bind("<ButtonPress-3>", self.botaoDireito)

        

        botaoBorda.configure(command=self.escolher_Cor_borda)
        botaoPreencher.configure(command=self.escolher_Cor_preenchimento)
        botaoApagar.configure(command=self.deletar)
        
        
    def clickMouse(self, event):
        self.mudarFerramenta(self.view.detectarFigura())

        self.ferramenta_atual.click(self, event)
    
    def arrastarMouse(self, event):
        self.ferramenta_atual.arrastar(self, event)
    
    def soltarMouse(self, event):
        self.ferramenta_atual.soltar(self, event)

    def botaoDireito(self, event):
        self.ferramenta_atual.botaoDireito(self, event)

    def mudarFerramenta(self, nome):
        
        if nome == "Linha":
            self.ferramenta_atual = FerramentaLinha()
        elif nome == "Retângulo":
            self.ferramenta_atual = FerramentaRetangulo()
        elif nome == "Oval":
            self.ferramenta_atual = FerramentaOval()
        elif nome == "Rabisco":
            self.ferramenta_atual = FerramentaRabisco()
        elif nome == "Polígono":
            self.ferramenta_atual = FerramentaPoligono()
        elif nome == "Círculo":
            self.ferramenta_atual = FerramentaCirculo()

        # E assim por diante
    
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
            