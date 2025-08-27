

## 🐳✨ Guía de Configuración de Docker y Split (Feature Flags)
Este documento explica cómo configurar y ejecutar la aplicación de contador de visitas utilizando Docker, y cómo integrar correctamente el SDK de Split para feature flags, siguiendo buenas prácticas de portabilidad y simulación de usuarios.



### 📋 Requisitos Previos
- 🐳 Docker y Docker Compose instalados en tu sistema.
- 🪄 Acceso a una cuenta de Split.io y una API Key de SDK para el ambiente de pre-producción.


---


---

## 🚩 Problemáticas y Buenas Prácticas Abordadas


### 1️⃣ Configuración del entorno Split y elección de la API Key
- 🔑 Ingresa a Split.io y copia la API Key del SDK correspondiente al ambiente de pre-producción (no uses la de producción ni la de test).
- 🚫 No incluyas la API Key directamente en el código fuente.
- 📄 Guarda la API Key en el archivo `.env` como:
  
    SPLIT_API_KEY=tu_api_key_de_split


### 2️⃣ Uso de variables de entorno para portabilidad
- 🌍 El archivo `app.py` obtiene la API Key de Split desde la variable de entorno `SPLIT_API_KEY`.
- 🔄 Esto permite cambiar de ambiente o de key sin modificar el código, solo editando el archivo `.env`.


### 3️⃣ Librería adecuada y configuración de dependencias
- 📦 Se utiliza la librería oficial `splitio-client` para Python, declarada en `requirements.txt`.
- 🛠️ El `Dockerfile` y `docker-compose.yml` están configurados para instalar y exponer correctamente las dependencias y variables de entorno.


### 4️⃣ Simulación de visitantes distintos
- 👥 Para simular diferentes usuarios y ver el A/B testing, accede a la app con URLs como:
  
      🌐 http://localhost:5000/?key=usuario1
      🌐 http://localhost:5000/?key=usuario2
      ...
      🌐 http://localhost:5000/?key=usuario10

  🔄 Cada key simula un usuario distinto y Split asignará el tratamiento correspondiente.


### 5️⃣ Mantener el usuario en la navegación interna
- 🔗 La app propaga el parámetro `key` en todos los enlaces internos (reiniciar, health, volver), de modo que el usuario simulado no cambia al navegar por la app.
- 🟢🔴 Así, siempre verás el mismo tratamiento (feature on/off) para el usuario seleccionado.

---


---

### 📁 Paso 6: Navega al directorio raíz del proyecto
Asegúrate de que los archivos Dockerfile, docker-compose.yml, requirements.txt, app.py y start.sh estén en el mismo directorio.



### ▶️ Paso 7: Inicia la aplicación con Docker Compose
Este comando leerá el archivo docker-compose.yml para construir la imagen (basada en el Dockerfile) y luego ejecutará el contenedor:

    🚀 docker-compose up

* 🏗️ El archivo docker-compose.yml utiliza la instrucción `build: .` para indicar que debe construir la imagen a partir del Dockerfile en el directorio actual.
* 🔌 La instrucción `ports: - "5000:5000"` mapea el puerto 5000 del contenedor al puerto 5000 de tu máquina local.
* ♻️ Si la imagen ya ha sido construida y no ha habido cambios en los archivos, Docker Compose reutilizará la imagen existente para mayor eficiencia.


### 💤 Paso 8: Ejecuta en segundo plano (opcional)

    docker-compose up -d

### 🔄 Paso 9: Fuerza la reconstrucción de la imagen (opcional)
Esto es útil cuando has hecho cambios en el Dockerfile o en los archivos de la aplicación y quieres asegurarte de que se apliquen.

    docker-compose up --build

### 🛑 Paso 10: Detén la aplicación

    docker-compose down



---

### ⚙️ Detalles de la Configuración
**📝 Dockerfile:**

* 🐍 `FROM python:3.9`:  Define la imagen base.
* 📂 `WORKDIR /app`:  Establece el directorio de trabajo dentro del contenedor.
* 📦 `COPY requirements.txt .` y `RUN pip install -r requirements.txt`: Copia el archivo de requisitos e instala las dependencias de Python, incluyendo `splitio-client`.
* 📁 `COPY . .`: Copia todos los archivos del proyecto al contenedor.
* 🔒 `RUN chmod +x start.sh`:  Hace que el script de inicio sea ejecutable.
* 🌐 `EXPOSE 5000`:  Documenta que el contenedor expone el puerto 5000.
* 🏁 `CMD ["./start.sh"]`:  Define el comando que se ejecuta cuando el contenedor se inicia, el cual inicia la aplicación Flask.

**docker-compose.yml:**

* `version: "3.9"`:  Define la versión del formato de Docker Compose.
* `services`: Define los servicios `web` (la app Flask) y `redis` (la base de datos en memoria).
* `build: .`:  Indica a Docker Compose que debe construir la imagen para este servicio utilizando el Dockerfile en el directorio actual.
* `ports: - "5000:5000"`:  Mapea los puertos para que la aplicación sea accesible desde el exterior del contenedor.
* `env_file: - .env`:  Carga las variables de entorno, incluyendo la API Key de Split.
* `depends_on: - redis`:  Asegura que Redis esté disponible antes de iniciar la app.


### Acceder y Probar la Aplicación 🚀
Una vez que la aplicación esté en funcionamiento, abre tu navegador web y visita:

    http://localhost:5000/?key=usuario1

Puedes cambiar el valor de `key` en la URL para simular distintos usuarios y ver el comportamiento del feature flag (A/B testing). Navega por las rutas internas (reiniciar, health, volver) y verás que el usuario simulado se mantiene.