import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import sqlite3 

#load credential from authorization.json
credentials = json.load(open("/Users/mohammedakel/Desktop/CS1951A-Spring2022/rim-dj/data_deliverable/authorization.json"))
client_id = credentials['client_id']
client_secret = credentials['client_secret']

# print(client_id)
# print(client_secret) 

client_credentials_manager = SpotifyClientCredentials(client_id=client_id,client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def getTrackId(song_title, artist_name, max_result=5):
	'''This functions returns a list of tracks that match our search
	param: title of the song to search for
	param: name of the artist of the song to search for
	param: maximum number of tracks to return (default is 5)
	return: a  list of  max_result tracks that match our search'''

	params = 'artist:' + artist_name + ' track:' + song_title
	result = sp.search(q=params, type='track', limit=max_result)
	return(result['tracks']['items'])


'''
check if the above function works: 
result = getTrackId("Lonely World", "Moses Sumney", 2) 
print(type(result['tracks']['items']))
for i in result['tracks']['items']: 
	print(i)
	print("---------")
'''

def getAllArtists(artists_list):
	'''a basic function used to processe a list of all artists
	param: artist_list obtained from the track Json
	return: list of artists names'''

	result = []
	for artist in artists_list:
		name = artist['name']
		result.append(name)
	return result 


def getSongAudioFeatures(features_list): 
	'''a basic function to process a song audio feautres
	param: Features_list obtained from track Json
	return: map of audio feautres to their values'''

	track_danceability = 0.0 
	track_liveness = 0.0 
	track_loudness = 0.0 
	track_speechiness = 0.0
	track_instrumental = 0.0
	track_acoustic = 0.0
	track_energy = 0.0
	track_tempo = 0.0
	track_valence = 0.0
	track_duration = 0 
	for song in features_list:
			track_danceability = song['danceability']
			track_liveness = song['liveness']
			track_loudness = song['loudness']
			track_speechiness = song['speechiness']
			track_instrumental = song['instrumentalness']
			track_acoustic = song['acousticness']
			track_energy = song['energy']
			track_tempo = song['tempo']
			track_valence = song['valence']
			track_duration = song['duration_ms']

	return({"liveness": track_liveness,
                      "loudness": track_loudness,
                      "speechiness": track_speechiness,
                      "instrumentalness": track_instrumental,
                      "energy": track_energy,
                      "tempo": track_tempo,
                      "valence": track_valence,
                      "duration_ms": track_duration,
                      "acousticness": track_acoustic,
                      "danceability": track_danceability})


def getSongData(song_title, artist_name, max_result):
	'''given a track titel and artist name, this function returns the Spotify Track data for the given title and artisit
	param: title of the song to search for
	param: name of the artist of the song to search for
	param: maximum number of tracks to return (default is 5)
	return: list of dictionaries of track features returned by the search'''

	tracks_list = getTrackId(song_title, artist_name, max_result)
	processed_tracks = []
	for track in tracks_list:	
		# print(track)	
		track_id = track['id']
		track_title = track['name']
		# print(track_title)
		artists_final = getAllArtists(track['artists'])
		track_popularity = track['popularity']
		track_expicit = track['explicit']
		
		features = sp.audio_features(track_id)
		audio_features_map = getSongAudioFeatures(features)
		#print(audio_features_map)
		track_danceability = audio_features_map["danceability"]
		track_liveness = audio_features_map["liveness"]
		track_loudness = audio_features_map["loudness"]
		track_speechiness = audio_features_map["speechiness"]
		track_instrumental = audio_features_map["instrumentalness"]
		track_acoustic = audio_features_map["acousticness"]
		track_energy = audio_features_map["energy"]
		track_tempo = audio_features_map["tempo"]
		track_valence = audio_features_map["valence"]
		track_duration = audio_features_map["duration_ms"]
		temp = {"title": track_title,
                      "artists": artists_final,
                      "popularity": track_popularity,
                      "explicit": track_expicit,
                      "liveness": track_liveness,
                      "loudness": track_loudness,
                      "speechiness": track_speechiness,
                      "instrumentalness": track_instrumental,
                      "energy": track_energy,
                      "tempo": track_tempo,
                      "valence": track_valence,
                      "duration_ms": track_duration,
                      "acousticness": track_acoustic,
                      "danceability": track_danceability}
		processed_tracks.append(temp)
	return processed_tracks
    

''''
result = getSongData("Lonely World", "Moses Sumney", 2)
print(result)
#check why name is not being printed as "name"
'''

# print("End")

