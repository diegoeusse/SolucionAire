import cv2
import imutils
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import calculoSencillo as cS
import calculoTabular as cT

class Home:
    def __init__(self, root):
        self.root = root
        root.title("Cálculo de CFM Fugados - SoluciónAIRE")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = 500
        window_height = 500
        x_coordinate = (screen_width/2) - (window_width/2)
        y_coordinate = (screen_height/2) - (window_height/2)
        self.root.geometry('%dx%d+%d+%d' % (window_width, window_height, x_coordinate, y_coordinate))
        self.root.resizable(False, False)
        self.root.configure(bg = 'white')
        
        # Header
        espacio = tk.Label(self.root, text = '', fg = 'black', font = ('arial', 25), height = 1, bg = 'white')
        espacio.pack()
        titulo_home = tk.Label(self.root, text = 'Cálculo de CFM Fugados', fg = 'black', font = ('arial', 20), height = 1, bg = 'white')
        titulo_home.pack()

        # Imagen SolucionAIRE
        logo = cv2.imread('Imagenes/Logo.png')
        logo = imutils.resize(logo, height = 150, width = 250)
        logo = ImageTk.PhotoImage(image = Image.fromarray(cv2.cvtColor(logo, cv2.COLOR_BGR2RGB)))
        logo_label = tk.Label(self.root, image = logo, borderwidth = 0)
        logo_label.image = logo
        logo_label.pack(pady=20)

        #Botones de la Home page
        # Botón para abrir Ventana 1
        self.btn_ventana1 = tk.Button(self.root, text="Cálculo Sencillo", command=self.calculo_sencillo, fg = 'black', font = ('arial', 14), bg='#e0e0e0', width=15, highlightbackground='white', borderwidth=4, relief=tk.GROOVE, cursor='hand2')
        self.btn_ventana1.pack(pady=10)

        # Botón para abrir Ventana 2
        self.btn_ventana2 = tk.Button(self.root, text="Cálculo Tabular", command=self.calculo_tabular, fg = 'black', font = ('arial', 14), bg='#e0e0e0', width=15, highlightbackground='white', borderwidth=4, relief=tk.GROOVE, cursor='hand2')
        self.btn_ventana2.pack(pady=10)

        self.btn_salir = tk.Button(self.root, text = 'Salir', command = self.root.destroy, fg = 'black', font = ('arial', 14), bg='#e0e0e0', width=15, highlightbackground='white', borderwidth=4, relief=tk.GROOVE, cursor='hand2')
        self.btn_salir.pack(pady=10)

        self.copyright = tk.Label(self.root, text = 'Diego Eusse-Naranjo y Jhonatan Toro-Vásquez para SoluciónAIRE ® 2024.', fg = 'black', font = ('arial', 8), height = 1, bg = 'white', anchor = 'w')
        self.copyright.place(x = 130, y = 480)

    def calculo_sencillo(self):
        # Ocultar la ventana principal
        self.root.destroy()
        calculoSencillo = tk.Tk()
        cS.CalculoSencillo(calculoSencillo)
        calculoSencillo.mainloop()

    def calculo_tabular(self):
        # Ocultar la ventana principal
        self.root.destroy()
        calculoTabular = tk.Tk()
        cT.CalculoTabular(calculoTabular)
        calculoTabular.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    Home(root)
    root.mainloop()