import requests

def get_place_id(nombreNegocio, apiKey):
    """
    Obtiene el Place ID de un negocio a partir de su nombre.
    """
    URL = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={nombreNegocio}&inputtype=textquery&fields=place_id&key={apiKey}"
    response = requests.get(URL)
    data = response.json()

    if "candidates" in data and data["candidates"]:
        place_id = data["candidates"][0]["place_id"]
        print("✅ Place ID encontrado:", place_id)
        return place_id
    else:
        print("❌ No se encontró el negocio.")
        return None  # Retornar None si no se encuentra el negocio

def obtener_resenas(apiKey, place_id):
    """
    Obtiene las reseñas de un negocio a partir de su Place ID.
    """
    if place_id is None:
        print("❌ No se puede obtener reseñas sin un Place ID válido.")
        return []

    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=name,rating,reviews&key={apiKey}"
    response = requests.get(url)
    data = response.json()

    # Verificar si hay un mensaje de error en la API
    if "error_message" in data:
        print("❌ Error de la API de Google:", data["error_message"])
        return []

    # Extraer reseñas
    reviews = data.get("result", {}).get("reviews", [])
    
    if not reviews:
        print("⚠️ No hay reseñas disponibles para este negocio.")
        return []

    # Guardar en una lista de diccionarios
    resenas_array = [{"autor": r["author_name"], "rating": r["rating"], "texto": r["text"]} for r in reviews]
    
    print("✅ Reseñas obtenidas correctamente.")

    return resenas_array