import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ.get('DATABASE_URL')

def conectar():
    return psycopg2.connect(DATABASE_URL)

def crear_usuario(usuario, contrasena):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("INSERT INTO locales (usuario, contrasena) VALUES (%s, %s) ON CONFLICT (usuario) DO NOTHING", (usuario, contrasena))
    conn.commit()
    cur.close()
    conn.close()

def validar_usuario(usuario, contrasena):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM locales WHERE usuario=%s AND contrasena=%s", (usuario, contrasena))
    resultado = cur.fetchone()
    cur.close()
    conn.close()
    return resultado is not None
