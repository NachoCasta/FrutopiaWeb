import time
import threading

if __name__ == "__main__":
    from pedido_parser import Parser
    from descargar_dropbox import descargar_excels
    rel = ""
else:
    rel = "bot/"
    from bot.pedido_parser import Parser
    from bot.descargar_dropbox import descargar_excels


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
            "lector": self.lector
            }
        self.parser = Parser()
        self.bot = bot

    @no_bot
    @historial
    def responder(self, mensaje, chat_id):
        if mensaje[0] == "/":
            mensaje = mensaje.split()
            func, args = mensaje[0].strip("/"), mensaje[1:]
            generador = self.funciones[func](*args)
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
            p = self.parser
            thread = threading.Thread(target=p.actualizar_equivalencias)
            thread.start()
            yield "Espera un segundo...", "wait"
            while thread.is_alive():
                yield "Espera un segundo...", "wait"
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

def leer(texto):
    with open(rel+"mensajes/{}.txt".format(texto)) as file:
        s = "\n".join(file.readlines())
    return s

def guardar_mensaje(chat_id, emisor, mensaje):
    with open(rel+"historial/{}.txt".format(chat_id), "a") as file:
        tiempo = time.strftime("%Y-%m-%d %H:%M:%S")
        file.write("{0} {1:<4}: {2}\n".format(tiempo, emisor, mensaje))

if __name__ == "__main__":
    h = MessageHandler()

    i = 1

    while True:
        r = h.responder(input(">>> "), i)
        print(r)

