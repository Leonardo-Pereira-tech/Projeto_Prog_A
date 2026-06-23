import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tkinter import *
from tkinter import ttk 
from tkinter import colorchooser
from Model.fig import *;from Model.desenho import *
from Controller.controller import *


class canvasView:
    def __init__(self,janela):
        self.janela = janela
        self.janela.title("Entrega_Principal")

        self.frame = ttk.Frame(self.janela)
        self.lbl = ttk.Label(self.frame,text="Escolher Tipo de Desenho");self.lbl.pack(side=LEFT)
        self.tipo_figura = StringVar(value="Retângulo")
        self.menu = ttk.Combobox(self.frame,textvariable=self.tipo_figura,values=["Retângulo","Círculo","Oval","Linha", "Rabisco","Polígono"]);self.menu.pack(side=RIGHT,padx=5) 
        self.menu.configure(state="readonly")
        self.frame.pack(fill=X)      
        
        self.separador = ttk.Separator(self.frame,orient="vertical")
        self.separador.pack(side=LEFT, fill=Y,padx=10)

        self.coresBorda = ttk.Button(self.frame,text="Escolher Borda",command=None)#substituir comando quando controller tiver pronto
        self.coresBorda.pack(side=LEFT,padx=5)
        self.coresPreencher = ttk.Button(self.frame,text="Preencher figura",command=None)
        self.coresPreencher.pack(side=LEFT,padx=5)

        self.estiloBotao = ttk.Style()
        self.estiloBotao.configure("botãoApagar.TButton",foreground="Red",background="red")
        self.apagar = ttk.Button(self.frame, text="Resetar", command=None, style="botãoApagar.TButton")
        self.apagar.pack(side=RIGHT,padx=20)

        self.canvas = Canvas(janela, width= 600, height= 600,bg ="white" )
        self.canvas.pack(pady=10, padx= 10,fill=BOTH)
        
    def redesenhar(self,listaFiguras,figuraAtual):
        #interge com model, mas nao tem problema
        self.canvas.delete("all")
        for figura in listaFiguras.obter_figuras():
            figura.desenhar(self.canvas)
        if figuraAtual:
            figuraAtual.desenhar(self.canvas)
    
    def detectarFigura(self):
        return self.tipo_figura.get()
    
    def corBorda(self,comandoController):
        if comandoController:
            self.coresBorda.configure(command=comandoController)

    def corPreenchimento(self,comandoController):
        if comandoController:
            self.coresPreencher.configure(command=comandoController)
    
    def apagarDesenho(self,comandoController):
        if comandoController:
            self.apagar.configure(command=comandoController)
    
    def inicioDesenho(self,comandoController):
        if comandoController:
            self.canvas.bind("<ButtonPress-1>", comandoController)   
    
    def atualizarDesenho(self,comandoController):
        if comandoController:
            self.canvas.bind("<B1-Motion>", comandoController)  
    
    def atualizarDesenhoPolígono(self,comandoController):
        if comandoController:
            self.canvas.bind("<Motion>", comandoController)
    
    def terminarDesenho(self,comandoController):
        if comandoController:
            self.canvas.bind("<ButtonRelease-1>", comandoController)

    def terminarPoligono(self,comandoController):
        if comandoController:
            self.canvas.bind("<ButtonPress-3>", comandoController)
    def obterCanvas(self):
        return self.canvas
    def obterJanela(self):
        return self.janela