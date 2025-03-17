import re
import spacy
import nltk
from collections import Counter
from pysentimiento import create_analyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from serpOpinions import scrape_all_opinions
from dotenv import load_dotenv
import os
from serpOpinions import scrap_urls
from googleOpinions import get_place_id
from googleOpinions import obtener_resenas

load_dotenv()

nombreNegocio = "Restaurante Bonilla Huelva"  # 🔹 Se usará para limpiar texto

# Cargar modelo de NLP en español
nlp = spacy.load("es_core_news_sm")

# Crear analizador de sentimientos
analyzer = create_analyzer(task="sentiment", lang="es")

# Google API KEY
apiKey = os.getenv("API_KEY")
serpApiKey = os.getenv("SERP_API_KEY")

# Descargar stopwords
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('spanish'))
stop_words.update(["bueno", "malo", "ser", "estar", "toda", "todo", "día", "noche"])  # 🔹 Más palabras irrelevantes

# Obtener opiniones
place_id = get_place_id(nombreNegocio, apiKey)
resenas_google = obtener_resenas(apiKey, place_id)
enlaces = scrap_urls(nombreNegocio, serpApiKey)
resenas_serp = scrape_all_opinions(enlaces)

# Unir todas las opiniones
opiniones = resenas_serp + resenas_google

# Listas para clasificar palabras clave
positivas = []
negativas = []

def extraer_texto(opinion):
    """Extrae el texto de una opinión sin importar su formato."""
    if isinstance(opinion, dict):
        return opinion.get("text", "")
    elif isinstance(opinion, list) and opinion:
        return str(opinion[0])
    return str(opinion)

for opinion in opiniones:
    opinion = extraer_texto(opinion)  

    # 🔹 Eliminar menciones al negocio
    opinion = re.sub(nombreNegocio.lower(), "", opinion.lower())  

    # Obtener sentimiento
    resultado = analyzer.predict(opinion)
    sentimiento = resultado.output  # Usar .output en lugar de .label

    # Limpiar texto
    opinion = re.sub(r'\d+', '', opinion)  # Eliminar números
    opinion = re.sub(r'[^\w\s]', '', opinion.lower())  
    palabras = word_tokenize(opinion)
    
    # Eliminar stopwords
    palabras_filtradas = [word for word in palabras if word not in stop_words]

    # Procesar con Spacy y extraer solo sustantivos
    doc = nlp(" ".join(palabras_filtradas))
    palabras_sustantivos = [token.text for token in doc if token.pos_ == "NOUN"]

    # Guardar palabras clave según sentimiento
    if sentimiento == "POS":
        positivas.extend(palabras_sustantivos)
    elif sentimiento == "NEG":
        negativas.extend(palabras_sustantivos)

# Contar frecuencia de palabras
top_positivas = Counter(positivas).most_common(5)
top_negativas = Counter(negativas).most_common(5)

print("🔹 Características más mencionadas en opiniones **positivas**:")
for palabra, freq in top_positivas:
    print(f"- {palabra} ({freq} veces)")

print("\n🔻 Características más mencionadas en opiniones **negativas**:")
for palabra, freq in top_negativas:
    print(f"- {palabra} ({freq} veces)")
