import concurrent.futures
import requests
import threading

def obtener_datos_paginados(url):
    datos_totales = []

    def obtener_pagina(page):
        response = requests.get(f"{url}?page={page}")
        if response.status_code == 200:
            datos_pagina = response.json()
            return datos_pagina['data']
        else:
            print(f"Error al obtener los datos de la página {page}.")
            return []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        page = 0
        while True:
            futures.append(executor.submit(obtener_pagina, page))
            page += 1
            if not futures[page - 1].result():
                break

        for future in concurrent.futures.as_completed(futures):
            datos_totales.extend(future.result())

    return datos_totales

def obtener_fondos_mas_rindieron(fecha_inicio, fecha_fin):
    url_fondos = "https://api.cafci.org.ar/fondo/"
    fondos = obtener_datos_paginados(url_fondos)
    fondos_filtrados = []
    fondos_procesados = 0
    fondos_totales = len(fondos)

    lock = threading.Lock()  # Lock para sincronizar el acceso a la variable compartida

    def procesar_fondo(fondo):
        nonlocal fondos_procesados

        url_clase = f"https://api.cafci.org.ar/fondo/{fondo['id']}/clase"
        response_clase = requests.get(url_clase)

        if response_clase.status_code == 200:
            fondos_clase = response_clase.json()['data']
            for fondoclase in fondos_clase:
                url_rendimiento = f"{url_clase}/{fondoclase['id']}/rendimiento/{fecha_inicio}/{fecha_fin}"
                response_rendimiento = requests.get(url_rendimiento)

                if response_rendimiento.status_code == 200:
                    rendimiento = response_rendimiento.json()
                    if 'error' not in rendimiento:
                        with lock:
                            fondos_filtrados.append({'nombre_fondo': fondo['nombre'], 'id_fondo': fondo['id'], 'rendimiento': rendimiento['data']['rendimiento']})

                fondos_procesados += 1
                mostrar_progreso(fondos_procesados, fondos_totales)

    def mostrar_progreso(procesados, totales):
        with lock:
            print(f"Fondos procesados: {procesados}/{totales}")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(procesar_fondo, fondos)

    fondos_filtrados = [f for f in fondos_filtrados if not isinstance(f, str)]
    fondos_filtrados = sorted(fondos_filtrados, key=lambda x: x['rendimiento'], reverse=True)

    return fondos_filtrados

print(obtener_fondos_mas_rindieron("2023-01-01", "2023-06-30"))