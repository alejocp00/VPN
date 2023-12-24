import sqlite3

def insert_vlanIprange(vlanId, ipRangeId):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("INSERT INTO vlans_iprange VALUES (?, ?)",
              vlanId, ipRangeId)
    conn.commit()
    conn.close()

def select_iprange_by_vlan(vlanId):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT iprangeId FROM vlans_iprange WHERE vlanId=?", (vlanId,))
    ipranges = c.fetchall()
    conn.close()
    return ipranges

def delete_vlanIprange(vlanId, ipRangeId):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("DELETE FROM vlans_iprange WHERE vlanId=? AND iprangeId=?", (vlanId, ipRangeId)
              )
    conn.commit()
    conn.close()

def delete_all_iprange(vlanId):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("DELETE FROM vlans_iprange WHERE userId=?", (vlanId,)
              )
    conn.commit()
    conn.close()