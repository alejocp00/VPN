import sqlite3

conn = sqlite3.connect('vpn.db') #create connection with db
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        password TEXT NOT NULL
) """)
          
c.execute("""CREATE TABLE IF NOT EXISTS vlans(
        id INTEGER PRIMARY KEY,
        inicialIpRange VARCHAR,
        finalIpRange VARCHAR
) """)
          
c.execute("""CREATE TABLE IF NOT EXISTS iprange(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        inicialIp VARCHAR NOT NULL,
        finalIp VARCHAR NOT NULL
)""")
          
conn.close()
