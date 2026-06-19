from tkinter import *
from tkinter import ttk 
from tkinter import colorchooser


def iniciar_figura(event):
    global x1, y1
    x1 = event.x
    y1 = event.y
    
def atualizar_figura(event):
    global x1, x2, y1, y2, figura_nova
    x2, y2 = event.x, event.y
    if(figura_nova):
        canvas.delete(figura_nova)
    figura_nova = desenhar()
    

def terminar_figura(event):
    global figura_nova
    figura_nova = None
    
def desenhar():
    global x1, y1, x2, y2, figura_nova, cor_carregada, cor_preenchimento
    figura = tipo_figura.get()
    if figura == "Retângulo":
        return canvas.create_rectangle(x1,y1,x2,y2,outline=cor_carregada,fill=cor_preenchimento)
    elif figura == "Oval":
        return canvas.create_oval(x1,y1,x2,y2,outline=cor_carregada,fill=cor_preenchimento)
    elif figura == "Linha":
        return canvas.create_line(x1,y1,x2,y2,fill=cor_carregada)
    elif figura == "Rabisco":
        canvas.create_line(x1,y1,x2,y2, fill=cor_carregada)
        x1,y1 = x2,y2
    elif figura == "Círculo":
        r = ((x2 - x1) **2 + (y2 - y1)**2)**0.5
        return canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r,outline=cor_carregada,fill=cor_preenchimento)

cor_carregada = "Black"
def escolher_Cor_borda(): 
    global cor_carregada
    cor = colorchooser.askcolor(title="Selecionar Cor")
    if cor and cor[1]:
        cor_carregada = cor[1]

cor_preenchimento = None
def escolher_Cor_preenchimento(): 
    global cor_preenchimento
    cor = colorchooser.askcolor(title="Selecionar Cor para preencher")
    if cor and cor[1]:
        cor_preenchimento = cor[1]

def deletar():
    canvas.delete("all")

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
canvas.pack(pady=10, padx= 10)

#Botao de Apagar
apagar = Button(frame, text="Apagar", command=deletar)
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