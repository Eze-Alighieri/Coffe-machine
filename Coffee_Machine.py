import json

with open("recursos_y_requerimientos.json", "r") as archivo:
    datos = json.load(archivo)


recursos_disponibles = datos["recursos_disponibles"]
requerimientos = datos["requerimientos"]
ventas = datos["ventas"]
dinero_inicial = datos["dinero_inicial"]

def vueltas(a):
    cant_1000 = a // 1000
    cant_500 = (a % 1000) // 500
    cant_200 = ((a % 1000) % 500) // 200
    cant_100 = (((a % 1000) % 500) % 200) // 100
    remover_monedas(cant_1000, cant_500, cant_200, cant_100)
    print(f"Su cambio es ${a}\n")
    lista_monedas = [cant_1000, cant_500, cant_200, cant_100]
    tipo_monedas = ["1000", "500", "200", "100"]
    i = 0
    for item in lista_monedas:
        if item == 0 or item > 1:
            print(f"{item} monedas de ${tipo_monedas[i]}")
        else:
            print(f"{item} moneda de ${tipo_monedas[i]}")
        i += 1
    print()

def guardar_datos(data):
    with open("recursos_y_requerimientos.json", "w") as file:
        json.dump(data, file, indent=4)

def checkear_suf_recursos(entrada_):
    if recursos_disponibles["agua"][0] >= requerimientos[entrada_]["agua"] and \
            recursos_disponibles["cafe"][0] >= requerimientos[entrada_]["cafe"] and \
            recursos_disponibles["leche"][0] >= requerimientos[entrada_]["leche"]:
        return True
    else:
        return False

def actualizar_recursos(entrada_):
    for _key in ["agua", "cafe", "leche"]:
        recursos_disponibles[_key][0] -= requerimientos[entrada_][_key]
    recursos_disponibles["dinero"][1] += requerimientos[entrada_]["precio"]
    ventas[entrada_] += 1
    guardar_datos(datos)


def reporte():
    temp = 0
    for key in dinero_inicial:
        temp += dinero_inicial[key][0]*dinero_inicial[key][1]

    recursos_disponibles["dinero"][1] = temp

    print()
    for key_ in recursos_disponibles:
        print(f"{key_.capitalize()}: {''.join([str(item) for item in recursos_disponibles[key_]])}")
    print()
    
def agregar_monedas(monedas_1000, monedas_500, monedas_200, monedas_100):
    monedas = [monedas_1000, monedas_500, monedas_200, monedas_100]
    i = 0
    for key in dinero_inicial:
        dinero_inicial[key][0] += monedas[i]
        i += 1

def remover_monedas(monedas_1000, monedas_500, monedas_200, monedas_100):
    monedas = [monedas_1000, monedas_500, monedas_200, monedas_100]
    i = 0
    for key in dinero_inicial:
        dinero_inicial[key][0] -= monedas[i]
        i += 1

def insertar_monedas(precio_bebida, entrada_):
    print("Por favor inserte las monedas.")
    m_mil = int(input("Cuantas monedas de $1000?: "))
    m_quinientos = int(input("Cuantas monedas de $500?: "))
    m_docientos = int(input("Cuantas monedas de $200?: "))
    m_cien = int(input("Cuantas monedas de $100?: "))
    agregar_monedas(m_mil, m_quinientos, m_docientos, m_cien)
    print()
    
    print()
    total_en_monedas = m_cien*100 + m_docientos*200 + m_quinientos*500 + m_mil*1000
    cambio = total_en_monedas - precio_bebida

    if total_en_monedas < precio_bebida:
        remover_monedas(m_mil, m_quinientos, m_docientos, m_cien)
        print("Lo siento, no es la cantidad suficiente, dinero devuelto.")
        print()
    else:
        vueltas(cambio)
        print(f"Aquí está su {entrada_.capitalize()} \u2615 que lo disfrute!")
        print()
        actualizar_recursos(entrada_)

def reiniciar():
    global datos, recursos_disponibles, requerimientos, ventas, dinero_inicial
    with open("reinicio.json") as file:
        estructura_inicial = json.load(file)
    with open("recursos_y_requerimientos.json", "w") as archivo:
        json.dump(estructura_inicial, archivo, indent=4)
    datos = estructura_inicial
    recursos_disponibles = datos["recursos_disponibles"]
    requerimientos = datos["requerimientos"]
    ventas = datos["ventas"]
    dinero_inicial = datos["dinero_inicial"]

print("Lista de precios")
print(f"Tinto:      ${requerimientos["tinto"]["precio"]}")
print(f"Latte:      ${requerimientos["latte"]["precio"]}")
print(f"Cappuccino: ${requerimientos["cappuccino"]["precio"]}\n")

encendido = True
while encendido:
    entrada = input("Qué te gustaría tomar? (Tinto / Latte / Cappuccino): ")
    if entrada.lower() == "tinto" or entrada.lower() == "latte" or entrada.lower() == "cappuccino":
        if checkear_suf_recursos(entrada.lower()):
            insertar_monedas(requerimientos[entrada.lower()]["precio"], entrada.lower())
        else:
            for key in ["agua", "cafe", "leche"]:
                if recursos_disponibles[key][0] <= requerimientos[entrada][key]:
                    print(f"Lo sentimos, no hay suficiente {key}", end="\n")
    elif entrada.lower() == "reporte":
        reporte()
    elif entrada.lower() == "ventas":
        print()
        print("Productos vendidos")
        for key_ in ventas:
            print(f"{key_}: {ventas[key_]}")
        print()
    elif entrada.lower() == "off":
        encendido = False
    elif entrada.lower() == "reiniciar":
        reiniciar()
    elif entrada.lower() == "monedas":
        for key in dinero_inicial:
            print(key, f" {dinero_inicial[key][0]}")
