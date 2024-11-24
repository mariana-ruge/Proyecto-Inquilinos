# Proyecto Inquilinos
## Descripción
- Este proyecto evalúa la compatibilidad entre aspirante de inquilinos a un edificio, para ello usa un modelo que evalúa la similitud de las características e intereses de cada uno. Esto nos permite asignar mejor quien puede compartir cuarto en cada apartamento, y permite predecir como ubicarlos. Primero pregunta el ID de las personas que ya estan viviendo en el piso, y los evalua en la base de datos del CSV, compara los gustos dependiendo del ID seleccionado, y asigna otros inquilinos con gustos similares.
- Posteriormente genera una gráfica y una tabla para poder comparar los atributos.

## Estructura del proyecto
**app.py:**  Es la parte que controla la interfaz gráfica del proyecto, la cuál se maneja con streamlit.
* Tiene una advertencia sobre un comando anterior de Python, pero sin eso no funciona correctamente. Se podría actualizar en versiones futuras.

**ayudantes.py:** Contiene las funciones para generar los gráficos y tablas en la interfaz, recorre los objetos y los organiza para su correcta visualización.

**dataset_inquilinos.csv** Es el archivo en csv, que permite traer todos los datos de los inquilinos, y sus categorías.

**datos.ipynb**: Son unas pruebas de escritorio, sobre como se estaban mostrando y manejando los datos, para evitar errores de que no se encontraban las columnas, los datos, o que se estaba manipulando una columna que no existía. Puede ser usado para varias pruebas sobre el csv antes de modificarlo en el archivo .py

**lógica negocio.py**: Manipula y transforma los datos en el proyecto, para hacer los filtros y consultas correctamente, genera la matriz de similaridad entre los inquilinos y contiene la función que hace el cálculo de la compatibilidad, además de la media y los registros buscados y similares. Devuelve el resultado en una Pandas series. Usa numpy para que la matriz y sus valores esten en terminos de porcentajes de 0 a 100.

## Requisitos
- Python 3.x
- **Librerias: **
	- numpy, 
	- pandas, 
	- sklearn (scikit learn), 
	- seaborn,
	- plotly, 
	- matplotlib, 
	- y streamlit para que funcione en web.
- **Mas información de las librerias y paquetes instalados con sus versiones  en el archivo `requirements.txt`**
- Terminal unix, o powershell en windows.

## Uso
- Si quieres aportar o probar el proyecto, puedes hacerlo de la siguiente forma
1.  Clona el proyecto de forma local, con:

		 git clone https://github.com/mariana-ruge/Proyecto-Inquilinos

2.  Revisa que se hayan clonado bien los archivos descritos en la **Estructura del Proyecto.**
3. Abre tu terminal (powershell o linux) y ejecuta este comando
		 streamlit run 'ruta al app.py'
4. Esto comenzará a cargar el proyecto en streamlit te mostrará el puerto que esta usando y la url donde puedes ver la ejecución.
5. **Por el momento el proyecto recibe los inquilinos con un ID no con cadenas de texto, por la estructura del DataFrame que recibe como paramétro para hacer la visualización**
6. Mostrará una tabla con la compatibilidad y una gráfica para tomar mejores desiciones de a quien se va a asignar la habitación.
