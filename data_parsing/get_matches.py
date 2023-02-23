import csv
import random
from glicko2 import Player
from datetime import date
import pickle

def get_data(start_year, end_year, output_filepath):
    match_data = gather_data(start_year, end_year)
    write_data(match_data, output_filepath)

def gather_data(start_year, end_year):
    match_data = []
    for year in range(start_year, end_year+1):
        path1 = f'tennis_atp/atp_matches_{year}.csv'
        path2 = f'tennis_atp/atp_matches_qual_chall_{year}.csv'
        with open(path1, newline='') as readfile:
            reader = csv.reader(readfile, delimiter=',')

            for row in reader:
                if invalid_entry(row):
                    continue
                match_data.append(row)
        with open(path2, newline='') as readfile:
            reader = csv.reader(readfile, delimiter=',')

            for row in reader:
                if invalid_entry(row):
                    continue
                match_data.append(row)

    return sorted(match_data, key=lambda row:row[5])
            
def invalid_entry(row):
    tournament_name = row[1]
    surface = row[2]
    score = row[23]
    if 'Davis Cup' in tournament_name:
        return True
    elif not row[12] or not row[14] or not row[20] or not row[22]: #if height or age is missing
        return True
    elif any(c.isalpha() for c in score):
        return True
    elif surface == 'Carpet':
        return True
    else:
        return False

