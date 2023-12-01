import sqlite3
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, name, login, password):
        self.id = id
        self.name = name
        self.login = login
        self.password = password
    id = -1
    name = ""
    login = ""
    password = ""


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_user(idn):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM PERSON WHERE id='+str(idn)).fetchall()
    conn.close()
    user_wrap = User(user[0][0], user[0][1], user[0][2], user[0][3])
    return user_wrap


def get_user_login(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM PERSON WHERE login= "%s"' % username).fetchall()
    conn.close()
    user_wrap = User(user[0][0], user[0][1], user[0][2], user[0][3])
    return user_wrap


def add_user(name, login, password):
    conn = get_db_connection()
    conn.execute(f'INSERT INTO person (NAME, LOGIN, PASSWORD) VALUES ({name}, {login}, {password})')
    conn.close()
    return 1


def get_all_risks():
    conn = get_db_connection()
    risks = conn.execute(
        'SELECT risk.id, name, date(created), category, impact, proximity, response, status, contact, description '
        'FROM risk, person WHERE risk.owner_id = person.id').fetchall()
    conn.close()
    return risks


def get_risks_by_owner(name):
    conn = get_db_connection()
    risks = conn.execute(
        'SELECT risk.id, name, date(created), category, impact, proximity, response, status, contact, description '
        'FROM risk, person WHERE risk.owner_id = person.id AND name = "%s"' % name).fetchall()
    conn.close()
    return risks


def get_risk(idn):
    conn = get_db_connection()
    risk_data = conn.execute(
        'SELECT risk.id, name, date(created), category, impact, proximity, response, status, contact, description '
        'FROM risk, person WHERE risk.owner_id = person.id AND risk.id = %i' % idn).fetchall()
    conn.close()
    return risk_data[0]


def add_risk():
    return 1
