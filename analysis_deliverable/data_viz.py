from hypothesis_testing import * 
import pandas as pd 

print("start")
charts_file_path = "/Users/mohammedakel/Desktop/CS1951A-Spring2022/rim-dj/analysis_deliverable/charts"

def attributes_corr_heatmap(df):
    '''given a data frame, the function returns a heatmap depeciting the correlation between all the attributes in the dataframe'''
    matrix = df.corr().round(2)
    graph = sns.heatmap(matrix, annot=True)
    file_path = CHARTS_FILE + "/heatmap_test.png"
    plt.savefig(charts_file_path)
    plt.show()

trough_dancability = get_trough_attribute("danceability")
print("loaded trough dancability")
peak_dancability = get_peak_attribute("danceability")
print("loaded peak dancability")
dancability_boxPlot = pd.concat([trough_dancability, peak_dancability], axis=1).boxplot()
print(dancability_boxPlot)


#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
attributes = ["dancability", "popularity", "duration_ms", "explicit", "liveness", "loudness", "speech", "instrumental", "Acoustic", "Energy", "tempo", "valance"]

trough_dancability = get_trough_attribute("danceability")
print("loaded")
#trough_name = get_trough_attribute("name")
trough_popularity = get_trough_attribute("popularity")
print("loaded")
trough_duration_ms = get_trough_attribute("duration_ms")
print("loaded")
trough_explicit = get_trough_attribute("explicit")
print("loaded")
trough_liveness = get_trough_attribute("liveness")
print("loaded")
trough_loudness = get_trough_attribute("loudness")
print("loaded")
trough_speech = get_trough_attribute("speech")
print("loaded")
trough_instrumental = get_trough_attribute("instrumental")
print("loaded")
trough_Acoustic = get_trough_attribute("Acoustic")
print("loaded")
trough_Energy = get_trough_attribute("Energy")
print("loaded")
trough_tempo = get_trough_attribute("tempo")
print("loaded")
trough_valance = get_trough_attribute("valance")
print("loaded")


trough_tb = list(zip(trough_dancability, trough_popularity, trough_duration_ms, trough_explicit, trough_liveness, trough_loudness, trough_speech,
              trough_instrumental, trough_Acoustic, trough_Energy, trough_tempo, trough_valance))

print("table created")

trough_df = pd.DataFrame(trough_tb, columns=attributes)
attributes_corr_heatmap(trough_df)


peak_dancability = get_peak_attribute("danceability")
#peak_name = get_peak_attribute("name")
peak_popularity = get_peak_attribute("popularity")
peak_duration_ms = get_peak_attribute("duration_ms")
peak_explicit = get_peak_attribute("explicit")
peak_liveness = get_peak_attribute("liveness")
peak_loudness = get_peak_attribute("loudness")
peak_speech = get_peak_attribute("speech")
peak_instrumental = get_peak_attribute("instrumental")
peak_Acoustic = get_peak_attribute("Acoustic")
peak_Energy = get_peak_attribute("Energy")
peak_tempo = get_peak_attribute("tempo")
peak_valance = get_peak_attribute("valance")

peak_tb = list(zip(peak_dancability, peak_popularity, peak_duration_ms, peak_explicit, peak_liveness, peak_loudness, peak_speech,
              peak_instrumental, peak_Acoustic, peak_Energy, peak_tempo, peak_valance))

peak_df = pd.DataFrame(peak_tb, columns=attributes)
attributes_corr_heatmap(peak_df)

#box_plots that compare attributed during peaks and troughs
dancability_boxPlot = pd.concat(trough_dancability, peak_dancability], axis=1).boxplot()
savefig("output.png")
'''
