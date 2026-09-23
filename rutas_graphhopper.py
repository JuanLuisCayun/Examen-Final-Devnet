import os
import requests

API_KEY = os.getenv("GRAPHHOPPER_API_KEY")
URL_GEOCODING = "https://graphhopper.com/api/1/geocode"
URL_ROUTE = "https://graphhopper.com/api/1/route"

if not API_KEY:
    print("Error: no se encontró la clave API de GraphHopper.")
    print("Configure la variable GRAPHHOPPER_API_KEY antes de ejecutar.")
    raise SystemExit(1)

def obtener_coordenadas(ciudad, pais):
    parametros = {
        "q": f"{ciudad}, {pais}",
        "locale": "es",
        "limit": 1,
        "key": API_KEY
    }

    respuesta = requests.get(
        URL_GEOCODING,
        params=parametros,
        timeout=15
    )
    respuesta.raise_for_status()
    resultados = respuesta.json().get("hits", [])

    if not resultados:
        return None

    ubicacion = resultados[0]
    return {
        "nombre": ubicacion.get("name", ciudad),
        "latitud": ubicacion["point"]["lat"],
        "longitud": ubicacion["point"]["lng"]
    }

def calcular_ruta(origen, destino, perfil):
    parametros = [
        ("point", f"{origen['latitud']},{origen['longitud']}"),
        ("point", f"{destino['latitud']},{destino['longitud']}"),
        ("profile", perfil),
        ("locale", "es"),
        ("instructions", "true"),
        ("calc_points", "true"),
        ("key", API_KEY)
    ]

    respuesta = requests.get(
        URL_ROUTE,
        params=parametros,
        timeout=30
    )
    respuesta.raise_for_status()
    rutas = respuesta.json().get("paths", [])

    if not rutas:
        return None

    return rutas[0]

def seleccionar_transporte():
    opciones = {
        "1": ("car", "Automóvil"),
        "2": ("bike", "Bicicleta"),
        "3": ("foot", "A pie")
    }

    print("\nSeleccione el medio de transporte:")
    print("1. Automóvil")
    print("2. Bicicleta")
    print("3. A pie")

    while True:
        opcion = input("Ingrese una opción (1-3): ").strip()

        if opcion in opciones:
            return opciones[opcion]

        print("Opción no válida. Intente nuevamente.")

def mostrar_resultados(ruta, transporte):
    distancia_metros = ruta["distance"]
    distancia_km = distancia_metros / 1000
    distancia_millas = distancia_km * 0.621371

    duracion_minutos = ruta["time"] / 60000
    horas = int(duracion_minutos // 60)
    minutos = int(duracion_minutos % 60)

    print("\n========== RESUMEN DE LA RUTA ==========")
    print(f"Medio de transporte: {transporte}")
    print(f"Distancia: {distancia_km:.2f} kilómetros")
    print(f"Distancia: {distancia_millas:.2f} millas")
    print(f"Duración estimada: {horas} horas y {minutos} minutos")

    print("\n========== INDICACIONES DE VIAJE ==========")
    instrucciones = ruta.get("instructions", [])

    for numero, instruccion in enumerate(instrucciones, start=1):
        texto = instruccion.get("text", "Continúe por la ruta")
        distancia = instruccion.get("distance", 0) / 1000
        print(f"{numero}. {texto} ({distancia:.2f} km)")

def main():
    print("=== PLANIFICADOR DE RUTAS CHILE - ARGENTINA ===")
    print("Escriba 'v' en cualquier ciudad para salir.")

    while True:
        ciudad_origen = input(
            "\nIngrese la ciudad de origen en Chile: "
        ).strip()

        if ciudad_origen.lower() == "v":
            print("Programa finalizado.")
            break

        ciudad_destino = input(
            "Ingrese la ciudad de destino en Argentina: "
        ).strip()

        if ciudad_destino.lower() == "v":
            print("Programa finalizado.")
            break

        try:
            origen = obtener_coordenadas(ciudad_origen, "Chile")
            destino = obtener_coordenadas(ciudad_destino, "Argentina")

            if origen is None:
                print("No se encontró la ciudad de origen.")
                continue

            if destino is None:
                print("No se encontró la ciudad de destino.")
                continue

            perfil, transporte = seleccionar_transporte()

            print(
                f"\nCalculando ruta desde {origen['nombre']} "
                f"hasta {destino['nombre']}..."
            )

            ruta = calcular_ruta(origen, destino, perfil)

            if ruta is None:
                print("No fue posible calcular una ruta.")
                continue

            mostrar_resultados(ruta, transporte)

        except requests.RequestException as error:
            print(f"Error al comunicarse con GraphHopper: {error}")
        except KeyError:
            print("La respuesta recibida no contiene los datos esperados.")


if __name__ == "__main__":
    main()
