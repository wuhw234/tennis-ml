import pickle
import numpy as np
import tensorflow as tf
import pandas as pd


def get_bets():
    player_dict = get_player_dict()
    p1 = 'novakdjokovic'
    p2 = 'bornagojo'
    get_row_entry(player_dict[p1], player_dict[p2], 'USA', 'h', 1)
def get_row_entry(p1, p2, tourney_country, tourney_surface, is_bo5):
    # go to get_predictions and see format of data_frame features
    is_hard = 1 if tourney_surface == 'h' else 0
    is_clay = 1 if tourney_surface == 'c' else 0
    is_grass = 1 if tourney_surface == 'g' else 0
    height_diff = float(p1['height']) - float(p2['height'])
    age_diff = float(p1['age']) - float(p2['age'])
    p1_home = 1 if p1['home_country'] == tourney_country else 0
    p2_home = 1 if p2['home_country'] == tourney_country else 0
    rating_diff = float(p1['rating']) - float(p2['rating'])
    deviation_diff = float(p1['rating_dev']) - float(p2['rating_dev'])
    p1_surface_rating, p1_surface_dev = get_surface_rating(p1, tourney_surface)
    p2_surface_rating, p2_surface_dev = get_surface_rating(p2, tourney_surface)
    surface_rating_diff = p1_surface_rating - p2_surface_rating
    surface_deviation_diff = p1_surface_dev - p2_surface_dev
    w_diff = p1['w'] - p2['w']
    l_diff = p1['l'] - p2['l']
    p1_surface_w, p1_surface_l = get_surface_record(p1, tourney_surface)
    p2_surface_w, p2_surface_l = get_surface_record(p2, tourney_surface)
    surface_w_diff = p1_surface_w - p2_surface_w
    surface_l_diff = p1_surface_l - p2_surface_l
    inactive_diff = p1['inactive_days'] - p2['inactive_days']

    recent_30_diff = float(p1['recent_30']) - float(p2['recent_30'])
    recent_20_diff = float(p1['recent_20']) - float(p2['recent_20'])
    recent_10_diff = float(p1['recent_10']) - float(p2['recent_10'])


    ace_30_diff = p1['ace_30'] - p2['ace_30']
    df_30_diff = p1['df_30'] - p2['df_30']
    first_serve_30_diff = p1['first_serve_30'] - p2['first_serve_30']
    second_serve_30_diff = p1['second_serve_30'] - p2['second_serve_30']
    first_return_30_diff = p1['first_return_30'] - p2['first_return_30']
    second_return_30_diff = p1['second_return_30'] - p2['second_return_30']

    ace_20_diff = p1['ace_20'] - p2['ace_20']
    df_20_diff = p1['df_20'] - p2['df_20']
    first_serve_20_diff = p1['first_serve_20'] - p2['first_serve_20']
    second_serve_20_diff = p1['second_serve_20'] - p2['second_serve_20']
    first_return_20_diff = p1['first_return_20'] - p2['first_return_20']
    second_return_20_diff = p1['second_return_20'] - p2['second_return_20']
    
    ace_10_diff = p1['ace_10'] - p2['ace_10']
    df_10_diff = p1['df_10'] - p2['df_10']
    first_serve_10_diff = p1['first_serve_10'] - p2['first_serve_10']
    second_serve_10_diff = p1['second_serve_10'] - p2['second_serve_10']
    first_return_10_diff = p1['first_return_10'] - p2['first_return_10']
    second_return_10_diff = p1['second_return_10'] - p2['second_return_10']
    rankings_diff = p1['rank'] - p2['rank']

    features_dict = {
        'is_hard': np.array([is_hard]),
        'is_clay': np.array([is_clay]),
        'is_grass': np.array([is_grass]),
        'is_bo5': np.array([is_bo5]),
        'p1_home': np.array([p1_home]),
        'p2_home': np.array([p2_home]),
        'height_diff': np.array([height_diff]),
        'age_diff': np.array([age_diff]),
        'inactive_diff': np.array([inactive_diff]),
        'rating_diff': np.array([rating_diff]),
        'recent_30_diff': np.array([recent_30_diff]),
        'recent_20_diff': np.array([recent_20_diff]),
        'recent_10_diff': np.array([recent_10_diff]),
        'deviation_diff': np.array([deviation_diff]),
        'surface_rating_diff': np.array([surface_rating_diff]),
        'surface_deviation_diff': np.array([surface_deviation_diff]),
        'w_diff': np.array([w_diff]),
        'l_diff': np.array([l_diff]),
        'surface_w_diff': np.array([surface_w_diff]),
        'surface_l_diff': np.array([surface_l_diff]),
        'ace_30': np.array([ace_30_diff]),
        'df_30': np.array([df_30_diff]),
        'first_serve_30': np.array([first_serve_30_diff]),
        'second_serve_30': np.array([second_serve_30_diff]),
        'first_return_30': np.array([first_return_30_diff]),
        'second_return_30': np.array([second_return_30_diff]),
        'ace_20': np.array([ace_20_diff]),
        'df_20': np.array([df_20_diff]),
        'first_serve_20': np.array([first_serve_20_diff]),
        'second_serve_20': np.array([second_serve_20_diff]),
        'first_return_20': np.array([first_return_20_diff]),
        'second_return_20': np.array([second_return_20_diff]),
        'ace_10': np.array([ace_10_diff]),
        'df_10': np.array([df_10_diff]),
        'first_serve_10': np.array([first_serve_10_diff]),
        'second_serve_10': np.array([second_serve_10_diff]),
        'first_return_10': np.array([first_return_10_diff]),
        'second_return_10': np.array([second_return_10_diff]),
        'rankings_diff': np.array([rankings_diff])

    }
    model = pickle.load(open('random_forest/model2.sav', 'rb'))
    dataframe = pd.DataFrame(features_dict)
    p1_prob = model.predict_proba(dataframe)[0][1]
    print(p1_prob)



def get_surface_rating(player, tourney_surface):
    if tourney_surface == 'c':
        return float(player['clay_rating']), float(player['clay_rating_dev'])
    elif tourney_surface == 'h':
        return float(player['hard_rating']), float(player['hard_rating_dev'])
    else:
        return float(player['grass_rating']), float(player['grass_rating_dev'])

def get_surface_record(player, tourney_surface):
    if tourney_surface == 'c':
        return player['Clay_w'], player['Clay_l']
    elif tourney_surface == 'h':
        return player['Hard_w'], player['Hard_l']
    else:
        return player['Grass_w'], player['Grass_l']

def get_tourney_info():
    surface = None
    match_type = None
    country = ''
    while surface != 'h' and surface != 'c' and surface != 'g':
        surface = input('Are the courts hard, clay, or grass? (h, c, or g)')
    while match_type != '3' and match_type != '5':
        match_type = input('Are the matches bo3 or bo5? (3 or 5)')
    while len(country) != 3:
        country = input('Enter the country code for the tournament: ').upper()

    return surface, match_type, country
    
def get_player_dict():
    with open('data/players.pickle', 'rb') as handle:
        player_dict = pickle.load(handle)

    return player_dict

if __name__ == '__main__':
    get_bets()