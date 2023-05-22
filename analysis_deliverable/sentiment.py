# Inspiration from: https://towardsdatascience.com/the-best-python-sentiment-analysis-package-1-huge-common-mistake-d6da9ad6cdeb
# And also: https://rileymjones.medium.com/sentiment-anaylsis-with-the-flair-nlp-library-cfe830bfd0f4

from flair.models import TextClassifier
from flair.data import Sentence
import sqlite3

sia = TextClassifier.load('en-sentiment')

def flair_prediction(x):
    sentence = Sentence(x)
    sia.predict(sentence)
    value = sentence.labels[0].to_dict()['value'] 
    if value == 'POSITIVE':
        result = sentence.to_dict()['all labels'][0]['confidence']
    else:
        result = -(sentence.to_dict()['all labels'][0]['confidence'])
    return round(result, 3)

# Create connection to database
conn = sqlite3.connect('../data_deliverable/data/billboard.db')
c = conn.cursor()

select_cmd = '''
SELECT 
	title, artist, lyrics
FROM
	lyrics
'''
c.execute(select_cmd)

conn2 = sqlite3.connect('../data_deliverable/data/billboard.db')
c2 = conn2.cursor()

for row in c:
    if row[2] != "":
        t = row[0]
        a = row[1]
        l = row[2]
        sent = flair_prediction(l)
        print("Song: ", t)
        print("Sentiment: ", sent)
        c2.execute('INSERT INTO lyrics VALUES (?, ?, ?, ?)', (t, a, l, sent))

conn2.commit()
c2.close()
conn2.close()

conn.commit()
c.close()
conn.close()