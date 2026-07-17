from abc import ABC, abstractmethod
from tkinter import *
import math

class Figuras(ABC):
    def __init__(self,corLinha,corFundo= None, tamanho=1.0):
        self.corLinha = corLinha
        self.corFundo = corFundo
        self.selecionada = False
        self.tamanho = tamanho

    def atualizar(self,x, y):
        pass
        
    @abstractmethod
    def desenhar(self,canvas):
        pass

    @abstractmethod
    def contem(self, x, y):
        pass

    def mover(self,dx,dy): # Padrão para figuras como Linha,Retângulo, Oval e Círculo (Polígono e Rabisco possuem outra forma por serem listas)
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

    def estilo(self):

        if self.selecionada:
            return {
                "dash": (10, 5),
                "width": self.tamanho + 1
            }

        return {
            "width": self.tamanho #substituir por atributo borda depois
        }
    @abstractmethod
    def Copiar(self):
        pass
    
    @abstractmethod
    def obter_pontos(self):
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
        canvas.create_line(self.x1,self.y1,self.x2,self.y2,fill=self.corLinha,**self.estilo())#O ** pega o dicionario do metodo estilo e transforma em argumentos
        
    def contem(self,x, y):
        return distancia(self.x1,self.x2,self.y1,self.y2, x, y) <= 5
    
    def Copiar(self):
        return Linha(self.x1,self.y1,self.x2,self.y2,self.corLinha,self.tamanho)

    def obter_pontos(self):
        return self.x1, self.y1

class Retangulo(Figuras):
    def __init__(self,x1,y1,x2,y2,corLinha,corFundo,tamanho):
        super().__init__(corLinha,corFundo,tamanho)
        self.x1,self.y1 = x1,y1
        self.x2,self.y2 = x2,y2

    def atualizar(self,x, y):
        self.x2 = x
        self.y2 = y
    
    def desenhar(self,canvas):
        canvas.create_rectangle(self.x1,self.y1,self.x2, self.y2,fill=self.corFundo, outline=self.corLinha,**self.estilo() )
        
    def contem(self,x, y):
        return (min(self.x1, self.x2) <= x <= max(self.x1, self.x2)) and \
            (min(self.y1, self.y2) <= y <= max(self.y1, self.y2))
            
    def Copiar(self):
        return Retangulo(self.x1,self.y1,self.x2, self.y2,self.corFundo,self.corLinha,self.tamanho )

    def obter_pontos(self):
        return self.x1,self.y1

class Oval(Figuras):
    def __init__(self,x1, y1, x2, y2,corLinha,corFundo,tamanho):
        super().__init__(corLinha,corFundo,tamanho)
        self.x1,self.y1 = x1,y1
        self.x2, self.y2 = x2, y2

    def atualizar(self,x, y):
        self.x2 = x
        self.y2 = y

    def desenhar(self, canvas):
        canvas.create_oval(self.x1,self.y1,self.x2, self.y2,fill=self.corFundo, outline=self.corLinha,**self.estilo() )

    def contem(self,x, y):
        esquerda = min(self.x1, self.x2)
        direita = max(self.x1,self.x2)
        cima = max(self.y1,self.y2)
        baixo = min(self.y1,self.y2)
        
        cx = (direita + esquerda)/2
        cy = (cima + baixo)/2
        
        a = (direita - esquerda)/ 2
        b = (cima - baixo)/ 2
        
        return ((x - cx) ** 2) / (a ** 2) + ((y - cy) ** 2) / (b ** 2) <= 1
        #A equação da Elipse é (x - c1)**2/a**2 + (y - c2)**2/b** = 1
    def Copiar(self):
        return Oval(self.x1,self.y1,self.x2, self.y2,self.corFundo, self.corLinha,self.tamanho )

    def obter_pontos(self):
        return self.x1,self.y1

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
                                fill=self.corFundo, outline=self.corLinha,**self.estilo() )
    def contem(self,x, y):
        return  ((x - self.x1) **2 + (y - self.y1)**2)**0.5 <= self.raio

    def Copiar(self):
        return Circulo(self.x1,self.y1, self.x2, self.y2,
                                self.corFundo, self.corLinha,self.tamanho )

    def obter_pontos(self):
        return self.x1,self.y1
    
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
            
            canvas.create_line(x1,y1,x2,y2, fill=self.corLinha,**self.estilo())

    def contem(self, x, y):
        for i in range(len(self.pontos)-1):
            x1,y1 = self.pontos[i]
            x2,y2 = self.pontos[i + 1]
            if distancia(x1,x2,y1,y2,x,y) <= 5:
                return True
        return False
    
    def mover(self,dx,dy):
        self.pontos = [(dx+x , dy+y) for x,y in self.pontos] # Compreensão de listas para atualizar simultaneamente o x e o y
    
    def Copiar(self):
        novo = Rabisco(self.pontos[0][0],
                       self.pontos[0][1],
                       self.corLinha,self.tamanho)
        novo.pontos = self.pontos
        return novo

    def obter_pontos(self):
        return self.pontos[0][0],self.pontos[0][1]

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
            canvas.create_polygon(coordenadas, fill=self.corFundo, outline=self.corLinha,**self.estilo())
        else:
            canvas.create_polygon(coordenadas, fill=self.corLinha if self.corLinha else "black")

    def contem(self, x, y) :
        """
        Verifica se o ponto (x, y) está dentro de um polígono.
        O polígono está especificado na lista de tuplas self.pontos: [(x1, y1), (x2, y2), ...].
        """
        dentro = False
        n = len(self.pontos)

        # Se o polígono não tiver pelo menos 3 vértices, não é um polígono válido
        if n < 3:
            return False

        # Inicializa o último vértice do polígono como ponto de partida
        p1x, p1y = self.pontos[0]

        for i in range(n + 1):
            # Avança para o próximo vértice
            p2x, p2y = self.pontos[i % n]

            # Verifica se o raio horizontal intercepta a aresta do polígono
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        # Calcula a interceptação X exata da aresta
                        if p1y != p2y:
                            x_interceptado = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        # Se o ponto estiver à esquerda da interceptação, inverte o estado
                        if p1x == p2x or x <= x_interceptado:
                            dentro = not dentro

            p1x, p1y = p2x, p2y

        return dentro
    
    def mover(self,dx,dy):
        self.pontos = [(dx+x , dy+y) for x , y in self.pontos] # Compreensão de listas para atualizar simultaneamente o x e o y
        
    def Copiar(self):
        novo = Poligono(self.pontos[0][0],
                        self.pontos[0][1],
                        self.corLinha,
                        self.corFundo,self.tamanho)
        novo.pontos = self.pontos
        novo.finalizado = self.finalizado
        return novo
    
    def obter_pontos(self):
        return self.pontos[0][0],self.pontos[0][1]
    
