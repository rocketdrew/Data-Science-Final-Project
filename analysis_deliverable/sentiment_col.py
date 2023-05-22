import sqlite3

# Create connection to database
conn = sqlite3.connect('../data_deliverable/data/billboard.db')
c = conn.cursor()

lyrics_cmd = '''
ALTER TABLE 
	lyrics
ADD
	sentiment numeric
'''

c.execute(lyrics_cmd)

conn.commit()
c.close()
conn.close()