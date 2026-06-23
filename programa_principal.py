from tkinter import *
from tkinter import ttk 
from tkinter import colorchooser
from Model.fig import *
from Model.desenho import *
from View.view import *
from Controller.controller import *


#MAIN


figuras = Desenho()
figura_nova = None

janela = Tk();janela.title("Entrega1")

menu = canvasView(janela)

controlador = Controlador(figuras,menu)

janela.mainloop()