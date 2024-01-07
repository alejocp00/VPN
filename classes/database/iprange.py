import sqlite3


def insert_ip_range(rangeIp):
    conn = sqlite3.connect("vpn.db")
    c = conn.cursor()
    c.execute("INSERT INTO iprange (rangeIp) VALUES (?)", (rangeIp,))
    conn.commit()
    conn.close()


def select_all_ipranges():
    conn = sqlite3.connect("vpn.db")
    c = conn.cursor()
    c.execute("SELECT * FROM iprange")
    ipranges = c.fetchall()
    conn.close
    return ipranges


def select_id_for_ip_range(iprange):
    conn = sqlite3.connect("vpn.db")
    c = conn.cursor()
    c.execute("SELECT id FROM iprange WHERE rangeIp=?", (iprange,))
    iprange = c.fetchone()[0]
    conn.close()
    return iprange
