import pytesseract as tess
tess.pytesseract.tesseract_cmd=r'C:\Users\user\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
from PIL import Image

img = Image.open('WiDpa.jpg')
text = tess.image_to_string(img)

print(text)