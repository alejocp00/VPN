import sqlite3

def insert_user(user, ip):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (id, name, password, vlanId, ipId) VALUES (?, ?, ?, ?, ?)",
              (user.id, user.name, user.password, user.vlan, ip))
    conn.commit()
    conn.close()

def select_user_by_name(name):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE name=?", (name,))
    user = c.fetchone()
    conn.close()
    return user

def select_user_by_id(id):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id=?", (id,))
    user = c.fetchone()
    conn.close()
    return user

def select_user_by_ip(ip):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE ipId=?", (ip,))
    user = c.fetchone()
    conn.close()
    return user

def delete_user(id):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (id,)
              )
    conn.commit()
    conn.close()