import sqlite3

def insert_ip(ip, vlanId):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("INSERT INTO ips (ip, vlanId) VALUES (?, ?)",
              (ip, vlanId))
    conn.commit()
    conn.close()

def select_ip(id):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ips WHERE id=?", (id,))
    ip = c.fetchone()
    conn.close()
    return ip

def delete_ip(id):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("DELETE FROM ips WHERE id=?", (id,)
              )
    conn.commit()
    conn.close()

def select_all_ips():
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ips")
    ips = c.fetchall()
    conn.close
    return ips