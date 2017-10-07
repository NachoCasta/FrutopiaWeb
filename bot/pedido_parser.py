import pandas as pd
import threading

if __name__ == "__main__":
    from descargar_dropbox import descargar_jefes
    from excel import excel_to_table
    rel = ""
else:
    rel = "bot/"
    from bot.descargar_dropbox import descargar_jefes
    from bot.excel import excel_to_table

class Parser:

    def __init__(self):
        self.texto = ""
        self.jefes = []
        self.productos = {}
        self.total_por_jefe = {}
        self.cargar_equivalencias()
        self.repartos = []

    def parse(self, texto, limite=20):
        self.texto = texto
        self.jefes = []
        self.productos = {}
        self.total_por_jefe = {}
        self.cargar_equivalencias()
        self.repartos = []
        self.parse_lines()
        self.parse_jefes()

    def parse_lines(self):
        pedidos = []
        for i, line in enumerate(self.texto):
            if i == 0:
                self.pedido = line.strip("_")
                continue
            line = line.strip().strip("*").strip("_")
            if line == "":
                continue
            if line[0] != "-":
                producto = line
                self.productos[producto] = []
            if line[0] == "-":
                line = line.strip("-").strip()
                line = line.split()
                jefe, cantidad = " ".join(line[:-1]), int(line[-1])
                jefe = mayus(jefe)
                jefe = self.equivalente(jefe)
                self.productos[producto].append([jefe, cantidad])

    def cargar_equivalencias(self):
        descargar_jefes(rel+"datos")
        tabla = excel_to_table(rel+"datos/Jefes 2017-2.xlsx", "Apodos")
        self.equivalencias = tabla

    def total_por_producto(self):
        s = ""
        for producto, pedidos in self.productos.items():
            total = sum(p[1] for p in pedidos)
            s += producto + " - " + str(total) + "\n"
        return s.strip()
            
    def parse_jefes(self):
        self.jefes = {}
        for producto, pedidos in self.productos.items():
            for pedido in pedidos:
                jefe = pedido[0]
                if jefe not in self.jefes:
                    self.jefes[jefe] = {}
        for jefe in self.jefes:
            for producto, pedidos in self.productos.items():
                for j, unidades in pedidos:
                    if jefe == j:
                        self.jefes[jefe][producto] = unidades
                        break
                else:
                    self.jefes[jefe][producto] = 0

    def total(self, jefe):
        return sum(p[1] for p in self.jefes[jefe].items())

    def equivalente(self, jefe):
        for equivalencia in self.equivalencias:
            if jefe in equivalencia:
                return equivalencia[0]
        return jefe

    def resumen_pedidos(self):
        s = ""
        for jefe in sorted(self.jefes.keys()):
            s += "{0:<20}:".format(jefe)
            for producto in self.productos:
                s += "{0: ^4}".format(self.jefes[jefe][producto])
            s += "{0: ^5}".format(self.total(jefe))
            s += "\n"
        return s.strip()

    def total_por_jefes(self):
        s = ""
        for jefe in sorted(self.jefes.keys()):
            s += "{0: <20}:".format(jefe)
            s += "{0: ^5}".format(self.total(jefe))
            s += "\n"
        return s.strip()

def mayus(string):
    return " ".join([s[0].upper() + s[1:] for s in string.split()])

if __name__ == "__main__":
    with open("pedidos whatsapp.txt") as file:
        texto = file.readlines()
    p = Parser()
    p.parse(texto, 20)
    print(p.total_por_producto())
    print()
    print(p.resumen_pedidos())
