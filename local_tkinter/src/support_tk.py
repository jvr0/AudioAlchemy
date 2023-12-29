import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('utopia/data/inventario.csv')

def tamaño_inventario_venta():
    df = pd.read_csv('utopia/data/inventario.csv')
    df = df[df.status == 'For Sale']
    return len(df)

def tamaño_inventario_vendido():
    df = pd.read_csv('utopia/data/inventario.csv')
    df = df[df.status == 'Sold']
    return len(df)


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
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=50)

    # Agregar un círculo blanco para crear el donut
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig.gca().add_artist(centre_circle)

    # Ajustes
    ax.axis('equal')  # Asegurar que el gráfico sea circular
    plt.tight_layout()

    # Retornar la figura en lugar de mostrarla
    return fig
 