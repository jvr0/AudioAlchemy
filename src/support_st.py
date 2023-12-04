import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('data/inventario.csv')
df = df[df.status == 'For Sale']

# La siguiente función permite que cuando se inicia el st tener un dato actualizado del inventario que estamos manejando
def tamaño_inventario ():
    df = pd.read_csv('data/inventario.csv')
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


def pie_chart():
    # Contar los valores 'Y' y 'N'
    counts = df.accept_offer.value_counts()

    # Obtener los valores y etiquetas para el gráfico
    sizes = counts.values
    labels = counts.index

    # Crear la figura y los ejes
    fig, ax = plt.subplots()

    # pie chart
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=50)

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

    # Mostrar los gráficos
    plt.tight_layout()
    plt.show()