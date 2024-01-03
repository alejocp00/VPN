import sqlite3

def insert_user(user, assignedIp):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, password, userIp, vlanId, ipId) VALUES (?, ?, ?, ?, ?)",
              (user.name, user.password, user.userIp, user.vlan, assignedIp))
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

def select_user_by_original_ip(ip):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE userIp=?", (ip,))
    user = c.fetchone()
    conn.close()
    return user

def get_assigned_ip_by_original_ip(ip):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT ips.ip FROM users INNER JOIN ips ON users.ipId=ips.id WHERE users.userIp=?", (ip,))
    assigned_ip = c.fetchone()
    conn.close()
    return assigned_ip


def delete_user(id):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (id,)
              )
    conn.commit()
    conn.close()

def exists_user(name):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE name=?", (name,)
              )
    result = c.fetchone()[0]
    conn.close()
    return result != 0 

def exists_user_by_id(id):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users WHERE id=?", (id,)
              )
    result = c.fetchone()[0]
    conn.close()
    return result != 0 

def select_id_for_username(name):
     conn = sqlite3.connect('vpn.db')
     c = conn.cursor()
     c.execute("SELECT id FROM users WHERE name=?",(name,))
     id = c.fetchone()[0]
     conn.close()
     return id
