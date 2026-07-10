import sqlite3

connection = sqlite3.connect('stores.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS stores (
    store_id INTEGER PRIMARY KEY,
    location TEXT NOT NULL
)
''')

cursor.execute('''insert into stores (store_id, location) values (1, 'New York')''')
cursor.execute('''insert into stores (store_id, location) values (2, 'Los Angeles')''')


cursor.execute('SELECT * FROM stores')

row = cursor.fetchall()
for row in row:
    print(row)
    
connection.commit()
connection.close()
