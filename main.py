import urllib3
import time

import telepot
from flask import Flask, render_template, redirect, url_for, request, \
     send_file, send_from_directory

from grafica.datos import agregar_datos, agregar_datos_multiples, \
     agregar_datos_vendedores, agregar_datos_frutillas_cerezas
from utilidades import mayus, obtener_productos, crear_template_multiple
from grafica.difusion_multiple import crear_difusion_multiple
from bot.message_handler import MessageHandler

secret = "hgckmlwpojik9fbfdihbsiuo"
bot = telepot.Bot("462586547:AAF0sLikfUc2-ixPIJ125NsWIhifMWQiBv8")
bot.setWebhook("https://www.frutopiachile.cl/{}".format(secret), max_connections=1)

handler = MessageHandler(True)

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

@app.route("/difusion_vendedores", methods=['GET', 'POST'])
def difusion_vendedores():
    error = None
    if request.method == 'POST':
        nombre = request.form["nombre"].lower().strip()
        apellido = request.form["apellido"].lower().strip()
        telefono = request.form["telefono"]
        if len(telefono) < 8:
            error = "Telefono no válido."
        else:
            telefono = "+569" + telefono.strip().replace(" ", "")[-8:]
        nombre = mayus(nombre)
        apellido = mayus(apellido)
        numero = telefono
        file = agregar_datos_vendedores(nombre, apellido, numero)
        return send_file(file, mimetype='image/gif')
    return render_template('difusion_datos_vendedores.html', error=error)

@app.route("/frutillas_cerezas", methods=['GET', 'POST'])
def difusion_fru_cere():
    error = None
    if request.method == 'POST':
        nombre = request.form["nombre"].lower().strip()
        apellido = request.form["apellido"].lower().strip()
        telefono = request.form["telefono"]
        if len(telefono) < 8:
            error = "Telefono no válido."
        else:
            telefono = "+569" + telefono.strip().replace(" ", "")[-8:]
        nombre = mayus(nombre)
        apellido = mayus(apellido)
        numero = telefono
        file = agregar_datos_frutillas_cerezas(nombre, apellido, numero)
        return send_file(file, mimetype='image/gif')
    return render_template('difusion_datos_vendedores.html', error=error)

@app.route("/difusion_multiple", methods=['GET', 'POST'])
def difusion_multiple():
    error = None
    productos = obtener_productos()
    if request.method == 'POST':
        nombre = request.form["nombre"].lower().strip()
        apellido = request.form["apellido"].lower().strip()
        telefono = request.form["telefono"]
        vendedor = {
            "nombre": nombre,
            "apellido": apellido,
            "telefono": telefono
            }
        if len(telefono) < 8:
            error = "Telefono no válido."
        else:
            file = crear_difusion_multiple(vendedor, productos)
            return send_file(file, mimetype='image/gif')
    crear_template_multiple(productos)
    return render_template('difusion_multiple.html', error=error)

@app.route("/excel_vendedor")
def excel_vendedor():
    return send_from_directory(directory="descargas",
                               filename="Vendedores.xlsx",
                               as_attachment=True)

@app.route('/{}'.format(secret), methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if "message" in update:
        status = None
        mensaje = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        #bot.sendMessage(chat_id, mensaje)
        try:
            respuesta = handler.responder(mensaje, chat_id)
        except Exception as err:
            bot.sendMessage(chat_id, str(err))
        if len(list(respuesta)) == 2:
            respuesta, status = respuesta
        if stats == "error":
            bot.sendMessage(chat_id, respuesta)
        if status == "wait":
            bot.sendMessage(chat_id, respuesta, "Markdown")
            while status == "wait":
                respuesta, status = handler.responder("waiting", chat_id)
        if status == "more":
            while status == "more":
                bot.sendMessage(chat_id, respuesta, "Markdown")
                respuesta, status = handler.responder("more", chat_id)
        if respuesta == "":
            respuesta = "Error."
        try:
            bot.sendMessage(chat_id, respuesta, "Markdown")
        except Exception as err:
            bot.sendMessage(chat_id, str(err))
    return "OK"

@app.route("/construccion")
def construccion():
    return "Página en construcción"

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