class PoligonosRegulares(Figuras):
    def __init__(self,x,y,corLinha,corFundo,tamanho):
        super().__init__(corLinha, corFundo,tamanho)
        self.cx, self.cy = x, y
        self.lados = 3
        
        self.finalizado = False
        
    def atualizar(self, x, y):
        if not self.finalizado:
            dx = x - self.cx
            dy = y - self.cy

            
            self.raio = ((x - self.cx) **2 + (y - self.cy)**2)**0.5
            self.angulo_inicial = math.atan2(dy,dx)
            
    def adicionar_lado(self):
        if not self.finalizado:
            self.lados += 1
            
    def finalizar(self):
        self.finalizado = True
        
    def desenhar(self, canvas):
        angulo_passo = (2 * math.pi)/self.lados
        
        self.pontos = []
        for i in range(self.lados):
            angulo = self.angulo_inicial + i * angulo_passo
            x = self.cx + (self.raio * math.cos(angulo))
            y = self.cy + (self.raio * math.sin(angulo))
            self.pontos.append([x,y])
        canvas.create_polygon(self.pontos, fill=self.corFundo, outline=self.corLinha,**self.estilo())
    def finalizar(self):
        self.finalizado = True
    def contem(self, x, y):
        dentro = False
        n = len(self.pontos)

        # Se o polígono não tiver pelo menos 3 vértices, não é um polígono válido
        if n < 3:
            return False

        # Inicializa o último vértice do polígono como ponto de partida
        p1x, p1y = self.pontos[0]

        for i in range(n + 1):
            # Avança para o próximo vértice
            p2x, p2y = self.pontos[i % n]

            # Verifica se o raio horizontal intercepta a aresta do polígono
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        # Calcula a interceptação X exata da aresta
                        if p1y != p2y:
                            x_interceptado = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        # Se o ponto estiver à esquerda da interceptação, inverte o estado
                        if p1x == p2x or x <= x_interceptado:
                            dentro = not dentro

            p1x, p1y = p2x, p2y

        return dentro
    
    def mover(self,dx,dy):
        self.cx += dx
        self.cy += dy
    
    def Copiar(self):
        novo = PoligonosRegulares(self.cx, self.cy,
                                  self.corLinha,
                                  self.corFundo,
                                  self.tamanho)
        novo.pontos = self.pontos
        novo.finalizado = self.finalizado 
        novo.raio = self.raio
        novo.lados = self.lados
        return novo
    def obter_pontos(self):
        return self.cx, self.cy
    
class FiguraComposta(Figuras):
    def __init__(self, figuras):
        super().__init__(None,None)
        self.figuras = figuras
        self.selecionada = False

    def desenhar(self, canvas):
        for figura in self.figuras:
            figura.selecionada = self.selecionada
            figura.desenhar(canvas)

    def contem(self, x, y):
        for figura in self.figuras:
            if figura.contem(x, y):
                return True
        return False
    
    def mover(self, dx, dy):
        for figura in self.figuras:
            figura.mover(dx, dy)

    def Copiar(self):
        copias = []
        for figura in self.figuras:
            copias.append(figura.Copiar())
        return FiguraComposta(copias)
    
    def obter_pontos(self):
        """ Retorna o ponto mais superior/esquerdo da figura composta.
        Usado pela seleção por caixa"""
        pontos = []
        for figura in self.figuras:
            pontos.append(figura.obter_pontos())
        menor_x = min(p[0] for p in pontos)
        menor_y = min(p[1] for p in pontos)
        return menor_x, menor_y
    
    def desagrupar(self):
        return self.figuras.copy()
        
def distancia(x1, x2, y1, y2, px, py) :
    # Vetor direção do segmento (AB)
    dx = x2 - x1
    dy = y2 - y1

    # Comprimento do segmento ao quadrado
    ab_len_sq = dx**2 + dy**2

    # Caso o segmento seja apenas um ponto (A e B são iguais)
    if ab_len_sq == 0:
        return ((px - x1)**2 + (py - y1)**2)**0.5

    # Vetor do ponto A ao ponto P (AP)
    ap_x = px - x1
    ap_y = py - y1

    # Produto escalar de AP e AB dividido pelo comprimento ao quadrado (fator t)
    t = (ap_x * dx + ap_y * dy) / ab_len_sq

    # Limita t entre 0 e 1 para garantir que a projeção fique dentro do segmento
    t = max(0.0, min(1.0, t))

    # Coordenadas do ponto mais próximo no segmento
    ponto_proximo_x = x1 + t * dx
    ponto_proximo_y = y1 + t * dy

    return ((px - ponto_proximo_x)**2 + (py - ponto_proximo_y)**2)**0.5