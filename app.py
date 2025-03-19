from flask import Flask, render_template
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

load_dotenv()

app = Flask(__name__)

nombreNegocio = "Restaurante Bonilla Huelva"  # 🔹 Se usará para limpiar texto

# Google API KEY
apiKey = os.getenv("API_KEY")
serpApiKey = os.getenv("SERP_API_KEY")

# Obtener opiniones
place_id = get_place_id(nombreNegocio, apiKey)
resenas_google = obtener_resenas(apiKey, place_id)
enlaces = scrap_urls(nombreNegocio, serpApiKey)
resenas_serp = scrape_all_opinions(enlaces)

# Unir todas las opiniones
opiniones = resenas_serp + resenas_google

@app.route('/')
def index():
    # Ejecutar el análisis de opiniones
    positivas, negativas = sentiment_analysis(opiniones, nombreNegocio)
    # Generar gráficos
    img_positivas = generar_wordcloud(positivas, "Blues")
    img_negativas = generar_wordcloud(negativas, "Reds")
    
    return render_template('index.html', img_positivas=img_positivas, img_negativas=img_negativas)

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
