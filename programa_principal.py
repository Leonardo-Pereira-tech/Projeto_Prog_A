from tkinter import *
from tkinter import ttk 
from tkinter import colorchooser
from Model.fig import *
from Model.desenho import *
from View.view import *

#Aqui a função define a classe(tipo da figura)
def iniciar_figura(event):
    global x1, y1, x2, y2, figura_nova, cor_linha, cor_fundo, figuras
    x1,y1,x2,y2 = event.x,event.y,event.x,event.y
    figura = menu.detectarFigura()

    # Caso especial se for um polígono sendo desenhado
    if figura == "Polígono" and isinstance(figura_nova, Poligono) and not figura_nova.finalizado:
        figura_nova.adicionar_ponto(event.x, event.y)
        menu.redesenhar(figuras,figura_nova)
        figura_nova.desenhar(menu.canvas)
        return
    
    elif figura == "Retângulo":
        figura_nova = Retangulo(x1,y1,x2,y2,cor_linha,cor_fundo)
    elif figura == "Oval":
        figura_nova = Oval(x1,y1,x2,y2,cor_linha,cor_fundo)
    elif figura == "Linha":
        figura_nova = Linha(x1,y1,x2,y2,cor_linha)
    elif figura == "Rabisco":
        figura_nova = Rabisco(x1,y1,cor_linha)
    elif figura == "Círculo":
        figura_nova = Circulo(x1,y1,x2,y2,cor_linha,cor_fundo)
    elif figura == "Polígono":
        figura_nova = Poligono(x1, y1, cor_linha, cor_fundo)
        
        
#Aqui é atualizado o segundo ponto,enquanto desenha a figura atual e armazenadas
def atualizar_figura(event):
    global figura_nova
    
    # Esse event.state é para o acaso do mouse estiver se movendo solto (0)
    if event.state == 0 and menu.detectarFigura() != "Polígono":
        return
    
    if figura_nova:
        figura_nova.atualizar(event.x, event.y)
        menu.redesenhar(figuras,figura_nova)
        figura_nova.desenhar(menu.canvas)
    
#Aqui é armazenada a figura atual
def terminar_figura(event):
    global figuras, figura_nova

    if menu.detectarFigura() != "Polígono":
        figuras.adicionar_figura(figura_nova)
        figura_nova = None

#Função para finalizar o polígono
def finalizar_poligono(event):
    global figura_nova
    if menu.detectarFigura() == "Polígono" and isinstance(figura_nova, Poligono):
        figura_nova.finalizar()
        figuras.adicionar_figura(figura_nova)
        menu.redesenhar(figuras,figura_nova)
        figura_nova = None
    
    
cor_linha = "black"
def escolher_Cor_borda(): 
    global cor_linha
    cor = colorchooser.askcolor(title="Selecionar Cor")
    if cor and cor[1]:
        cor_linha = cor[1]

cor_fundo = ""
def escolher_Cor_preenchimento(): 
    global cor_fundo
    cor = colorchooser.askcolor(title="Selecionar Cor para preencher")
    if cor and cor[1]:
        cor_fundo = cor[1]
def deletar():
    global figuras,cor_linha,cor_fundo
    cor_linha, cor_fundo = "black",""
    menu.canvas.delete("all")
    figuras.limpar()

#MAIN

x1 = None
y1 = None
x2 = None
y2 = None

figuras = Desenho()
figura_nova = None

janela = Tk();janela.title("Entrega1")

menu = canvasView(janela)

menu.corBorda(escolher_Cor_borda)
menu.corPreenchimento(escolher_Cor_preenchimento)
menu.apagarDesenho(deletar)

menu.inicioDesenho(iniciar_figura)
menu.atualizarDesenho(atualizar_figura)
menu.terminarDesenho(terminar_figura)
menu.atualizarDesenhoPolígono(atualizar_figura)
menu.terminarPoligono(finalizar_poligono) # Finaliza o polígono com o botão direito

janela.mainloop()