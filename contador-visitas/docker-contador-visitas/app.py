# --- Importación de librerías principales ---
from flask import Flask, request  # Framework web para Python
import redis  # Cliente para conectarse a Redis
import time   # Para manejar esperas/reintentos
import os     # Para acceder a variables de entorno
from splitio import get_factory  # SDK de Split para feature flags

# --- Inicialización de la aplicación Flask ---
app = Flask(__name__)

# --- Obtiene la API Key de Split desde las variables de entorno ---
SPLIT_API_KEY = os.environ.get("SPLIT_API_KEY")
if not SPLIT_API_KEY:
    raise ValueError("La variable de entorno SPLIT_API_KEY no está configurada. Por favor, asegúrate de que esté en tu archivo .env.")

# --- Inicializa el SDK de Split y espera a que esté listo ---
FACTORY = get_factory(SPLIT_API_KEY)
FACTORY.block_until_ready() 

# --- Espera a que el servicio de Redis esté disponible antes de continuar ---
def wait_for_redis():
    max_retries = 10
    retry_delay = 1
    for i in range(max_retries):
        try:
            # Intenta conectarse a Redis (host 'redis' por docker-compose)
            redis_client = redis.Redis(host='redis', port=6379, db=0)
            redis_client.ping()
            print("✅ Redis conectado exitosamente")
            return redis_client
        except redis.ConnectionError:
            print(f"⏳ Esperando por Redis... ({i+1}/{max_retries})")
            time.sleep(retry_delay)
    raise Exception("❌ No se pudo conectar a Redis")

# --- Ruta principal: muestra el contador de visitas y aplica lógica de feature flag con Split ---
@app.route('/')
def contador_visitas():
    try:
        # Espera y obtiene el cliente de Redis
        redis_client = wait_for_redis()
        # Incrementa el contador de visitas en Redis
        visitas = redis_client.incr('visitas')

        # Obtiene la key para Split (puede ser pasada por query param para simular usuarios)
        split_key = request.args.get('key', request.remote_addr)
        # Crea el cliente de Split (SDK)
        split_client = FACTORY.client()
        # Obtiene el tratamiento para el usuario según el feature flag
        split_treatment = split_client.get_treatment(split_key, 'nueva_funcionalidad_dark_launch')

        # Prepara el sufijo de la query string para los enlaces internos
        key_param = f"?key={split_key}" if 'key' in request.args else ""

        # Lógica condicional según el tratamiento recibido de Split
        if split_treatment == 'on':
            message = "¡Has sido seleccionado para ver la nueva versión! 🎉"
            # Ejemplo de lógica adicional: cambia el color de fondo según el número de visitas
            if visitas == 0:
                body_style = "background-color: #f0f0f0;"
            elif visitas % 2 == 0:
                body_style = "background-color: #e6f9e6;"  # Verde claro
            else:
                body_style = "background-color: #ffe6e6;"  # Rojo claro
        else:
            message = "¡Estás viendo la versión original! 👻"
            body_style = "background-color: #f0f0f0;"

        # Renderiza la respuesta HTML con los enlaces propagando la key
        return f'''
        <html>
            <body style="font-family: Arial; text-align: center; padding: 50px; {body_style}">
                <h1 style="color: #4CAF50;">✨ ¡Contador de Visitas! ✨</h1>
                <p style="font-size: 28px; color: #333;">{message}</p>
                <p style="font-size: 24px; color: #007bff;">Número de visitas: <strong>{visitas}</strong></p>
                <p>✅ Redis funcionando correctamente</p>
                <a href="/reiniciar{key_param}" style="color: #ff5722;">🔄 Reiniciar contador</a> | 
                <a href="/health{key_param}" style="color: #2196F3;">❤️ Health check</a>
            </body>
        </html>
        '''
    except Exception as e:
        # Manejo de errores: muestra el error en pantalla
        return f'❌ Error: {str(e)}'

# --- Ruta para reiniciar el contador de visitas ---
@app.route('/reiniciar')
def reiniciar_contador():
    try:
        redis_client = wait_for_redis()
        redis_client.set('visitas', 0)
        # Propaga la key en el enlace de retorno
        key_param = f"?key={request.args.get('key')}" if request.args.get('key') else ""
        return f'✅ ¡Contador reiniciado! <a href="/{key_param}">Volver</a>'
    except Exception as e:
        return f'❌ Error: {str(e)}'

# --- Ruta de health check para verificar el estado de Redis ---
@app.route('/health')
def health_check():
    try:
        redis_client = wait_for_redis()
        redis_client.ping()
        # Propaga la key en el enlace de retorno
        key_param = f"?key={request.args.get('key')}" if request.args.get('key') else ""
        return f'✅ OK <a href="/{key_param}">Volver</a>'
    except Exception as e:
        return f'❌ Error: {str(e)}'

# --- Punto de entrada principal de la aplicación Flask ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)