import csv
from get_matches import get_data
from add_predictions import add_predictions, get_predictions
from test_profit import test

def get_csv_info(start_year, end_year):
    match_data = {}
    forbidden = set()
    for year in range(start_year, end_year+1):
        with open(f'data/{year}.csv', newline='') as readfile:
            reader = csv.reader(readfile, delimiter=',')

            for row in reader:
                if invalid_entry(row):
                    continue
                hash = get_hash(row, year)
                if hash in forbidden:
                    continue
                winner_odds, loser_odds = row[30], row[31]
                if hash in match_data:
                    match_data.pop(hash)
                    forbidden.add(hash)
                match_data[hash] = {}
                match_data[hash]['w_odds'] = winner_odds
                match_data[hash]['l_odds'] = loser_odds

    return match_data


def get_hash(row, year):
    w_name, l_name = row[9].lower(), row[10].lower()
    w_rank, l_rank = row[11], row[12]
    w_points, l_points = row[13], row[14]
    w_initial, l_initial = get_initial(w_name), get_initial(l_name)
    w_two, l_two = get_last_two(w_name), get_last_two(l_name)

    hash = str(year) + w_initial + w_two + w_rank + l_initial + l_two + l_rank + w_points + l_points
    return hash
    
def get_initial(name):
    if '.' not in name:
        print('ERROR, no period', name)
    arr = name.split()
    for chars in arr:
        if '.' in chars:
            return chars[0]

def get_last_two(name):
    arr = name.split()
    valid = -1
    for i in range(0, len(arr)):
        name = arr[i]
        if '.' not in name:
            valid = i
        else:
            break
    first_name = arr[valid]
    two_chars = first_name[-2:]
    return two_chars

def pair_data(odds_dict, unpaired_filepath, paired_filepath):
    all_rows = []
    paired = []
    with open(unpaired_filepath, newline='') as readfile:
        reader = csv.reader(readfile, delimiter=',')
        for row in reader:
            all_rows.append(row)
    
    header_row = all_rows.pop(0)
    header_row.append('p1_prob')
    header_row.append('p2_prob')
    paired.append(header_row)

    for row in all_rows:
        match_hash = row[0]

        p1_win = row[-1]
        if match_hash in odds_dict:
            winner_odds, loser_odds = odds_dict[match_hash]['w_odds'], odds_dict[match_hash]['l_odds']
            if not winner_odds or not loser_odds:
                continue
            winner_prob, loser_prob = 1/float(winner_odds), 1/float(loser_odds)
            if not winner_prob or not loser_prob:
                continue
            if p1_win == '1':
                row.append(winner_prob)
                row.append(loser_prob)
            else:
                row.append(loser_prob)
                row.append(winner_prob)
            paired.append(row)
    write_paired(paired, paired_filepath)

def write_paired(arr, filepath):
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        for line in arr:
            writer.writerow(line)

def invalid_entry(row):
    w_rank, l_rank = row[11], row[12]
    w_points, l_points = row[13], row[14]
    w_name, l_name = row[9], row[10]

    if any(not c.isnumeric() for c in w_rank) or any(not c.isnumeric() for c in l_rank):
         return True
    elif not w_rank or not l_rank:
        return True
    elif not w_points or not l_points or any(not c.isnumeric() for c in w_points) or any(not c.isnumeric() for c in l_points):
        return True
    elif '.' not in w_name or '.' not in l_name:
        return True
    return False


if __name__ == '__main__':
    unpaired_csv = 'data/matches_test.csv'
    paired_csv = 'data/paired_odds.csv'
    # get_data(2010, 2023, unpaired_csv)
    odds_dict = get_csv_info(2010, 2023)
    pair_data(odds_dict, unpaired_csv, paired_csv)
    predictions = get_predictions()
    add_predictions(predictions, 'data/predictions.csv')
                    