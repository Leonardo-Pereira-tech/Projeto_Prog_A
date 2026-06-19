from tkinter import *
from tkinter import ttk 

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
    global x1, y1, x2, y2, figura_nova
    figura = tipo_figura.get()
    if figura == "Retângulo":
        return canvas.create_rectangle(x1,y1,x2,y2)
    elif figura == "Oval":
        return canvas.create_oval(x1,y1,x2,y2)
    else:
        r = ((x2 - x1) **2 + (y2 - y1)**2)**0.5
        return canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r)
    
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
menu = OptionMenu(frame,tipo_figura,"Retângulo","Círculo","Oval");menu.pack(side=RIGHT)
frame.pack(fill=X)

#Criação do Espaço Canvas
canvas = Canvas(janela, width= 600, height= 600,bg ="white" )
canvas.pack(pady=10, padx= 10)

#Botao de Apagar
apagar = Button(frame, text="Apagar", command=deletar)
apagar.pack(side=TOP)

canvas.bind("<ButtonPress-1>", iniciar_figura)
canvas.bind("<B1-Motion>", atualizar_figura)
canvas.bind("<ButtonRelease-1>", terminar_figura)

janela.mainloop()
