#imports needed modules and libraries 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import sqlite3

from Spotify_Song_Data import getSongData

# authorization.json -> responsible for storing and accessing the tokens
# playlists_like_dislike.json -> manage URL for multiple playlists
# can fetch data of up to 99 songs in a single connection session

#load credential from authorization.json
credentials = json.load(open(r'C:\Users\fangd\Desktop\cs1951a\rim-dj\data_deliverable\authorization.json'))
client_id = credentials['client_id']
client_secret = credentials['client_secret']

client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def extract_from_billboard():
    db = r'C:\Users\fangd\Desktop\cs1951a\rim-dj\data_deliverable\data\billboard.db'
    # create a database connection
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT LOWER(title), LOWER(artist) FROM billboard")

    rows = cur.fetchall()

    song_titles = []
    artist_names = []
    for row in rows:
        song_titles.append(row[0])
        artist_names.append(row[1])

    return song_titles, artist_names

def get_all_song_data():
    titles, artists = extract_from_billboard()
    data = []
    for i in range(len(titles)):
        data = data + getSongData(titles[i], artists[i], 1)
    return data

# Create connection to database
conn = sqlite3.connect('data\\songs.db')
c = conn.cursor()

# Delete tables if they exist
c.execute('DROP TABLE IF EXISTS "songs";')

# use CREATE TABLE to create the covid table in the database
create_songs_table_command = '''
CREATE TABLE IF NOT EXISTS songs (
    title VARCHAR,
    artist VARCHAR,
    popularity REAL,
    liveness REAL,
    speechiness REAL,
    instrumentalness REAL,
    energy REAL,
    tempo REAL,
    valence REAL,
    duration_ms REAL,
    acousticness REAL,
    danceability REAL,    
    loudness REAL,
    PRIMARY KEY (title, artist)
    );
'''
c.execute(create_songs_table_command)

# use INSERT to add data to the tables in the database
data = get_all_song_data()
for song in range(len(data)):
    # initialize the title value
    ti = data[song]["title"]
    # initialize the artist value
    ar = data[song]["artists"][0]
    # initialize the popularity value
    p = data[song]["popularity"]
    # initialize the liveness value
    li = data[song]["liveness"]
    # initialize the speechiness value
    s = data[song]["speechiness"]
    # initialize the instrumentalness value
    i = data[song]["instrumentalness"]
    # initialize the energy value
    e = data[song]["energy"]
    # initialize the tempo value
    te = data[song]["tempo"] 
    # initialize the valence value
    v = data[song]["valence"]
    # initialize the duration_mus value
    du = data[song]["duration_ms"]
    # initialize the acousticness value
    ac = data[song]["acousticness"]
    # initialize the danceability value
    da = data[song]["danceability"]
    # initialize the loudness value
    lo = data[song]["loudness"]

    c.execute('INSERT OR IGNORE INTO songs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', 
    (ti, ar, p, li, s, i, e, te, v, du, ac, da, lo))

conn.commit()