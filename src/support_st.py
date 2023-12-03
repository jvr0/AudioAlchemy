import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('../data/inventario.csv')
df = df[df.status == 'For Sale']

# La siguiente función permite que cuando se inicia el st tener un dato actualizado del inventario que estamos manejando
def tamaño_inventario ():
    df = pd.read_csv('../data/inventario.csv')
    df = df[df.status == 'For Sale']
    return(len(df))

def graficazo():
    # Obtener los 10 artistas y sellos discográficos más frecuentes
    conteo_artistas = df['artist'].value_counts().head(11)
    top_10_artistas = conteo_artistas[1:]
    top_10_sellos = df['label'].value_counts().head(10)



    # Crear figura y ejes para el gráfico. Color del fondo
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('#fffef4')
    ax.patch.set_facecolor('#fffef4')

    # Calcular el rango de valores para el eje y
    y_values = range(10)

    # Escalar los valores para el eje x proporcionalmente
    max_value = max(top_10_artistas.values.max(), top_10_sellos.values.max())
    scaled_artistas = top_10_artistas.values * max_value / top_10_artistas.values.max()
    scaled_sellos = top_10_sellos.values * max_value / top_10_sellos.values.max()

    # Graficar las barras de los artistas hacia la derecha
    bars_artistas = ax.barh(y_values, scaled_artistas, color='skyblue', align='center', label='Top 10 Artistas')

    # Graficar las barras de los sellos hacia la izquierda (negativo)
    bars_sellos = ax.barh(y_values, -scaled_sellos, color='orange', align='center', label='Top 10 Sellos Discográficos')

    # Configuración de etiquetas y título
    ax.set_yticks(y_values)
    ax.set_yticklabels(top_10_artistas.index)

    # Ocultar el eje x
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    for spine in ax.spines.values():
        spine.set_visible(False)

    # Mostrar el nombre del artista y el recuento en las barras de artistas
    for i, bar in enumerate(bars_artistas):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, 
                f' {top_10_artistas.index[i]} ({top_10_artistas.values[i]})', 
                va='center', ha='left', color='black', fontsize=8)

    # Mostrar el nombre del sello discográfico en las barras de sellos
    for i, bar in enumerate(bars_sellos):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, 
                f'{top_10_sellos.index[i]} ({top_10_sellos.values[i]}) ', 
                va='center', ha='right', color='black', fontsize=8)

    # Mostrar el gráfico
    plt.show()