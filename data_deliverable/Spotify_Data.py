#imports needed modules and libraries 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import sqlite3

# authorization.json -> responsible for storing and accessing the tokens
# playlists_like_dislike.json -> manage URL for multiple playlists
# can fetch data of up to 99 songs in a single connection session

#load credential from authorization.json
credentials = json.load(open(r'C:\Users\fangd\Desktop\cs1951a\rim-dj\data_deliverable\authorization.json'))
client_id = credentials['client_id']
client_secret = credentials['client_secret']

# print(client_id)
# print(client_secret)


#index and load playlists from playlists_like_dislike.json
playlists_json = json.load(open(r'C:\Users\fangd\Desktop\cs1951a\rim-dj\data_deliverable\Playlists_like_dislike.json'))
client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

uri = playlists_json[0]["uri"]
username = uri.split(':')[0]
playlist_id = uri.split(':')[2]

playlists_row = []
for playlist_info in playlists_json:
    uri = playlist_info["uri"]
    username = uri.split(':')[0]
    playlist_id = uri.split(':')[2]
    temp = sp.playlist(playlist_id)
    playlists_row.append(temp)

tracks_details = {}
tracks_row = []       
for playlist in playlists_row:
    playlist_tracks_data = playlist['tracks']
    """
    for K, V in playlist_tracks_data.items():
        print(K)
        print(V)
    """
    items = playlist_tracks_data['items']
    for track in items:
        #release_date = track['track']['release_date']
        #release_date_type = track['track']['release_date_precision']
        #print(release_date)
        #print(release_date_type)
        track_id = track['track']['id']
        track_title = track['track']['name']
        artisits = []
        for artist in track['track']['artists']:
            artisits.append(artist['name'])
        track_popularity = track['track']['popularity']
        track_expicit = track['track']['explicit']
        features = sp.audio_features(track_id)
        track_dancability = features[0]['danceability']
        track_liveness = features[0]['liveness']
        track_Loudness = features[0]['loudness']
        track_speechniess = features[0]['speechiness']
        track_instrumental = features[0]['instrumentalness']
        track_acoustic = features[0]['acousticness']
        track_energy = features[0]['energy']
        track_tempo = features[0]['tempo']
        track_valence = features[0]['valence']
        track_duration = features[0]['duration_ms']
        track_info = {
                      "title": track_title,
                      "artists": artisits,
                      "popularity": track_popularity,
                      "explicit": track_expicit,
                      "liveness": track_liveness,
                      "loudness": track_Loudness,
                      "speechiness": track_speechniess,
                      "instrumentalness": track_instrumental,
                      "energy": track_energy,
                      "tempo": track_tempo,
                      "valence": track_valence,
                      "duration_ms": track_duration,
                      "acousticness": track_acoustic,
                      "dancibility": track_dancability
                      }
        tracks_details[track_id] = track_info

#print(tracks_details)
tb_ids = []
tb_names = []
tb_popularity = []
tb_explixit = []
tb_dancability = []
tb_liveness = []
tb_loudness = []
tb_speech = []
tb_instrumental = []
tb_acoustic = []
tb_energy = []
tb_tempo = []
tb_valance = []
tb_artists = []
tb_duration = []

for track_id, track_info in tracks_details.items():
    tb_ids.append(track_id)
    tb_names.append(track_info['title'])
    tb_popularity.append(track_info['popularity'])
    tb_explixit.append(track_info['explicit'])
    tb_dancability.append(track_info['dancibility'])
    tb_liveness.append(track_info['liveness'])
    tb_loudness.append(track_info['loudness'])
    tb_speech.append(track_info['speechiness'])
    tb_instrumental.append(track_info['instrumentalness'])
    tb_acoustic.append(track_info['acousticness'])
    tb_tempo.append(track_info['tempo'])
    tb_valance.append(track_info['valence'])
    tb_artists.append(track_info['artists'])
    tb_duration.append(track_info['duration_ms'])



'''
query = "artist:Earth Wind and Fire, track=September"
Params = {'q': 'artist:Earth Wind and Fire, track=September', 'limit': 1, 'offset': 0, 'type': 'track', 'market': None}
find_21_september = sp.search('artist:Earth Wind and Fire, track=September', limit=1, type='track')

for k, v in find_21_september['tracks'].items():
    if (k == 'items'):
        for item in v:
            print(item)
            print("-------------------------------------------")
print(type(find_21_september['tracks']))
'''

# Create connection to database
conn = sqlite3.connect('data\\songs.db')
c = conn.cursor()

# Delete tables if they exist
c.execute('DROP TABLE IF EXISTS "songs";')

# use CREATE TABLE to create the billboard table in the database
create_billboard_table_command = '''
CREATE TABLE IF NOT EXISTS songs (
    id VARCHAR NOT NULL,
    name VARCHAR,
    popularity REAL,
    duration_ms REAL,
    explicit REAL,
    dancability REAL,
    liveness REAL,
    loudness REAL,
    speech REAL,
    instrumental REAL,
    Acoustic REAL,
    Emergy REAL,
    tempo REAL,
    valance REAL,
    PRIMARY KEY(id)
    );
'''

tb_ids = []
tb_names = []
tb_popularity = []
tb_explixit = []
tb_dancability = []
tb_liveness = []
tb_loudness = []
tb_speech = []
tb_instrumental = []
tb_acoustic = []
tb_energy = []
tb_tempo = []
tb_valance = []
tb_artists = []
tb_duration = []

tb = list(zip(tb_ids, tb_names, tb_popularity, tb_duration, tb_explixit, tb_dancability, tb_liveness, tb_loudness, tb_speech, tb_instrumental, tb_acoustic, tb_energy, tb_tempo, tb_valance))
c.execute(create_billboard_table_command)
c.executemany('INSERT INTO songs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', tb)
conn.commit()
print("END")

