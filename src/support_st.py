import pandas as pd

# La siguiente función permite que cuando se inicia el st tener un dato actualizado del inventario que estamos manejando
def tamaño_inventario ():
    df = pd.read_csv('../data/inventario.csv')
    df = df[df.status == 'For Sale']
    return(len(df))

