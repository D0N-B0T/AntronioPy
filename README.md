# AntronioPy

AntronioPy es una librería de Python que permite conectarse y hacer solicitudes a foros con el sistema de gestión de contenidos (CMS) Xenforo, en particular el foro Antronio.cl. La librería utiliza las bibliotecas requests y BeautifulSoup para hacer solicitudes y analizar el HTML de las respuestas.


## Uso básico

Para usar AntronioPy, primero se debe crear una instancia de la clase AntronioSession con un nombre de usuario y contraseña válidos:

```python
Copy code
from antroniopy import AntronioSession

username = "tu_usuario"
password = "tu_contraseña"

session = AntronioSession(username, password)
```

Después de crear la instancia, se puede hacer solicitudes al foro con el método session.session.get(url) o session.session.post(url, data):

```python
url = "https://www.antronio.cl/foro/"

response = session.session.get(url)
soup = BeautifulSoup(response.text, "html.parser")
```

# Ejemplos
## Obtener nuevos temas del foro

Este ejemplo muestra cómo se puede utilizar AntronioPy para obtener los títulos de los temas más recientes del foro Antronio y guardarlos en una base de datos SQLite. Si se ejecuta el script varias veces, solo se imprimirán los títulos de los temas nuevos desde la última vez que se ejecutó el script.

```python
from antroniopy import AntronioSession

username = "tu_usuario"
password = "tu_contraseña"
forum_url = "https://www.antronio.cl/foro/"

session = AntronioSession(username, password)

session.check_for_new_threads(forum_url)
```
## Publicar en el perfil de usuario

Este ejemplo muestra cómo se puede utilizar AntronioPy para publicar un mensaje en el perfil de un usuario en el foro Antronio.

```python
from antroniopy import AntronioSession

username = "tu_usuario"
password = "tu_contraseña"
message = "Hola mundo desde AntronioPy!"

session = AntronioSession(username, password)

response = session.post_on_profile(message)
if response.status_code == 200:
    print("El mensaje se publicó correctamente en tu perfil.")
else:
    print("No se pudo publicar el mensaje en tu perfil.")
```
## Contribuciones

Si deseas contribuir a AntronioPy, ¡no dudes en abrir un Pull Request! Agradecemos cualquier contribución, desde informes de errores hasta mejoras de documentación y nuevas funciones.

