import json
from collections import defaultdict

with open("clasificaciones.json", "r", encoding="utf-8") as f:
    clasificaciones = json.load(f)
# Cargar archivos
with open("users.json", "r", encoding="utf-8") as f:
    users_data = json.load(f)

campos_estadisticas = ["PTS", "PJ", "PG", "PE", "PP", "GF", "GC", "DG"]

ranking = {}
detalles_por_usuario = {}

for user_final, alternativos in users_data.items():
    nombres_a_buscar = [user_final] + alternativos
    estadisticas = defaultdict(int)
    temporadas_encontradas = 0
    ligas = 0
    detalles = {}

    for temporada, data_temporada in clasificaciones.items():
        usuario_encontrado = next(
            (usuario for nombre in nombres_a_buscar for usuario in data_temporada["users"] if nombre.lower() in usuario.lower()),
            None
        )
        if usuario_encontrado:
            user_stats = data_temporada["users"][usuario_encontrado]
            for campo in campos_estadisticas:
                estadisticas[campo] += int(user_stats.get(campo, 0))
            temporadas_encontradas += 1

            # Obtener equipo y posición
            colImagen = user_stats.get("colImagen", "")
            imagen_url = f"https://gesliga.com/{colImagen}" if colImagen else ""
            posicion = user_stats.get("colPosicion", "")
            if posicion == "1":
                ligas +=1
            posicion_str = f"{posicion}🏆" if str(posicion) == "1" else str(posicion)

            detalles[temporada] = {
                campo: int(user_stats.get(campo, 0)) for campo in campos_estadisticas
            }
            detalles[temporada]["EQUIPO"] = imagen_url
            detalles[temporada]["POS"] = posicion_str

    estadisticas["TEMPORADAS"] = temporadas_encontradas
    estadisticas["ligas"] = ligas
    ranking[user_final] = estadisticas
    detalles_por_usuario[user_final] = detalles

# Ordenar por PTS de mayor a menor
ranking_ordenado = sorted(ranking.items(), key=lambda x: x[1]["PTS"], reverse=True)

# Generar HTML
html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Ranking Histórico</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
        font-family: 'Poppins', sans-serif;
        }
    </style>    
    <style>
        table { border-collapse: collapse; width: 100%; font-family: Arial; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: center; }
        th { background-color: #f4f4f4; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .details { display: none; padding: 10px; border: 1px solid #ccc; margin: 5px 0; background-color: #eef; }
        .user-row:hover { cursor: pointer; background-color: #e0f7fa; }
        img { height: 25px; }
    </style>
    <script>
        function toggleDetails(userId) {
            var el = document.getElementById("details-" + userId);
            if (el.style.display === "none") {
                el.style.display = "block";
            } else {
                el.style.display = "none";
            }
        }
    </script>

<script>
function sortTable(n) {
    var table = document.getElementById("rankingTable");
    var switching = true;
    var dir = "desc";
    var switchcount = 0;

    while (switching) {
        switching = false;
        var rows = table.rows;
        for (var i = 1; i < rows.length - 2; i += 2) {
            var x = rows[i].getElementsByTagName("TD")[n];
            var y = rows[i + 2]?.getElementsByTagName("TD")[n];
            if (!y) break;

            var xVal = isNaN(x.innerHTML) ? x.innerHTML.toLowerCase() : parseFloat(x.innerHTML);
            var yVal = isNaN(y.innerHTML) ? y.innerHTML.toLowerCase() : parseFloat(y.innerHTML);

            if ((dir === "asc" && xVal > yVal) || (dir === "desc" && xVal < yVal)) {
                rows[i].parentNode.insertBefore(rows[i + 2], rows[i]);
                rows[i].parentNode.insertBefore(rows[i + 3], rows[i + 1]);
                switching = true;
                switchcount++;
                break;
            }
        }
        if (switchcount === 0 && dir === "desc") {
            dir = "asc";
            switching = true;
        }
    }
}
</script>

</head>
<body>
    <h2>Ranking Histórico Primera División CORONITAS</h2>
    <table id="rankingTable">
        <thead>
            <tr>
                <th onclick="sortTable(0)">Usuario</th>
                <th onclick="sortTable(1)">PTS</th>
                <th onclick="sortTable(2)">PJ</th>
                <th onclick="sortTable(3)">PG</th>
                <th onclick="sortTable(4)">PE</th>
                <th onclick="sortTable(5)">PP</th>
                <th onclick="sortTable(6)">GF</th>
                <th onclick="sortTable(7)">GC</th>
                <th onclick="sortTable(8)">DG</th>
                <th onclick="sortTable(9)">Temporadas</th>
                <th onclick="sortTable(10)">Ligas 🏆</th>
            </tr>
        </thead>
        <tbody>
"""

for user, stats in ranking_ordenado:
    safe_user_id = user.replace(" ", "_").replace('"', '').replace("'", "")
    html += f'<tr class="user-row" style="background-color: #E5ECF1;" onclick="toggleDetails(\'{safe_user_id}\')"><td>{user}</td>'
    for campo in campos_estadisticas + ["TEMPORADAS"] + ["ligas"]:
        html += f"<td>{stats[campo]}</td>"
    html += "</tr>"

    detalles = detalles_por_usuario[user]
    detalles_html = f'<div class="details" id="details-{safe_user_id}"><strong>Detalle por temporada:</strong><br><table><tr><th>Temporada</th><th>Equipo</th><th>Posición</th>'
    for campo in campos_estadisticas:
        detalles_html += f"<th>{campo}</th>"
    detalles_html += "</tr>"
    
    for temporada, stats_temp in detalles.items():
        link_ges_temporada = clasificaciones[temporada]["link_ges"]
        detalles_html += f"<tr><td><a href='{link_ges_temporada}'> {temporada}</td>"
        equipo = stats_temp.get("EQUIPO", "")
        detalles_html += f'<td><img src="{equipo}" alt="Equipo"></td>'
        detalles_html += f"<td>{stats_temp.get('POS', '')}</td>"
        for campo in campos_estadisticas:
            detalles_html += f"<td>{stats_temp.get(campo, 0)}</td>"
        detalles_html += "</tr>"
    detalles_html += "</table></div>"

    html += f'<tr><td colspan="10">{detalles_html}</td></tr>'

html += """
        </tbody>
    </table>
</body>
</html>
"""

# Guardar el HTML
output_path = "ranking_historico_con_detalles.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)