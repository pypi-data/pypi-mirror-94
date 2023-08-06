import os
import requests
import json


API_URL = os.getenv('GADM_API_URL')
API_KEY = os.getenv('GADM_API_KEY')
HEADERS = {
    'Content-Type': 'application/json',
    'X-Api-Key': API_KEY,
}


def _id_to_level(id: str): return id.count('.')


def _get_gadm_data(gid: str, **kwargs):
    url = f"{API_URL}/{_id_to_level(gid)}"
    return requests.post(url, json.dumps(kwargs), headers=HEADERS).json() if API_URL else {}
