import sqlite3
def insert_iprange(inicialIp, finalIp):
     conn = sqlite3.connect('vpn.db')
     c = conn.cursor()
     c.execute("INSERT INTO iprange (inicialIp, finalIp) VALUES (?, ?)",
              (inicialIp, finalIp))
     conn.commit()
     conn.close()

def select_all_ipranges():
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT * FROM iprange")
    ipranges = c.fetchall()
    conn.close
    return ipranges