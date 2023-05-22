from scipy.stats import ttest_ind
import sqlite3

import sys
sys.path.append('../')
from Spotify_Song_Data import getSongData

def two_sample_ttest(peak_values, trough_values):
    """
    Input:
        - peak_values: the attribute values of songs during a COVID peak time period
        - trough_values the attribute values of songs from a COVID trough time period
    Output:
        - tstats: Test statistics (float)
        - p-value: P-value (float)
    """
    # Using scipy's ttest_ind
    # (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html)
    # to get the t-statistic and the p-value
    # Note: The code will disregard null (nan) values. We will assume equal variance.

    # Indepdendent two sample t-test, since testing unknown population means of 
    # two groups
    tstats, pvalue = ttest_ind(peak_values, trough_values, nan_policy='omit')

    # Print tstats, pvalue
    print("two_sample_ttest tstats: ", tstats)
    print("two_sample_ttest pvalue: ", pvalue)

    return tstats, pvalue

def get_songs_by_date(month, day, year):
    db = "/Users/mohammedakel/Desktop/CS1951A-Spring2022/rim-dj/data_deliverable/data/billboard.db"
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


'''
if __name__ == "__main__":
    # get the peak values and trough values for testing per attribute
    # Note: we can test additional attributes by changing the input argument in get_[peak/trough]_attribute()
    print("---Testing Danceability Difference---")
    peak_danceability = get_peak_attribute("danceability")
    trough_danceability = get_trough_attribute("danceability")
    two_sample_ttest(peak_values=peak_danceability, trough_values=trough_danceability)

    print("---Testing Energy Difference---")
    peak_energy = get_peak_attribute("energy")
    trough_energy = get_trough_attribute("energy")
    two_sample_ttest(peak_values=peak_energy, trough_values=trough_energy)

    print("---Testing Valence Difference---")
    peak_valence = get_peak_attribute("valence")
    trough_valence = get_trough_attribute("valence")
    two_sample_ttest(peak_values=peak_valence, trough_values=trough_valence)
'''

    
    
