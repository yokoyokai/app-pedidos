import sqlite3

def init_db():
    conn = sqlite3.connect('pedidos.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            productos TEXT NOT NULL,
            ingredientes TEXT
        )
    ''')
    conn.commit()
    conn.close()

def guardar_pedido(nombre, telefono, productos, ingredientes):
    conn = sqlite3.connect('pedidos.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO pedidos (nombre, telefono, productos, ingredientes)
        VALUES (?, ?, ?, ?)
    ''', (nombre, telefono, productos, ingredientes))
    conn.commit()
    conn.close()

def obtener_pedidos():
    conn = sqlite3.connect('pedidos.db')
    c = conn.cursor()
    c.execute('SELECT * FROM pedidos')
    pedidos = c.fetchall()
    conn.close()
    return pedidos

