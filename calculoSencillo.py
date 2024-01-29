import tkinter as tk
import numpy as np
import pandas as pd
import pickle
import sklearn
import Home as hm

class CalculoSencillo:

    def __init__(self, root):

        self.dB = None
        self.psi = None
        self.array = None

        self.root = root
        self.root.title("Cálculo Sencillo - CFM Fugados")
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
        self.titulo_sencillo = tk.Label(self.root, text = 'Cálculo Sencillo - CFM Fugados', fg = 'black', font = ('arial', 20), height = 1, bg = 'white')
        self.titulo_sencillo.pack(pady=20)

        # Crear etiquetas y campos de entrada
        self.label_dB = tk.Label(self.root, text="Decibeles [dB]:", fg = 'blue', font = ('arial', 14), height = 1, bg = 'white')
        self.label_dB.pack(pady=5)

        self.entry_dB = tk.Entry(self.root, justify='center', bg='lightgray', fg='black', font=('Arial', 14))
        self.entry_dB.pack(pady=10)

        self.label_psi = tk.Label(self.root, text="Presión [psi]:", fg = 'blue', font = ('arial', 14), height = 1, bg = 'white')
        self.label_psi.pack(pady=5)

        self.entry_psi = tk.Entry(self.root, justify='center', bg='lightgray', fg='black', font=('Arial', 14))
        self.entry_psi.pack(pady=20)

        # Etiqueta para mostrar el resultado
        self.label_resultado = tk.Label(self.root, text="", font = ('arial', 14), height = 1, bg = 'white')
        self.label_resultado.pack(pady=20)

        # Botón para calcular el resultado
        self.boton_calcular = tk.Button(self.root, text="Calcular", command = lambda: self.calcular_resultado(self.entry_dB, self.entry_psi), fg='black', font=('arial', 13), bg='#e0e0e0', width=15, highlightbackground='white', borderwidth=4, relief=tk.GROOVE, cursor='hand2')
        self.boton_calcular.pack(pady=10)

        # Botón para limpiar los inputs
        self.boton_limpiar = tk.Button(self.root, text="Limpiar", command = self.limpiar, fg='black', font=('arial', 13), bg='#e0e0e0', width=15, highlightbackground='white', borderwidth=4, relief=tk.GROOVE, cursor='hand2')
        self.boton_limpiar.pack(pady=10)

        # Botón para regresar a la self.root principal     
        self.btn_regresar = tk.Button(self.root, text = 'Regresar al inicio', command = self.open_home, fg = 'black', font = ('arial', 13), bg='#e0e0e0', width=15, highlightbackground='white', borderwidth=4, relief=tk.GROOVE, cursor='hand2')
        self.btn_regresar.pack(pady=10)

    def leer_modelos(self):
        # Abre el archivo en modo lectura binaria (rb)
        with open('Modelos/RFR.pkl', 'rb') as archivo:
        # Carga los datos desde el archivo
            rfr = pickle.load(archivo)

        with open('Modelos/xgb.pkl', 'rb') as archivo:
            # Carga los datos desde el archivo
            xgb = pickle.load(archivo)

        return rfr, xgb

    def calcular_resultado(self, entry_dB, entry_psi):
        rfr, xgb = self.leer_modelos()
        try:
            # Obtener los valores ingresados por el usuario
            self.dB = float(entry_dB.get())
            self.psi = float(entry_psi.get())
            self.array = np.array([[self.dB, self.psi]])

            # Realizar el cálculo (puedes cambiar esto según tus necesidades)
            y_pred_rfr = rfr.predict(self.array)
            y_pred_xgb = xgb.predict(self.array)
            cfm = float(np.mean((y_pred_rfr, y_pred_xgb), axis = 0))

            # Mostrar el resultado en la etiqueta de resultado
            self.label_resultado.config(text=f"CFM Fugados: {cfm}", fg="black")
        except ValueError:
            self.label_resultado.config(text="Error: Los valores ingresados no son correctos", fg="red")
    
    def limpiar(self):
        # Establecer los campos de entrada a una cadena vacía
        self.entry_dB.delete(0, tk.END)
        self.entry_psi.delete(0, tk.END)
        self.label_resultado.config(text="")
        self.dB = None
        self.psi = None
        self.array = None
    
    def open_home(self):
        self.root.destroy()
        home = tk.Tk()
        hm.Home(home)
        home.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    CalculoSencillo(root)
    root.mainloop()