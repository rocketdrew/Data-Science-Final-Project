# Credit to Jack Schultz for stencil code
# https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/

import sqlite3
import requests
from bs4 import BeautifulSoup
import re

base_url = "https://api.genius.com"
headers = {'Authorization': 'Bearer Cmy3VucAY4A_QoI6U8Zz5yO0ZCAlMc0Avk2DH2arPbXW4N-2wsUvv_309Cdi2MOW'}

# Create connection to database
conn = sqlite3.connect('data/billboard.db')
c = conn.cursor()

create_cmd = '''
CREATE TABLE IF NOT EXISTS
	lyrics
(
title text
, artist text
, lyrics text)
'''
c.execute(create_cmd)

select_cmd = '''
SELECT 
	DISTINCT title, artist
FROM
	billboard
ORDER BY artist
'''
c.execute(select_cmd)

update_cmd = '''
	UPDATE 
		billboard 
	SET 
		lyrics = ? 
	WHERE 
		title = ? AND artist = ?
	'''

test_cmd = '''
	SELECT * FROM 
		billboard 
	WHERE 
		title = ? AND artist = ?
	'''

count = 0

titles = []
artists = []
lyr = []

for row in c:

	count += 1

	song_title = row[0]
	artist_name = row[1]

	print(count, "Gathering lyrics for", song_title, "by", artist_name)

	def lyrics_from_song_api_path(song_api_path):
		song_url = base_url + song_api_path
		response = requests.get(song_url, headers=headers)
		json = response.json()
		path = json["response"]["song"]["path"]
	
		#gotta go regular html scraping... come on Genius
		page_url = "https://genius.com" + path
		page = requests.get(page_url)
		html = BeautifulSoup(page.text, "html.parser")
	
		#remove script tags that they put in the middle of the lyrics
		[h.extract() for h in html('script')]
	
		for br in html.find_all("br"):
			br.replace_with("\n")
		#print(html.prettify())
		matches = re.findall(r'Lyrics__Container.*?"', str(html))
		if len(matches) > 0:
			m = matches[0]
			lyrics = html.find('div', class_=m[:-1]).get_text().replace("'", "''")
			print("Success! \n")
			return lyrics
		else:
			print("API found song, but scraper did not \n")
			return ""
	
	#lyr = None

	if __name__ == "__main__":
		search_url = base_url + "/search"
		data = {'q': song_title}
		response = requests.get(search_url, params=data, headers=headers)
		json = response.json()
		if json["response"]["hits"] == []:
			print("Song DNE \n")
		song_info = None
		for hit in json["response"]["hits"]:
			if hit["result"]["primary_artist"]["name"] == artist_name:
				song_info = hit
				break
		
		if song_info:
			song_api_path = song_info["result"]["api_path"]
			
			lyr.append(lyrics_from_song_api_path(song_api_path).lstrip())
			titles.append(song_title)
			artists.append(artist_name)

			#conn2 = sqlite3.connect('data/billboard.db')
			#c2 = conn2.cursor()
			#c2.execute(test_cmd, (song_title, artist_name))
			#c2.execute(update_cmd, (lyr, song_title, artist_name))
			#c2.execute('INSERT INTO lyrics VALUES (?, ?, ?)', (song_title, artist_name, lyr))
		
		elif json["response"]["hits"] != []:
			print("Could not find artist", artist_name, "for song", song_title, "\n")

conn2 = sqlite3.connect('data/billboard.db')
c2 = conn2.cursor()

for i in range(len(lyr)):
	t = titles[i - 1]
	a = artists[i - 1]
	l = lyr[i - 1]
	c2.execute('INSERT INTO lyrics VALUES (?, ?, ?)', (t, a, l))

conn2.commit()
c2.close()
conn2.close()

conn.commit()
c.close()
conn.close()