from abc import ABC, abstractmethod
from tkinter import *

class Figuras(ABC):
    def __init__(self,corLinha,corFundo= None, tamanho=1.0):
        self.corLinha = corLinha
        self.corFundo = corFundo
        self.tamanho = tamanho

    def atualizar(self,x, y):
        pass
        
    @abstractmethod
    def desenhar(self,canvas):
        pass
    
#Pode criar Subclasse que separa as figuras do rabisco,evitando de escrever "atualizar" em todas outras figuras
class Linha(Figuras):
    def __init__(self,x1,y1,x2,y2,corLinha,tamanho):
        super().__init__(corLinha,None,tamanho)
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

    def atualizar(self,x, y):
        self.x2 = x
        self.y2 = y

    def desenhar(self,canvas):
        canvas.create_line(self.x1,self.y1,self.x2,self.y2,fill=self.corLinha,width=self.tamanho)

class Retangulo(Figuras):
    def __init__(self,x1,y1,x2,y2,corLinha,corFundo,tamanho):
        super().__init__(corLinha,corFundo,tamanho)
        self.x1,self.y1 = x1,y1
        self.x2,self.y2 = x2,y2

    def atualizar(self,x, y):
        self.x2 = x
        self.y2 = y
    
    def desenhar(self,canvas):
        canvas.create_rectangle(self.x1,self.y1,self.x2, self.y2,fill=self.corFundo, outline=self.corLinha,width=self.tamanho)

class Oval(Figuras):
    def __init__(self,x1, y1, x2, y2,corLinha,corFundo,tamanho):
        super().__init__(corLinha,corFundo,tamanho)
        self.x1,self.y1 = x1,y1
        self.x2, self.y2 = x2, y2

    def atualizar(self,x, y):
        self.x2 = x
        self.y2 = y
    
    def desenhar(self, canvas):
        canvas.create_oval(self.x1,self.y1,self.x2, self.y2,fill=self.corFundo, outline=self.corLinha,width=self.tamanho)

class Circulo(Figuras):
    def __init__(self,x1, y1,x2,y2,corLinha, corFundo,tamanho):
        super().__init__(corLinha, corFundo,tamanho)
        self.x1,self.y1 = x1,y1
        self.x2, self.y2 = x2,y2

    def atualizar(self,x, y):
        self.x2 = x
        self.y2 = y

    def desenhar(self, canvas):
        self.raio = ((self.x2 - self.x1) **2 + (self.y2 - self.y1)**2)**0.5
        canvas.create_oval(self.x1 - self.raio,self.y1 - self.raio, self.x1 + self.raio, self.y1 + self.raio,
                                fill=self.corFundo, outline=self.corLinha,width=self.tamanho)

class Rabisco(Figuras):
    def __init__(self,x,y,corLinha,tamanho):
        super().__init__(corLinha,None,tamanho)
        self.pontos = [(x,y)]
        self.tamanho = tamanho

    def atualizar(self,x, y):
        self.pontos.append((x,y))
        
    def desenhar(self, canvas):
        for i in range(len(self.pontos)-1):#Se tem x pontos, terão x - 1 linhas
            x1,y1 = self.pontos[i]
            x2,y2 = self.pontos[i + 1]
            
            canvas.create_line(x1,y1,x2,y2, fill=self.corLinha,width=self.tamanho)

class Poligono(Figuras):
    def __init__(self,x,y,corLinha,corFundo,tamanho):
        super().__init__(corLinha, corFundo,tamanho)
        self.pontos = [(x, y), (x,y)] # 1 ponto fixo e outro ponto temporario
        self.finalizado = False
        
    def atualizar(self,x,y):
        if not self.finalizado:
            self.pontos[-1] = (x,y)
    
    def adicionar_ponto(self,x,y):
        if not self.finalizado:
            self.pontos.append((x,y))
    
    def finalizar(self):
        self.finalizado = True
        if len(self.pontos) > 1:
            self.pontos.pop()

    def desenhar(self, canvas):
        if len(self.pontos) < 2:
            return
        coordenadas = []
        for x,y in self.pontos:
            coordenadas.extend([x,y])
        if self.finalizado and len(self.pontos) >= 3:
            canvas.create_polygon(coordenadas, fill=self.corFundo, outline=self.corLinha,width=self.tamanho)
        else:
            canvas.create_polygon(coordenadas,fill=self.corLinha if self.corLinha else "black")