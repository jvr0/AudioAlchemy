from altair import SelectionPredicateComposition
import streamlit as st
import pandas as pd
import schedule
import time
from PIL import Image
import webbrowser
import base64
import io

from src.support_API import *
from src.support_st import *


# CONFIG INICIAL
st.set_page_config(
    page_title="AudioAlchemy",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",)

# Contraseña para acceder a la aplicación
password = "Spyro190"  # contraseña

# Pide al usuario que ingrese la contraseña
password_placeholder = st.empty()
user_input = password_placeholder.text_input("Ingresa la contraseña:", type="password")

# Verifica si la contraseña ingresada es correcta
if user_input == password:
    # Elimina la celda de la contraseña si la contraseña es correcta
    password_placeholder.empty()
    size = tamaño_inventario()
    st.set_option('deprecation.showPyplotGlobalUse', False)

    def pagina_inicio():

        # MURO

        paquete = st.number_input("Ingresa el tamaño del paquete a enviar (min 2)",
                                    value=2,
                                    min_value=2,
                                    max_value=size,
                                    step=1)
        st.write(f"El paquete que se enviará es de: {paquete}")

        st.write("---")

        # PROGRAMAR ACTUALIZACIÓN

        st.write(f'### Programar actualización')

        # Widget para seleccionar la hora
        hora = st.slider("Selecciona la hora", 0, 23, 9)  # Valores de 0 a 23 para las horas

        programacion_activa = False

        def activar_programacion(hora, paquete):
            global programacion_activa
            schedule.every().day.at(f"{hora:02d}:00").do(lanzamiento_programado, paquete).tag(f"{hora}")

        def cancelar_programacion():
            global programacion_activa
            schedule.clear()

        if st.button(":green[Programar]"):
            activar_programacion(hora, paquete)
            programacion_activa = True

        if st.button(":red[Cancelar]"):
            cancelar_programacion()
            programacion_activa = False

        st.write(schedule.get_jobs())

        if programacion_activa == True:
            st.write(f':green[Estado de la programación: {programacion_activa}]')
        else:
            st.write(f':red[Estado de la programación: {programacion_activa}]')

        st.write("---")

        # PROGRAMACIÓN POR CATEGORÍAS

        st.write(f'### Modificación de precios por categoría')

        df = pd.read_csv('data/inventario.csv')
        # Obtener las categorías únicas de las columnas 'label' y 'artist'
        
        # df[df['status'] == 'For Sale']
        categorias = df.label.unique()
        artistas = df.artist.unique()

        # Selección de la categoría por el usuario
        categoria = st.selectbox('Selecciona el sello discográfico a actualizar', categorias)

        # Botón para ejecutar la modificación de precios
        if st.button('Modificar precios a través de sello'):
            resultado = lanzamiento_precio_resta_categoria(categoria)
            st.write(resultado)

        # Selección de la categoría por el usuario
        artista = st.selectbox('Selecciona el artista a actualizar', artistas)

        # Botón para ejecutar la modificación de precios
        if st.button('Modificar precios a través de artista'):
            resultado = lanzamiento_precio_resta_artista(artista)
            st.write(resultado) 

        st.write("---")

        # ACTUALIZAR AHORA

        st.write(f'### Actualizar ahora')

        if st.button (f':green[Actualizar sumando al precio]'):
                user = lanzamiento_precio_aumento(paquete)
                st.info(user)

        if st.button (f':green[Actualizar restando al precio]'):
                user = lanzamiento_precio_resta(paquete)
                st.info(user)

        # Estado de la programación y ejecutar tareas programadas
        while True:
            if programacion_activa == True:
                schedule.run_pending()  # Ejecutar tareas programadas
                time.sleep(2)
            else:
                time.sleep(2)

    def statistics():
        df = df = pd.read_csv('data/inventario.csv')
        df = df[df.status == 'For Sale']

        st.title("Estadísticas")

        size = tamaño_inventario()
        mean = round(df.price.mean(), 2)
        st.write(f'#### Tamaño inventario: {size}')
        st.write(f'#### Precio medio del inventario: {mean}€')
        
        st.write(f'#### Top 10 artistas y sellos por recuento de items:')
        graph = graficazo()
        st.pyplot(graph)

        st.write(f'#### Porcentajes de condición de los items:')
        condi = condition()
        st.pyplot(condi)
        
        st.write(f'#### Porcentajes posibilidad de aceptar de oferta:')
        pie = pie_chart()
        st.pyplot(pie)

    def documentacion():
        st.write('### API')
        
        st.write('##### Validación app')
        st.write('El primer paso para la utilización de la api es la creación de una app en la: [web developer Discogs](https://www.discogs.com/es/settings/developers "web developer Discogs"). A continuación será necesario validar esta APP. Para mayor información de cómo validar la app ver el notebook [authorization](https://github.com/jvr0/AudioAlchemy/blob/main/notebooks/authorization.ipynb "authorization.ipynb"). Si fuera necesaria más documentación sobre esta API se puede encontrar en el siguiente [enlace](https://www.discogs.com/developers/# "enlace"). A continuación la estructura de la variable auth:')
        st.write("```python\noauth = OAuth1(\n        key,\n        client_secret=secret,\n        resource_owner_key=access_oauth_token,\n        resource_owner_secret=access_oauth_token_secret,\n        verifier=oauth_verifier)")
        
        st.write('##### Endpoints')
        st.write('Los endpoints utilizados para este proyecto son aquellos relacionados con el manejo y actualización del inventario. A continuación los ejemplos de uso. Para más información sobre el uso de los endpoints: [SRC](https://github.com/jvr0/AudioAlchemy/blob/main/src/support_API.py "SRC")')
        
        if st.button('Autorización'):
            st.write("```python\nurl = 'https://api.discogs.com/oauth/identity'\nres = req.get(url, auth=oauth)``` ")
        
        if st.button('Solicitud inventario'):
            st.write("```python\nurl = 'https://api.discogs.com/inventory/export'\nres = req.post(url, auth=oauth)``` ")
        
        if st.button('Descarga último inventario'):
            st.write("```python\nurl = 'https://api.discogs.com/inventory/export'\nres = req.get(url, auth=oauth)\nurl_inv= res.json()['items'][-1]['download_url']\nres = req.get(url_inv, auth=oauth)\nzip_file = zipfile.ZipFile(io.BytesIO(res.content))\ncsv_file = zip_file.namelist()[0]\ncsv_data = zip_file.read(csv_file).decode('utf-8')``` ")
        
        if st.button('Actualización inventario'):
            st.write("```python\nurl = 'https://api.discogs.com/inventory/upload/change'\ncsv_file_path = 'data/upload.csv'\nfiles = {'upload': ('upload.csv', open(csv_file_path, 'rb'), 'text/csv')}\nres = req.post(url, auth=oauth, files=files)``` ")

        st.write('##### Formato Archivos')
        st.write("A la hora de la recepción y envío de archivos en la API se debe tener en cuenta lo siguiente:")
        st.write("1. El archivo recibido en el endpoint ```url = 'https://api.discogs.com/inventory/export'``` será un ZIP, por lo que es necesaria la librería ```zipfile``` para poder descomprimirlo y abrirlo.")
        st.write("2. El archivo enviado para actualizar archivos al endpoint ```url = 'https://api.discogs.com/inventory/upload/change'``` debe ser un csv que previamente haya sido abierto en nuestro código.")
        st.write("3. El archivo csv enviado requería que se siguiera estrictamente el siguiente formato ```listing_id,release_id,price``` siendo price la columna que se desea modificar entre las opciones que se pueden encontrar en la documentación de la propia API.")
        
        if st.button('Flujo de datos'):
            image = Image.open('img/diagrama.png')
            st.image(image, use_column_width=True)
        
        st.write('### Producción')
        st.write('Para la puesta en producción de este proyecto se ha optado por seguir dos caminos. El primero, el deploy nativo que podemos encontrar en todas las web creadas con [Streamlit](https://streamlit.io "Streamlit"). Y, el segundo, la puesta en producción ofrecida por AWS utilizando su capa gratuita para el producto [Amazon EC2 (Elastic Compute Cloud)](https://aws.amazon.com/es/ec2/ "Amazon EC2 (Elastic Compute Cloud)")')
        st.write('##### Streamlit Deploy')
        st.write("Nuestro primer proceso en la puesta en producción se ha llevado a cabo utilizando la propia funcionalidad de streamlit para este proceso. Nuestro objetivo era poder enviarle a nuestro cliente una url funcional donde el pudierá iniciar el programa desde su máquina. Para complir con esta propuesta se han hecho leves modificaciones en el código que permitan la funcionalidad online del programa. Algunas de estas moficiaciones han sido: cambio de rutas o leves cambios en la configuración de las funciones.")
        st.write('###### Seguridad y Secretos')
        st.write("Debido al carácter privado de este proyecto se ha buscado la implementación de dos tipos de seguridad. En primer lugar se ha utilizado, en la creación del streamlit, el uso de una contraseña para permitir al usuario el acceso a la información y funcionalidad. Y, en segundo lugar, se ha utilizado el apartado de secretos ofrecido por streamlit para el almacenamiento de los tokens necesarios por la API.")
        st.write('###### Ejecutable')
        st.write("Por último se ha utilizado la herramienta nativefier para la creación de un ejecutable fácilmente transferible. Se ha añadido el logotipo del proyecto y se han creado versiones tanto para Mac como para Windows.")
        st.write('##### AWS')

        st.write('### Next Steps')

    def manual():
        st.write('# Manual de uso')
        st.write('Para la correcta utilización de este software es necesario tener en cuenta las siguientes cuestiones:')
        st.write('1. Los inventarios se actualizan de forma dinámica dentro de la memoria de la web. Esto es, se necesita actualizar el inventario a través del botón ```Preparar descarga inventario``` para operar con el inventario actualizado.') 
        st.write('2. Cuando se realizan actualizaciones programadas no es necesario actualizar el inventario. Se realiza de forma automática a través de la función escrita.')
        st.write('3. El tamaño del paquete enviado hace referencia a los items aleatorios que se seleccionarán para su actualización en Discogs. Darle a este parámetro la totalidad del inventario selecciona todos los items.')
        st.write('4. El funcionamiento de las actualizaciones programadas sigue una lógica de azar para seleccionar el tipo de envió. Selecciona a un 50/50 de probabilidades si suma o resta al precio, con el tiempo se estabilizará dejando el precio inalterado pero con los productos actualizados.')

    # NAVEGACIÓN SIDEBAR

    st.sidebar.title('AudioAlchemy')
    
    if st.sidebar.button(':blue[Personal Links]'):
        st.sidebar.write('[Git](https://github.com/jvr0)"Git"')
        st.sidebar.write('[Linkedin](https://www.linkedin.com/in/joaquín-villaverde-roldán-4b9803230)"Linkedin"')
        st.sidebar.write('[Repositorio](https://github.com/jvr0/AudioAlchemy)"Repositorio"')
    
    size = tamaño_inventario()
    st.sidebar.write(f'### Tamaño inventario: {size}')

    if st.sidebar.button(':orange[Pedir nuevo inventario a discogs]'):
        new = nuevo_inventario()
        st.sidebar.info(new)


    if st.sidebar.button(':orange[Preparar descarga inventario]'):
        descarga_inventario()
        csv_content = descarga_streamlit()    
        size = tamaño_inventario()
        st.sidebar.write(f'### Tamaño actualizado {size}')
        if csv_content:
            st.sidebar.download_button(label=':blue[Descargar inventario]', data=csv_content, file_name='inventario.csv', mime='text/csv')
            st.sidebar.info('Inventario descargado correctamente')
        else:
            st.sidebar.warning('Hubo un problema al descargar el inventario')

    # Sidebar navigation
    opciones = {
        "Inicio": pagina_inicio,
        "Estadísticas": statistics,
        "Documentacion": documentacion,
        "Manual": manual,
    }

    # Sidebar navigation selection
    st.sidebar.write("## Navegación")
    opcion_seleccionada = st.sidebar.radio("Ir a", list(opciones.keys()))

    # Display the selected page
    if opcion_seleccionada in opciones:
        opciones[opcion_seleccionada]()



elif user_input != "" and user_input != password:
    st.error("Contraseña incorrecta. Por favor, intenta nuevamente.")