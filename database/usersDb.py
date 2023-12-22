import sqlite3

def insert_user(user):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, ?)",
              (user.name, user.password, user.vlan))
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

def delete_user(id):
    conn = sqlite3.connect('vpn.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id=?", (id,)
              )
    conn.commit()
    conn.close()