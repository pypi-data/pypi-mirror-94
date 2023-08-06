####IMPORTS### RELATIVE IMPORTS / ABSOLUTE IMPORTS
import argparse
from webscraping.utilities.utility import get_html, downloadimages, downloadinfo_url, descargarimagen

def leer_inputs():
    parser = argparse.ArgumentParser(description='Descarga todas las imagnes de tu url preferida!')
    parser.add_argument('--url', type=str, help='Pon tu url a descargar las imagines i.e --url www.wikipedia.com')
    parser.add_argument('--nimg', type=int, help='Pon el número de imágenes a descargar')
    args = parser.parse_args()
    return args.url, args.nimg



def main():
    enlace, nimg = leer_inputs()
    downloadinfo_url(enlace, nimg) 



####EJECUCION
if __name__ == "__main__":
    main()
