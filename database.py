import psycopg2
import os

# Usamos esta variable de entorno que configurarás en Render
DATABASE_URL = os.environ.get('DATABASE_URL')

def conectar():
    return psycopg2.connect(DATABASE_URL)

import datetime  # Esto debe estar arriba del todo en database.py (por si no lo tienes)

def guardar_pedido(nombre, telefono, productos, ingredientes):
    conn = conectar()
    cur = conn.cursor()

    # obtener fecha y hora actual
    fecha = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cur.execute(
        "INSERT INTO pedidos (nombre, telefono, productos, ingredientes, fecha) VALUES (%s, %s, %s, %s, %s)",
        (nombre, telefono, productos, ingredientes, fecha)
    )
    conn.commit()
    cur.close()
    conn.close()


def obtener_pedidos():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pedidos ORDER BY id DESC")
    pedidos = cur.fetchall()
    cur.close()
    conn.close()
    return pedidos

def init_db():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id SERIAL PRIMARY KEY,
            nombre TEXT,
            telefono TEXT,
            productos TEXT,
            ingredientes TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def exportar_pedidos_a_txt(nombre_archivo='respaldo_pedidos.txt'):
    pedidos = obtener_pedidos()
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        for p in pedidos:
            f.write(f"{p}\n")
    print(f"✅ Respaldo guardado en {nombre_archivo}")

