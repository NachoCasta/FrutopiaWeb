from pedido_parser import Parser
from excel import parser_to_excel

if __name__ == "__main__":
    with open("pedidos whatsapp.txt") as file:
        texto = file.readlines()
    p = Parser()
    p.parse(texto, 20)
    parser_to_excel(p, "Diciembre", "Sabado 23")
    
