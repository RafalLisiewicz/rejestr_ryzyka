import sqlite3

connection = sqlite3.connect('database.db')


# with open('schema.sql') as f:
#    connection.executescript(f.read())

cur = connection.cursor()
cur.execute('SELECT risk.id, name, date(created), category, impact, proximity, response, status, contact, description '
            'FROM risk, person WHERE risk.owner_id = person.id AND name = "Jon Smith"')
print(cur.fetchall()[0])
