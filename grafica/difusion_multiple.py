import math

import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def mayus(string):
    return " ".join([s[0].upper() + s[1:] for s in string.split()])

def crear_difusion_multiple(vendedor, productos):
    n = len(productos)
    ancho_franja = 2000//n
    alto = 2000
    ancho = (ancho_franja//2)*2*n
    img = Image.new("RGB", (ancho, alto))
    ancho_producto = int(ancho_franja*0.9)
    x_offset = 0
    y_formato = 600
    y_precio = y_formato + 150
    y_producto = 900
    x_nombre = 680
    y_nombre = 1680
    x_telefono = 750
    y_telefono = 1785
    draw = ImageDraw.Draw(img)
    s = min(360//n, int(360/3.6))
    font_numeros = ImageFont.truetype("grafica/Fuentes/din_bold.ttf", s)
    font_telefono = ImageFont.truetype("grafica/Fuentes/din_bold.ttf", 120)
    circulo = Image.open("grafica/Fotos/circulo.png")
    circulo_size = min((int(ancho_franja*0.9)), 500)
    x_circulo = (ancho_franja-circulo_size)//2
    y_circulo = 100
    circulo = circulo.resize((circulo_size, circulo_size))
    cantidad_lineas = min(max(n//2, 1), 3)
    for producto in productos:
        franja = Image.open("grafica/Fotos/"+producto["foto"])
        franja = franja.crop((ancho//2-ancho_franja//2-1, 0,
                              ancho//2+ancho_franja//2+1, alto))
        img.paste(franja, (x_offset, 0))
        
        img.paste(circulo, (int(x_offset+x_circulo), y_circulo),
                  mask=circulo)
        formato = producto["masa"] + " " + producto["unidad"].upper()
        str_precio = precio(producto["precio"])
        texto = formato + "\n" + str_precio
        _, h = font_numeros.getsize(formato)
        h = int(h*2.5)
        w = max(font_numeros.getsize(formato)[0], font_numeros.getsize(str_precio)[0])
        x = x_circulo+(circulo_size-w)//2
        y = y_circulo+(circulo_size-h)//2
        draw.multiline_text((x_offset+x, y),
                            texto, (255, 255, 255),
                            font_numeros, align="center")
        
        nombre = producto["producto"]
        detalle = None
        if len(nombre.split()) > 1:
            nombre, detalle = nombre.split()
        lineas_producto = cantidad_lineas
        while len(nombre)/lineas_producto <= 2:
            lineas_producto -= 1
        largo_linea = math.ceil(len(nombre)/lineas_producto)
        i = 0
        lineas = []
        while len(lineas) < lineas_producto:
            if len(lineas)+2 == lineas_producto and len(nombre)%largo_linea == 1:
                    j = min(i+largo_linea+1, len(nombre))
                    lineas.append(nombre[i:j])
                    lineas_producto -= 1
                    i += 1
            else:
                j = min(i+largo_linea, len(nombre))
                lineas.append(nombre[i:j])
            i += largo_linea
        if detalle is not None:
            lineas.append(detalle)
            lineas_producto += 1
        y_offset = y_producto
        for i, linea in enumerate(lineas):
            s = 180
            font_producto = ImageFont.truetype(
                "grafica/Fuentes/DK Canoodle.otf", s)
            limite = ancho_producto
            if detalle is not None and \
               linea == lineas[-1]:
                limite = int(ancho_producto*0.8)
            while font_producto.getsize(linea)[0] > limite:
                s -= 1
                font_producto = ImageFont.truetype(
                    "grafica/Fuentes/DK Canoodle.otf", s)
            if lineas_producto == 2 and i == 0:
                y_offset -= h/2
            if lineas_producto == 3 and i == 0:
                y_offset -= h
            w, h = font_producto.getsize(linea)
            x, y = x_offset+(ancho_franja-w)//2, y_offset-h/2
            draw.text((x, y), linea, (255, 255, 255), font_producto)
            y_offset += h
        
        x_offset += ancho_franja
    img.paste(Image.open("grafica/Fotos/banner.jpg"), (0, alto-400))
    nombre = vendedor["nombre"]
    apellido = vendedor["apellido"]
    telefono = vendedor["telefono"]
    telefono = "+569" + telefono.strip().replace(" ", "")[-8:]
    telefono = str(telefono)[-8:]
    telefono = "+56 9 {} {}".format(telefono[:4],telefono[4:])
    nombre_completo = nombre + " " + apellido
    s = 200
    font_nombres = ImageFont.truetype("grafica/Fuentes/DK Canoodle.otf", s)
    while font_nombres.getsize(nombre_completo)[0] > 1200:
        font_nombres = ImageFont.truetype("grafica/Fuentes/DK Canoodle.otf", s)
        s -= 1        
    w, h = font_nombres.getsize(nombre_completo)
    x, y = x_nombre-w/2, y_nombre-h/2
    draw.text((x, y), nombre_completo, (0, 0, 0), font_nombres)
    w, h = font_telefono.getsize(telefono)
    x = x_telefono-w/2   
    draw.text((x, y_telefono), telefono, (0, 0, 0), font_telefono)
    file = "grafica/Vendedores/Multiple {}.jpg".format(nombre_completo)
    img.save(file)
    return file

def precio(s):
    s = str(s)
    return "${}.{}".format(s[:-3], s[-3:])

if __name__ == "__main__":
    pass
