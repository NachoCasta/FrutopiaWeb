import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def mayus(string):
    return " ".join([s[0].upper() + s[1:] for s in string.split()])

def texto_con_borde(draw, font, text, x, y, grosor=1,
                    color_texto=(0,0,0), color_borde=(255,255,255)):
    draw.text((x+grosor, y), text, color_borde, font=font) 
    draw.text((x-grosor, y), text, color_borde, font=font) 
    draw.text((x, y+grosor), text, color_borde, font=font) 
    draw.text((x, y-grosor), text, color_borde, font=font) 
    draw.text((x, y), text, color_texto, font=font)

def texto_centrado(draw, font, text, x, y, color=(0,0,0),
                   borde=0, color_borde=(255,255,255)):
    w, h = font.getsize(text)
    x, y = x-w/2, y-h/2
    if borde == 0:
        draw.text((x, y), text, color, font=font)
    else:
        texto_con_borde(draw, font, text, x, y, borde, color, color_borde)

def agregar_datos(nombre, apellido, numero, fruta="frutillas", precio=6500):
    numero = str(numero)[-8:]
    numero = "56 9 {} {}".format(numero[:4],numero[4:])
    img = Image.open("grafica/Fotos/{} {}.jpg".format(fruta, precio))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("grafica/Fuentes/DK Canoodle.otf", 220)
    draw.text((215, 1880), nombre, (255, 255, 255), font) # Nombre
    draw.text((215, 2070), apellido, (255, 255, 255), font) # Apellido
    font = ImageFont.truetype("grafica/Fuentes/din_bold.ttf", 150)
    x, y = 430, 2310
    draw.text((x+100, y), numero, (255, 255, 255), font) # Numero
    font = ImageFont.truetype("grafica/Fuentes/din_bold.ttf", 150)
    draw.text((x, y-20), "+", (255, 255, 255), font)
    draw = ImageDraw.Draw(img)
    file = "grafica/Vendedores/{} {} {}.jpg".format(mayus(fruta), nombre, apellido)
    img.save(file)
    return file

def agregar_datos_multiples(nombre, apellido, numero,
                            frutillas=6000, uvas=5000,
                            paltas=6000, limones=6000):
    numero = str(numero)[-8:]
    numero = "+56 9 {} {}".format(numero[:4],numero[4:])
    img = Image.open("grafica/Fotos/todos.jpg")
    draw = ImageDraw.Draw(img)
    #font = ImageFont.truetype("grafica/Fuentes/DK Canoodle.otf", 220)
    font = ImageFont.truetype("grafica/Fuentes/DK Canoodle.otf", 300)
    #y_n = 2550
    #draw.text((40, y_n), nombre, (0, 0, 0), font) # Nombre
    #draw.text((40, y_n+190), apellido, (0, 0, 0), font) # Apellido
    y_n = 2300
    #draw.text((2600, y_n), nombre, (0, 0, 0), font) # Nombre
    #draw.text((2600, y_n+190+40), apellido, (0, 0, 0), font) # Apellido
    texto_centrado(draw, font, nombre, 3000, y_n)
    texto_centrado(draw, font, apellido, 3000, y_n+250)
    font = ImageFont.truetype("grafica/Fuentes/BebasNeue.otf", 270)
    x = 2350
    draw.text((x, y_n+545), numero, (0, 0, 0), font) # Numero
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("grafica/Fuentes/BebasNeue.otf", 400)
    #y_p = 430
    y_p = 1400
    ##y_p = 2200
    draw.text((3350, y_p), precio(paltas), (255, 255, 255), font) # Paltas
    ##draw.text((660, y_p), precio(arandanos3), (255, 255, 255), font) # Arandanos
    draw.text((1800, y_p), precio(frutillas), (255, 255, 255), font) # Frutillas
    ##draw.text((1860, y_p), precio(cerezas2), (255, 255, 255), font) # Cerezas
    ##draw.text((2460, y_p), precio(duraznos), (255, 255, 255), font) # Duraznos
    y_p = 4500
    draw.text((1750, y_p), precio(limones), (255, 255, 255), font) # Limones
    draw.text((3300, y_p), precio(uvas), (255, 255, 255), font) # Uvas
    ##draw.text((660, y_p), precio(arandanos1), (255, 255, 255), font) # Arandanos
    ##draw.text((1860-20, y_p), precio(cerezas5), (255, 255, 255), font) # Cerezas
    file = "grafica/Vendedores/Multiple {} {}.jpg".format(nombre, apellido)
    img.save(file)
    return file

def agregar_datos_vendedores(nombre, apellido, numero):
##    numero = str(numero)[-8:]
##    numero = "+56 9 {} {}".format(numero[:4],numero[4:])
##    img = Image.open("grafica/Fotos/difusion_vendedores.jpg")
##    draw = ImageDraw.Draw(img)
##    font = ImageFont.truetype("grafica/Fuentes/DK Canoodle.otf", 300)
##    y_n = 2300
##    texto_centrado(draw, font, nombre, 3000, y_n)        # Nombre
##    texto_centrado(draw, font, apellido, 3000, y_n+250)  # Apellido
##    font = ImageFont.truetype("grafica/Fuentes/BebasNeue.otf", 270)
##    x = 2350
##    draw.text((x, y_n+545), numero, (0, 0, 0), font) # Numero
##    draw = ImageDraw.Draw(img)
##    font = ImageFont.truetype("grafica/Fuentes/BebasNeue.otf", 400)
    numero = str(numero)[-8:]
    numero = "+56 9 {} {}".format(numero[:4],numero[4:])
    img = Image.open("grafica/Fotos/difusion_vendedores.jpg")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("grafica/Fuentes/DK Canoodle.otf", 100)
    y_n = 1060
    texto_centrado(draw, font, nombre, 240, y_n+60)        # Nombre
    texto_centrado(draw, font, apellido, 240, y_n+150)  # Apellido
    font = ImageFont.truetype("grafica/Fuentes/BebasNeue.otf", 100)
    x = 160
    draw.text((x, y_n-100), numero, (0, 0, 0), font) # Numero
    draw = ImageDraw.Draw(img)
    file = "grafica/Vendedores/Vendedores {} {}.jpg".format(nombre, apellido)
    img.save(file)
    return file

def precio(s):
    s = str(s)
    return "${}.{}".format(s[:-3], s[-3:])

if __name__ == "__main__":
    agregar_datos_multiples("Ignacio", "Castañeda", 82328250)
