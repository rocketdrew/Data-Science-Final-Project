# script for data visulization 
import sqlite3
from Spotify_Song_Data import getSongData
import pandas as pd 
import plotnine
from plotnine import *
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.offline as pyo
import statistics
from math import sqrt

CHARTS_FILE = "/Users/mohammedakel/Desktop/CS1951A-Spring2022/rim-dj/analysis_deliverable/charts"

def get_songs_by_date(month, day, year):
    db = '/Users/mohammedakel/Desktop/CS1951A-Spring2022/rim-dj/data_deliverable/data/billboard.db'
    # create a database connection
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT title, artist FROM billboard WHERE month=? AND day=? AND year=?", (month, day, year,))
    rows = cur.fetchall()
    song_titles = []
    artist_names = []
    for row in rows:
        song_titles.append(row[0])
        artist_names.append(row[1])

    return song_titles, artist_names


def get_peak_attribute(attribute):
    # Peaks: 4/10/2020, 7/24/2020, 1/11/2021, 9/13/2021, 1/15/2022
    titles = []
    names = []
    attribute_values = []
    
    titles_one, names_one = get_songs_by_date(4, 10, 2020)
    titles_two, names_two = get_songs_by_date(7, 24, 2020)
    titles_three, names_three = get_songs_by_date(1, 11, 2021)
    titles_four, names_four = get_songs_by_date(9, 13, 2021)
    titles_five, names_five = get_songs_by_date(1, 15, 2022)

    titles = titles + titles_one + titles_two + titles_three + titles_four + titles_five
    names = names + names_one + names_two + names_three + names_four + names_five

    for i in range(len(titles)):
        song = getSongData(titles[i], names[i], 1)
        if len(song) != 0:
            attribute_values.append(song[0][attribute])

    return attribute_values

def get_trough_attribute(attribute):
    # Troughs: 9/11/2020, 12/30/2020, 6/22/2021, 10/26/2021, 11/28/2021
    titles = []
    names = []
    attribute_values = []
    
    titles_one, names_one = get_songs_by_date(9, 11, 2020)
    titles_two, names_two = get_songs_by_date(12, 30, 2020)
    titles_three, names_three = get_songs_by_date(6, 22, 2021)
    titles_four, names_four = get_songs_by_date(10, 26, 2021)
    titles_five, names_five = get_songs_by_date(11, 28, 2022)

    titles = titles + titles_one + titles_two + titles_three + titles_four + titles_five
    names = names + names_one + names_two + names_three + names_four + names_five

    for i in range(len(titles)):
        song = getSongData(titles[i], names[i], 1)
        if len(song) != 0:
            attribute_values.append(song[0][attribute])

    return attribute_values



 # ---------------------------------------------------
 # code for creating boxplots by attribute 
 #attributes = ["id", "name", "popularity", "duration_ms", "explicit", "dancability", "liveness", "loudness", "speech", "instrumental", "Acoustic", "Energy", "tempo", "valance"]

def create_attribute_boxplot(attribute): 
	attribute_peak = get_peak_attribute(attribute)
	print("loaded peak data for " + attribute)
	attribute_trough = get_trough_attribute(attribute)
	print("loaded trough data for " + attribute)
	attribute_col = np.concatenate([attribute_peak, attribute_trough])
	a = np.full(len(attribute_peak), "peak", dtype=np.str)
	b = np.full(len(attribute_trough), "trough", dtype=np.str)
	level = np.concatenate([a, b], dtype=np.str)
	tb = list(zip(attribute_col, level))
	df = pd.DataFrame(tb, columns=["values", "level"])
	p10 = (
    ggplot(df, aes("level", "values"))
    + geom_boxplot(colour="#1F3552", fill="#4271AE")
    + geom_jitter()
    + xlab("COVID-19 Peaks vs Troughs")
    + ylab("song " + str(attribute))
    + ggtitle("Distribution of Spotify's " + str(attribute) + " Attribute\n For Top Songs During COVID Peaks and Troughs with jitter")
    + theme(
        axis_line=element_line(size=1, colour="black"),
        panel_grid_major=element_line(colour="#d3d3d3"),
        panel_grid_minor=element_blank(),
        panel_border=element_blank(),
        panel_background=element_blank(),
        plot_title=element_text(size=15, family="Tahoma", 
                                face="bold"),
        text=element_text(family="Tahoma", size=11),
        axis_text_x=element_text(colour="black", size=10),
        axis_text_y=element_text(colour="black", size=10),
    	)
	)
	ggsave(plot=p10,filename = str(attribute) + "_boxplot_jitter.png", path=CHARTS_FILE)
	p11 = (
    ggplot(df, aes("level", "values"))
    + geom_boxplot(colour="#1F3552", fill="#4271AE")
    + xlab("COVID-19 Peaks vs Troughs")
    + ylab("song " + str(attribute))
    + ggtitle("Distribution of Spotify's " + str(attribute) + " Attribute\n For Top Songs During COVID Peaks and Troughs")
    + theme(
        axis_line=element_line(size=1, colour="black"),
        panel_grid_major=element_line(colour="#d3d3d3"),
        panel_grid_minor=element_blank(),
        panel_border=element_blank(),
        panel_background=element_blank(),
        plot_title=element_text(size=15, family="Tahoma", 
                                face="bold"),
        text=element_text(family="Tahoma", size=11),
        axis_text_x=element_text(colour="black", size=10),
        axis_text_y=element_text(colour="black", size=10),
    	)
	)
	ggsave(plot=p11,filename = str(attribute) + "_boxplot.png", path=CHARTS_FILE)
	final = "saved graphs for " + str(attribute)
	return final


