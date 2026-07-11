import sys
import os
from tkinter import colorchooser,filedialog

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Model.fig import *;from Model.desenho import *
from View.view import *
from Controller.FerramentaState import *
from PIL import ImageGrab
import pickle
class Controlador():
    
    def __init__(self,desenho,view):
        self.desenho = desenho
        self.view = view
        
        self.cor_linha = "black"
        self.cor_fundo = ""
        self.espessura_linha = 1.0

        self.figura_nova = None
        
        self.ferramenta = FerramentaRetangulo()
        
        self.figurasCopiadas = [] # lista exclusiva para copiar e colar
        self.figuras_selecionadas = [] # Figura agora virou uma lista para fazer a implementação correta de múltipla
        self.caixa_selecao = False # Variável criada como uma "flag" uma permissão a criação do retângulo
        self.retangulo_selecao = None #variável criada somente para virar um retângulo

        self.clickX = None # Criei isso aqui porque tava pedindo como parâmetro para as cooords
        self.clickY = None
        
        canvas = self.view.canvas
        botaoBorda = self.view.coresBorda
        botaoPreencher = self.view.coresPreencher
        botaoApagar = self.view.apagar
        botaoPrintar = self.view.printar
        botaoAbrir = self.view.abrir
        botaoSalvarProjeto = self.view.salvar
        escalaBorda = self.view.escala
        
        canvas.bind("<ButtonPress-1>", self.clickMouse)
        canvas.bind("<B1-Motion>", self.arrastarMouse)
        canvas.bind("<Motion>", self.arrastarMouse)  
        canvas.bind("<ButtonRelease-1>", self.soltarMouse)
        canvas.bind("<ButtonPress-3>", self.botaoDireitoMouse)
        canvas.bind("<BackSpace>",self.apagarDesenho)
        canvas.bind("<Delete>",self.apagarDesenho)
        canvas.bind("<Right>", self.moverFrente)
        canvas.bind("<Left>", self.moverTras)
        canvas.bind("<Up>", self.moverTopo)
        canvas.bind("<Down>", self.moverFundo)      
        canvas.bind("<Control-c>",self.copiar)
        canvas.bind("<Control-v>",self.colar)
        
        botaoBorda.configure(command=self.escolher_Cor_borda)
        botaoPreencher.configure(command=self.escolher_Cor_preenchimento)
        botaoApagar.configure(command=self.deletar)
        botaoPrintar.configure(command=self.printar_imagem)
        botaoAbrir.configure(command=self.abrir_imagem)
        botaoSalvarProjeto.configure(command=self.salvar_projeto)
        escalaBorda.configure(command=self.tamanhoBorda)
        
        self.view.menu.bind("<<ComboboxSelected>>", self.mudarFerramenta)
        
    def clickMouse(self,event):
        self.ferramenta.click(self,event)
    
    def arrastarMouse(self,event):
        self.ferramenta.arrastar(self,event)
    
    #Aqui é armazenada a figura atual
    def soltarMouse(self, event):
        self.ferramenta.soltar(self, event)
    
    #Função para finalizar o polígono
    def botaoDireitoMouse(self, event):
        self.ferramenta.botaoDireito(self, event) 
    
    def escolher_Cor_borda(self): 
        cor = colorchooser.askcolor(title="Selecionar Cor")
        if cor and cor[1]:
            if self.figuras_selecionadas:
                for figura in self.figuras_selecionadas:
                    figura.corLinha = cor[1]
                self.view.redesenhar(self.desenho,None)
            else:
                self.cor_linha = cor[1]
    
    def tamanhoBorda(self,valor):
        self.espessura_linha = float(valor)
    
    def escolher_Cor_preenchimento(self): 
        cor = colorchooser.askcolor(title="Selecionar Cor para preencher")
        if cor and cor[1]:
            if self.figuras_selecionadas:
                for figura in self.figuras_selecionadas:
                    figura.corFundo = cor[1]
                self.view.redesenhar(self.desenho,None)
            else:
                self.cor_fundo = cor[1]
            
    def deletar(self):
        
        self.cor_linha, self.cor_fundo = "black",""
        self.view.canvas.delete("all")
        self.desenho.limpar()
    
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
        elif nome == "Selecionar":
            self.ferramenta = FerramentaSelecionar()

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
    
    def apagarDesenho(self, event=None):
        for figura in self.figuras_selecionadas:
            self.desenho.apagar_desenho(figura)
            self.figuras_selecionadas = []
        self.view.redesenhar(self.desenho,None)


#Todas as funções abaixo foram adaptadas para implementação de lista


    def moverFrente(self, event=None):
        self.figuras_selecionadas.sort(key=lambda f: self.desenho.figuras.index(f),reverse=True) # Esse lambda foi quase um ctrl c + v, mas ele ordena de acordo com a figura que foi desenhada primeiro. Vale testar todas porque so testei algumas funções
        for figura in self.figuras_selecionadas:
            self.desenho.mover_frente(figura)
        self.view.redesenhar(self.desenho,None)
        
    def moverTras(self, event=None):
        self.figuras_selecionadas.sort(key=lambda f: self.desenho.figuras.index(f)) # De maneira abstrata, moverFrente ou moverTras é tipo um sentido horário e anti-horário, enquanto 
        for figura in self.figuras_selecionadas:                                    # um vai para um lado, o outro segue o caminho oposto
            self.desenho.mover_atras(figura)
        self.view.redesenhar(self.desenho,None)

    def moverTopo(self, event=None):
        self.figuras_selecionadas.sort(key=lambda f: self.desenho.figuras.index(f),reverse=True)
        for figura in self.figuras_selecionadas:
            self.desenho.mover_topo(figura)
        self.view.redesenhar(self.desenho,None)
        
    def moverFundo(self, event=None):
        self.figuras_selecionadas.sort(key=lambda f: self.desenho.figuras.index(f))
        for figura in self.figuras_selecionadas:
            self.desenho.mover_fundo(figura)
        self.view.redesenhar(self.desenho,None)


    def copiar(self,event=None): # Fiz mudanças até q grandes aqui
       self.figurasCopiadas = [] # Depois de copiar, caso copie de novo a lista volta a ficar vazia, para não salvar coisas passadas
       for figura in self.figuras_selecionadas:
           copia = figura.Copiar() #Crio uma nova variável para adicionar na lista das cópias
            #copia.selecionada = False    #Talvez precise, caso dê algum bug
           self.figurasCopiadas.append(copia)

    def colar(self,event=None):
        if not self.figurasCopiadas:
            return

        for figura in self.figuras_selecionadas:
            figura.selecionada = False
        self.figuras_selecionadas = []

        deslocamento = 20 #Para a copia não sobrepor, mais por design mesmo

        for figuraCopiada in self.figurasCopiadas:
            novaFigura = figuraCopiada.Copiar()
            
            novaFigura.mover(deslocamento,deslocamento)
            novaFigura.selecionada = True
            
            self.desenho.adicionar_figura(novaFigura)
            self.figuras_selecionadas.append(novaFigura)
 
        self.view.redesenhar(self.desenho,None)