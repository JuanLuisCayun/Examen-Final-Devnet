from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
from werkzeug.security import generate_password_hash

app = Flask(__name__)
BASE_DATOS = "usuarios.db"


def conectar():
    conexion = sqlite3.connect(BASE_DATOS)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_base_datos():
    conexion = conectar()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    """)

    usuarios_iniciales = [
        ("juan.cayun", "Devnet2026"),
        ("administrador", "Cisco123")
    ]

    for nombre, password in usuarios_iniciales:
        password_cifrada = generate_password_hash(password)
        conexion.execute(
            "INSERT OR IGNORE INTO usuarios (nombre, password) VALUES (?, ?)",
            (nombre, password_cifrada)
        )

    conexion.commit()
    conexion.close()

PAGINA = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Usuarios DEVNET</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #eef2f7;
            margin: 40px;
        }
        .contenedor {
            max-width: 750px;
            margin: auto;
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        }
        h1 { color: #174ea6; }
        input, button {
            padding: 10px;
            margin: 5px;
        }
        button {
            background: #174ea6;
            color: white;
            border: none;
            cursor: pointer;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #cccccc;
            padding: 10px;
            text-align: left;
            word-break: break-all;
        }
        th {
            background: #174ea6;
            color: white;
        }
    </style>
</head>
<body>
<div class="contenedor">
    <h1>Administración de usuarios DEVNET</h1>
    <p>Aplicación Flask con SQLite y contraseñas cifradas.</p>

    <form method="POST">
        <input name="nombre" placeholder="Nombre de usuario" required>
        <input name="password" type="password" placeholder="Contraseña" required>
        <button type="submit">Agregar usuario</button>
    </form>

    <table>
        <tr>
            <th>ID</th>
            <th>Usuario</th>
            <th>Contraseña cifrada</th>
        </tr>
        {% for usuario in usuarios %}
        <tr>
            <td>{{ usuario["id"] }}</td>
            <td>{{ usuario["nombre"] }}</td>
            <td>{{ usuario["password"] }}</td>
        </tr>
        {% endfor %}
    </table>
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def inicio():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        password = request.form["password"]

        if nombre and password:
            conexion = conectar()
            try:
                conexion.execute(
                    "INSERT INTO usuarios (nombre, password) VALUES (?, ?)",
                    (nombre, generate_password_hash(password))
                )
                conexion.commit()
            except sqlite3.IntegrityError:
                pass
            finally:
                conexion.close()

        return redirect(url_for("inicio"))

    conexion = conectar()
    usuarios = conexion.execute(
        "SELECT id, nombre, password FROM usuarios ORDER BY id"
    ).fetchall()
    conexion.close()

    return render_template_string(PAGINA, usuarios=usuarios)


if __name__ == "__main__":
    crear_base_datos()
    app.run(host="0.0.0.0", port=5800, debug=False)

