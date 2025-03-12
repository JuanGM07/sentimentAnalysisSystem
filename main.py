import re
import nltk
from collections import Counter
from pysentimiento import create_analyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from serpOpinions import scrape_all_opinions
from dotenv import load_dotenv
import os
from serpOpinions import scrap_urls
from serpOpinions import scrape_all_opinions
from googleOpinions import get_place_id
from googleOpinions import obtener_resenas

load_dotenv()

nombreNegocio = "Confiteria Guillen Huelva"

# Crear analizador de sentimientos
analyzer = create_analyzer(task="sentiment", lang="es")

# Google API KEY
apiKey = os.getenv("API_KEY")
serpApiKey = os.getenv("SERP_API_KEY")

# Descargar stopwords en español
nltk.download('stopwords')
nltk.download('punkt_tab')
stop_words = set(stopwords.words('spanish'))

# Obtener opiniones de Google 
place_id = get_place_id(nombreNegocio, apiKey)
resenas_google = obtener_resenas(apiKey, place_id)

# Obtener opiniones de Serp
enlaces = scrap_urls(nombreNegocio, serpApiKey)
resenas_serp = scrape_all_opinions(enlaces)

# Unir todas las opiniones
opiniones = resenas_serp + resenas_google

# Diccionarios para clasificar palabras clave
positivas = []
negativas = []

def extraer_texto(opinion):
    """ 
    Extrae el texto de la opinión si es un diccionario o una lista.
    Si es un diccionario, usa la clave 'text'. 
    Si es una lista, toma el primer elemento válido.
    """
    if isinstance(opinion, dict):
        return opinion.get("text", "")  # Devuelve el valor de 'text' o un string vacío si no existe
    elif isinstance(opinion, list) and opinion:
        return opinion[0] if isinstance(opinion[0], str) else str(opinion[0])  
    return str(opinion)  # Asegurar que siempre sea string


for opinion in opiniones:
    opinion = extraer_texto(opinion)  # Convertirlo en string siempre

    # Obtener sentimiento con pysentimiento
    resultado = analyzer.predict(opinion)

    if isinstance(resultado, list) and resultado:  
        sentimiento = resultado[0].output  # Accede al primer elemento si es lista
    else:
        sentimiento = resultado.output  # Si es un solo objeto, accede directamente

    # Limpiar texto y tokenizar
    opinion = re.sub(r'[^\w\s]', '', opinion.lower())  # Eliminar signos de puntuación
    palabras = word_tokenize(opinion)
    palabras = [word for word in palabras if word not in stop_words]  # Eliminar stopwords


    # Guardar palabras clave según sentimiento
    if sentimiento == "POS":
        positivas.extend(palabras)
    elif sentimiento == "NEG":
        negativas.extend(palabras)

# Contar frecuencia de palabras
top_positivas = Counter(positivas).most_common(5)
top_negativas = Counter(negativas).most_common(5)

print("🔹 Características más mencionadas en opiniones **positivas**:")
for palabra, freq in top_positivas:
    print(f"- {palabra} ({freq} veces)")

print("\n🔻 Características más mencionadas en opiniones **negativas**:")
for palabra, freq in top_negativas:
    print(f"- {palabra} ({freq} veces)")

