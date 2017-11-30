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
                detalles["producto"] = producto
                productos.append(detalles)
    return productos

def crear_template_multiple(productos):
    with open("templates/difusion_multiple.html", "w", encoding="utf8") as file:
        with open("templates/inicio_multiple.txt",
                  "r", encoding="latin-1") as f:
            inicio = "".join(f.readlines())
        file.write(inicio)
        
        for producto in sorted(productos, key=lambda k: k["orden"]):
  
            file.write('''
          <div class="checkbox__row">
            <svg class="login__icon pass svg-icon svg-phone" ''')
##            viewBox="0 0 60 60">
##              ''')
            with open("svgs/"+producto["svg"], "r", encoding="latin-1") as f:
                svg = "".join(f.readlines())
            file.write(svg)
            file.write('''" fill="#FFFFFF"/>
              </svg>
            <label class="checkbox__label">
              <input checked type="checkbox" class="checkbox__input"
              name="productos" size="25" value="''')
            file.write(producto["variable"])
            file.write('''">''')
            file.write(producto["nombre"])
            file.write('''
            </label>
          </div>''')
            
        with open("templates/fin_multiple.txt", "r", encoding="latin-1") as f:
            fin = "".join(f.readlines())
        file.write(fin)

if __name__ == "__main__":
##    vendedor = {
##        "nombre": "Rodrigo",
##        "apellido": "Fernandez",
##        "telefono": "+56986194003"
##        }
    productos = obtener_productos()
##    productos.pop()
##    productos.pop()
##    productos.pop()
##    productos.pop()
##    crear_difusion_multiple(vendedor, productos)
    crear_template_multiple(productos)
        
