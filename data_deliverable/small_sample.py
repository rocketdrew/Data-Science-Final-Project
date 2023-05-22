from bs4 import BeautifulSoup
import requests
import sqlite3

# BILLBOARD URLS
SEPT_11_2020_URL = 'https://web.archive.org/web/20200911/https://www.billboard.com/charts/hot-100#/charts/hot-100/'

# Initalize data slice
data = []

# Use BeautifulSoup and requests to collect data
urls = [SEPT_11_2020_URL]
for url in urls:
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    chart = soup.find(id='charts').find('div', 'chart-list container')
    items = chart.find('ol').find_all('li')
    rows = []
    for item in items:
        rows.append(item.find('button'))

    # extract and insert into data slice
    for row in rows:
        pos_wrapper = row.find('span')
        song_wrapper = row.find('span', 'chart-element__information').find_all('span')

        # get song ranking
        pos = int(pos_wrapper.find('span').string.strip())
        # get song title
        title = song_wrapper[0].string.strip()
        # get song artist
        artists = song_wrapper[1].string.strip()
        r = artists.replace(' &', ',').replace(' /', ',').replace(' X ', ', ').replace(' x ', ', ').replace(' +', ',')
        r2 = r.replace(' (', ', ').replace(' Featuring', ',').replace(' With', ',')
        names = r2.split(', ')
        if names[-1][-1] == ")":
            names[-1] = names[-1][:-1]
        # get month
        month = int(url[32:34])
        # get day
        day = int(url[34:36])
        # get year
        year = int(url[28:32])

        data.append({
            'pos': pos,
            'title': title,
            'artists': names,
            'month': month,
            'day': day,
            'year': year
        })

# Create connection to database
conn = sqlite3.connect('data\\small_sample.db')
c = conn.cursor()

# Delete tables if they exist
c.execute('DROP TABLE IF EXISTS "billboard";')

# use CREATE TABLE to create the billboard table in the database
create_billboard_table_command = '''
CREATE TABLE IF NOT EXISTS billboard (
    rank REAL,
    title VARCHAR NOT NULL,
    artist VARCHAR NOT NULL,
    month REAL,
    day REAL,
    year REAL,
    PRIMARY KEY (title, artist, month, day, year)
);
'''
c.execute(create_billboard_table_command)

# use INSERT to add data to the tables in the database
for idx in range(len(data)):
    # initialize the rank value
    r = data[idx]['pos']
    # initialize the title value
    t = data[idx]['title']
    # initialize the artist value (only the first artist)
    a = data[idx]['artists'][0]
    # initialize the month value
    m = data[idx]['month']
    # initialize the day value
    d = data[idx]['day']
    # initialize the year value
    y = data[idx]['year']

    c.execute('INSERT INTO billboard VALUES (?, ?, ?, ?, ?, ?)', (r, t, a, m, d, y))

conn.commit()