import time
import threading
import difflib
import json
import os

if __name__ == "__main__":
    from pedido_parser import Parser
    from descargar_dropbox import descargar_excels, descargar_jefes
    from chatbot import ChatBot
    from excel import excel_to_table, cargar_pedidos, deudas_jefe
    rel = ""
else:
    rel = "bot/"
    from bot.pedido_parser import Parser
    from bot.descargar_dropbox import descargar_excels, descargar_jefes
    from bot.chatbot import ChatBot
    from bot.excel import excel_to_table, cargar_pedidos, deudas_jefes


def historial(func):
    def _responder(self, mensaje, chat_id):
        guardar_mensaje(chat_id, "USER", mensaje)
        respuesta = func(self, mensaje, chat_id)
        if type(respuesta).__name__ == "tuple":
            respuesta_a_guardar = respuesta[0]
        else:
            respuesta_a_guardar = respuesta
        guardar_mensaje(chat_id, "BOT", respuesta_a_guardar)
        return respuesta
    return _responder

def no_bot(func):
    def _responder(self, mensaje, chat_id):
        respuesta = func(self, mensaje, chat_id)
        if not self.bot:
            if type(respuesta).__name__ == "tuple":
                respuesta = respuesta[0]
        return respuesta
    return _responder

def permiso(*roles):
    def _permiso(func):
        def _func(self, chat_id, *args):
            for rol in roles:
                if chat_id in self.roles[rol]:
                    break
            else:
                def no_permiso():
                    yield "No tienes permiso para utilizar esta función"
                return no_permiso()
            return func(self, chat_id, *args)
        return _func
    return _permiso
    

