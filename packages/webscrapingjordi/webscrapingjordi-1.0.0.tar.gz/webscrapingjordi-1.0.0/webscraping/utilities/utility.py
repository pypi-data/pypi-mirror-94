import requests
from bs4 import BeautifulSoup
import pandas as pd
from os.path  import basename
import io


def get_html(enlace):
    r = requests.get(enlace)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup

def downloadimages(soup, nimg=-1):
    imagenes_desc = []
    myimg = soup.findAll("img")
    for link in myimg[0:nimg]:
        name_imagen_desc = descargarimagen(link)
        imagenes_desc.append(name_imagen_desc)
    return imagenes_desc

def downloadparrafos(soup):
    parrafos = soup.findAll("p")
    textoparrafo = []
    for parrafo in parrafos:
        textoparrafo.append(parrafo.text)
    descargartexto(textoparrafo)
    return textoparrafo

def downloadinfo_url(enlace,nimg):
    soup = get_html(enlace)
    imagenes_desc = downloadimages(soup, nimg)
    parrafos = downloadparrafos(soup)
    return imagenes_desc

def descargartexto(textoparrafo):
    with io.open("Output.txt", "w", encoding="utf-8") as text_file:
        str1 = ''.join(textoparrafo)
        text_file.write(str1)


def descargarimagen(link):
    lnk = link.get('src')
    lnk= "https:" + lnk
    name_imagen_des = basename(lnk)
    with open(name_imagen_des, "wb") as f:
        f.write(requests.get(lnk).content)
    return name_imagen_des