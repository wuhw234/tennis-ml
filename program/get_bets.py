import pickle
import numpy as np
import tensorflow as tf


def get_bets():
    player_dict = get_player_dict()
    p1 = 'novakdjokovic'
    p2 = 'stefanostsitsipas'
    get_row_entry(player_dict[p1], player_dict[p2], 'USA', 'h', 1)
def get_row_entry(p1, p2, tourney_country, tourney_surface, is_bo5):
    # go to get_predictions and see format of data_frame features
    is_hard = 1 if tourney_surface == 'h' else 0
    is_clay = 1 if tourney_surface == 'c' else 0
    is_grass = 1 if tourney_surface == 'g' else 0
    p1_height, p2_height = float(p1['height']), float(p2['height'])
    p1_age, p2_age = float(p1['age']), float(p2['age'])
    p1_home = 1 if  p1['home_country'] == tourney_country else 0
    p2_home = 1 if  p2['home_country'] == tourney_country else 0
    p1_rating, p1_dev = float(p1['rating']), float(p1['rating_dev'])
    p2_rating, p2_dev = float(p2['rating']), float(p2['rating_dev'])
    p1_surface_rating, p1_surface_dev = get_surface_rating(p1, tourney_surface)
    p2_surface_rating, p2_surface_dev = get_surface_rating(p2, tourney_surface)
    p1_recent_rating, p2_recent_rating = float(p1['recent_rating']), float(p2['recent_rating'])
    p1_w, p1_l = p1['w'], p1['l']
    p2_w, p2_l = p2['w'], p2['l']
    p1_surface_w, p1_surface_l = get_surface_record(p1, tourney_surface)
    p2_surface_w, p2_surface_l = get_surface_record(p2, tourney_surface)
    p1_inactive_days, p2_inactive_days = p1['inactive_days'], p2['inactive_days']

    features_dict = {
        'is_hard': np.array([is_hard]),
        'is_clay': np.array([is_clay]),
        'is_grass': np.array([is_grass]),
        'is_bo5': np.array([is_bo5]),
        'p1_height': np.array([p1_height]),
        'p2_height': np.array([p2_height]),
        'p1_age': np.array([p1_age]),
        'p2_age': np.array([p2_age]),
        'p1_home': np.array([p1_home]),
        'p2_home': np.array([p2_home]),
        'p1_rating': np.array([p1_rating]),
        'p2_rating': np.array([p2_rating]),
        'p1_dev': np.array([p1_dev]),
        'p2_dev': np.array([p2_dev]),
        'p1_surface_rating': np.array([p1_surface_rating]),
        'p2_surface_rating': np.array([p2_surface_rating]),
        'p1_surface_dev': np.array([p1_surface_dev]),
        'p2_surface_dev': np.array([p2_surface_dev]),
        'p1_recent_rating': np.array([p1_recent_rating]),
        'p2_recent_rating': np.array([p2_recent_rating]),
        'p1_w': np.array([p1_w]),
        'p2_w': np.array([p2_w]),
        'p1_l': np.array([p1_l]),
        'p2_l': np.array([p2_l]),
        'p1_surface_w': np.array([p1_surface_w]),
        'p2_surface_w': np.array([p2_surface_w]),
        'p1_surface_l': np.array([p1_surface_l]),
        'p2_surface_l': np.array([p2_surface_l]),
        'p1_inactive_days': np.array([p1_inactive_days]),
        'p2_inactive_days': np.array([p2_inactive_days]),
    }
    reloaded = tf.keras.models.load_model('neural_network/test0')
    predictions = reloaded.predict(features_dict)
    # print(features_dict)
    print(predictions)



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