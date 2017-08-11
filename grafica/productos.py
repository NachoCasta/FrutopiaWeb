import json

productos = {
    "frutillas": {
        "2": {
            "nombre": "Frutillas 2 kg",
            "variable": "frutillas",
            "variable_precio": "f_precio",
            "formato": "cajas",
            "unidad": "kg",
            "foto": "frutillas.jpg",
            "disponible": False,
            "precio": "6000",
            "svg": "frutilla.txt"
            }
        },
    "paltas": {
        "2": {
            "nombre": "Paltas 2 kg",
            "variable": "paltas",
            "variable_precio": "p_precio",
            "formato": "mallas",
            "unidad": "kg",
            "foto": "paltas.jpg",
            "disponible": True,
            "precio": "6000",
            "svg": "frutilla.txt"
            }
        },
    "naranjas": {
        "5": {
            "nombre": "Naranjas 5 kg",
            "variable": "naranjas",
            "variable_precio": "nar_precio",
            "formato": "mallas",
            "unidad": "kg",
            "foto": "naranjas.jpg",
            "disponible": True,
            "precio": "4000",
            "svg": "frutilla.txt"
            }
        },
    "mandarinas": {
        "4": {
            "nombre": "Mandarinas 4 kg",
            "variable": "mandarinas",
            "variable_precio": "m_precio",
            "formato": "mallas",
            "unidad": "kg",
            "foto": "mandarinas.jpg",
            "disponible": True,
            "precio": "6000",
            "svg": "frutilla.txt"
            }
        },
    "quesos": {
        "1050": {
            "nombre": "Quesos 1050 gr",
            "variable": "quesos",
            "variable_precio": "q_precio",
            "formato": "packs",
            "unidad": "gr",
            "foto": "quesos.jpg",
            "disponible": True,
            "precio": "10000",
            "svg": "frutilla.txt"
            }
        },
    "tomates cherry": {
        "1": {
            "nombre": "Tomates Cherry 1 kg",
            "variable": "tomatecherry",
            "variable_precio": "t_precio",
            "formato": "cajas",
            "unidad": "kg",
            "foto": "tomatescherry.jpg",
            "disponible": True,
            "precio": "6000",
            "svg": "frutilla.txt"
            }
        },
    "nueces": {
        "500": {
            "nombre": "Nueces 500 gr",
            "variable": "nueces",
            "variable_precio": "nue_precio",
            "formato": "cajas",
            "unidad": "gr",
            "foto": "nueces.jpg",
            "disponible": True,
            "precio": "7000",
            "svg": "frutilla.txt"
            }
        }
    }

with open("productos.json", "w") as file:
    json.dump(productos, file, sort_keys=True, indent=4)