#uncomment to create boxplots. check CHART_FILE 
'''
print(create_attribute_boxplot("energy"))
print(create_attribute_boxplot("popularity"))
print(create_attribute_boxplot("duration_ms")) 
print(create_attribute_boxplot("danceability")) 
print(create_attribute_boxplot("liveness")) 
print(create_attribute_boxplot("loudness")) 
print(create_attribute_boxplot("speechiness")) 
print(create_attribute_boxplot("instrumentalness")) 
print(create_attribute_boxplot("acousticness")) 
print(create_attribute_boxplot("tempo")) 
print(create_attribute_boxplot("valence"))

'''

# sample graphs 
'''
p10 = (
    ggplot(df, aes("level", "energy"))
    + geom_boxplot(colour="#1F3552", fill="#4271AE")
    + geom_jitter()
    + xlab("COVID-19 Peaks vs Troughs")
    + ylab("Song Energy")
    + scale_y_continuous(breaks=np.arange(0, 2, 0.1), 
                         limits=[0, 1])
    + ggtitle("Distribution of Spotify's Energy Attribute\n For Top Songs During COVID Peaks and Troughs")
    + theme(
        axis_line=element_line(size=1, colour="black"),
        panel_grid_major=element_line(colour="#d3d3d3"),
        panel_grid_minor=element_blank(),
        panel_border=element_blank(),
        panel_background=element_blank(),
        plot_title=element_text(size=15, family="Tahoma", 
                                face="bold"),
        text=element_text(family="Tahoma", size=11),
        axis_text_x=element_text(colour="black", size=10),
        axis_text_y=element_text(colour="black", size=10),
    )
)

p11 = (
    ggplot(df, aes("level", "energy"))
    + geom_boxplot(colour="#1F3552", fill="#4271AE")
    + xlab("COVID-19 Peaks vs Troughs")
    + ylab("Song Energy")
    + scale_y_continuous(breaks=np.arange(0, 2, 0.1), 
                         limits=[0, 1])
    + ggtitle("Distribution of Spotify's Energy Attribute\n For Top Songs During COVID Peaks and Troughs")
    + theme(
        axis_line=element_line(size=1, colour="black"),
        panel_grid_major=element_line(colour="#d3d3d3"),
        panel_grid_minor=element_blank(),
        panel_border=element_blank(),
        panel_background=element_blank(),
        plot_title=element_text(size=15, family="Tahoma", 
                                face="bold"),
        text=element_text(family="Tahoma", size=11),
        axis_text_x=element_text(colour="black", size=10),
        axis_text_y=element_text(colour="black", size=10),
    )
)

p12 = (
    ggplot(df, aes("level", "energy"))
    + geom_boxplot(colour="#1F3552", fill="#4271AE", notch=True)
    + xlab("COVID-19 Peaks vs Troughs")
    + ylab("Song Energy")
    + scale_y_continuous(breaks=np.arange(0, 2, 0.1), 
                         limits=[0, 1])
    + ggtitle("Distribution of Spotify's Energy Attribute\n For Top Songs During COVID Peaks and Troughs")
    + theme(
        axis_line=element_line(size=1, colour="black"),
        panel_grid_major=element_line(colour="#d3d3d3"),
        panel_grid_minor=element_blank(),
        panel_border=element_blank(),
        panel_background=element_blank(),
        plot_title=element_text(size=15, family="Tahoma", 
                                face="bold"),
        text=element_text(family="Tahoma", size=11),
        axis_text_x=element_text(colour="black", size=10),
        axis_text_y=element_text(colour="black", size=10),
    )
)

'''

#------------------------------------------------------------------------------------------------
#code for creating radar maps
#"valence"
#peak = 0.5096528571428571
#trough=  0.5066308483290489

