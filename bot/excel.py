import pandas as pd
import os

try:
    from lector_excel import cargar_pedido, hojas
    rel = ""
except Exception:
    rel = "bot/"
    from bot.lector_excel import cargar_pedido, hojas

def excel_to_table(file, hoja):
    table = pd.read_excel(
        file, sheetname=hoja, header=0,
        parse_cols="A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q," + \
        " R, S, T, U, V, W, X, Y, Z")
    fin = 0
    for i in range(len(table)):
        fila = table.iloc[i].real
        nombre = fila[0]
        fin = i
        if str(nombre) == " " or str(nombre) == "nan" or str(nombre) == "":
            break
    tabla = table[0:fin]
    tabla = [[j for j in tabla.iloc[i].real]
             for i in range(len(tabla))]
    return tabla

def cargar_pedidos(path):
    pedidos_totales = {}
    files = [f for f in os.listdir(path) if f[0:2] == "20" and ".xl" in f]
    files.remove("2017 - 08 (Agosto).xlsx")
    for file in files:
        sheets = hojas(path + "/" + file)[1:]
        for hoja in sheets:
            pedido, info = cargar_pedido(path + "/" + file, hoja)
            pedidos_totales[info["fecha_formato"]] = pedido
    return pedidos_totales

def deudas_jefe(jefe, path=rel+"datos"):
    pedidos = cargar_pedidos(path)
    deudas_jefe = []
    for fecha in sorted(list(pedidos.keys())):
        for persona in pedidos[fecha]:
            if persona["nombre"] == jefe:
                if persona["pagado"] == "NO":
                    deudas_jefe.append((fecha, persona["deuda"]))
    return deudas_jefe
            

if __name__ == "__main__":
    d = deudas("Majo Castañeda")
