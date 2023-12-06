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
    page_icon=":alembic:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Contraseña para acceder a la aplicación
password = st.secrets['password']  # contraseña

# Pide al usuario que ingrese la contraseña
password_placeholder = st.empty()
user_input = password_placeholder.text_input("Ingresa la contraseña:", type="password")

# Verifica si la contraseña ingresada es correcta
if user_input == password:
    # Elimina la celda de la contraseña si la contraseña es correcta
    password_placeholder.empty()
    size = tamaño_inventario_venta()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    

    # Display del panel de control
    def pagina_inicio():

        if 'programacion_activa' not in st.session_state:
            st.session_state['programacion_activa'] = False    
        # MURO 

        # PROGRAMAR ACTUALIZACIÓN

        st.write(f'## Programar actualización')

        # Widget para seleccionar la hora
        hora = st.slider("Selecciona la hora", 0, 23, 9)  # Valores de 0 a 23 para las horas

        def activar_programacion(hora):
            global programacion_activa
            schedule.every().day.at(f"{hora:02d}:00").do(lanzamiento_programado).tag(f"{hora}")

        def cancelar_programacion():
            global programacion_activa
            schedule.clear()

        if st.button(":green[Programar]"):
            activar_programacion(hora)
            st.session_state['programacion_activa'] = True

        if st.button(":red[Cancelar]"):
            cancelar_programacion()
            st.session_state['programacion_activa'] = False

        st.write(schedule.get_jobs())

        if st.session_state['programacion_activa']:
            st.write(f':green[Estado de la programación: {st.session_state["programacion_activa"]}]')
        else:
            st.write(f':red[Estado de la programación: {st.session_state["programacion_activa"]}]')

        st.write("---")

        # PROGRAMACIÓN POR CATEGORÍAS

        st.write(f'## Modificación de precios por categoría')

        df = pd.read_csv('data/inventario.csv')
        # Obtener las categorías únicas de las columnas 'label' y 'artist'
        
        df = df[df['status'] == 'For Sale']
        categorias = df.label.unique()
        artistas = df.artist.unique()

        # Selección de la categoría por el usuario
        categoria = st.selectbox('Selecciona el sello discográfico a actualizar', categorias)

        # Botón para ejecutar la modificación de precios
        if st.button(':green[Modificar precios a través de sello]'):
            resultado = lanzamiento_precio_resta_categoria(categoria)
            st.write(resultado)

        # Selección de la categoría por el usuario
        artista = st.selectbox('Selecciona el artista a actualizar', artistas)

        # Botón para ejecutar la modificación de precios
        if st.button(':green[Modificar precios a través de artista]'):
            resultado = lanzamiento_precio_resta_artista(artista)
            st.write(resultado) 

        st.write("---")

        # ACTUALIZAR AHORA

        st.write(f'## Actualizar ahora')

        paquete = st.number_input("Ingresa el tamaño del paquete a enviar (min 2)",
                                    value=2,
                                    min_value=2,
                                    max_value=size,
                                    step=1)
        st.write(f"El paquete que se enviará es de: {paquete}")

        if st.button (f':green[Actualizar sumando al precio]'):
                user = lanzamiento_precio_aumento(paquete)
                st.info(user)

        if st.button (f':green[Actualizar restando al precio]'):
                user = lanzamiento_precio_resta(paquete)
                st.info(user)


        while st.session_state['programacion_activa'] == True:
            schedule.run_pending()
            time.sleep(2)

    # Display de las estadísticas
    def statistics():
        global programacion_activa
        df = df = pd.read_csv('data/inventario.csv')
        df = df[df.status == 'For Sale']

        # tamaño y p medio
        size_venta = tamaño_inventario_venta()
        size_vendido = tamaño_inventario_vendido()
        mean = round(df.price.mean(), 2)
        st.write(f'#### Nº items a la venta: {size_venta}')
        st.write(f'#### Nº items vendidos: {size_vendido}')
        st.write(f'#### Precio medio del inventario: {mean}€')
        
        st.write('---')

        st.markdown('<div style="text-align: center; font-size: 24px;">Top 10 artistas y sellos por recuento de items </div>', unsafe_allow_html=True)
        graph = graficazo() # gráfico eje 0 artista/sello
        st.pyplot(graph)

        st.write('---')

        st.markdown('<div style="text-align: center; font-size: 24px;">Porcentajes de condición de los items </div>', unsafe_allow_html=True)
        condi = condition() # gráfico condición items
        st.pyplot(condi)

        st.write('---')
        
        st.markdown('<div style="text-align: center; font-size: 24px;">Porcentajes posibilidad de aceptar de oferta </div>', unsafe_allow_html=True)
        pie = pie_chart() # gráfico de donut
        st.pyplot(pie)

        st.write('---')

        st.markdown('<div style="text-align: center; font-size: 24px;">Recuento de tipo de items a la venta </div>', unsafe_allow_html=True)
        recuento_venta = item_count_sale() # gráfico barras de recuento venta
        st.pyplot(recuento_venta)

        st.write('---')

        st.markdown('<div style="text-align: center; font-size: 24px;">Recuento de tipos de items vendidos </div>', unsafe_allow_html=True)
        recuento_vendido = item_count_sold() # gráfico barras de recuento vendidos
        st.pyplot(recuento_vendido)

    # Display de la documentación
    def documentacion():
        global programacion_activa
        st.write('### API')

        st.write('##### Validación de la aplicación')
        st.write('El primer paso para utilizar la API es la creación de una aplicación en: [web developer Discogs](https://www.discogs.com/es/settings/developers "web developer Discogs"). A continuación, será necesario validar esta aplicación. Para obtener más información sobre cómo validar la aplicación, consulta el notebook [authorization](https://github.com/jvr0/AudioAlchemy/blob/main/notebooks/authorization.ipynb "authorization.ipynb"). Si necesitas más documentación sobre esta API, puedes encontrarla en el siguiente [enlace](https://www.discogs.com/developers/# "enlace"). A continuación, la estructura de la variable auth, necesaria para autentificarte cómo desarrollador de la app.')
        st.write("```python\noauth = OAuth1(\n        key,\n        client_secret=secret,\n        resource_owner_key=access_oauth_token,\n        resource_owner_secret=access_oauth_token_secret,\n        verifier=oauth_verifier)")
                
        st.write('##### Endpoints')
        st.write('Los endpoints utilizados para este proyecto son aquellos relacionados con el manejo y actualización del inventario. A continuación, se muestran ejemplos de uso. Para obtener más información sobre el uso de estos endpoints: [SRC](https://github.com/jvr0/AudioAlchemy/blob/main/src/support_API.py "SRC")')

        if st.button('Autorización'):
            st.write("```python\nurl = 'https://api.discogs.com/oauth/identity'\nres = req.get(url, auth=oauth)``` ")
                
        if st.button('Solicitud de inventario'):
            st.write("```python\nurl = 'https://api.discogs.com/inventory/export'\nres = req.post(url, auth=oauth)``` ")
                
        if st.button('Descargar el último inventario'):
            st.write("```python\nurl = 'https://api.discogs.com/inventory/export'\nres = req.get(url, auth=oauth)\nurl_inv = res.json()['items'][-1]['download_url']\nres = req.get(url_inv, auth=oauth)\nzip_file = zipfile.ZipFile(io.BytesIO(res.content))\ncsv_file = zip_file.namelist()[0]\ncsv_data = zip_file.read(csv_file).decode('utf-8')``` ")
                
        if st.button('Actualizar inventario'):
            st.write("```python\nurl = 'https://api.discogs.com/inventory/upload/change'\ncsv_file_path = 'data/upload.csv'\nfiles = {'upload': ('upload.csv', open(csv_file_path, 'rb'), 'text/csv')}\nres = req.post(url, auth=oauth, files=files)``` ")

        st.write('##### Formato de archivos')
        st.write("Al recibir y enviar archivos a través de la API, se debe tener en cuenta lo siguiente:")
        st.write("1. El archivo recibido en el endpoint ```url = 'https://api.discogs.com/inventory/export'``` será un ZIP, por lo que es necesaria la librería ```zipfile``` para poder descomprimirlo y abrirlo.")
        st.write("2. El archivo enviado para actualizar archivos en el endpoint ```url = 'https://api.discogs.com/inventory/upload/change'``` debe ser un archivo CSV que haya sido previamente abierto en nuestro código.")
        st.write("3. El archivo CSV enviado debe seguir estrictamente el siguiente formato: ```listing_id,release_id,price```, siendo 'price' la columna que se desea modificar, entre las opciones que se pueden encontrar en la documentación de la propia API.")

        st.write('##### Flujo de datos')
        if st.button('Diagráma'):
            image = Image.open('img/diagrama.png')
            st.image(image, use_column_width=True)

        st.write('---')
        
        st.write('### Producción')
        st.write('Para la puesta en producción de este proyecto se ha optado por realizar el deploy utilizando las herramientas propias de [Streamlit](https://streamlit.io "Streamlit"). Esta plataforma permite una producción sencilla y gratuita donde presentar proyectos sin perder las funcionalidades que estos puedan tener en un despliegue local.')
        st.write('##### Streamlit Deploy')
        st.write("La puesta en producción ha seguido los pasos marcados por la propia plataforma, utilizando las herramientas que esta ofrece. Recodrdemos que nuestro objetivo era poder enviarle a nuestro cliente una url funcional donde él pudierá iniciar el programa desde su máquina. Para complir con esta propuesta se han hecho leves modificaciones en el código que permitan la funcionalidad online del programa. Algunas de estas moficiaciones han sido: cambio de rutas o leves cambios en la configuración de las funciones.")
        st.write("**Seguridad y Secretos** Debido al carácter privado de este proyecto se ha buscado la implementación de dos tipos de seguridad. En primer lugar se ha utilizado, en la creación del streamlit, el uso de una contraseña para permitir al usuario el acceso a la información y funcionalidad. Y, en segundo lugar, se ha utilizado el apartado de secretos ofrecido por streamlit para el almacenamiento de los tokens necesarios por la API.")
        st.write("**Ejecutable** Por último se ha utilizado la herramienta nativefier para la creación de un ejecutable fácilmente transferible. Se ha añadido el logotipo del proyecto y se han creado versiones tanto para Mac como para Windows.")

        st.write('---')

        st.write('### Next Steps')
        st.write('1. Mejoras de seguridad.')
        st.write('2. Mejoras de funcionalidad y calidad visual.')
        st.write('3. Creación de una base de datos en la nube.')
        st.write('4. Posibilidad de construir una interfaz gráfica local.')
        st.write('5. Puesta en producción con AWS.')
    
    # Display del manual para usuario
    def manual():
        global programacion_activa
        st.write('# Manual de uso')
        st.write('Para la correcta utilización de este software es necesario tener en cuenta las siguientes cuestiones:')
        st.write('1. Los inventarios se actualizan de forma dinámica dentro de la memoria de la web. Esto es, se necesita actualizar el inventario a través del botón ```Preparar descarga inventario``` para operar con el inventario actualizado.') 
        st.write('2. Cuando se realizan actualizaciones programadas no es necesario actualizar el inventario. Se realiza de forma automática a través de la función escrita.')
        st.write('3. El tamaño del paquete enviado hace referencia a los items aleatorios que se seleccionarán para su actualización en Discogs. Darle a este parámetro la totalidad del inventario selecciona todos los items.')
        st.write('4. El funcionamiento de las actualizaciones programadas sigue una lógica de azar para seleccionar el tipo de envió. Selecciona a un 50/50 de probabilidades si suma o resta al precio, con el tiempo se estabilizará dejando el precio inalterado pero con los productos actualizados.')
        st.write('5. Aunque nuestra plataforma realiza el procesamiento y envio de datos en un corto periodo de tiempo (45-90 segundos) es necesario tener en cuenta que Discogs también debe realizar su propio procesamiento. Esto se debe tener en consideración a la hora de programar actualizaciones.')
        st.write('---')
        st.write('Para más información sobre el funcionamiento de la aplicación referirse a los links presentados en la barra lateral.')

    # ICONO

    icono = Image.open('img/icono.png')
    st.sidebar.image(icono, width=100)

    st.sidebar.write('---')

    size = tamaño_inventario_venta()
    st.sidebar.write(f'### Tamaño inventario: {size}')


    # CONTROL DEL INVENTARIO

    if st.sidebar.button(':orange[Pedir nuevo inventario a discogs]'):
        new = nuevo_inventario()
        st.sidebar.info(new)

    if st.sidebar.button(':orange[Preparar descarga inventario]'):
        descarga_inventario()
        csv_content = descarga_streamlit()    
        size = tamaño_inventario_venta()
        st.sidebar.write(f'### Tamaño actualizado {size}')
        if csv_content:
            st.sidebar.download_button(label=':blue[Descargar inventario]', data=csv_content, file_name='inventario.csv', mime='text/csv')
            st.sidebar.info('Inventario descargado correctamente')
        else:
            st.sidebar.warning('Hubo un problema al descargar el inventario')

    st.sidebar.write('---')

    # NAVEGACIÓN

    # opciones display
    opciones = {
        "Inicio": pagina_inicio,
        "Estadísticas": statistics,
        "Documentacion": documentacion,
        "Manual": manual,
    }

    # Navegación
    st.sidebar.write("## Navegación")
    opcion_seleccionada = st.sidebar.radio("Ir a", list(opciones.keys()))

    # Display pagina seleccionada
    if opcion_seleccionada in opciones:
        opciones[opcion_seleccionada]()

    # LINKS

    st.sidebar.write('---')

    if st.sidebar.button(':blue[Personal Links]'):
        st.sidebar.write('https://github.com/jvr0')
        st.sidebar.write('https://www.linkedin.com/in/joaquín-villaverde-roldán-4b9803230')
        st.sidebar.write('https://github.com/jvr0/AudioAlchemy')




elif user_input != "" and user_input != password:
    st.error("Contraseña incorrecta. Por favor, intenta nuevamente.")