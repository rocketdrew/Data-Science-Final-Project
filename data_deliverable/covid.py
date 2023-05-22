from bs4 import BeautifulSoup
import requests
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# read in the covid data
df = pd.read_csv('data\\covid.csv')
# select relevant columns
relevant = ['location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']
table = df[relevant]
# select relevant rows
us_rows = table[table['location'] == 'United States']

# Create connection to database
conn = sqlite3.connect('data\\covid.db')
c = conn.cursor()

# Delete tables if they exist
c.execute('DROP TABLE IF EXISTS "covid";')

# use CREATE TABLE to create the covid table in the database
create_covid_table_command = '''
CREATE TABLE IF NOT EXISTS covid (
    location VARCHAR NOT NULL,
    date VARCHAR NOT NULL,
    total_cases REAL,
    new_cases REAL,
    total_deaths REAL,
    new_deaths REAL,
    PRIMARY KEY (location, date)
);
'''
c.execute(create_covid_table_command)

# use INSERT to add data to the tables in the database
us_rows = us_rows.reset_index()
for idx, row in us_rows.iterrows():
    # initialize the location value
    l = row['location'].strip()
    # initialize the date value
    d = row['date']
    # initialize the total_cases value
    tc = row['total_cases']
    # initialize the new_cases value
    nc = row['new_cases']
    # initialize the total_deaths value
    td = row['total_deaths']
    # initialize the new_deaths value
    nd = row['new_deaths']

    c.execute('INSERT INTO covid VALUES (?, ?, ?, ?, ?, ?)', (l, d, tc, nc, td, nd))

conn.commit()

# # use Matplotlib to visualize the data. need to fix x-axis visibility
# # increase the size of the plot
# fig, ax = plt.subplots(figsize=(20, 12))
# # make x axis labels vertical
# plt.xticks(rotation=90)
# us_rows[['date', 'new_cases']].plot(kind='bar', ax=ax)
# # add labels to the plot
# ax.set_title("New U.S. Covid Cases Over Time")
# ax.set_xlabel("Date")
# ax.set_ylabel("New Cases")
# plt.show()