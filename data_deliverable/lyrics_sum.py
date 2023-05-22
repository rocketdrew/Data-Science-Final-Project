import sqlite3

# Create connection to database
conn = sqlite3.connect('data/billboard.db')
c = conn.cursor()

select_cmd = '''
SELECT *
FROM lyrics
'''

c.execute(select_cmd)

for row in c:
	print(row)