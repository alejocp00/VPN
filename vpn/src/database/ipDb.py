import sqlite3

def insert_ip(ip, vlanId):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("INSERT INTO ips (ip, vlanId, active) VALUES (?, ?, ?)",
              (ip, vlanId, 0))
    conn.commit()
    conn.close()

def select_ip(id):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ips WHERE id=?", (id,))
    ip = c.fetchone()
    conn.close()
    return ip

def get_ip_id(ip):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT id FROM ips WHERE ip=?", (ip,))
    ip = c.fetchone()[0]
    conn.close()
    return ip


def select_ip(vlanId):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT ip FROM ips WHERE vlanId=?", (vlanId,))
    ips = c.fetchall()
    conn.close()
    return ips

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

def update_active_ip(ip, value):
     conn = sqlite3.connect('vpn.db')
     c = conn.cursor()
     c.execute("UPDATE ips SET active=? WHERE ip=?", (value,ip))
     conn.commit()
     conn.close()
