from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import markdown2

from src.support_tk import *
from src.support_API import *


"""-------------------------------------------------------------------------------------------------------------------"""

def actualizar_inventario(tamaño_venta_label, tamaño_vendido_label):
    descarga_inventario()
    inven_venta = tamaño_inventario_venta()
    inven_vendido = tamaño_inventario_vendido()
    tamaño_venta_label.config(text=f'For Sale: {inven_venta}')
    tamaño_vendido_label.config(text=f'Sold: {inven_vendido}')


def mostrar_pantalla1():
    inven_venta = tamaño_inventario_venta()
    inven_vendido = tamaño_inventario_vendido()
    
    pantalla2.pack_forget()
    pantalla3.pack_forget()
    pantalla1.pack()

    titulo = tk.Label(pantalla1, text='Actualizar')
    titulo.pack()

    tamaño_vendido = tk.Label(pantalla1, text=f'Sold: {inven_vendido}', bg='lightblue')
    tamaño_vendido.pack(side=tk.RIGHT, padx=10, pady=5)

    tamaño_venta = tk.Label(pantalla1, text=f'For Sale: {inven_venta}', bg='lightblue')
    tamaño_venta.pack(side=tk.RIGHT, padx=10, pady=5)

    # Crear un botón para actualizar el inventario
    actualizar_btn = tk.Button(pantalla1, text='Actualizar inventario', command=lambda: actualizar_inventario(tamaño_venta, tamaño_vendido))
    actualizar_btn.pack(side=tk.BOTTOM, padx=10, pady=10)

def mostrar_pantalla2():
    pantalla1.pack_forget()
    pantalla3.pack_forget()
    pantalla2.pack()

    titulo = tk.Label(pantalla2, text='Estadísticas')
    titulo.pack()

    fig = pie_chart()

    canvas = FigureCanvasTkAgg(fig, master=pantalla2)
    canvas.draw()
    canvas.get_tk_widget().pack()

def mostrar_pantalla3():
    pantalla1.pack_forget()
    pantalla2.pack_forget()
    pantalla3.pack()

    titulo = tk.Label(pantalla3, text='Documentación')
    titulo.pack()

    mark = tk.Text(pantalla3, wrap='word')
    mark.pack(expand=True, fill='both')

    mark_text = """
    El siguiente proyecto consiste en un encargo realizado por la compañía de venta online [El Ártico Discos](https://www.discogs.com/es/seller/elarticodiscos/profile "El Ártico Discos"). Se ha propuesto un trabajo de ingeniería para la actualización automática del inventario. El objetivo es mejorar la ubicación de los items dentro de la plataforma [Discogs](https://www.discogs.com/es/ "Discogs").

    La problemática presentada por el cliente fue la siguiente. Los items a la venta recién añadidos o actualizados son aquellos que se muestran de primeros al público. Para resolver este problema se planteo la construcción de tres herramientas interconectadas: 
    - Un programa que pudiera conectarse a la plataforma y actualizar la totalidad del inventario a la venta.
    - Un temporizador que permitiera al cliente programar actualizaciones automáticas a lo largo del día.
    - Una interfaz gráfica utilizable por usuarios sin conocimiento técnico."""

    html_content = markdown2.markdown(mark_text)
    mark.insert(tk.END, html_content)

    



root = tk.Tk()
root.title("Audio Alchemy 2.0")
root.geometry("1200x700")
root.config(bg='#FFDAB9')

'''
icono16 = tk.PhotoImage('utopia/img/icono160.png')
icono32 = tk.PhotoImage('utopia/img/icono32.png')
root.iconphoto(False, icono16, icono32)
'''

barra_menu = tk.Menu()

mostrar = tk.Menu(barra_menu, tearoff=False)
mostrar.add_command(label='Actualizar', accelerator="Cmd+A", command=mostrar_pantalla1)
mostrar.add_command(label='Estadísticas', accelerator="Cmd+E", command=mostrar_pantalla2)
mostrar.add_command(label='Documentación', accelerator="Cmd+D", command=mostrar_pantalla3)
barra_menu.add_cascade(label="Mostrar", menu=mostrar)

# Asignar atajos de teclado para mostrar pantallas
root.bind_all("<Command-a>", lambda event: mostrar_pantalla1())
root.bind_all("<Command-e>", lambda event: mostrar_pantalla2())
root.bind_all("<Command-d>", lambda event: mostrar_pantalla3())

inventario = tk.Menu(barra_menu, tearoff=False)
inventario.add_command(label='Nuevo inventario', command=nuevo_inventario)
inventario.add_command(label='Actualizar inventario', accelerator="Cmd+I",
                       command=lambda: actualizar_inventario(tamaño_venta, tamaño_vendido))
barra_menu.add_cascade(label="Mostrar", menu=inventario)

root.config(menu=barra_menu)

# Pantallas
pantalla1 = tk.Frame(root, width=1200, height=700)
pantalla2 = tk.Frame(root, width=1200, height=700)
pantalla3 = tk.Frame(root, width=1200, height=700, bg='green')

# Variables para las etiquetas de tamaño_venta y tamaño_vendido
tamaño_venta = tk.Label(pantalla1, text='', bg='lightblue')
tamaño_vendido = tk.Label(pantalla1, text='', bg='lightblue')


root.mainloop()