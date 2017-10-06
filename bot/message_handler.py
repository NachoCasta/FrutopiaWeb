if __name__ == __main__:
    from pedido_parser import Parser
    from descargar_dropbox import descargar_excels
else:
    from bot.pedido_parser import Parser
    from bot.descargar_dropbox import descargar_excels


class MessageHandler:

    def __init__(self):
        self.conversaciones = {}
        self.funciones = {
            "start": self.start,
            "help": self.help,
            "ayuda": self.help,
            "lector": self.lector
            }

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
        return "Soy chat bot"
    
    def start(self):
        yield leer("start")

    def help(self):
        yield leer("help")

    def lector(self):
        pedidos = yield "Envíame la lista de pedidos!"
        print(pedidos)
        try:
            p = Parser(pedidos.split("\n"))
            respuesta = "```"
            respuesta += p.total_por_producto()
            respuesta += "\n\n"
            respuesta += p.total_por_jefes()
            respuesta += "```"
        except Exception as err:
            respuesta = str(err)
        if respuesta.strip() == "":
            respuesta = "Lo siento, no entendí."
        yield respuesta

def leer(texto):
    with open("mensajes/{}.txt".format(texto)) as file:
        s = "\n".join(file.readlines())
    return s

if __name__ == "__main__":
    h = MessageHandler()

    i = 1

    while True:
        r = h.responder(input(">>> "), i)
        print(r)

