import requests
import os
from bs4 import BeautifulSoup


def scrap_urls(nombreNegocio, api_key):
    url = "https://serpapi.com/search"
    params = {
        "q": f"{nombreNegocio} opiniones OR reseñas OR críticas",
        "hl": "es",
        "gl": "es",
        "api_key": api_key
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    # Extraer URLs de los resultados
    enlaces = [res["link"] for res in data.get("organic_results", [])]
    return enlaces

def scrape_opinions(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error al acceder a {url}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    # Buscar opiniones dentro de etiquetas de texto (esto varía según el sitio)
    opiniones = []
    for tag in soup.find_all(["p", "span", "div"]):  # Modificar si es necesario
        texto = tag.get_text().strip()
        if 50 < len(texto) < 500:  # Filtrar opiniones muy cortas o largas
            opiniones.append(texto)

    return opiniones

def scrape_all_opinions(enlaces):
    todas_opiniones = []
    for url in enlaces:
        print(f"Scrapeando: {url}")
        opiniones = scrape_opinions(url)
        todas_opiniones.extend(opiniones)
    return todas_opiniones