radar_attributes = ["energy", "danceability", "liveness", "speechiness",  "instrumentalness", "acousticness", "valence", "energy"]
peak_means_cal = [0.6318510204081632, 0.667104081632653, 0.17550040816326534,  0.11316204081632653, 0.004349192102040816,
                  0.21523781428571429, 0.5096528571428571, 0.6318510204081632]
trough_means_cal = [0.6099922879177377, 0.6611876606683804, 0.16838020565552697, 0.12052750642673524, 0.0028522052442159383,
                    0.2492472673521851, 0.5066308483290489, 0.6099922879177377]


'''
for att in radar_attributes:
    peak_data = get_peak_attribute(att)
    print("loaded peak data for: " + str(att))
    mean_peak = np.mean(peak_data)
    print("peak_mean for " + str(att) + " is:")
    print(mean_peak)
    peak_means.append(mean_peak)
    trough_data = get_trough_attribute(att)
    print("loaded trough data for: " + str(att))
    mean_trough = np.mean(trough_data)
    print("trough_mean for " + str(att) + " is:")
    print(mean_trough)
    trough_means.append(mean_trough)
'''

'''
label_loc = np.linspace(start=0, stop=2 * np.pi, num=len(peak_means_cal))
plt.figure(figsize=(6, 6))
plt.subplot(polar=True)
plt.plot(label_loc, peak_means_cal, label='Peaks')
plt.plot(label_loc, trough_means_cal, label='Troughs')
plt.title('Attributes Means for Top 100 Songs', size=16)
lines, labels = plt.thetagrids(np.degrees(label_loc), labels=radar_attributes)
plt.legend()
plt.show()


fig = go.Figure(
    data=[
        go.Scatterpolar(r=peak_means_cal, theta=radar_attributes, fill='toself', name='Peaks'),
        go.Scatterpolar(r=trough_means_cal, theta=radar_attributes, fill='toself',  name='Troughs'),
    ],
    layout=go.Layout(
        title=go.layout.Title(text='Attributes Means for Top 100 Songs'),
        polar={'radialaxis': {'visible': True}},
        showlegend=True
    )
)

pyo.plot(fig)
'''


def plot_confidence_interval(x, values, z=1.96, color='#2187bb', horizontal_line_width=0.25):
    mean = statistics.mean(values)
    stdev = statistics.stdev(values)
    confidence_interval = z * stdev / sqrt(len(values))

    left = x - horizontal_line_width / 2
    top = mean - confidence_interval
    right = x + horizontal_line_width / 2
    bottom = mean + confidence_interval
    plt.plot([x, x], [top, bottom], color=color)
    plt.plot([left, right], [top, top], color=color)
    plt.plot([left, right], [bottom, bottom], color=color)
    plt.plot(x, mean, 'o', color='#f44336')

    return mean, confidence_interval

valence_peak_data = get_peak_attribute("valence")
print("loaded peak data for valence")
print("peak avg: ", sum(valence_peak_data)/len(valence_peak_data))
valence_trough_data = get_trough_attribute("valence")
print("loaded trough data for valence")
print("trough avg: ", sum(valence_trough_data)/len(valence_trough_data))

plt.xticks([1, 2], ['Peaks', 'Troughs'])
plt.title('Confidence Interval for Valence')
plot_confidence_interval(1, valence_peak_data)
plot_confidence_interval(2, valence_trough_data)
plt.show()



loudness_peak_data = get_peak_attribute("loudness")
print("loaded peak data for loudness")
print("peak avg: ", sum(loudness_peak_data)/len(loudness_peak_data))
loudness_trough_data = get_trough_attribute("loudness")
print("loaded trough data for loudness")
print("trough avg: ", sum(loudness_trough_data)/len(loudness_trough_data))



plt.xticks([1, 2], ['Peaks', 'Troughs'])
plt.title('Confidence Interval for Loudness')
plot_confidence_interval(1, loudness_peak_data)
plot_confidence_interval(2, loudness_trough_data)
plt.show()


danceability_peak_data = get_peak_attribute("danceability")
print("loaded peak data for danceability")
print("peak avg: ", sum(danceability_peak_data)/len(danceability_peak_data))
danceability_trough_data = get_trough_attribute("danceability")
print("loaded trough data for danceability")
print("trough avg: ", sum(danceability_trough_data)/len(danceability_trough_data))


plt.xticks([1, 2], ['Peaks', 'Troughs'])
plt.title('Confidence Interval for danceability')
plot_confidence_interval(1, danceability_peak_data)
plot_confidence_interval(2, danceability_trough_data)
plt.show()



