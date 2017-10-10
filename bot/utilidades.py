import json

try:
    import chatbot
    rel = "datos/"
except Exception:
    rel = "bot/datos/"


def mayus(string):
    return " ".join([s[0].upper() + s[1:] for s in string.split()])

def obtener_productos(archivo=rel+"productos.json", todos=False):
    with open(archivo, "r") as file:
        data = json.load(file)
    productos = []
    for producto, formatos in data.items():
        for formato, detalles in formatos.items():
            if detalles["disponible"] or todos:
                detalles["masa"] = formato
                detalles["producto"] = producto
                productos.append(detalles)
    return productos
