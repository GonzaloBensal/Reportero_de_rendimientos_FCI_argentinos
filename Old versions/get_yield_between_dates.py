import requests

def obtener_fondos_mas_rindieron(fecha_inicio, fecha_fin):
    url = f"https://api.cafci.org.ar/fondo/"
    
    # Realizar la solicitud a la API de CNV
    response = requests.get(url)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        fondos = response.json()

        # Filtrar los fondos por fecha y rendimiento
        fondos_filtrados = []
        for fondo in fondos:
            url = f"https://api.cafci.org.ar/fondo/{fondo}/clase"
            # Realizar la solicitud a la API de CNV
            response = requests.get(url)
            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                fondos= response.json()
                for fondoclase in fondos:
                    url+=f"/clase/{fondoclase}/rendimiento/{fecha_inicio}/{fecha_fin}"
                    response = requests.get(url)
                    if response.status_code == 200:
                        # fondosclases = response.json()
                        fondos_filtrados.append((fondoclase['nombre'], fondoclase['rendimiento']))       
                        url= f"https://api.cafci.org.ar/fondo/{fondo}/clase"
        
        # Ordenar los fondos filtrados por rendimiento de mayor a menor
        fondos_ordenados = sorted(fondos_filtrados, key=lambda x: x[1], reverse=True)
        
        print(fondos_ordenados)
    else:
        print("Error al obtener los fondos de inversión.")
        return None