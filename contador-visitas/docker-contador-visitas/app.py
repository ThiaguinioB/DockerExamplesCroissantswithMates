from flask import Flask, request
import redis
import time
import os


app = Flask(__name__)

#------------------------------------------------------------------------------------------
# flagsmith 
from flagsmith import Flagsmith

flagsmith = Flagsmith(
    environment_key="XYvDRZ8RzugQuuuCPsJPxY",
)

#------------------------------------------------------------------------------------------
def wait_for_redis():
    """Esperar a que Redis esté disponible"""
    max_retries = 10
    retry_delay = 1
    
    for i in range(max_retries):
        try:
            redis_client = redis.Redis(host='localhost', port=6379, db=0)
            redis_client.ping()
            print("✅ Redis conectado exitosamente")
            return redis_client
        except redis.ConnectionError:
            print(f"⏳ Esperando por Redis... ({i+1}/{max_retries})")
            time.sleep(retry_delay)
    
    raise Exception("❌ No se pudo conectar a Redis")

@app.route('/')
def contador_visitas():
    try:
        redis_client = wait_for_redis()
        visitas = redis_client.incr('visitas')


        # Verificamos si la feature flag está activada
        flags = flagsmith.get_environment_flags()
        mostrar_enlace = flags.is_feature_enabled('contadordonaciones')
        #estado de flag guardado en variable para mostrar o no el enlace
        if mostrar_enlace: 
            donaciones_html = '<p>Si quieres donar, haz clic <a href="/donaciones">aquí</a> 💖</p>'
        else: 
                donaciones_html = ''

        return f'''
    
        <html>
            <body style="font-family: Arial; text-align: center; padding: 50px;">
                <h1>📊 Contador de Visitas</h1>
                <p style="font-size: 24px;">¡Número de visitas: <strong>{visitas}</strong>! 🎉</p>
                <p>✅ Redis funcionando correctamente</p>
                <a href="/reiniciar">🔄 Reiniciar contador</a> | 
                <a href="/health">❤️ Health check</a>
                {donaciones_html}
                
            </body>
        </html>
        '''
    except Exception as e:
        return f'❌ Error: {str(e)}'

@app.route('/reiniciar')
def reiniciar_contador():
    try:
        redis_client = wait_for_redis()
        redis_client.set('visitas', 0)
        return '✅ ¡Contador reiniciado! <a href="/">Volver</a>'
    except Exception as e:
        return f'❌ Error: {str(e)}'

@app.route('/health')
def health_check():
    try:
        redis_client = wait_for_redis()
        redis_client.ping()
        return '✅ Health check: Todo funciona correctamente (Flask + Redis)'
    except Exception as e:
        return f'❌ Health check failed: {str(e)}'

@app.route('/donaciones', methods=['GET', 'POST'])
def contador_donaciones():
    try:
        redis_client = wait_for_redis()

        
        # Verificamos si la feature flag está activada
        flags = flagsmith.get_environment_flags()
        mostrar_donaciones = flags.is_feature_enabled('contadordonaciones')
        
        # Si la flag está desactivada, mostramos un mensaje y no permitimos donar
        if not mostrar_donaciones:
            return '<p>❌ La funcionalidad de donaciones está deshabilitada.</p> <a href="/">🏠 Volver</a>'

        # Incrementar donaciones si se presiona el botón
        if request.method == 'POST':
            redis_client.incr('donaciones')

        donaciones = redis_client.get('donaciones')
        donaciones = int(donaciones) if donaciones else 0

        return f'''
        <html>
            <body style="font-family: Arial; text-align: center; padding: 50px; background-color: #f4f4f9;">
                <h1>💖 Contador de Donaciones</h1>
                <p style="font-size: 24px;">
                    Total donado: <strong>{donaciones}</strong> $USD 🙏
                </p>

                <form method="POST">
                    <button type="submit" style="font-size: 20px; padding: 10px 20px; border-radius: 10px; background: #4CAF50; color: white; border: none;">
                        ➕ Donar 1 USD
                    </button>
                </form>

                <br>
                <a href="/reiniciar_donaciones">🔄 Reiniciar contador de donaciones</a> | 
                <a href="/">🏠 Volver a inicio</a>
            </body>
        </html>
        '''
    except Exception as e:
        return f'❌ Error en donaciones: {str(e)}'



@app.route('/reiniciar_donaciones')
def reiniciar_donaciones():
    try:
        redis_client = wait_for_redis()
        redis_client.set('donaciones', 0)
        return '✅ ¡Contador de donaciones reiniciado! <a href="/donaciones">Volver</a>'
    except Exception as e:
        return f'❌ Error: {str(e)}'


if __name__ == '__main__':
    print("🚀 Iniciando aplicación Flask + Redis...")
    app.run(host='0.0.0.0', port=5000)