def write_data(data, filepath):
    header = ['match_hash','tourney_name','tourney_date','is_hard', 'is_clay', 'is_grass',
              'is_bo5', 'p1_name', 'p2_name', 'p1_height', 'p1_age','p1_home', 'p1_rating', 'p1_dev',
              'p1_surface_rating', 'p1_surface_dev', 'p1_recent_rating', 'p1_w', 'p1_l', 'p1_surface_w', 'p1_surface_l','p1_inactive_days',
              'p2_height', 'p2_age','p2_home', 'p2_rating', 'p2_dev',
              'p2_surface_rating', 'p2_surface_dev', 'p2_recent_rating', 'p2_w', 'p2_l', 'p2_surface_w', 'p2_surface_l', 'p2_inactive_days', 'p1_win']
    player_dict = {}
    random_list = [i for i in range(0, len(data))]
    random.shuffle(random_list)
    p1_winner = set(random_list[:len(random_list) // 2])


    with open(f'{filepath}', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(header)

        for i, row in enumerate(data):
            p1_win = True if i in p1_winner else False
            write_row(writer, row, player_dict, p1_win)

    clean_dict(player_dict)
    with open('data/players.pickle', 'wb') as file:
        pickle.dump(player_dict, file, protocol=pickle.HIGHEST_PROTOCOL)

def clean_dict(player_dict):
    for player in player_dict.keys():
        val = player_dict[player]
        rating = val.pop('overall')
        clay_rating = val.pop('Clay')
        hard_rating = val.pop('Hard')
        grass_rating = val.pop('Grass')

        val['rating'] = rating.getRating()
        val['clay_rating'] = clay_rating.getRating()
        val['hard_rating'] = hard_rating.getRating()
        val['grass_rating'] = grass_rating.getRating()

        val['rating_dev'] = rating.getRd()
        val['clay_rating_dev'] = clay_rating.getRd()
        val['hard_rating_dev'] = hard_rating.getRd()
        val['grass_rating_dev'] = grass_rating.getRd()

        val['recent_rating'] = get_recent_rating(val)
        val.pop('recent_matches')
        val.pop('recent_dev')
        val.pop('recent_results')

        val['inactive_days'] = get_time_since_last_match(val, date.today())

def write_row(writer, row, player_dict, p1_winner):
    #TODO: REMOVE LEFTY
    tournament_dict = get_tournament_dict()
    tourney_name = row[1]
    tourney_country = tournament_dict[tourney_name]
    tourney_surface = row[2]
    is_clay = 1 if tourney_surface == 'Clay' else 0
    is_hard = 1 if tourney_surface == 'Hard' else 0
    is_grass = 1 if tourney_surface == 'Grass' else 0
    winner_rank, loser_rank = standardize_name(row[45]), standardize_name(row[47])
    winner_name, loser_name = standardize_name(row[10]), standardize_name(row[18])
    tourney_date = row[5]
    is_bo5 = 1 if row[24] == '5' else 0

    if p1_winner: # winner is p1
        p1_name = standardize_name(row[10])
        p1_height = row[12]
        p1_home_country = row[13]
        p1_home = 1 if p1_home_country == tourney_country else 0
        p1_age = row[14]
        p2_name = standardize_name(row[18])
        p2_height = row[20]
        p2_home_country = row[21]
        p2_home = 1 if p2_home_country == tourney_country else 0
        p2_age = row[22]
        p1_win = 1
    else: # winner is p2
        p2_name = standardize_name(row[10])
        p2_height = row[12]
        p2_home_country = row[13]
        p2_home = 1 if p2_home_country == tourney_country else 0
        p2_age = row[14]
        p1_name = standardize_name(row[18])
        p1_height = row[20]
        p1_home_country = row[21]
        p1_home = 1 if p1_home_country == tourney_country else 0
        p1_age = row[22]
        p1_win = 0

    if p1_name not in player_dict:
        initialize_dict(player_dict, p1_name, tourney_date)
        player_dict[p1_name]['home_country'] = p1_home_country
    if p2_name not in player_dict:
        initialize_dict(player_dict, p2_name, tourney_date)
        player_dict[p2_name]['home_country'] = p2_home_country

    p1, p2 = player_dict[p1_name], player_dict[p2_name]
    # update player age, height
    p1['age'] = p1_age
    p2['age'] = p2_age
    p1['height'] = p1_height
    p2['height'] = p2_height
    # update deviations with inactivity
    curr_year, curr_month, curr_day = int(tourney_date[:4]), int(tourney_date[4:6]), int(tourney_date[6:])
    curr_date = date(curr_year, curr_month, curr_day)

    p1_inactive_days = get_time_since_last_match(p1, curr_date)
    p2_inactive_days = get_time_since_last_match(p2, curr_date)

    update_inactivity(p1, curr_date, 'overall')
    update_inactivity(p2, curr_date, 'overall')

    p1_rating, p1_deviation = p1['overall'].getRating(), p1['overall'].getRd()
    p2_rating, p2_deviation = p2['overall'].getRating(), p2['overall'].getRd()
    
    update_inactivity(p1, curr_date, tourney_surface)
    update_inactivity(p2, curr_date, tourney_surface)
    p1_surface_rating, p1_surface_deviation = p1[tourney_surface].getRating(), p1[tourney_surface].getRd()
    p2_surface_rating, p2_surface_deviation = p2[tourney_surface].getRating(), p2[tourney_surface].getRd()

    p1_w, p1_l = p1['w'], p1['l']
    p1_surface_w, p1_surface_l = p1[f'{tourney_surface}_w'], p1[f'{tourney_surface}_l']
    p2_w, p2_l = p2['w'], p2['l']
    p2_surface_w, p2_surface_l = p2[f'{tourney_surface}_w'], p2[f'{tourney_surface}_l']

    w_points, l_points = row[46], row[48]
    match_hash = str(curr_year) + winner_name[0] + winner_name[-2:] + winner_rank + loser_name[0] + loser_name[-2:] + loser_rank + w_points + l_points

    p1_recent_rating = get_recent_rating(p1)
    p2_recent_rating = get_recent_rating(p2)

    writer.writerow([match_hash, tourney_name, tourney_date, is_hard, is_clay, is_grass, 
                     is_bo5, p1_name, p2_name, p1_height, p1_age, p1_home, p1_rating, p1_deviation,
                     p1_surface_rating, p1_surface_deviation, p1_recent_rating, p1_w, p1_l, p1_surface_w,
                     p1_surface_l, p1_inactive_days, p2_height, p2_age, p2_home, p2_rating, p2_deviation,
                     p2_surface_rating, p2_surface_deviation, p2_recent_rating, 
                     p2_w, p2_l, p2_surface_w, p2_surface_l, p2_inactive_days, p1_win])
    # update glicko ratings and wins and losses
    update_ratings(p1, p2, p1_win, tourney_surface)
    update_recent_rating(p1, p2_rating, p2_deviation, True if p1_win else False)
    update_recent_rating(p2, p1_rating, p1_deviation, False if p1_win else True)


def get_recent_rating(player):
    player_rating = Player()
    recent_matches, recent_dev, recent_results = player['recent_matches'], player['recent_dev'], player['recent_results']
    if not recent_matches:
        return player_rating.getRating()
    
    player_rating.update_player(recent_matches, recent_dev, recent_results)

    return player_rating.getRating()

def update_recent_rating(player, opponent_rating, opponent_dev, result):
    if len(player['recent_matches']) > 13:
        player['recent_matches'].pop(0)
        player['recent_dev'].pop(0)
        player['recent_results'].pop(0)
    player['recent_matches'].append(opponent_rating)
    player['recent_dev'].append(opponent_dev)
    player['recent_results'].append(result)

def get_time_since_last_match(player, curr_date):
    last_match = player['last_match']
    year, month, day = int(last_match[:4]), int(last_match[4:6]), int(last_match[6:])
    prev_date = date(year, month, day)
    inactive_days = curr_date - prev_date
    return inactive_days.days

def update_ratings(p1, p2, p1_win, surface):
    p1_rating, p1_dev = p1['overall'].getRating(), p1['overall'].getRd()
    p1_surface_rating, p1_surface_dev = p1[surface].getRating(), p1[surface].getRd()
    p2_rating, p2_dev = p2['overall'].getRating(), p2['overall'].getRd()
    p2_surface_rating, p2_surface_dev = p2[surface].getRating(), p2[surface].getRd()
    win = True if p1_win else False


    p1['overall'].update_player([p2_rating], [p2_dev], [win])
    p1[surface].update_player([p2_surface_rating], [p2_surface_dev], [win])
    p2['overall'].update_player([p1_rating], [p1_dev], [not win])
    p2[surface].update_player([p1_surface_rating], [p1_surface_dev], [not win])

    if win:
        p1['w'] += 1
        p1[f'{surface}_w'] += 1
        p2['l'] += 1
        p2[f'{surface}_l'] += 1
    else:
        p1['l'] += 1
        p1[f'{surface}_l'] += 1
        p2['w'] += 1
        p2[f'{surface}_w'] += 1

def initialize_dict(player_dict, name, tourney_date):
    player_dict[name] = { 'overall': Player(), 'Clay': Player(), 'Hard': Player(), 'Grass': Player(),
                                 'last_match': tourney_date, 'last_clay_match': tourney_date,
                                 'last_hard_match': tourney_date, 'last_grass_match': tourney_date,
                                 'w': 0, 'l': 0, 'Clay_w': 0, 'Clay_l': 0, 'Hard_w': 0, 'Hard_l': 0,
                                 'Grass_w': 0, 'Grass_l': 0, 'recent_matches': [], 'recent_dev': [],
                                 'recent_results': [] }

def update_inactivity(player, curr_date, rating_type):
    if rating_type == 'overall':
        last_match = player['last_match']
    elif rating_type == 'Clay':
        last_match = player['last_clay_match']
    elif rating_type == 'Hard':
        last_match = player['last_hard_match']
    else:
        last_match = player['last_grass_match']
    year, month, day = int(last_match[:4]), int(last_match[4:6]), int(last_match[6:])
    prev_date = date(year, month, day)
    inactive_days = curr_date - prev_date
    inactive_weeks = inactive_days.days / 7
    if rating_type == 'overall':
        player[rating_type].did_not_compete(inactive_weeks)
    else:
        player[rating_type].did_not_compete(inactive_weeks, 40)


    year_string = str(curr_date.year)
    month_string = str(curr_date.month)
    if len(month_string) < 2:
        month_string = '0' + month_string
    day_string = str(curr_date.day)
    if len(day_string) < 2:
        day_string = '0' + day_string
    date_string = year_string + month_string + day_string

    player['last_match'] = date_string
    if rating_type == 'Clay':
        player['last_clay_match'] = date_string
    elif rating_type == 'Hard':
        player['last_hard_match'] = date_string
    else:
        player['last_grass_match'] = date_string

def get_tournament_dict():
    path = 'data/tournaments.csv'
    tournament_dict = {}
    with open(path, newline='') as readfile:
        reader = csv.reader(readfile, delimiter=',')
        next(reader)
        for row in reader:
            tournament, country = row[0], row[1]
            tournament_dict[tournament] = country

    return tournament_dict

def standardize_name(name):
    alphabetic = ''.join([i for i in name if i.isalpha()])
    lower = alphabetic.lower()
    return lower

if __name__ == '__main__':
    get_data(2000, 2023, 'data/matches.csv')
