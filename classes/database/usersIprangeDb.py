import sqlite3

def insert_userIprange(userId, ipRangeId):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("INSERT INTO users_iprange VALUES (?, ?)",
              (userId, ipRangeId))
    conn.commit()
    conn.close()

def select_iprange_by_user(userId):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT iprangeId FROM users_iprange WHERE userId=?", (userId,))
    ipranges = c.fetchall()
    conn.close()
    return ipranges

def delete_userIprange(userId, ipRangeId):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("DELETE FROM users_iprange WHERE userId=? AND iprangeId=?", (userId, ipRangeId)
              )
    conn.commit()
    conn.close()

def delete_all_iprange(userId):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("DELETE FROM users_iprange WHERE userId=?", (userId,)
              )
    conn.commit()
    conn.close()