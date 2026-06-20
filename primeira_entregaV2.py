from tkinter import *
from tkinter import ttk 
from tkinter import colorchooser
from fig import *

#Aqui a função define a classe(tipo da figura)
def iniciar_figura(event):
    global x1, y1, x2, y2, figura_nova, cor_linha, cor_fundo
    x1,y1,x2,y2 = event.x,event.y,event.x,event.y
    figura = tipo_figura.get()
    if figura == "Retângulo":
        figura_nova = Retangulo(x1,y1,x2,y2,cor_linha,cor_fundo)
    elif figura == "Oval":
        figura_nova = Oval(x1,y1,x2,y2,cor_linha,cor_fundo)
    elif figura == "Linha":
        figura_nova = Linha(x1,y1,x2,y2,cor_linha)
    elif figura == "Rabisco":
        figura_nova = Rabisco(x1,y1,cor_linha)
    elif figura == "Círculo":
        figura_nova = Circulo(x1,y1,x2,y2,cor_linha,cor_fundo)
        
#Aqui é atualizado o segundo ponto,enquanto desenha a figura atual e armazenadas
def atualizar_figura(event):
    global figura_nova

    figura_nova.atualizar(event.x,event.y)
    desenhar()  
    figura_nova.desenhar(canvas)  
    
#Aqui é armazenada a figura atual
def terminar_figura(event):
    global figuras
    figuras.append(figura_nova)
    
#Aqui são desenhadas as figuras armazenadas 
def desenhar():
    global figuras
    canvas.delete("all")
    for figura in figuras:
        figura.desenhar(canvas)
    
cor_linha = None
def escolher_Cor_borda(): 
    global cor_linha
    cor = colorchooser.askcolor(title="Selecionar Cor")
    if cor and cor[1]:
        cor_linha = cor[1]

cor_fundo = None
def escolher_Cor_preenchimento(): 
    global cor_fundo
    cor = colorchooser.askcolor(title="Selecionar Cor para preencher")
    if cor and cor[1]:
        cor_fundo = cor[1]

def deletar():
    global figuras,cor_linha,cor_fundo
    cor_linha, cor_fundo = None, None
    canvas.delete("all")
    figuras = []

x1 = None
y1 = None
x2 = None
y2 = None

figuras = []
figura_nova = None

janela = Tk();janela.title("Entrega1")

#Criação do menu superior
frame = Frame(janela, relief=GROOVE, bd= 5)
lbl = Label(frame,text="Escolher Tipo de Desenho");lbl.pack(side=LEFT)
tipo_figura = StringVar(value="Retângulo")
menu = OptionMenu(frame,tipo_figura,"Retângulo","Círculo","Oval","Linha", "Rabisco");menu.pack(side=RIGHT)
frame.pack(fill=X)

#Criação do Espaço Canvas
canvas = Canvas(janela, width= 600, height= 600,bg ="white" )
canvas.pack(pady=10, padx= 10,fill=BOTH)

#Botao de Apagar
apagar = Button(frame, text="Resetar", command=deletar)
apagar.pack(side=TOP)

#Interface de cores
coresBorda = Button(frame,text="Escolher Borda",command=escolher_Cor_borda)
coresBorda.pack()
coresPreencher = Button(frame,text="Preencher figura",command=escolher_Cor_preenchimento)
coresPreencher.pack()

canvas.bind("<ButtonPress-1>", iniciar_figura)
canvas.bind("<B1-Motion>", atualizar_figura)
canvas.bind("<ButtonRelease-1>", terminar_figura)

janela.mainloop()