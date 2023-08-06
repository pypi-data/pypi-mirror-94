import os
import glob
from bs4 import BeautifulSoup
import requests

def clean_up(format):
    files = glob.glob(format)
    for file in files:
        os.remove(file)


def clean_enlace():
    r = requests.get("https://es.wikipedia.org/wiki/Anexo:Municipios_de_Espa%C3%B1a_por_poblaci%C3%B3n")
    soup = BeautifulSoup(r.text, 'lxml')
    return soup
