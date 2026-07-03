from tkinter import *
from Model.fig import *
from Model.desenho import *
from View.view import *
from Controller.controller import *


#MAIN


figuras = Desenho()
figura_nova = None

janela = Tk();janela.title("Entrega1")

menu = Canvasview(janela)

controlador = Controlador(figuras,menu)

janela.mainloop()
