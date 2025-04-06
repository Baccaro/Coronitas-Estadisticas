import requests
from bs4 import BeautifulSoup
import json

# Lista de URLs a scrapear
urls = [
    "https://gesliga.com/Clasificacion.aspx?Liga=466759", #1.
    "https://gesliga.com/Clasificacion.aspx?Liga=467358", #2
    "https://gesliga.com/Clasificacion.aspx?Liga=468133", #3
    "https://gesliga.com/Clasificacion.aspx?Liga=468953", #4
    "https://gesliga.com/Clasificacion.aspx?Liga=469670", #5
    "https://gesliga.com/Clasificacion.aspx?Liga=470462", #6
    "https://gesliga.com/Clasificacion.aspx?Liga=471376", #7
    "https://gesliga.com/Clasificacion.aspx?Liga=472170", #8
    "https://gesliga.com/Clasificacion.aspx?Liga=473116", #9
    "https://gesliga.com/Clasificacion.aspx?Liga=475139", #10
    "https://gesliga.com/Clasificacion.aspx?Liga=476651", #11
    "https://gesliga.com/Clasificacion.aspx?Liga=477370", #12
    "https://gesliga.com/Clasificacion.aspx?Liga=478009", #13
    "https://gesliga.com/Clasificacion.aspx?Liga=478560", #14
    "https://gesliga.com/Clasificacion.aspx?Liga=479234", #15
    "https://gesliga.com/Clasificacion.aspx?Liga=480311", #16
    "https://gesliga.com/Clasificacion.aspx?Liga=480581", #17
    "https://gesliga.com/Clasificacion.aspx?Liga=481263", #18
    "https://gesliga.com/Clasificacion.aspx?Liga=482130", #19
    "https://gesliga.com/Clasificacion.aspx?Liga=482892", #20
    "https://gesliga.com/Clasificacion.aspx?Liga=483656", #21
    "https://gesliga.com/Clasificacion.aspx?Liga=484331", #22
    "https://gesliga.com/Clasificacion.aspx?Liga=484969", #23
    "https://gesliga.com/Clasificacion.aspx?Liga=485591", #24
    "https://gesliga.com/Clasificacion.aspx?Liga=486129", #25
    "https://gesliga.com/Clasificacion.aspx?Liga=486678", #26
    "https://gesliga.com/Clasificacion.aspx?Liga=487457", #27
    "https://gesliga.com/Clasificacion.aspx?Liga=488077", #28
    "https://gesliga.com/Clasificacion.aspx?Liga=488706", #29
    "https://gesliga.com/Clasificacion.aspx?Liga=489314", #30
    "https://gesliga.com/Clasificacion.aspx?Liga=489964"  #31
]

resultados = {}

for url in urls:
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error al acceder a {url}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    # Obtener nombre de temporada
    nombre_temporada_tag = soup.find("span", id="ctl00_menuLigaDesktop_lblNombreLiga")
    if not nombre_temporada_tag:
        print(f"No se encontró nombre de liga en {url}")
        continue

    nombre_temporada = nombre_temporada_tag.text.strip()
    print(nombre_temporada)
    resultados[nombre_temporada] = {"users":{},"link_ges":url}

    # Obtener la tabla de posiciones
    tabla = soup.find("table", class_="TablaClasifica")
    if not tabla:
        print(f"No se encontró tabla en {url}")
        continue

    filas = tabla.find_all("tr")[1:]  # Saltamos cabecera

    for fila in filas:
        columnas = fila.find_all("td")
        if len(columnas) < 11:
            continue  # No es una fila válida

        colPosicion = columnas[0].text.strip()
        colImagen = columnas[1].find("img")["src"]
        colNombre = columnas[2].text.strip()
        puntos = columnas[3].text.strip()
        pj = columnas[4].text.strip()
        pg = columnas[5].text.strip()
        pe = columnas[6].text.strip()
        pp = columnas[7].text.strip()
        gf = columnas[8].text.strip()
        gc = columnas[9].text.strip()
        dg = columnas[10].text.strip()

        resultados[nombre_temporada]["users"][colNombre] = {
            "colPosicion": colPosicion,
            "colImagen": colImagen,
            "colNombre": colNombre,
            "PTS": puntos,
            "PJ": pj,
            "PG": pg,
            "PE": pe,
            "PP": pp,
            "GF": gf,
            "GC": gc,
            "DG": dg
        }

# Guardar en JSON
with open("clasificaciones.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, indent=4, ensure_ascii=False)

print("✔ Archivo 'clasificaciones.json' generado con éxito.")
