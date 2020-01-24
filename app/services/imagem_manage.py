import requests as req
import shutil
import pytesseract as ocr
import numpy as np
import cv2
from PIL import Image

ocr.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'

def busca_texto():
    imagem = Image.open('image.jpg').convert('RGB')

    npimagem = np.asarray(imagem).astype(np.uint8)

    # diminuição dos ruidos antes da binarização
    npimagem[:, :, 0] = 0 # zerando o canal R (RED)
    npimagem[:, :, 2] = 0 # zerando o canal B (BLUE)

    # atribuição em escala de cinza
    im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY) 

    # aplicação da truncagem binária para a intensidade
    # pixels de intensidade de cor abaixo de 127 serão convertidos para 0 (PRETO)
    # pixels de intensidade de cor acima de 127 serão convertidos para 255 (BRANCO)
    # A atrubição do THRESH_OTSU incrementa uma análise inteligente dos nivels de truncagem
    ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 

    # reconvertendo o retorno do threshold em um objeto do tipo PIL.Image
    binimagem = Image.fromarray(thresh) 

    # chamada ao tesseract OCR por meio de seu wrapper
    phrase = ocr.image_to_string(binimagem, lang='eng')

    # impressão do resultado
    return phrase.splitlines()

def salvar_imagem(caminho_da_imagem):
    print('Error tracking: ---> ', caminho_da_imagem)
    try:
        response = req.get(caminho_da_imagem)
        if response.status_code == 200:
            path = "image.jpg"
            with open(path, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
    except Exception as e:
        print(e)


def busca_texto_em_imagem(caminho_da_imagem):
    salvar_imagem(caminho_da_imagem)
    texto = busca_texto()

    return texto[0] if texto else 'Não foi possivel reconhecer nenhum nome na imagem.'
