import tkinter as tk
from tkinter import filedialog
import numpy as np
import pandas as pd
import pickle
import Home as hm
import sklearn
from datetime import datetime

class CalculoTabular:

    def __init__(self, root):

        self.df = None
        self.nombre_archivo = None

        self.root = root
        self.root.title("Cálculo Tabular - CFM Fugados")
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
        self.titulo_tabular = tk.Label(self.root, text = 'Cálculo Tabular - CFM Fugados', fg = 'black', font = ('arial', 20), height = 1, bg = 'white')
        self.titulo_tabular.pack(pady=20)

        # Crear etiquetas y campos de entrada
        self.label_dB = tk.Label(self.root, text="Leer archivo Excel - xlsx", fg = 'blue', font = ('arial', 14), height = 1, bg = 'white')
        self.label_dB.pack()

        self.boton_abrir = tk.Button(self.root, text="Abrir Archivo", command=self.abrir_archivo, fg = 'black', font=('arial', 13), bg='#e0e0e0', width=15, highlightbackground='white', borderwidth=4, relief=tk.GROOVE, cursor='hand2')
        self.boton_abrir.pack(pady=20)

        # Etiqueta para mostrar el estado de la lectura del archivo
        self.etiqueta_lectura = tk.Label(self.root, text="", font = ('arial', 14), height = 1, bg = 'white')
        self.etiqueta_lectura.pack(pady=20)

        # Botón calcular y guardar
        self.boton_calcular = tk.Button(self.root, text="Calcular y guardar", command = self.calcular_guardar, fg = 'black', font=('arial', 13), bg='#e0e0e0', width=15, highlightbackground='white', borderwidth=4, relief=tk.GROOVE, cursor='hand2')
        self.boton_calcular.pack(pady=20)

        # Etiqueta para mostrar el estado de cálculo
        self.exito = tk.Label(self.root, text="", font = ('arial', 14), height = 1, bg = 'white')
        self.exito.pack(pady=20)

        # Botón para reiniciar
        self.btn_reiniciar = tk.Button(self.root, text = 'Reiniciar', command = self.reiniciar, fg = 'black', font=('arial', 13), bg='#e0e0e0', width=15, highlightbackground='white', borderwidth=4, relief=tk.GROOVE, cursor='hand2')
        self.btn_reiniciar.pack(pady=10)

        # Botón para regresar a la ventana principal
        self.btn_regresar = tk.Button(self.root, text = 'Regresar al inicio', command = self.open_home, fg = 'black', font=('arial', 13), bg='#e0e0e0', width=15, highlightbackground='white', borderwidth=4, relief=tk.GROOVE, cursor='hand2')
        self.btn_regresar.pack()
    
    def abrir_archivo(self):
        # Muestra el cuadro de diálogo para seleccionar un archivo Excel
        self.archivo_excel = filedialog.askopenfilename(filetypes=[("Archivos Excel", "*.xlsx;*.xls")])
        self.nombre_archivo = self.archivo_excel.split('/')[-1]
        try:
            # Intenta leer el contenido del archivo Excel
            self.df = pd.read_excel(self.archivo_excel)

            # Actualiza la etiqueta con el mensaje de éxito
            self.etiqueta_lectura.config(text="Archivo leído correctamente: " + self.nombre_archivo, fg="green")

        except Exception as e:
            # Si hay un error al leer el archivo, muestra un mensaje de error
            self.etiqueta_lectura.config(text=f"Error al leer el archivo: {str(e)}", fg="red")

    def leer_modelos(self):
        # Abre el archivo en modo lectura binaria (rb)
        with open('Modelos/RFR.pkl', 'rb') as archivo:
        # Carga los datos desde el archivo
            rfr = pickle.load(archivo)

        with open('Modelos/xgb.pkl', 'rb') as archivo:
            # Carga los datos desde el archivo
            xgb = pickle.load(archivo)

        return rfr, xgb
    
    def calcular_guardar(self):
        rfr, xgb = self.leer_modelos()

        try:
            self.df.columns = ['db', 'PSI']
            y_pred_rfr = rfr.predict(self.df)
            y_pred_xgb = xgb.predict(self.df)
            cfm = np.mean((y_pred_rfr, y_pred_xgb), axis = 0)
            self.df['CFM'] = cfm

            current_datetime = datetime.now().strftime('%d_%m_%Y__%H_%M_%S')
            self.df.to_excel(self.nombre_archivo.split('.')[0] + '_' + current_datetime + '.xlsx', index=False)
            # Actualiza la etiqueta con el mensaje de éxito
            self.exito.config(text="Cálculo guardado con éxito", fg="green")

        except Exception as e:
            # Si hay un error al leer el archivo, muestra un mensaje de error
            self.exito.config(text=f"Error al realizar el cálculo", fg="red")

    def reiniciar(self):
        # Establecer los campos de entrada a una cadena vacía
        self.etiqueta_lectura.config(text="")
        self.exito.config(text="")
        self.df = None
        self.nombre_archivo = None

    def open_home(self):
        self.root.destroy()
        home = tk.Tk()
        hm.Home(home)
        home.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    CalculoTabular(root)
    root.mainloop()