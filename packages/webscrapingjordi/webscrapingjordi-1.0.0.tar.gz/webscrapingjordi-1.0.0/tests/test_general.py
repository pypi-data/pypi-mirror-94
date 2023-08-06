from webscraping.utilities.utility import descargarimagen, downloadinfo_url, downloadparrafos
from tests.utilities import clean_up, clean_enlace
import os


######UNIT TEST################
def test_descargarimagen():
    soup = clean_enlace()
    myimg = soup.findAll("img")[0]
    descargarimagen(myimg)
    assert os.path.exists("400px-Municipalities_of_Spain.svg.png") == True

def test_descargarparrafo():
    clean_up("*.txt")
    soup = clean_enlace()
    downloadparrafos(soup)
    assert os.path.exists("Output.txt") == True




#######END TO END TEST#############
def test_main():
    clean_up("*.png")
    clean_up("*.txt")
    enlace = "https://es.wikipedia.org/wiki/Anexo:Municipios_de_Espa%C3%B1a_por_poblaci%C3%B3n"
    nimg = 4
    imagenes_desc = downloadinfo_url(enlace,nimg)
    for img in imagenes_desc:
        assert os.path.exists(img) == True
    assert len(imagenes_desc) == nimg
    assert os.path.exists("Output.txt") == True





    