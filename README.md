# Reportero de rendimientos FCI argentinos
Este script funciona para obtener un reporte (JSON array) de los FCI de mayor a menor rendimiento entre dos fechas.

Ejemplo de uso:
print(obtener_fondos_mas_rindieron("2023-04-01", "2023-06-30"))

Devuelve algo así:
```
[
   {
      "nombre_fondo":"x",
      "id_fondo":"1",
      "rendimiento":"1.5"
   },
   {
      "nombre_fondo":"xy",
      "id_fondo":"2",
      "rendimiento":"1.4"
   },
   {
      "nombre_fondo":"xyz",
      "id_fondo":"3",
      "rendimiento":"1.3"
   }
]
```
