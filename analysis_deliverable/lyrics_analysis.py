import sqlite3
import numpy as np
from scipy.stats import ttest_ind
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.model_selection import KFold
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing

# SQL Things
conn = sqlite3.connect('../data_deliverable/data/billboard.db')
c = conn.cursor()

select_cmd = '''
SELECT *
FROM billboard as b
INNER JOIN lyrics as l
ON b.title = l.title and b.artist = l.artist
WHERE l.sentiment NOT NULL
'''
df = pd.read_sql_query(select_cmd, conn)
df["date"] = df["month"].astype(int).astype(str) + "-" + \
    df["day"].astype(int).astype(str) + "-" + df["year"].astype(int).astype(str)
df["peak_or_trough"] = np.where(
    (df["date"] == "7-24-2020") | 
    (df["date"] == "1-11-2021") |
    (df["date"] == "9-13-2021") |
    (df["date"] == "1-15-2022")
    , "peak", "trough")
df["peak_int"] = np.where(df["peak_or_trough"] == "peak", 1, 0)

dates = ["4-10-2020", "6-24-2020", "9-11-2020", "12-30-2020", "1-11-2021", \
    "6-22-2021", "9-13-2021", "10-26-2021", "11-28-2021", "1-15-2022"]

def f(row):
    if row['date'] == "4-10-2020": #trough
        val = 0
    elif row['date'] == "7-24-2020": #peak
        val = 1
    elif row['date'] == "9-11-2020": #trough
        val = 2
    elif row['date'] == "12-30-2020": #trough
        val = 3
    elif row['date'] == "1-11-2021": #peak
        val = 4
    elif row['date'] == "6-22-2021": #trough
        val = 5
    elif row['date'] == "9-13-2021": #peak
        val = 6
    elif row['date'] == "10-26-2021": #trough
        val = 7
    elif row['date'] == "11-28-2021": #trough
        val = 8
    elif row['date'] == "1-15-2022": #peak
        val = 9
    else:
        val = -1
    return val

df["date_int"] = df.apply(f, axis=1)

def countwords(row):
    return len(row['lyrics'].split(" "))

def unique(row):
    return len(set(row['lyrics'].split(" ")))

df["wordcount"] = df.apply(countwords, axis=1)

df["uq_words"] = df.apply(unique, axis=1)

sent_peaks = df.loc[df['peak_or_trough'].str.contains('peak'), 'sentiment']
sent_troughs = df.loc[df['peak_or_trough'].str.contains('trough'), 'sentiment']

word_peaks = df.loc[df['peak_or_trough'].str.contains('peak'), 'wordcount']
word_troughs = df.loc[df['peak_or_trough'].str.contains('trough'), 'wordcount']

uq_peaks = df.loc[df['peak_or_trough'].str.contains('peak'), 'uq_words']
uq_troughs = df.loc[df['peak_or_trough'].str.contains('trough'), 'uq_words']


conn.commit()
c.close()
conn.close()


# Run t-tests
sent_tstats, sent_pvalue = ttest_ind(sent_troughs, sent_peaks, equal_var=False, nan_policy='omit')
sent_dif = np.mean(sent_peaks) - np.mean(sent_troughs)
print("sentiment difference: ", sent_dif)
print("tstats: ", sent_tstats)
print("pvalue: ", sent_pvalue)

words_tstats, words_pvalue = ttest_ind(word_troughs, word_peaks, equal_var=False, nan_policy='omit')
words_dif = np.mean(word_peaks) - np.mean(word_troughs)
print("\nword count difference: ", words_dif)
print("tstats: ", words_tstats)
print("pvalue: ", words_pvalue)

uq_tstats, uq_pvalue = ttest_ind(uq_troughs, uq_peaks, equal_var=False, nan_policy='omit')
uq_dif = np.mean(uq_peaks) - np.mean(uq_troughs)
print("\nunique word count difference: ", uq_dif)
print("tstats: ", uq_tstats)
print("pvalue: ", uq_pvalue)


means = []
for i in range(10):
    avg = df.loc[df["date_int"] == i, "sentiment"].mean()
    means.append(avg)
#print(means)


# Bar chart viz
col1 = ['blue', 'red', 'blue', 'blue', 'red', 'blue', 'red', 'blue', 'blue', 'red']
col2 = ['blue', 'blue', 'blue', 'red', 'red', 'blue', 'red', 'blue', 'blue', 'red']
plt.bar(x = dates, height = means, color = col1)
plt.xticks(rotation=20)
plt.title("Lyrical Sentiment at Covid-19 Peaks and Troughs")
red_patch = mpatches.Patch(color='red', label='Peak')
blue_patch = mpatches.Patch(color='blue', label='Trough')

plt.legend(handles=[red_patch, blue_patch], loc='lower right')
plt.show()


# Logistic Regression w K-Fold Validation

df["labels"] = np.where(df["sentiment"] > 0, 1, 0)
accs = []
X = df.drop('sentiment', axis=1).drop('labels', axis=1).drop('title', axis=1) \
    .drop('artist', axis=1).drop('lyrics', axis=1).drop('date', axis=1).drop('peak_or_trough', axis=1).to_numpy()
y = df["labels"].to_numpy()

kf = KFold(n_splits=20, shuffle = True)

for train_index, test_index in kf.split(df):
    #print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    scaler = preprocessing.StandardScaler().fit(X_train)
    X_scaled = scaler.transform(X_train)
    clf = LogisticRegression(random_state=0).fit(X_scaled, y_train)
    score = clf.score(scaler.transform(X_test), y_test)
    accs.append(score)

print("\nAverage accuracy: ", np.mean(accs))
