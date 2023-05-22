import plotnine
from plotnine import *
from Spotify_Song_Data import getSongData
import sqlite3
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#list os songs dueing a COVID peak
#list of songs during a COVID low
CHARTS_FILE = "/Users/mohammedakel/Desktop/CS1951A-Spring2022/rim-dj/data_deliverable/charts"

# Create testing data
song_names_artis = {"Taylor Swift": "‘All Too Well",
              "Little Simz": "woman",
              "Allison Russell": "Nightflyer",
              "Aimee Mann": "Suicide Is Murder",
              "Lil Nas X": "That’s What I Want",
              "Brandi Carlile": "Broken Horses",
              "Adele": "To Be Loved",
              "Snail Mail": "Valentine",
              "Phoebe Bridgers": "That Funny Feeling",
              "Kanye West": "Come to Life",
              "Jazmine Sullivan": "Girl Like Me",
              "Yebba": "Boomerang"}

def get_spotify_song_artist(songsList):
    '''given a collection of song names and artists, this function returns a list of hashmaps
    of spotify data for the given songs. adds level column establishes connection to database
    currently, the function only works with hashmaps. can be edited to accomodate tulips ...'''

    #given that songs List is a dictionary
    songs_data = []
    for K, V in songsList.items():
        artist=K
        song = V
        temp = getSongData(song, artist, 1)
        songs_data.append(temp)
    return songs_data

result = get_spotify_song_artist(song_names_artis)
print(result)


# Create connection to database
conn = sqlite3.connect('/Users/mohammedakel/Desktop/CS1951A-Spring2022/rim-dj/data_deliverable/data/vizTestingTable.db')
c = conn.cursor()

# Delete tables if they exist
c.execute('DROP TABLE IF EXISTS "vizTestingTable";')

create_testing_table_command = """
CREATE TABLE IF NOT EXISTS vizTestingTable (
    id VARCHAR NOT NULL,
    name VARCHAR,
    popularity REAL,
    duration_ms REAL,
    liveness REAL,
    loudness REAL,
    speech REAL,
    instrumental REAL,
    Acoustic REAL,
    Energy REAL,
    tempo REAL,
    valance REAL,
    level REAL,
    PRIMARY KEY(id)
    );
"""

c.execute(create_testing_table_command)
counter = 1
for i in result:
    temp = counter
    ID = temp
    #print(ID)
    counter = counter + 1
    #print(counter)
    name = i[0]['title']
    #print(name)
    popularity = i[0]['popularity']
    #print(popularity)
    duration_ms = i[0]['duration_ms']
    #print(duration_ms)
    #explicit = i[0]['explicit']
    #print(explicit)
    #dancability = i[0]['dancability']
    #print(dancability)
    liveness = i[0]['liveness']
    #print(liveness)
    loudness = i[0]['loudness']
    #print(loudness)
    speech = i[0]['speechiness']
    #print(speech)
    instrumental = i[0]['instrumentalness']
    #print(instrumental)
    Acoustic = i[0]['acousticness']
    #print(Acoustic)
    artists = i[0]['artists'][0]
    #print(artists)
    tempo = i[0]['tempo']
    #print(tempo)
    valance = i[0]['valence']
    #print(valance)
    if counter < 7:
        level = 1
    else:
        level = 0
    #print(level)
    c.execute('INSERT INTO vizTestingTable VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (ID, name, popularity, duration_ms, liveness, loudness, speech, instrumental, Acoustic, artists, tempo, valance, level))

testing_df = pd.read_sql_query("SELECT * from vizTestingTable", conn)   
conn.commit()

print(testing_df.head())


"""
def boxplot_by_level(df, name_attributeColumn, name_ByColumn, title):
    '''given a dataframe that contains a coded categorical column represeting COVID level (eg: 1 for high incidence, 0 for low incidence ...), this function returns a box plots for the different
    attributes by COVID level'''
    #make sure that name_byCOlumn is categorical 
    df[name_ByColumn] = df[name_ByColumn].astype("category")
    graph = (
        ggplot(df) +
        aes(name_ByColumn, name_attributeColumn) +
        geom_boxplot(colour="rebeccapurple", fill="lightskyblue", alpha=0.7, outlier_shape=".", outlier_colour="steelblue") +
        xlab("COVID Incidence") +
        ylab(name_attributeColumn) +
        ggtitle(title) +
        theme_bw()
        )
    return graph 

#follow examples below to create and save box_plots 
instrumental_boxplot =  boxplot_by_level(testing_df, "instrumental", "level", "instrumental boxplot by COVID Level")
ggsave(plot=instrumental_boxplot,filename = "instrumental_boxplot_test.png", path=CHARTS_FILE)
dancability_boxplot =  boxplot_by_level(testing_df, "dancability", "level", "dancability boxplot by COVID Level")
ggsave(plot=dancability_boxplot,filename = "dancability_boxplot_test.png", path=CHARTS_FILE)
loudness_boxplot =  boxplot_by_level(testing_df, "loudness", "level", "loudness boxplot by COVID Level")
ggsave(plot=loudness_boxplot,filename = "loudness_boxplot_test.png", path=CHARTS_FILE)

def Two_Attributes_scatterplot_ByLevel(df, name_attributeColumnOne,name_attributeColumnTwo, name_ByColumn, title):
    '''given a dataframe that contains a coded categorical column represeting COVID level (eg: 1 for high incidence, 0 for low incidence ...),
    this function returns a scatter plots of the given attributed by level'''
    #make sure that name_byCOlumn is categorical 
    df[name_ByColumn] = df[name_ByColumn].astype("category")
    graph = (
        ggplot(df) +
        aes(name_attributeColumnOne, name_attributeColumnTwo, color=name_ByColumn) +
        geom_point() +
        ggtitle(title) +
        theme_bw()
        )
    return graph 

#follow examples below to create and save scatter_plots 
popularity_dancability_scatterplot_byLevel =  Two_Attributes_scatterplot_ByLevel(testing_df, "dancability", "popularity", "level", "Dancability vs Popularity By Level")
ggsave(plot=popularity_dancability_scatterplot_byLevel,filename = "dancability_popularity_test.png", path=CHARTS_FILE)
popularity_dancability_scatterplot_byLevel =  Two_Attributes_scatterplot_ByLevel(testing_df, "duration_ms", "popularity", "level", "Duration vs Popularity By Level")
ggsave(plot=popularity_dancability_scatterplot_byLevel,filename = "duration_popularity_test.png", path=CHARTS_FILE)
"""
    
def attributes_corr_heatmap(df):
    '''given a data frame, the function returns a heatmap depeciting the correlation between all the attributes in the dataframe'''
    matrix = df.corr().round(2)
    sns.set(font_scale=0.6)
    graph = sns.heatmap(matrix, annot=True)
    file_path = CHARTS_FILE + "/heatmap_test.png"
    plt.savefig(file_path)
    plt.show()


#follow examples below to create and save scatter_plots 
attributes_corr_heatmap(testing_df)

print("END")
