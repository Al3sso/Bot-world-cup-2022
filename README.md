# Bot del mundial 2022 Python

## Este bot te permitira saber todo lo referente al mundial Qatar 2022, ya sea partidos, clasificación de equipos, puntajes, etc.

Para utilizar el bot requiere seguir unos sencillos pasos de instalación que serán descritos a continuación.
---

#### Comandos del bot:
`/calc`: Para realizar operaciones matematicas sencillas deberá colocar el primer conjunto de numeros seguido de el signo de la operación que desea realizar y por ultimo el segundo conjunto de números.

`/pais`: Muestra información detallada del país que busque.

`/registro`: Este comando sirve para registrar tu usuario y el orden es: 'Usuario' 'correo' 'contraseña' 'confirmar contraseña'.

`/usuario`: Te mostrará el nombre de tu usuario.

`/eliminar`: Escriba el nombre de usuario que desea eliminar.

`/iniciar`: Luego de registrar tu usuario, este comando servira para poder utilizar todas las funciones del bot.

`/equipo`: Deberá colocar el nombre del país en inglés inmediatemente después de escribir el comando. Mostrará la 
información del equipo.

`/partidos`: Deberá colocar el nombre del país en inglés inmediatemente después de escribir el comando. Mostrará los siguientes 3 partidos del equipo.

`/grupo`: Deberá colocar el nombre del país en inglés inmediatemente después de escribir el comando. Muestra la información detallada del grupo.

`/help`: Guía de uso del bot.

***

## Todo lo necesario para instalar el bot:

#### Windows:

*   Para abrir los archivos necesitará un editor de código, existen muchas opciones y alternativas como Sublime Text o  Visual Studio Code. Vale la pena aclarar que este bot fue hecho en Visual Studio Code por lo que recomiendo utilizar este editor de código.	

*	Instalar Python, podra encontrar la versión mas reciente en: ( https://www.python.org/downloads/).

*	Para poder gestionar nuestra base de datos utilizaremos la extensión SQLITE que encontrará en el apartado de extensiones en la barra lateral izquierda de su Visual Studio Code.

*	Descarga Git para Windows, este te permitirá clonar el código más adelante; descárgalo a través de su web oficial: ( https://gitforwindows.org/).

## Dependencias necesarias para el bot:
*   os

*   json

*   sqlite3

*   PIL (https://pypi.org/project/Pillow/)

*   table2ascii (https://pypi.org/project/table2ascii/)

*   extcolors (https://pypi.org/project/extcolors/)

*   Discord (https://discordpy.readthedocs.io/en/stable/intro.html)

Para instalar las dependencia solo debe abrir el terminal de su Visual Studio Code el cual se encuentra en la franja inferior izquierda, click en los íconos que aparecen ahí y le saldrá un recuadro con multiples opciones. Haga click en terminal y posteriormente pegue los arhivos PIP que aparecerán en el inicio de las páginas que se mencionaron anteriormente.


#### Descargar el código:

1.	Crea una carpeta y ábrela con Visual Studio Code.
2.	En el terminal de VSCODE copia el siguiente comando:

`git clone https://github.com/Storgaro/python-bot`

Posteriormente da enter en _SI_ y espera a que la descarga de todos los archivos termine. ***Es necesario que deje su terminal abierto y siga con los siguientes pasos***

#### Configuración del Bot 

1.	En tu buscador de preferencia dirígete a la página de [Discord developer]( https://discord.com/developers/applications.).
2.	Clickea en el botón de **New Application**


3.	Posteriormente coloca el nombre que gustes a tu **Servidor de Discord**
4.	En el menu de la izquierda selecciona la pestaña de Bot.


5.	Daremos click donde dice **Add Bot**


6.	En este apartado daremos nombre al Bot y daremos click en el botón de **Reset Token**.


7.	Copiaremos el nuevo **Token** dado por el Bot y lo reservaremos para más adelante.

#### Creando el URL para añadir el bot al servidor:

1.	Nos dirigimos al menú del lado izquierdo y presionaremos la opción **OAuth2**; Copiaremos el **Cient ID** y lo reservaremos para más adelante.



2.	Daremos click al **URL GENERTOR** y seleccionaremos las opciones de **bot** y **applications.commands**


3.	Posteriormente marcaremos las casillas de los permisos y le daremos en siguiente.


4.	Copiaremos el **URL** que nos da al final y lo pegaremos en el navegador. Este traerá un menú de Discord y nos preguntará a que servidor queremos añadir el bot. Aquí seleccionaremos el servidor que creamos hace un momento y daremos **Confirmar**.



Por último, ya tenemos el bot dentro de nuestro servidor y ahora procederemos a activar sus funciones.

#### Configuración del bot:

Primero, deberá completar su archivo **.env**. Aquí deberá agregar su **token del bot y la ID de cliente para el bot**.

### Poner a funcionar el Bot:

En su terminal escriba el siguiente comando:

`py (seguido del nombre de su archivo .py). Ejemplo: py bot.py`

Posteriormente presione **Enter** y disfrute de todas las opciones y comandos que este bot le ofrece.
