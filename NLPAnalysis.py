import re
from collections import Counter
import spacy
import nltk
from pysentimiento import create_analyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Cargar modelo de NLP en español
nlp = spacy.load("es_core_news_sm")

# Crear analizador de sentimientos
analyzer = create_analyzer(task="sentiment", lang="es")
# Descargar stopwords
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('spanish'))
stop_words.update(["bueno", "malo", "ser", "estar", "toda", "todo", "día", "noche"])  # 🔹 Más palabras irrelevantes


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

def sentiment_analysis(opiniones, nombreNegocio):
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

    return positivas, negativas

