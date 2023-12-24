import sqlite3

conn = sqlite3.connect('vpn.db') #create connection with db
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
        vlanId INTEGER NOT NULL,
        FOREIGN KEY (vlanId) REFERENCES vlans (id)
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
          
c.execute("""CREATE TABLE IF NOT EXISTS users_iprange(
        userId INTEGER NOT NULL,
        iprangeId INTEGER NOT NULL,
        PRIMARY KEY (userId, iprangeId),
        FOREIGN KEY (userId) REFERENCES users (id),
        FOREIGN KEY (iprangeId) REFERENCES iprange (id)
) """)

c.execute("""CREATE TABLE IF NOT EXISTS vlans_iprange(
        vlanId INTEGER NOT NULL,
        iprangeId INTEGER NOT NULL,
        PRIMARY KEY (vlanId, iprangeId),
        FOREIGN KEY (vlanId) REFERENCES vlans (id),
        FOREIGN KEY (iprangeId) REFERENCES iprange (id)
) """) 
conn.close()
