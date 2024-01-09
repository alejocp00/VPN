import sqlite3

def insert_user(user, assignedIp):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, password, vlanId, ipId) VALUES (?, ?, ?, ?)",
              (user.name, user.password, user.vlan, assignedIp))
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

# def select_user_by_original_ip(ip):
#     conn = sqlite3.connect('vpn.db')
#     c = conn.cursor()
#     c.execute("SELECT * FROM users WHERE userIp=?", (ip,))
#     user = c.fetchone()
#     conn.close()
#     return user

def get_assigned_ip_by_name(name):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT ips.ip FROM users INNER JOIN ips ON users.ipId=ips.id WHERE users.name=?", (name,))
    assigned_ip = c.fetchone()[0]
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

def select_user_password(name):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE name=?",(name,))
    password = c.fetchone()[0]
    conn.close()
    return password

def select_vlan_for_username(username):
     conn = sqlite3.connect('vpn.db')
     c = conn.cursor()
     c.execute("SELECT vlanId FROM users WHERE name=?",(username,))
     vlan_id = c.fetchone()[0]
     conn.close()
     return vlan_id