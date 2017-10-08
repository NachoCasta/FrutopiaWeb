import pandas as pd

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
    tabla = [[j for j in tabla.iloc[i].real if str(j) != "nan"]
             for i in range(len(tabla))]
    return tabla

if __name__ == "__main__":
    t = excel_to_table("datos/Jefes 2017-2.xlsx", "Personas")
    print(t)
