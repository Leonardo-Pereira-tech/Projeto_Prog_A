import sys
import os
from tkinter import colorchooser,filedialog
from PIL import ImageGrab
import pickle

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
        
        self.ferramenta_atual = FerramentaLinha()
    
        canvas = self.view.canvas
        botaoBorda = self.view.coresBorda
        botaoPreencher = self.view.coresPreencher
        botaoApagar = self.view.apagar
        botaoPrintar = self.view.printar
        botaoAbrir = self.view.abrir
        botaoSalvarProjeto = self.view.salvar
        
        canvas.bind("<ButtonPress-1>", self.clickMouse)
        canvas.bind("<B1-Motion>", self.arrastarMouse)
        canvas.bind("<Motion>", self.arrastarMouse)  
        canvas.bind("<ButtonRelease-1>", self.soltarMouse)
        canvas.bind("<ButtonPress-3>", self.finalizar_poligono)
        
        botaoBorda.configure(command=self.escolher_Cor_borda)
        botaoPreencher.configure(command=self.escolher_Cor_preenchimento)
        botaoApagar.configure(command=self.deletar)
<<<<<<< Updated upstream
    
=======
        botaoPrintar.configure(command=self.printar_imagem)
        botaoAbrir.configure(command=self.abrir_imagem)
        botaoSalvarProjeto.configure(command=self.salvar_projeto)

        self.view.menu.bind("<<ComboboxSelected>>", self.mudarFerramenta)
        
>>>>>>> Stashed changes
    def clickMouse(self,event):
        self.ferramenta_atual.click(self,event)
    
    def arrastarMouse(self,event):
        self.ferramenta_atual.arrastar(self,event)
    
    def soltarMouse(self,event):
        self.ferramenta_atual.soltar(self,event)
        
    def mudarFerramenta(self,nome):
        if nome == "Linha":
            self.ferramenta_atual = FerramentaLinha()
        elif nome == "Retangulo":
            self.ferramenta_atual = FerramentaRetangulo()
        # E assim por diante...
        

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
<<<<<<< Updated upstream
            
=======
    
    def mudarFerramenta(self,nome , event = None):
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
        
    def printar_imagem(self):
        caminho_arquivo = filedialog.asksaveasfilename(
            defaultextension="png",
            filetypes=[("Todos os arquivos", "*.png"),("Todos os arquivos","*.*")])
        
        if caminho_arquivo:
            x1 = self.view.canvas.winfo_rootx()
            y1 = self.view.canvas.winfo_rooty()
            
            x2 = self.view.canvas.winfo_width() + x1
            y2 = self.view.canvas.winfo_height() + y1
            imagem = ImageGrab.grab(bbox=(x1,y1,x2,y2))
            imagem.save(caminho_arquivo)

    def abrir_imagem(self):
        caminho_arquivo = filedialog.askopenfilename(
            filetypes=[("Arquivos de Desenho","*.desenho"),("Todos os arquivos","*.*")]   
        )
        if caminho_arquivo:
            with open(caminho_arquivo,'rb') as arquivo:
                lista_figuras_carregadas = pickle.load(arquivo)
            self.desenho.figuras = lista_figuras_carregadas
            self.view.canvas.delete("all")
            for figura in self.desenho.figuras:
                figura.desenhar(self.view.canvas)

    def salvar_projeto(self):
        caminho_arquivo = filedialog.asksaveasfilename(
            defaultextension=".desenho",
            filetypes=[("Arquivos de Desenho","*.desenho"),("Todos os arquivos","*.*")]
        )
        if caminho_arquivo:
            with open(caminho_arquivo,'wb') as arquivo:
                pickle.dump(self.desenho.figuras, arquivo)
>>>>>>> Stashed changes
