import time
import threading
import difflib

if __name__ == "__main__":
    from pedido_parser import Parser
    from descargar_dropbox import descargar_excels, descargar_jefes
    from chatbot import ChatBot
    from excel import excel_to_table
    rel = ""
else:
    rel = "bot/"
    from bot.pedido_parser import Parser
    from bot.descargar_dropbox import descargar_excels, descargar_jefes
    from bot.chatbot import ChatBot
    from bot.excel import excel_to_table


def historial(func):
    def _responder(self, mensaje, chat_id):
        guardar_mensaje(chat_id, "USER", mensaje)
        respuesta = func(self, mensaje, chat_id)
        guardar_mensaje(chat_id, "BOT", respuesta)
        return respuesta
    return _responder

def no_bot(func):
    def _responder(self, mensaje, chat_id):
        respuesta = func(self, mensaje, chat_id)
        if not self.bot:
            if len(list(respuesta)) == 2:
                respuesta = respuesta[0]
        return respuesta
    return _responder

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
            "lector_detalles": self.lector_detalles
            }
        self.parser = Parser()
        self.bot = bot
        self.chatbot = ChatBot()

    @historial
    @no_bot
    def responder(self, mensaje, chat_id):
        if mensaje[0] == "/":
            mensaje = mensaje.split()
            func, args = mensaje[0].strip("/"), mensaje[1:]
            if func == "chat_id":
                return str(chat_id)
            try:
                generador = self.funciones[func](*args)
            except KeyError:
                return "Funcion no encontrada."
            except TypeError as err:
                return str(err)
            self.conversaciones[chat_id] = generador
            respuesta = next(generador)
            return respuesta
        elif chat_id in self.conversaciones:
            generador = self.conversaciones[chat_id]
        else:
            return self.chat_bot(mensaje)
        try:
            respuesta = generador.send(mensaje)
            return respuesta
        except (StopIteration, NameError):
            return self.chat_bot(mensaje)

    def chat_bot(self, mensaje):
        return "Chat"
    
    def start(self):
        yield leer("start")

    def help(self):
        yield leer("help")

    def lector(self):
        pedidos = yield "Envíame la lista de pedidos!"
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
        if respuesta.strip() == "":
            respuesta = "Lo siento, no entendí."
        yield respuesta, "continue"

    def lector_detalles(self):
        pedidos = yield "Envíame la lista de pedidos!"
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
        if respuesta.strip() == "":
            respuesta = "Lo siento, no entendí."
        yield respuesta, "continue"

    def jefes(self):
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
        yield s, "continue"
        
    def datos(self, id_jefe, *args):
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
                    s += "Esta es la coincidencia que se encontro:\n\n"
                else:
                    yield "No se han encontrado coincidencias", "continue"
            s += "Nombre: *{} {}*\n".format(jefe[0], jefe[1])
            s += "Direccion: {}, {}\n".format(jefe[2], jefe[3])
            s += "Telefono: +{}\n".format(jefe[7])
            s += "Mail: {}\n".format(jefe[8].replace("_", "\\_"))
            s += "Encargado: {}\n".format(jefe[9])
        except Exception as err:
            s = str(err)
        yield s, "continue"

    def deudas(self):
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

if __name__ == "__main__":
    h = MessageHandler()

    i = 1

    while True:
        r = h.responder(input(">>> "), i)
        print(r)

