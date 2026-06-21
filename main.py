import tkinter as tk
from tkinter import ttk

janela = tk.Tk()
janela.geometry("600x500")
janela.title("Layout Horizontal")

# 1. FRAME DOS BOTÕES (Fica no topo)
barra_botoes = ttk.Frame(janela, padding=5)
barra_botoes.pack(side=tk.TOP, fill=tk.X) # Ocupa toda a largura no topo

# Botões dentro do frame (alinhados à esquerda)
btn_cor = ttk.Button(barra_botoes, text="Escolher Cor")
btn_cor.pack(side=tk.LEFT, padx=5)

btn_limpar = ttk.Button(barra_botoes, text="Resetar")
btn_limpar.pack(side=tk.LEFT, padx=5)

# 2. CANVAS (Fica embaixo, ocupando o resto da tela)
canvas = tk.Canvas(janela, bg="white")
canvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

janela.mainloop()