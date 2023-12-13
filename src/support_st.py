import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

df = pd.read_csv('data/inventario.csv')
df = df[df.status == 'For Sale']

'''
Las siguientes funciones se utilizan para la preparación de datos con el fin de mostrarlos en el entorno gráfico.
Tenemos varias funciones de preparación y de display de diferentes tipos de gráficos.
'''

# La siguiente función permite que cuando se inicia el st tener un dato actualizado del inventario que estamos manejando
def tamaño_inventario_venta ():
    df = pd.read_csv('data/inventario.csv')
    df = df[df.status == 'For Sale']
    return(len(df))

def tamaño_inventario_vendido():
    df = pd.read_csv('data/inventario.csv')
    df = df[df.status == 'Sold']
    return (len(df))

def graficazo():
    # Obtener los 10 artistas y sellos discográficos más frecuentes
    conteo_artistas = df['artist'].value_counts().head(11)
    top_10_artistas = conteo_artistas[1:]
    top_10_sellos = df['label'].value_counts().head(10)

    # Crear figura y ejes para el gráfico. Color del fondo
    fig, ax = plt.subplots(figsize=(10, 6))
    # fig.patch.set_facecolor('#fffef4')
    # ax.patch.set_facecolor('#fffef4')

    # Calcular el rango de valores para el eje y
    y_values = range(10)

    # Escalar los valores para el eje x proporcionalmente
    max_value = max(top_10_artistas.values.max(), top_10_sellos.values.max())
    scaled_artistas = top_10_artistas.values * max_value / top_10_artistas.values.max()
    scaled_sellos = top_10_sellos.values * max_value / top_10_sellos.values.max()

    # Graficar las barras de los artistas hacia la derecha
    bars_artistas = ax.barh(y_values, scaled_artistas, color='skyblue', align='center', label='Top 10 Artistas')

    # Graficar las barras de los sellos hacia la izquierda (negativo)
    bars_sellos = ax.barh(y_values, -scaled_sellos, color='salmon', align='center', label='Top 10 Sellos Discográficos')

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


def pie_chart():
    # Contar los valores 'Y' y 'N'
    counts = df['accept_offer'].value_counts()

    # Obtener los valores y etiquetas para el gráfico
    sizes = counts.values
    labels = counts.index

    # Crear la figura y los ejes
    fig, ax = plt.subplots()

    colors = ['skyblue', 'salmon']

    # pie chart con colores personalizados
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=50 )

    # Agregar un círculo blanco para crear el donut
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Ajustes
    ax.axis('equal')  # Asegurar que el gráfico sea circular
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()

def condition():
    # Calcular los porcentajes de valores únicos en cada columna
    media_percentages = df['media_condition'].value_counts(normalize=True) * 100
    sleeve_percentages = df['sleeve_condition'].value_counts(normalize=True) * 100
    sleeve_percentages = sleeve_percentages[:6]

    # Crear la figura y los ejes para los gráficos de barras paralelos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))

    # Graficar el primer gráfico de barras (media_condition) con porcentajes
    media_percentages.plot(kind='bar', ax=ax1, color='skyblue')
    ax1.set_title('Media Condition')

    # Añadir etiquetas de porcentaje en las barras
    for i, v in enumerate(media_percentages):
        ax1.text(i, v + 1, f'{v:.1f}%', ha='center')

    # Graficar el segundo gráfico de barras (sleeve_condition) con porcentajes
    sleeve_percentages.plot(kind='bar', ax=ax2, color='salmon')
    ax2.set_title('Sleeve Condition')

    # Añadir etiquetas de porcentaje en las barras
    for i, v in enumerate(sleeve_percentages):
        ax2.text(i, v + 1, f'{v:.1f}%', ha='center')

    # Rotar las etiquetas del eje x
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45, ha='right')
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45, ha='right')

    # Mostrar los gráficos
    plt.tight_layout()
    plt.show()

def format_string(string):
    CD = False
    vinyl = False
    single = False

    if 'CD' in string:
        CD = True
    elif '7' in string or 'Single' in string:
        single = True
    elif '12' in string or 'Maxi' in string:
        vinyl = True
    else:
        vinyl = True

    return CD, vinyl, single

def item_count_sale():

    df = pd.read_csv('data/inventario.csv')
    df = df[df.status == 'For Sale']    

    df[['CD', 'vinyl', 'single']] = df['format'].apply(lambda x: pd.Series(format_string(x)))
    df.drop('format', axis=1, inplace=True)

    format_counts = df[['CD', 'vinyl', 'single']].sum()

    plt.figure(figsize=(6, 4))
    ax = format_counts.plot(kind='bar', color=['skyblue', 'salmon', 'yellow'])

    plt.ylabel('Recuento')

    # Ocultar solo el eje Y
    plt.gca().get_yaxis().set_visible(False)

    # Convertir los nombres del índice a una lista de cadenas para usar en xticks
    labels = list(format_counts.index)

    # Mostrar el recuento en las barras
    for i, count in enumerate(format_counts):
        x = i
        y = count
        plt.text(x, y + 0.5, f'{count}', ha='center', va='bottom')

    plt.xticks(range(len(format_counts)), labels, rotation=0)
    plt.show()

def item_count_sold():

    df = pd.read_csv('data/inventario.csv')
    df = df[df.status == 'Sold']    

    df[['CD', 'vinyl', 'single']] = df['format'].apply(lambda x: pd.Series(format_string(x)))
    df.drop('format', axis=1, inplace=True)

    format_counts = df[['CD', 'vinyl', 'single']].sum()

    plt.figure(figsize=(6, 4))
    ax = format_counts.plot(kind='bar', color=['skyblue', 'salmon', 'yellow'])

    plt.ylabel('Recuento')

    # Ocultar solo el eje Y
    plt.gca().get_yaxis().set_visible(False)

    # Convertir los nombres del índice a una lista de cadenas para usar en xticks
    labels = list(format_counts.index)

    # Mostrar el recuento en las barras
    for i, count in enumerate(format_counts):
        x = i
        y = count
        plt.text(x, y + 0.5, f'{count}', ha='center', va='bottom')

    plt.xticks(range(len(format_counts)), labels, rotation=0)
    plt.show()