import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def mayus(string):
    return " ".join([s[0].upper() + s[1:] for s in string.split()])

def crear_difusion_multiple(vendedor, productos):
    n = len(productos)
    arriba = productos[:n//2-1]
    abajo = productos[n//2-1:]
    alto = 1000*n + 2000
    ancho = 2000
    img = Image.new("RGB", (ancho, alto))
    y_offset = 0
    x_circulo = 500
    x_centro = 1000
    y_formato = 500
    y_precio = y_formato + 150
    y_nombre = 1630
    y_telefono = y_nombre + 155
    draw = ImageDraw.Draw(img)
    font_numeros = ImageFont.truetype("grafica/Fuentes/din_bold.ttf", 130)
    font_telefono = ImageFont.truetype("grafica/Fuentes/din_bold.ttf", 120)
    for producto in arriba:
        img.paste(Image.open("grafica/Fotos/"+producto["foto"]), (0, y_offset))
        formato = producto["masa"] + " " + producto["unidad"].upper()
        w, h = font_numeros.getsize(formato)
        x = x_circulo-w/2
        draw.text((x, y_offset+y_formato),
                  formato, (255, 255, 255),
                  font_numeros)
        str_precio = precio(producto["precio"])
        w, h = font_numeros.getsize(str_precio)
        x = x_circulo-w/2
        draw.text((x, y_offset+y_precio),
                  str_precio, (255, 255, 255),
                  font_numeros)
        y_offset += 1000
    img.paste(Image.open("grafica/Fotos/centro.jpg"), (0, y_offset))
    nombre = vendedor["nombre"]
    apellido = vendedor["apellido"]
    telefono = vendedor["telefono"]
    telefono = "+569" + telefono.strip().replace(" ", "")[-8:]
    telefono = str(telefono)[-8:]
    telefono = "+56 9 {} {}".format(telefono[:4],telefono[4:])
    nombre_completo = nombre + " " + apellido
    s = 220
    font_nombres = ImageFont.truetype("grafica/Fuentes/DK Canoodle.otf", s)
    while font_nombres.getsize(nombre_completo)[0] > 1800:
        font_nombres = ImageFont.truetype("grafica/Fuentes/DK Canoodle.otf", s)
        s -= 1        
    w, h = font_nombres.getsize(nombre_completo)
    x, y = x_centro-w/2, y_offset+y_nombre-h/2
    draw.text((x, y), nombre_completo, (0, 0, 0), font_nombres)
    w, h = font_telefono.getsize(telefono)
    x = x_centro-w/2   
    draw.text((x, y_offset+y_telefono), telefono, (0, 0, 0), font_telefono)
    y_offset += 2000
    for producto in abajo:
        img.paste(Image.open("grafica/Fotos/"+producto["foto"]), (0, y_offset))
        formato = producto["masa"] + " " + producto["unidad"].upper()
        w, h = font_numeros.getsize(formato)
        x = x_circulo-w/2
        draw.text((x, y_offset+y_formato),
                  formato, (255, 255, 255),
                  font_numeros)
        str_precio = precio(producto["precio"])
        w, h = font_numeros.getsize(str_precio)
        x = x_circulo-w/2
        draw.text((x, y_offset+y_precio),
                  str_precio, (255, 255, 255),
                  font_numeros)
        y_offset += 1000
    file = "grafica/Vendedores/Multiple {}.jpg".format(nombre_completo)
    img.save(file)
    return file

def precio(s):
    s = str(s)
    return "${}.{}".format(s[:-3], s[-3:])

if __name__ == "__main__":
    pass
