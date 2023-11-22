# discogs

### 1. acceder al token

Necesario key y secret(contraseña).
    opción1: Enviar correo para la obtención
    opción2: /settings/developer

Aplicar key y secret a mi llamada para autentificarme antes de trabajar.

### 2. test de las posibilidades

Actualización del inventario: 
endpoint de change_inventory: get.post(url/inventory/upload/change)

importante a tener en cuenta:
- se actualizará en base a coincidencia con release_id
- nombre columnas específico
- Los items cambiados se pondrán automáticamente en estado 'for sale'.
-La información de la moneda será obtenida de nuestros ajustes del marketplace (Entiendo que si tenemos marketplace situado en europa nos pondrá la currenci en euro)

Si esto no funcionará para refrescar los items se pasaría a trabajar con los enpoints de upload y delete:
- /inventory/upload/add
- /inventory/upload/delete

### 3. creación de la app

Hasta aquí se ha trabajado exclusivamente con código. El siguiente paso sería la creación de una interfaz gráfica que conectará el código para la actualización (backend) con un una interfaz que permita establecer parámetros: 
- cambios simples en los items
- pedirle que lo haga cada x tiempo
- pedirle que arranque a una determinada hora
- surgirán otros

### 4. next_steps

Establecer una página web propia conectada a través de la API con Discogs