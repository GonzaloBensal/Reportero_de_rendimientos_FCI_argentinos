#reformular esta función para no depender del argumento lastpage (esta función obtiene todos los datos de cada paginación de la respuesta de la api)
# def obtener_datos_paginados(url, lastpage=139):
#     datos_totales = []
#     page = 0
#     while page <= lastpage:
#         # Realizar la solicitud a la API
#         response = requests.get(url + f"?page={page}")

#         # Verificar si la solicitud fue exitosa
#         if response.status_code == 200:
#             datos_pagina = response.json()
#             datos_totales.extend(datos_pagina['data'])
#             page += 1
#         else:
#             print("Error al obtener los datos.")
#             return None

#     return datos_totales


import requests

#reformulada
def obtener_datos_paginados(url):
    datos_totales = []
    page = 0
    while True:
        print(page)
        # Realizar la solicitud a la API
        response = requests.get(f"{url}?page={page}")
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            datos_pagina = response.json()
            datos_totales.extend(datos_pagina['data'])
            if page >= datos_pagina['lastPage']:
                return datos_totales
            page += 1
        else:
            print("Error al obtener los datos.")
            return None

    # return datos_totales


def obtener_fondos_mas_rindieron(fecha_inicio, fecha_fin):
    url_fondos = "https://api.cafci.org.ar/fondo/"
    fondos = obtener_datos_paginados(url_fondos)
    fondos_filtrados = []
    for fondo in fondos:
        print('entra')
        url_clase = f"https://api.cafci.org.ar/fondo/{fondo['id']}/clase"
        response_clase = requests.get(url_clase)

        if response_clase.status_code == 200:
            fondos_clase = response_clase.json()['data']
            for fondoclase in fondos_clase:
                print('entra2')
                url_rendimiento = f"{url_clase}/{fondoclase['id']}/rendimiento/{fecha_inicio}/{fecha_fin}"
                response_rendimiento = requests.get(url_rendimiento)

                if response_rendimiento.status_code == 200:
                    rendimiento = response_rendimiento.json()
                    if 'error' not in rendimiento:
                        fondos_filtrados.append({'nombre_fondo': fondo['nombre'], 'id_fondo': fondo['id'], 'rendimiento': rendimiento['data']['rendimiento']})
                else:
                    fondos_filtrados.append("No hay información")

    # Quitar los fondos de fondos_filtrados en los que "rendimiento" = {'error': 'inexistence'}
    fondos_filtrados = [f for f in fondos_filtrados if not isinstance(f, str)]

    # Ordenar los fondos_filtrados por rendimiento de mayor a menor
    fondos_filtrados = sorted(fondos_filtrados, key=lambda x: x['rendimiento'], reverse=True)

    return fondos_filtrados


print(obtener_fondos_mas_rindieron("2023-01-01", "2023-06-30"))