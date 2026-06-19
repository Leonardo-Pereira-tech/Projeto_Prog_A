from abc import ABC, abstractmethod

class Figuras(ABC):
    def __init__(self,corLinha,corFundo):
        self.corLinha = corLinha
        self.corFundo = corFundo

    @abstractmethod
    def desenhar(self,canvas):
        pass

class Linha(Figuras):
    def __init__(self,x1,y1,x2,y2,corLinha,corFundo):
        super.__init__(corLinha, corFundo)
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

    def desenhar(self,canvas):
        self.canvas.create_line(self.x1,self.y1,self.x2,self.y2,fill=self.corLinha)

class Retangulo(Figuras):
    def __init__(self,x1,y1,x2,y2,corLinha,corFundo):
        super.__init__(corLinha,corFundo)
        self.x1,self.y1 = x1,y1
        self.x2,self.y2 = x2,y2
    
    def desenhar(self,canvas):
        self.canvas.create_rectangle(self.x1,self.y1,self)
