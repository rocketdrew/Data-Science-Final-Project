import os

import numpy as np
import csv
import matplotlib.pyplot as plt
from matplotlib import cm
from sklearn.cluster import KMeans
import argparse
import json
import random
import pandas as pd
from scipy import stats
import sqlite3

# from mpl_toolkits.mplot3d import Axes3D  # Not used but needed to make 3D plots

# feature_columns = ["energy", "loudness"]
# MAX_CLUSTERS = 10
# cmap = cm.get_cmap('tab10', MAX_CLUSTERS)

# take database and put it into dataframes
conn = sqlite3.connect('energy.db') 
c = conn.cursor()
c.execute(''' SELECT energy FROM regression
            WHERE (month = 4 AND day = 10 AND year = 2020)
            OR (month = 7 AND day = 24 AND year = 2020) 
            OR (month = 1 AND day = 11 AND year = 2021) 
            OR (month = 9 AND day = 13 AND year = 2021) 
            OR (month = 1 AND day = 15 AND year = 2022) ''')

df_energy_peak = (pd.DataFrame(c.fetchall(), columns=['energy']))["energy"].tolist()    

c.execute(''' SELECT energy FROM regression
            WHERE (month = 9 AND day = 11 AND year = 2020)
            OR (month = 12 AND day = 30 AND year = 2020) 
            OR (month = 6 AND day = 22 AND year = 2021) 
            OR (month = 10 AND day = 26 AND year = 2021) 
            OR (month = 11 AND day = 28 AND year = 2021) ''')

df_energy_trough = pd.DataFrame(c.fetchall(), columns=['energy'])["energy"].tolist()

conn = sqlite3.connect('loudness.db') 
c = conn.cursor()
c.execute(''' SELECT loudness FROM regression
            WHERE loudness != 0 
            AND ((month = 4 AND day = 10 AND year = 2020)
            OR (month = 7 AND day = 24 AND year = 2020) 
            OR (month = 1 AND day = 11 AND year = 2021) 
            OR (month = 9 AND day = 13 AND year = 2021) 
            OR (month = 1 AND day = 15 AND year = 2022)) ''')

df_loudness_peak = (pd.DataFrame(c.fetchall(), columns=['loudness']))["loudness"].tolist()    

c.execute(''' SELECT loudness FROM regression
            WHERE (month = 9 AND day = 11 AND year = 2020)
            OR (month = 12 AND day = 30 AND year = 2020) 
            OR (month = 6 AND day = 22 AND year = 2021) 
            OR (month = 10 AND day = 26 AND year = 2021) 
            OR (month = 11 AND day = 28 AND year = 2021) ''')

df_loudness_trough = pd.DataFrame(c.fetchall(), columns=['loudness'])["loudness"].tolist()

print(len(df_energy_peak))
print(len(df_loudness_peak))

# first, we will do clustering on peaks
plt.scatter(df_energy_peak, df_loudness_peak)
# plt.show()

a = [df_energy_peak, df_loudness_peak]
X = np.array(a).transpose()
print(X.shape)

km = KMeans(
    n_clusters=3, init='random',
    n_init=10, max_iter=300, 
    tol=1e-04, random_state=0
)
y_km = km.fit_predict(X)
print(y_km)

plt.scatter(
    X[y_km == 0, 0], X[y_km == 0, 1],
    s=50, c='lightgreen', edgecolor='black',
    label='cluster 1'
)

plt.scatter(
    X[y_km == 1, 0], X[y_km == 1, 1],
    s=50, c='orange', edgecolor='black',
    label='cluster 2'
)

plt.scatter(
    X[y_km == 2, 0], X[y_km == 2, 1],
    s=50, c='blue', edgecolor='black',
    label='cluster 3'
)

plt.scatter(
    km.cluster_centers_[:, 0], km.cluster_centers_[:, 1],
    s=50, 
    c='red', edgecolor='black',
    label='centroids'
)

plt.legend(scatterpoints=1)
plt.grid()
plt.show()
plt.savefig('kmeans.png')

# calculating the inertias
distortions = []
for i in range(1, 11):
    km = KMeans(
        n_clusters=i, init='random',
        n_init=10, max_iter=300,
        tol=1e-04, random_state=0
    )
    km.fit(X)
    distortions.append(km.inertia_)

# plot
plt.plot(range(1, 11), distortions, marker='o')
plt.xlabel('Number of clusters')
plt.ylabel('Distortion')
plt.show()
plt.savefig('elbow.png')


# convert the dataframe to a 2d numpy array


