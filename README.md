# Reviews Analyzer

[![Screenshot-from-2025-03-24-16-38-44.png](https://i.postimg.cc/gkQS6jJZ/Screenshot-from-2025-03-24-16-38-44.png)](https://postimg.cc/ppQYw2KW)

Analyzer Reviews es una herramienta diseñada para dar una vista general sobre las opiniones positivas y negativas de cualquier negocio (especialmente los españoles, porque todo el proceso de NPL se hace en español). Recopila informacion de Google Places, además de scrapear información de decenas de páginas webs. Luego realiza un limpiado y posterior análisis de sentimiento clasificando que aspectos son los mas negativos y positivos. Todo el código está en mi GitHub. Para cualquier problema o propuesta: juanglezm3@gmail.com

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

Vas a necesitar dos api-keys, y una clave secreta que guardaras con las api-keys:

* [Google Places Api-Key](https://developers.google.com/maps/documentation/places/web-service/get-api-key) -> Enlace para obtenerla.
* [Serp Api Key](https://serpapi.com/) -> Enlace para obtenerla.

En primer lugar crea un archivo .env, ahí guardaras tus claves con el siguiente par clave valor:

* API_KEY = "tu_api_key" (esta será tu api_key de Google Places, no cambies el nombre)
* SERP_API_KEY = "tu_api_key" (esta será tu api_key de Serp, no cambies el nombre)
* SECRET_KEY = "clave_aleatoria" (se utiliza para el control de uso del usuario, ya que está programada para que solo se pueda usar una vez al día, se puede cambiar eliminando la funcio control_acceso() de app.py y quitandola de la funcion index() de app.py) 

### Pre-requisitos 📋

Todos los requerimientos estan en requirements.txt:
```bash
  pip install -r requirements.txt
```
He utilizado python 3.12.3, para perfecta compatibilidad utilizar misma versión.

### Instalación 🔧

_Creamos un virtual environment_

_Linux/MacOS:_

```
python3 -m venv nombre_venv
source nombre_venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

_Windows_

```
python3 -m venv nombre_venv
nombre venv\Scripts\activate.bat
pip install -r requirements.txt
python3 app.py
```

_Ya tendrias la herramienta corriendo en tu maquina local_

## Construido con 🛠️

* [Flask](https://flask.palletsprojects.com/en/stable/) - El framework web usado
* [spaCy](https://spacy.io/) - Análisis de NLP
* [NLTK](https://www.nltk.org/) - Análisis de NLP
* [pysentimiento](https://arxiv.org/abs/2106.09462) - Herramienta de python para análisis de opinion, y recolección de reviews.


## Licencia 📄

Mira el archivo [LICENSE.md](LICENSE.md) para detalles. Si quieres usar esta herramienta para tu uso personal, agrega un enlace a este repositorio en tu readme por favor. Espero que sea de utilidad.

## Expresiones de Gratitud 🎁

* Comenta a otros sobre este proyecto 📢
* Mis redes sociales son: 
* [Tiktok](https://www.tiktok.com/@jgmdev) 
* [Linkedin](https://www.linkedin.com/in/jgmdatascience/) 






