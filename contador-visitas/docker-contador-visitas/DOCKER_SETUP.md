## Guía de Configuración de Docker
Este documento explica cómo configurar y ejecutar la aplicación de contador de visitas utilizando Docker, con un enfoque en el uso de los archivos Dockerfile y docker-compose.yml.

### Requisitos Previos 📋
Asegúrate de tener Docker y Docker Compose instalados en tu sistema.

### Construir y Ejecutar la Aplicación 🐳
La forma más sencilla de ejecutar esta aplicación es utilizando Docker Compose, que gestionará tanto la construcción de la imagen como la ejecución del contenedor.

#### 1. Navega al directorio raíz del proyecto. Asegúrate de que los archivos Dockerfile, docker-compose.yml, requirements.txt, app.py y start.sh estén en el mismo directorio.

#### 2. Inicia la aplicación con Docker Compose. Este comando leerá el archivo docker-compose.yml para construir la imagen (basada en el Dockerfile) y luego ejecutará el contenedor.


    docker-compose up


* El archivo docker-compose.yml utiliza la instrucción build: . para indicar que debe construir la imagen a partir del Dockerfile en el directorio actual.

* La instrucción ports: - "5000:5000" mapea el puerto 5000 del contenedor al puerto 5000 de tu máquina local.

* Si la imagen ya ha sido construida y no ha habido cambios en los archivos, Docker Compose reutilizará la imagen existente para mayor eficiencia.

#### 3. Para ejecutar la aplicación en segundo plano, añade el flag -d.

    docker-compose up -d 

#### 4. Para forzar la reconstrucción de la imagen, usa el flag --build. Esto es útil cuando has hecho cambios en el Dockerfile o en los archivos de la aplicación y quieres asegurarte de que se apliquen.
    docker-compose up --build

#### 5. Para detener la aplicación en ejecución, utiliza el siguiente comando:

    docker-compose down

### Detalles de la Configuración ⚙️
**Dockerfile: Este archivo es la receta para construir la imagen de Docker.**

* FROM python:3.9:  Define la imagen base.

* RUN apt-get install -y redis-server:  Instala Redis Server dentro del contenedor, lo que es necesario para que la aplicación funcione.

* WORKDIR /app:  Establece el directorio de trabajo dentro del contenedor.

* COPY requirements.txt . y RUN pip install -r requirements.txt: Copia el archivo de requisitos e instala las dependencias de Python.

* COPY . .: Copia todos los archivos del proyecto al contenedor.

* RUN chmod +x start.sh:  Hace que el script de inicio sea ejecutable.

* EXPOSE 5000:  Documenta que el contenedor expone el puerto 5000.

* CMD ["./start.sh"]:  Define el comando que se ejecuta cuando el contenedor se inicia, el cual inicia tanto Redis como la aplicación Flask.

        docker-compose.yml

**Este archivo es para orquestar los servicios. En este caso, define un único servicio llamado web.**

* version: "3.9":  Define la versión del formato de Docker Compose.

* services: web:  Define un servicio llamado web.

* build: .:  Indica a Docker Compose que debe construir la imagen para este servicio utilizando el Dockerfile en el directorio actual.

* ports: - "5000:5000":  Mapea los puertos para que la aplicación sea accesible desde el exterior del contenedor.

### Acceder a la Aplicación 🚀
Una vez que la aplicación esté en funcionamiento, abre tu navegador web y visita http://localhost:5000 para ver el contador de visitas.