# def parse_args():
#     """
#     Parses the CLI args with argparse
#     :return: args from command line
#     """
#     parser = argparse.ArgumentParser(description='Machine Learning song_clustering (Problem 2)')
#     parser.add_argument('-d', help='path to data file', default='../data/ml/spotify.csv')
#     parser.add_argument('-o', help='path to output data directory', default='output')
#     return parser.parse_args()


# def read_data(path):
#     """
#     Reads the data at the provided files path. Performs some pre-processing
#     - removes outliers (data points that are more than 3 stdev away along any
#       feature column
#     - removes duplicates

#     :param path: path to dataset
#     :return: raw data, raw music data (only numeric columns)
#     """
#     # Load the data set into a 2D numpy array
#     with open(path) as data_file:
#         data = pd.read_csv(data_file)[feature_columns].to_numpy()

#     music_data = data[:, 2:].astype(np.float)
#     # Calculate z-score for all data points (how many standard deviations away from mean) for each column
#     z = np.abs(stats.zscore(music_data))
#     # Find all the rows where all values in each row have a z-score less than 3
#     ind = np.all((z < 3), axis=1)

#     data = data[ind]
#     music_data = music_data[ind]
#     return data, music_data


'''
def export_centroid_idx(centroids, idx, centroids_sklearn, idx_sklearn):
    """
    Exports the centroid centers and centroid indices for each data point
    :param centroids: numpy ndarray of cluster centers
    :param idx: centroid indices for each data point
    :param centroids_sklearn: numpy ndarray of cluster centers from sklearn
    :param idx_sklearn: centroid indices for each data point from sklearn
    """
    output = {"centroids": centroids.tolist(),
              "indices": idx.tolist(),
              "centroids_sklearn": centroids_sklearn.tolist(),
              "indices_sklearn": idx_sklearn.tolist()}
    with open("/song_clusters.json", 'w') as outfile:
        json.dump(output, outfile)


def visualize_songs_clusters(data, centroids=None, centroid_indices=None,
                             is_lib_kmean=False):
    """
    Visualizes the song data points and (optionally) the calculated k-means
    cluster centers.
    Points with the same color are considered to be in the same cluster.

    Optionally providing centroid locations and centroid indices will color the
    data points to match their respective cluster and plot the given centroids.
    Otherwise, only the raw data points will be plotted.

    :param data: 2D numpy array of song data
    :param centroids: 2D numpy array of centroid locations
    :param centroid_indices: 1D numpy array of centroid indices for each data point in data
    :return:
    """
    def plot_songs(fig, color_map=None):
        x, y, z = np.hsplit(data, 3)
        fig.scatter(x, y, z, c=color_map)

    def plot_clusters(fig):
        x, y, z = np.hsplit(centroids, 3)
        fig.scatter(x, y, z, c="black", marker="x", alpha=1, s=200)

    plt.clf()
    cluster_plot = centroids is not None and centroid_indices is not None

    ax = plt.figure(num=1).add_subplot(111, projection='3d')
    colors_s = None

    if cluster_plot:
        if max(centroid_indices) + 1 > MAX_CLUSTERS:
            print(f"Error: Too many clusters. Please limit to fewer than {MAX_CLUSTERS}.")
            exit(1)
        colors_s = [cmap(l / MAX_CLUSTERS) for l in centroid_indices]
        plot_clusters(ax)

    plot_songs(ax, colors_s)

    ax.set_xlabel(feature_columns[0])
    ax.set_ylabel(feature_columns[1])
    ax.set_zlabel(feature_columns[2])

    plot_name = "dancibility, energy, and valence"
    plot_name = plot_name + "_clusters" if cluster_plot else plot_name + "_raw"
    plot_name = plot_name + "_sklearn" if is_lib_kmean else plot_name

    ax.set_title(plot_name[1:])
    
    # Helps visualize clusters
    plt.gca().invert_xaxis()
    plt.savefig(plot_name + ".png")
    plt.show()


def elbow_point_plot(cluster, errors):
    """
    This function helps create a plot representing the tradeoff between the
    number of clusters and the inertia values.

    :param cluster: 1D np array that represents K (the number of clusters)
    :param errors: 1D np array that represents the inertia values
    """
    plt.clf()
    plt.plot(cluster, errors)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Inertia')
    plt.title('elbow_plot')
    plt.savefig("/elbow_plot.png")
    plt.show()


# ---- DO NOT CHANGE ANYTHING ABOVE THIS LINE ----


def min_max_scale(data):
    """
    Pre-processes the data by performing MinMax scaling.

    MinMax scaling prevents different scales of the data features from
    influencing distance calculations.

    MinMax scaling is performed by
        X_new = (X - X_min) / (X_max - X_min),

    where X_new is the newly scaled value, X_min is the minimum and X_max is the
    maximum along a single feature column.

    :param data: 2D numpy array of raw data
    :return: preprocessed data
    """
    # TODO: Standardize each column's features by subtracting the columns min and
    # dividing by the column's max - the column's min

    # check for formatting of min and min on a 2d array
    # print(data)
    trans = np.transpose(data)
    # trans = data

        # for each item in the 2d array
    count = 0
    for row in trans:
        minimum = min(row.tolist())
        maximum = max(row.tolist())
        # print("minimum")
        # print(minimum)
        # print("maximum")
        # print(maximum)

        
        for x in range(len(row)):
            # print(trans[count][x]) 
            numerator = trans[count][x] - minimum
            denominator = maximum - minimum

            # NOT SURE IF THIS EDITS/UPDATES THE DATA CORRECTLY
            trans[count][x] = numerator / denominator
        count += 1
    
    output = np.transpose(trans)
    # print(output)

    # return the array
    return output


def sk_learn_cluster(X, K):
    """
    Performs k-means clustering using library functions (scikit-learn). You can
    experiment with different initialization settings, but please initialize
    without any optional arguments (other than n_clusters) before submitting.

    :param X: 2D np array containing features of the songs
    :param K: number of clusters
    :return: a tuple of (cluster centroids, indices for each data point)
    """
    # TODO:

    # need to look up library functions to perform k means
    kmeans = KMeans(n_clusters=K)

    kmeans.fit(X)

    indices = kmeans.predict(X)

    centroids = kmeans.cluster_centers_

    tup = tuple((centroids, indices))

    return tup




def cluster_songs(music_data, max_iters=300):
    """
    Performs k-means clustering on the provided music data. Here is where you
    will visualize the raw data, use elbow_point_plot to determine the
    optimal K, and run k-means with this value of K. Follow the TODO comments
    below for more details.

    You should return 4 things from this function (documented below)

    :param music_data: 2D numpy array of music data
    :param max_iters: max number of iterations to run k-means
    :return:
        centroids: calculated cluster centroids from YOUR k-means object
        idx: centroid indices for each data point from YOUR k-means object
        centroids_sklearn: calculated cluster centroids from the sklearn k-means object
        idx_sklearn: centroid indices for each data point from the sklearn k-means object
    """

    # TODO: Perform MinMax scaling on the music_data
    data = min_max_scale(music_data)

    # TODO: Visualize the raw data with visualize_songs_clusters
    visualize_songs_clusters(data)

    # TODO: Use elbow_point_plot() to determine the optimal K (number of clusters)
    errors = np.zeros((5,), dtype=int)
    clusters = [1, 3, 5, 7, 9]
    for k in range(len(clusters)): 
        object = KMeans(data, clusters[k], max_iters)
        centroids, idx = object.run()
        errors[k] = KMeans.inertia(object, centroids, idx)

    elbow_point_plot(clusters, errors)


    # TODO: Run k-means with your chosen K
    # chosen k = 7
    object = KMeans(data, 7, max_iters)
    centroids, idx = object.run()

    # TODO: Use the visualize_songs_clusters() function to plot clusters
    visualize_songs_clusters(data, centroids, idx, True)

    # TODO: Visually compare the output from your Kmeans object to sk_learn_cluster() (print clusters and plot the song clusters)

    centroids_sklearn, idx_sklearn = sk_learn_cluster(music_data, 7)
    visualize_songs_clusters(data, centroids_sklearn, idx_sklearn, True)
    
    return centroids, idx, centroids_sklearn, idx_sklearn


# ---- DO NOT CHANGE ANYTHING BELOW THIS LINE ----


def main():
    """
    Main function for running song clustering. You should not have to change
    anything in this function.
    """
    # Set random seeds
    np.random.seed(0)
    random.seed(0)

    # data, music_data = read_data(data_dir)
    max_iters = 300  # Number of times the k-mean should run

    # if not os.path.exists(output_dir):
    #     os.makedirs(output_dir)

    centroids, idx, centroids_sklearn, idx_sklearn = cluster_songs(music_data, max_iters=max_iters)
    export_centroid_idx(centroids, idx, centroids_sklearn, idx_sklearn)


if __name__ == '__main__':
    # Make args global variable
    # args = parse_args()
    
    # data_dir = args.d
    # output_dir = args.o

    main()
'''