import os
import requests
from constantes import BASE_URL
from dotenv import load_dotenv
import re
import logging
from pathlib import Path
import time


logging.basicConfig(
    filename=os.path.join(str(Path.home()), "aeroporto.log"),
    format="%(asctime)s %(message)s",
    filemode="w"
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


BASE_DIR = os.path.dirname(__file__)
env_path = os.path.join(BASE_DIR, "config", ".env")

load_dotenv(env_path)


token = os.getenv("APP_KEY")
app_id = os.getenv("APP_ID")

def get_endpoint (endpoint, endpoint_id=None, params=None):

    headers = {
        "Accept": "application/json",
        "app_id": app_id,
        "app_key": token,
        "ResourceVersion": "v4"
    }

    url = BASE_URL + endpoint

    if endpoint_id:
        url += f"/{endpoint_id}"

    resultados = []

    response = requests.get(url, headers=headers, params=params)

    response.raise_for_status() # interrompe a execução se a resposta for um erro HTTP

    resultados.append(response.json())

    numero_paginas = processar_headers_numero_paginas(response.headers)

    link = processar_headers_next(response.headers)

    while link:= processar_headers_next(response.headers): #enquanto eu tiver um link (:= operador morsa)
        time.sleep(0.5) # pra não fazer várias requisições ao mesmo tempo
        logger.info(f"Páginas: {numero_paginas} link:{link}")
        response = requests.get(link, headers=headers, params=params)
        response.raise_for_status()
        resultados.append(response.json())

    return resultados


def processar_headers_next(headers):

    headers_link = headers.get("link")

    if not headers_link:
        return None
    
    link_partes = headers_link.split(",")

    for parte in link_partes:
        if 'rel="next"' in parte:
            link = parte.split(";")[0].strip()
            link = re.sub(r'^<|>$', '', link)  # Remove < and > from the start and end
            return link


def processar_headers_numero_paginas(headers):

    headers_link = headers.get("link")

    if not headers_link:
        return 0
    
    link_partes = headers_link.split(",")

    for parte in link_partes:

        if 'rel="last"' in parte:
            numero = parte.split(";")[0]
            numero = re.search(r'page=(\d+)', numero).group(1)

            return int(numero)



if __name__ == "__main__":
    get_endpoint("flights")

