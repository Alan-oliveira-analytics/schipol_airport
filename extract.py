import os
import requests
from constantes import BASE_URL
from dotenv import load_dotenv
import re
import logging
from pathlib import Path
import time
import pytz
from datetime import datetime, timedelta

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

def get_endpoint (endpoint, endpoint_id=None, params=None, teste=False):

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

    page_test = 0

    numero_paginas = processar_headers_numero_paginas(response.headers)

    link = processar_headers_next(response.headers)

    while link:= processar_headers_next(response.headers): #enquanto eu tiver um link (:= operador morsa)
        time.sleep(0.5) # pra não fazer várias requisições ao mesmo tempo
        logger.info(f"Páginas: {numero_paginas} link:{link}")
        response = requests.get(link, headers=headers)
        response.raise_for_status()
        resultados.append(response.json())

        if teste == True:
            page_test +=1

        if page_test == 5:
            break

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


    return 0


def get_flights_agendado_hoje():
    return get_endpoint("flights")


def get_flights_agendado_ontem():

    agora = datetime.now(pytz.timezone("Europe/Amsterdam")) #pra pegar a data e hora atual no fuso horário de Amsterdam
    ontem = agora.date() - timedelta(days=1) #pra pegar a data de ontem

    ontem = ontem.strftime("%Y-%m-%d") #pra formatar a data de ontem no formato YYYY-MM-DD - informado doc API

    params = {
        "scheduleDate": ontem
    }
    print(params)

    return get_endpoint(endpoint="flights", params=params)


def get_flights_por_id(flight_id):
    return get_endpoint(endpoint="flights", endpoint_id=flight_id)

def get_airlines():
    return get_endpoint("airlines")

def get_airlines_por_iata_icao(iata_ou_icao):
    return get_endpoint("airlines", endpoint_id=iata_ou_icao)

def get_aircraft_types():
    return get_endpoint("aircrafttypes")

def get_destinations():
    return get_endpoint("destinations", teste=True)

def get_destinations_por_iata(iata):
    return get_endpoint("destinations", endpoint_id=iata)
