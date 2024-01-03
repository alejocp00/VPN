import sqlite3

def insert_vlan(vlan):
    conn = sqlite3.connect('./vpn.db')
    c = conn.cursor()
    c.execute("INSERT INTO vlans VALUES (?, ?, ?, ?)",
              (vlan.id, vlan.network, vlan.mask, vlan.hostNumber))
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

def exists_vlan(id):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM vlans WHERE id=?", (id,)
              )
    result = c.fetchone()[0]
    conn.close()
    return result != 0 

def is_vlan_full(id, hostNumber):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE vlanId=?", (id,)
              )
    count = c.fetchone()[0]
    conn.close()
    
    return count >= hostNumber
    

    