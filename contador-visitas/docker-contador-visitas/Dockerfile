# Usa una imagen oficial de Python como base
FROM python:3.9

# Instala dependencias del sistema necesarias para compilar paquetes Python
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias y las instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de la aplicación
COPY . .

# Da permisos de ejecución al script de inicio
RUN chmod +x start.sh

# Expone el puerto 5000 para acceder a la app Flask
EXPOSE 5000

# Comando por defecto para iniciar la aplicación
CMD ["./start.sh"]
