import sqlite3

def insert_vlan(vlan):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("INSERT INTO vlans VALUES (?, ?)",
              vlan.network, vlan.mask)
    conn.commit()
    conn.close()

def select_vlan(id):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT * FROM vlans WHERE id=?", (id,))
    vlan = c.fetchone()
    conn.close()
    return vlan

def delete_vlan(id):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("DELETE FROM vlans WHERE id=?", (id,)
              )
    conn.commit()
    conn.close()