class MessageHandler:

    def __init__(self, bot=False):
        self.conversaciones = {}
        self.funciones = {
            "start": self.start,
            "help": self.help,
            "ayuda": self.help,
            "lector": self.lector,
            "jefes": self.jefes,
            "datos": self.datos,
            "lector_detalles": self.lector_detalles,
            "agregar": self.agregar_usuario,
            "chat_id": self.chat_id,
            "ver_roles": self.ver_roles,
            "encargados": self.encargados,
            "deudas": self.deudas,
            "cobranza": self.cobranza,
            "productos": self.productos,
            "precio": self.cambiar_precio
            }
        with open(rel+"datos/roles.json", "r") as file:
            self.roles = json.load(file)
        self.parser = Parser()
        self.bot = bot
        self.chatbot = ChatBot()

    @historial
    @no_bot
    def responder(self, mensaje, chat_id):
        if mensaje[0] == "/":
            mensaje = mensaje.split()
            func, args = mensaje[0].strip("/"), mensaje[1:]
            try:
                generador = self.funciones[func](chat_id, *args)
            except KeyError as err:
                return "Funcion no encontrada."
            except TypeError as err:
                return str(err)
            self.conversaciones[chat_id] = generador
            respuesta = next(generador)
            return respuesta
        elif chat_id in self.conversaciones:
            generador = self.conversaciones[chat_id]
        else:
            return self.chat_bot(chat_id, mensaje)
        try:
            respuesta = generador.send(mensaje)
            return respuesta
        except (StopIteration, NameError):
            return self.chat_bot(chat_id, mensaje)

    def chat_bot(self, chat_id, mensaje):
        return "Chat"
    
    def start(self, chat_id):
        yield leer("start")

    def help(self, chat_id):
        yield leer("help")

    @permiso("owner", "admin", "moderador")
    def lector(self, chat_id):
        pedidos = yield "Envíame la lista de pedidos!"
        status = "continue"
        try:
            if self.bot:
                yield "Espera un segundo...", "wait"
            p = self.parser
            p.actualizar_equivalencias()
            p.parse(pedidos.split("\n"))
            respuesta =  "```\n"
            respuesta += "{}:\n\n".format(p.pedido)
            respuesta += "Total por producto:\n"
            respuesta += p.total_por_producto()
            respuesta += "\n\n"
            respuesta += "Total por persona:\n"
            respuesta += p.total_por_jefes()
            respuesta += "```"
        except Exception as err:
            respuesta = str(err)
            status = "error"
        if respuesta.strip() == "":
            respuesta = "Lo siento, no entendí."
        yield respuesta, status

    @permiso("owner", "admin", "moderador")
    def lector_detalles(self, chat_id):
        pedidos = yield "Envíame la lista de pedidos!"
        status = "continue"
        try:
            if self.bot:
                yield "Espera un segundo...", "wait"
            p = self.parser
            p.actualizar_equivalencias()
            p.parse(pedidos.split("\n"))
            respuesta =  "```\n"
            respuesta += "{}:\n\n".format(p.pedido)
            respuesta += "Total por producto:\n"
            respuesta += p.total_por_producto()
            respuesta += "\n\n"
            respuesta += "Detalle:\n"
            respuesta += p.resumen_pedidos()
            respuesta += "``` "
            respuesta += "Poner en modo horizontal para ver correctamente."
        except Exception as err:
            respuesta = str(err)
            status = "error"
        if respuesta.strip() == "":
            respuesta = "Lo siento, no entendí."
        yield respuesta, status

    @permiso("owner", "admin", "moderador", "repartidor")
    def jefes(self, chat_id):
        status = "continue"
        try:
            if self.bot:
                yield "Espera un segundo...", "wait"
            descargar_jefes(rel+"datos")
            tabla = excel_to_table(rel+"datos/Jefes 2017-2.xlsx", "Personas")
            s = ""
            for i, jefe in enumerate(tabla):
                s += "{0:<2} - {1} {2}\n".format(i+1, jefe[0], jefe[1])
        except Exception as err:
            s = str(err)
            status = "error"
        yield s, status

    @permiso("owner", "admin", "moderador", "repartidor")
    def datos(self, chat_id, id_jefe, *args):
        status = "continue"
        try:
            s = ""
            if self.bot:
                yield "Espera un segundo...", "wait"
            descargar_jefes(rel+"datos")
            tabla = excel_to_table(rel+"datos/Jefes 2017-2.xlsx", "Personas")
            if is_int(id_jefe):
                jefe = tabla[int(id_jefe)-1]
            else:
                nombres = [j[0] + " " + j[1] for j in tabla]
                nombre = " ".join([id_jefe]+list(args))
                match = difflib.get_close_matches(nombre, nombres)
                if len(match) > 0:
                    jefe = tabla[nombres.index(match[0])]
                    s = ""
                    yield "Esta es la coincidencia que se encontro:", "more"
                else:
                    yield "No se han encontrado coincidencias", "continue"
            s += "*{} {}*\n\n".format(jefe[0], jefe[1])
            s += "Direccion: {}, {}\n".format(jefe[2], jefe[3])
            s += "Telefono: +{}\n".format(jefe[7])
            s += "Mail: {}\n".format(jefe[8].replace("_", "\\_"))
            s += "Encargado: {}\n".format(jefe[9])
        except Exception as err:
            s = str(err)
            status = "error"
        yield s, status

    @permiso("owner")
    def agregar_usuario(self, chat_id, rol, id_usuario):
        if len(id_usuario) != 9 or not is_int(id_usuario):
            yield "chat\_id no valida."
        try:
            self.roles[rol].append(int(id_usuario))
        except KeyError:
            yield "Rol no válido."
        with open(rel+"datos/roles.json", "w") as file:
            json.dump(self.roles, file, sort_keys=True, indent=4)
        yield "Hecho!"

    def chat_id(self, chat_id):
        yield str(chat_id)

    @permiso("owner", "admin")
    def ver_roles(self, chat_id):
        s = ""
        for rol in self.roles:
            s += mayus(rol) + ":\n"
            for usuario in self.roles[rol]:
                s += " - {}\n".format(usuario)
        yield s.strip()

    @permiso("owner", "admin")
    def deudas(self, chat_id, id_jefe, *args):
        status = "continue"
        try:
            s = ""
            if self.bot:
                yield "Espera un segundo...", "wait"
            descargar_excels(rel+"datos")
            tabla = excel_to_table(rel+"datos/Jefes 2017-2.xlsx", "Personas")
            if is_int(id_jefe):
                jefe = tabla[int(id_jefe)-1]
            else:
                nombres = [j[0] + " " + j[1] for j in tabla]
                nombre = " ".join([id_jefe]+list(args))
                match = difflib.get_close_matches(nombre, nombres)
                if len(match) > 0:
                    jefe = tabla[nombres.index(match[0])]
                    s = ""
                    yield "Esta es la coincidencia que se encontro:", "more"
                else:
                    yield "No se han encontrado coincidencias", "continue"
            nombre = jefe[0] + " " + jefe[1]
            deudas = deudas_jefe(nombre)
            s += "*{}*\n\n".format(nombre)
            s += "Deudas:\n"
            total = 0
            for fecha, deuda in deudas:
                s += "- {}: {}\n".format(fecha, deuda)
                total += int(deuda)
            s += "Total: {}".format(total)
        except Exception as err:
            s = str(err)
            status = "error"
        yield s.strip(), status

    @permiso("owner", "admin")
    def cobranza(self, chat_id, encargado, *args):
        status = "continue"
        try:
            if self.bot:
                yield "Espera un segundo...", "wait"
            descargar_excels(rel+"datos")
            tabla = excel_to_table(rel+"datos/Jefes 2017-2.xlsx", "Personas")
            encargados = list(set([jefe[9] for jefe in tabla]))
            encargados = [e for e in encargados if str(e) != "nan"]
            apodos = excel_to_table(rel+"datos/Jefes 2017-2.xlsx",
                                    "Apodos Cobranza")
            apodos = {nombre: apodo for nombre, apodo in apodos}
            if is_int(encargado):
                encargado = encargados[int(encargado)-1]
            else:
                nombre = " ".join([encargado]+list(args))
                match = difflib.get_close_matches(nombre, encargados)
                if len(match) > 0:
                    encargado = match[0]
                else:
                    yield "No se han encontrado coincidencias", "continue"
            yield "Encargado: {}".format(encargado), "more"
            jefes = [jefe[0] + " " + jefe[1] for jefe in tabla
                     if jefe[9] == encargado]
            deudas_totales = deudas_jefes(jefes)
            for jefe in jefes:
                deudas = deudas_totales[jefe]
                s = leer("texto_deudas")
                d = ""
                total = 0
                for fecha, deuda in deudas:
                    d += "- {}: {}\n".format(fecha, deuda)
                    total += int(deuda)
                if total == 0:
                    continue
                d += "Total: {}".format(total)
                s = s.format(nombre=apodos[jefe], deudas=d)
                yield jefe, "more"
                yield s, "more"
            s = "Listo!"
        except Exception as err:
            s = str(err)
            status = "error"
        yield s, status

    @permiso("owner", "admin")
    def encargados(self, chat_id):
        status = "continue"
        try:
            if self.bot:
                yield "Espera un segundo...", "wait"
            descargar_jefes(rel+"datos")
            tabla = excel_to_table(rel+"datos/Jefes 2017-2.xlsx", "Personas")
            encargados = list(set([jefe[9] for jefe in tabla]))
            s = ""
            for i, encargado in enumerate(encargados):
                s += "{0:<2} - {1}\n".format(i+1, encargado)
        except Exception as err:
            s = str(err)
            status = "error"
        yield s.strip(), status

    def productos(self, chat_id):
        path = "grafica"
        if rel != "bot/":
            parent = os.path.relpath(os.path.join(rel, os.pardir))
            path = os.path.join(parent, path)
        with open(path + "/productos.json", "r") as file:
            data = json.load(file)
        s = ""
        for producto, formatos in data.items():
            for formato, detalles in formatos.items():
                s += ""

    def cambiar_precio(self, producto, formato, precio):
        pass
        
        
def leer(texto):
    with open(rel+"mensajes/{}.txt".format(texto)) as file:
        s = "".join(file.readlines())
    return s

def guardar_mensaje(chat_id, emisor, mensaje):
    with open(rel+"historial/{}.txt".format(chat_id), "a") as file:
        tiempo = time.strftime("%Y-%m-%d %H:%M:%S")
        file.write("{0} {1:<4}: {2}\n".format(tiempo, emisor, mensaje))

def is_int(n):
    try:
        int(n)
        return True
    except ValueError:
        return False

def mayus(string):
    return " ".join([s[0].upper() + s[1:] for s in string.split()])

if __name__ == "__main__":
    h = MessageHandler()

    i = 111111111

    while True:
        r = h.responder(input(">>> "), i)
        print(r)

