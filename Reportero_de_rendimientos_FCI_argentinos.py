import concurrent.futures
import requests
import threading
import time
import csv

def obtener_tiempo_formateado(tiempo):
    minutos, segundos = divmod(tiempo, 60)
    segundos, milisegundos = divmod(segundos, 1)
    milisegundos = round(milisegundos * 1000)
    return minutos, segundos, milisegundos

def exportar_a_csv(datos, nombre_archivo):
    with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo_csv:
        writer = csv.DictWriter(archivo_csv, fieldnames=datos.keys())
        writer.writeheader()
        writer.writerows(datos)
    print(f'Los datos se han exportado correctamente en el archivo {nombre_archivo}.')

def obtener_datos_paginados(url):
    print('Comienza el proceso, va a llevar tiempo...')
    init_time = time.time() #empieza a procesar la función
    datos_totales = []

    def obtener_pagina(page):
        response = requests.get(f"{url}?page={page}")
        if response.status_code == 200:
            datos_pagina = response.json()
            return datos_pagina['data']
        else:
            print(f"Error al obtener los datos de la pagina {page}.")
            return []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        page = 0
        while True:
            print(f'Procesando datos de la pagina numero {page} de la API...')
            futures.append(executor.submit(obtener_pagina, page))
            page += 1
            if not futures[page - 1].result():
                break

        for future in concurrent.futures.as_completed(futures):
            datos_totales.extend(future.result())

    #Medición del tiempo de ejecución
    elapsed = time.time() - init_time
    minutos, segundos, milisegundos = obtener_tiempo_formateado(elapsed)
    print(f'La obtencion de los datos paginados de la API tuvo una duracion de: {minutos} minutos, {segundos} segundos y {milisegundos} milisegundos.')

    return datos_totales

def obtener_fondos_mas_rindieron(fecha_inicio, fecha_fin):
    init_time = time.time()
    url_fondos = "https://api.cafci.org.ar/fondo/"
    fondos = obtener_datos_paginados(url_fondos)
    fondos_filtrados = []
    fondos_procesados = 0
    fondos_totales = len(fondos)

    lock = threading.Lock()  # Lock para sincronizar el acceso a la variable compartida

    def procesar_fondo(fondo):
        nonlocal fondos_procesados, fondos_totales

        url_clase = f"https://api.cafci.org.ar/fondo/{fondo['id']}/clase"
        response_clase = requests.get(url_clase)

        if response_clase.status_code == 200:
            fondos_clase = response_clase.json()['data']
            fondos_totales += len(fondos_clase)

            for fondo_clase in fondos_clase:
                print(f'Analizando rendimiento de: {fondo_clase["nombre"]}...')

                url_rendimiento = f"{url_clase}/{fondo_clase['id']}/rendimiento/{fecha_inicio}/{fecha_fin}"
                response_rendimiento = requests.get(url_rendimiento)

                if response_rendimiento.status_code == 200:
                    rendimiento = response_rendimiento.json()
                    if 'error' not in rendimiento:
                        with lock:
                            fondos_filtrados.append({'nombre_fondo': fondo['nombre'], 'id_fondo': fondo['id'], 'rendimiento': rendimiento['data']['rendimiento']})

                with lock:
                    fondos_procesados += 1

    # def mostrar_progreso():
    #         print(f"\nFondos procesados: {fondos_procesados}/{fondos_totales}")


    # mostrar_progreso_thread = threading.Thread(target=mostrar_progreso)
    # mostrar_progreso_thread.start()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(procesar_fondo, fondos)

    # mostrar_progreso_thread.join()

    fondos_filtrados = [f for f in fondos_filtrados if not isinstance(f, str)]
    fondos_filtrados = sorted(fondos_filtrados, key=lambda x: float(x['rendimiento']), reverse=True)

    #Medición del tiempo de ejecución
    elapsed = time.time() - init_time
    minutos, segundos, milisegundos = obtener_tiempo_formateado(elapsed)
    print(f'La obtencion de la totalidad de los datos de los FCI tuvo una duracion de: {minutos} minutos, {segundos} segundos y {milisegundos} milisegundos.')

    return fondos_filtrados


print(obtener_fondos_mas_rindieron("2023-06-01", "2023-06-30"))