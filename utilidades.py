import json

from grafica.difusion_multiple import crear_difusion_multiple

def mayus(string):
    return " ".join([s[0].upper() + s[1:] for s in string.split()])

def obtener_productos(archivo="grafica/productos.json"):
    with open(archivo, "r") as file:
        data = json.load(file)
    productos = []
    for producto, formatos in data.items():
        for formato, detalles in formatos.items():
            if detalles["disponible"]:
                detalles["masa"] = formato
                productos.append(detalles)
    return productos

def crear_template_multiple(productos):
    with open("templates/difusion_multiple.html", "w", encoding="utf8") as file:
        with open("templates/inicio_multiple.txt",
                  "r", encoding="latin-1") as f:
            inicio = "".join(f.readlines())
        file.write(inicio)
        for producto in productos:
            pass
            file.write('''
          <div class="login__row">
            <svg class="login__icon svg-phone" viewBox="0 0 59 59" width="512px" height="512px">
                <path d="''')
            with open("svgs/"+producto["svg"], "r", encoding="latin-1") as f:
                svg = "".join(f.readlines())
            file.write(svg)
            file.write('''" fill="#FFFFFF"/>
              </svg>
            <input type="text" class="login__input pass" placeholder="''')
            file.write(producto["nombre"])
            file.write('''" 
            name="''')
            file.write(producto["variable"])
            file.write('''" size="25" value="{{ request.form.''')
            file.write(producto["variable"])
            file.write(''' }}"/>
          </div>''')
        with open("templates/fin_multiple.txt", "r", encoding="latin-1") as f:
            fin = "".join(f.readlines())
        file.write(fin)

if __name__ == "__main__":
    vendedor = {
        "nombre": "Ignacio",
        "apellido": "Castañeda",
        "telefono": "+56982328250"
        }
    crear_difusion_multiple(vendedor, obtener_productos())
        
