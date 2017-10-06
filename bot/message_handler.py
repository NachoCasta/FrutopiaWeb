from bot.pedido_parser import Parser

class MessageHandler:

    def __init__(self):
        self.conversaciones = {}

    def responder(mensaje, chat_id):
        if mensaje == "/start":
            return "Hola!"
        try:
            p = Parser(mensaje.split("\n"))
            respuesta = ""
            respuesta += p.total_por_producto()
            respuesta += "\n\n"
            respuesta += p.total_por_jefes()
        except Exception as err:
            respuesta = str(err)
        return respuesta
