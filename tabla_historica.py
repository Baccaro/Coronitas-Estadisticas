import requests
from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict
import unicodedata

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

# Función para normalizar nombres (quita tildes y mayúsculas)
def normalizar_nombre(nombre):
    nombre = nombre.upper().strip()
    nombre = unicodedata.normalize('NFD', nombre).encode('ascii', 'ignore').decode("utf-8")
    return nombre

# Estructura para acumular los datos históricos
historico = defaultdict(lambda: {
    "Nombre": "",
    "PJ": 0, "PG": 0, "PE": 0, "PP": 0, "GF": 0, "GC": 0, "DG": 0, "Pt": 0
})

for url in urls:
    print(f"Procesando {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    temporada = soup.find("span", id_="ctl00_menuLigaDesktop_lblNombreLiga").get_text(strip=True)
    print(temporada)    
    tabla = soup.find("table", class_="TablaClasifica")
    
    if not tabla:
        print(f"No se encontró la tabla en {url}")
        continue

    filas = tabla.find_all("tr")[1:]  # Omitimos cabecera

    for fila in filas:
        celdas = fila.find_all("td")
        if len(celdas) < 11:
            continue

        nombre_original = celdas[2].get_text(strip=True).split(" - ")[0]
        nombre_key = normalizar_nombre(nombre_original)

        pt = int(celdas[3].get_text())
        pj = int(celdas[4].get_text())
        pg = int(celdas[5].get_text())
        pe = int(celdas[6].get_text())
        pp = int(celdas[7].get_text())
        gf = int(celdas[8].get_text())
        gc = int(celdas[9].get_text())
        dg = int(celdas[10].get_text().replace("+", ""))

        jugador = historico[nombre_key]
        jugador["Nombre"] = nombre_original  # Mostramos nombre original en tabla
        jugador["Pt"] += pt
        jugador["PJ"] += pj
        jugador["PG"] += pg
        jugador["PE"] += pe
        jugador["PP"] += pp
        jugador["GF"] += gf
        jugador["GC"] += gc
        jugador["DG"] += dg
        jugador["TEMP"] +=1
# Convertimos a DataFrame
df = pd.DataFrame(historico.values())
df = df.sort_values(by="Pt", ascending=False).reset_index(drop=True)

# Mostramos en consola (opcional)
print(df.to_string(index=False))

# Guardamos a HTML
html_output = df.to_html(index=False, classes="tabla-historica", border=0)
with open("tabla_historica.html", "w", encoding="utf-8") as f:
    f.write(html_output)

print("Tabla histórica generada correctamente.")
