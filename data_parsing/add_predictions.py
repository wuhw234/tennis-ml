import pandas as pd
import numpy as np
import tensorflow as tf
import csv

def add_predictions(predictions, path):
    all_rows = []
    with open('data/paired_odds.csv', newline='') as readfile:
        reader = csv.reader(readfile, delimiter=',')
        for row in reader:
            all_rows.append(row)
    
    header_row = all_rows[0]
    header_row.append('p1_prediction')

    for i in range(1, len(all_rows)):
        all_rows[i].append(predictions[i-1].tolist()[0])

    write_predictions(all_rows, path)

def write_predictions(rows, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for row in rows:
            writer.writerow(row)

        
def get_predictions(hidden_layer, learning_rate, dropout, trial):
    dataframe = pd.read_csv('data/paired_odds.csv')
    dataframe.pop('p1_win')
    dataframe.pop('match_hash')
    dataframe.pop('tourney_name')
    dataframe.pop('tourney_date')
    dataframe.pop('p1_name')
    dataframe.pop('p2_name')
    dataframe.pop('p1_prob')
    dataframe.pop('p2_prob')

    dataframe_features = dataframe.copy()

    features_dict = {name: np.array(value) for name, value in dataframe_features.items()}

    reloaded = tf.keras.models.load_model(f'neural_network/hidden{hidden_layer}lr{learning_rate}dropout{dropout}trial{trial}')
    # reloaded = tf.keras.models.load_model(f'neural_network/test0')


    predictions = reloaded.predict(features_dict)

    return predictions