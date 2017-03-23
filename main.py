from flask import Flask, render_template, redirect, url_for, request, \
     send_file, send_from_directory
from grafica.datos import agregar_datos, agregar_datos_multiples
from utilidades import mayus
    
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home_page.html")

@app.route("/difusion", methods=['GET', 'POST'])
def difusion():
    error = None
    if request.method == 'POST':
        nombre = request.form["nombre"].lower().strip()
        apellido = request.form["apellido"].lower().strip()
        telefono = request.form["telefono"]
        fruta = request.form["fruta"]
        precio = request.form["precio"]
        if len(telefono) < 8:
            error = "Telefono no válido."
        else:
            telefono = "+569" + telefono.strip().replace(" ", "")[-8:]
            return redirect(url_for(
                "difusion_datos", nombre=nombre, apellido=apellido,
                numero=telefono, fruta=fruta, precio=precio))
    return render_template('difusion_datos.html', error=error)

@app.route("/difusion/<nombre>-<apellido>-<numero>-<fruta>-<precio>")
def difusion_datos(nombre, apellido, numero, fruta, precio):
    nombre = mayus(nombre)
    apellido = mayus(apellido)
    precio = int(precio)
    frutas = {
        "0": "frutillas",
        "1": "cerezas",
        "2": "paltas",
        "3": "arandanos",
        "4": "duraznos",
        "5": "uvas"
        }
    file = agregar_datos(nombre, apellido, numero, frutas[fruta], precio)
    return send_file(file, mimetype='image/gif')

@app.route("/difusion_multiple", methods=['GET', 'POST'])
def difusion_multiple():
    error = None
    if request.method == 'POST':
        nombre = request.form["nombre"].lower().strip()
        apellido = request.form["apellido"].lower().strip()
        telefono = request.form["telefono"]
        frutillas = request.form["frutillas"]
        uvas= request.form["uvas"]
        paltas = request.form["paltas"]
        limones = request.form["limones"]
        
        frutillas = 6000 if frutillas == "" else frutillas
        uvas = 5000 if uvas == "" else uvas
        paltas = 6000 if paltas == "" else paltas
        limones = 6000 if limones == "" else limones
        
        if len(telefono) < 8:
            error = "Telefono no válido."
        else:
            telefono = "+569" + telefono.strip().replace(" ", "")[-8:]
            print("Hola")
            return redirect(url_for(
                "difusion_datos_multiples",
                nombre=nombre, apellido=apellido, numero=telefono,
                frutillas=frutillas, uvas=uvas,
                paltas=paltas, limones=limones))
    return render_template('difusion_multiple.html', error=error)

@app.route(
    "/difusion_multiple/<nombre>-<apellido>-<numero>-<frutillas>-"+
    "<uvas>-<paltas>-<limones>")
def difusion_datos_multiples(nombre, apellido, numero,
                   frutillas, uvas, paltas, limones):
    file = agregar_datos_multiples(nombre, apellido, numero,
                                   frutillas, uvas, paltas, limones)
    return send_file(file, mimetype='image/gif')

@app.route("/excel_vendedor")
def excel_vendedor():
    return send_from_directory(directory="descargas",
                               filename="Vendedores.xlsx",
                               as_attachment=True)

@app.route("/construccion")
def construccion():
    return "Página en construcción"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
