from bs4 import BeautifulSoup
import requests
import sqlite3

# Peaks: 4/10/2020, 7/24/2020, 1/11/2021, 9/13/2021, 1/15/2022
# Troughs: 9/11/2020, 12/30/2020, 6/22/2021, 10/26/2021, 11/28/2021

# BILLBOARD URLS
APR_10_2020_URL = 'https://web.archive.org/web/20200410/https://www.billboard.com/charts/hot-100#/charts/hot-100/'
JUL_24_2020_URL = 'https://web.archive.org/web/20200724/https://www.billboard.com/charts/hot-100#/charts/hot-100/'
SEPT_11_2020_URL = 'https://web.archive.org/web/20200911/https://www.billboard.com/charts/hot-100#/charts/hot-100/'
DEC_30_2020_URL = 'https://web.archive.org/web/20201230/https://www.billboard.com/charts/hot-100#/charts/hot-100/'
JAN_11_2021_URL = 'https://web.archive.org/web/20210111/https://www.billboard.com/charts/hot-100#/charts/hot-100/'
JUNE_22_2021_URL = 'https://web.archive.org/web/20210622/https://www.billboard.com/charts/hot-100#/charts/hot-100/'
SEPT_13_2021_URL = 'https://web.archive.org/web/20210913/https://www.billboard.com/charts/hot-100#/charts/hot-100/'
OCT_26_2021_URL = 'https://web.archive.org/web/20211026/https://www.billboard.com/charts/hot-100#/charts/hot-100/'
NOV_28_2021_URL = 'https://web.archive.org/web/20211128/https://www.billboard.com/charts/hot-100#/charts/hot-100/'
JAN_15_2022_URL = 'https://web.archive.org/web/20220115/https://www.billboard.com/charts/hot-100#/charts/hot-100/'

# Initalize data slice
data = []

# Use BeautifulSoup and requests to collect data before Nov 2021
urls = [APR_10_2020_URL, JUL_24_2020_URL, SEPT_11_2020_URL, DEC_30_2020_URL, 
        JAN_11_2021_URL, JUNE_22_2021_URL, SEPT_13_2021_URL, OCT_26_2021_URL]
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

# Use BeautifulSoup and requests to collect data after Nov 2021 (HTML layout changed)
urls = [NOV_28_2021_URL, JAN_15_2022_URL]
for url in urls:
    r = requests.get(url).text
    soup = BeautifulSoup(r, 'html.parser')
    items = soup.find_all('div', 'o-chart-results-list-row-container')
    rows = []
    for item in items:
        rows.append(item.find('ul'))
    
    # extract and insert into data slice
    for row in rows:
        pos_wrapper = row.find('li', 'o-chart-results-list__item')
        song_wrapper = row.find('li', 'lrv-u-width-100p').find('ul').find('li')

        # get song ranking
        pos = int(pos_wrapper.find('span').string.strip())
        # get song title
        title = song_wrapper.find('h3').string.strip()
        # get song artist
        artists = song_wrapper.find('span').string.strip()
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
conn = sqlite3.connect('data\\billboard.db')
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
