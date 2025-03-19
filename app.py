import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import io
import base64
from dotenv import load_dotenv
import os
from serpOpinions import scrap_urls, scrape_all_opinions
from googleOpinions import get_place_id, obtener_resenas
from NLPAnalysis import sentiment_analysis
from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for, session
import secrets

load_dotenv()

app = Flask(__name__)

# Google API KEY
apiKey = os.getenv("API_KEY")
serpApiKey = os.getenv("SERP_API_KEY")
app.secret_key = os.getenv('SECRET_KEY')  # Leer la clave desde el archivo .env

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombreNegocio = request.form['business_name']

        # Llamar a la función de control de acceso
        if not controlar_acceso():
            return render_template('error.html', message="Ya has utilizado la herramienta hoy.")

        # Obtener opiniones
        place_id = get_place_id(nombreNegocio, apiKey)
        resenas_google = obtener_resenas(apiKey, place_id)
        enlaces = scrap_urls(nombreNegocio, serpApiKey)
        resenas_serp = scrape_all_opinions(enlaces)

        # Unir todas las opiniones
        opiniones = resenas_serp + resenas_google
        
        # Ejecutar el análisis de opiniones
        positivas, negativas = sentiment_analysis(opiniones, nombreNegocio)
        
        # Generar gráficos
        img_positivas = generar_wordcloud(positivas, "Blues")
        img_negativas = generar_wordcloud(negativas, "Reds")
        
        return render_template('dashboard.html', business=nombreNegocio, img_positivas=img_positivas, img_negativas=img_negativas)

    return render_template('index.html')

def controlar_acceso():
    if session.get('usos_hoje') == 1:
        # Si ya se ha utilizado hoy, redirige a otra página o muestra un mensaje
        return False
    else:
        # Si no se ha usado, establece la variable en la sesión
        session['usos_hoje'] = 1
        return True

def generar_wordcloud(palabras, color):
    """ Genera una imagen de nube de palabras y la convierte a base64."""
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap=color).generate_from_frequencies(Counter(palabras))
    
    img = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

if __name__ == '__main__':
    app.run(debug=True)
