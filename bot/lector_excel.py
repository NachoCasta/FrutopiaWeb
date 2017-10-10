import pandas as pd
import json

try:
    import bot.utilidades as utilidades
except Exception:
    import utilidades

def cargar_pedido(file, hoja):
    table = pd.read_excel(
        file, sheetname=hoja, header=3,
        parse_cols="B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q," + \
        " R, S, T, U, V, W, X, Y, Z")
    deseadas = ["Nombre", "Apellido", "Direccion", "Comuna", "Sector",
                "Encargado", "Pagado", "Telefono", "Mail", "Deuda"]
    columnas = {}
    productos_keys = {}
    agregar = False
    for i, head in enumerate(list(table)):
        if head == "Total":
            columnas[head.lower()] = i
            break
        if head in deseadas:
            columnas[head.lower()] = i
        if agregar:
            productos_keys[head.lower().replace(" ","")] = i
        if head == "Deuda":
            agregar = True
    fin = 0
    for i in range(len(table)):
        fila = table.iloc[i].real
        nombre = fila[0]
        if str(nombre) == "nan":
            fin = i
            break
    tabla = table[0:fin]
    precios = table.iloc[fin+9].real

    pedidos = []
    productos = utilidades.obtener_productos(todos=True)
    productos_disponibles = {}
    for variable in productos_keys:
        for producto in productos:
            if producto["variable"] == variable:
                productos_disponibles[variable] = producto
    for i in range(len(tabla)):
        fila = tabla.iloc[i].real
        if fila[columnas["total"]] == 0:
            continue
        pedido = {}
        pedido["direccion"] = ", ".join((str(fila[columnas["direccion"]]),
                                         str(fila[columnas["comuna"]]),
                                         str(fila[columnas["sector"]])))
        pedido["nombre"] = " ".join((str(fila[columnas["nombre"]]),
                                     str(fila[columnas["apellido"]])))
        pedido["numero"] = int(fila[columnas["telefono"]])
        pedido["mail"] = fila[columnas["mail"]]
        pedido["encargado"] = fila[columnas["encargado"]]
        pedido["pagado"] = fila[columnas["pagado"]]
        for variable, x in productos_keys.items():
            producto = productos_disponibles[variable]
            pedido[variable] = fila[x]
            pedido[producto["variable_precio"]] = precios[x]
        pedido["deuda"] = fila[columnas["deuda"]]
        pedidos.append(pedido)

    fecha_formato = file.replace(" ","").split("(")[0] + \
                    "-" + hoja.split()[1].zfill(2)
    fecha_formato = fecha_formato.split("/")[-1]

    info = {
        "pedido": hoja,
        "productos": list(productos_disponibles.values()),
        "fecha_formato": fecha_formato,
        "fecha": " de ".join((hoja, file.split("(")[1].split(")")[0],
                              file.split(" - ")[0]))
            }
    
    return pedidos, info

def hojas(file="nuevo excel.xlsx"):
    excel = pd.ExcelFile(file)
    return excel.sheet_names

if __name__ == "__main__":
    t = cargar_pedido("2017 - 09 (Septiembre).xlsm", "Sabado 23")
