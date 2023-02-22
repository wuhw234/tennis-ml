import csv
from get_matches import get_data
from add_predictions import add_predictions, get_predictions
from test_profit import test

def get_csv_info(source_paths):
    match_data = {}
    for path in source_paths:
        year = path[5:9]
        with open(path, newline='') as readfile:
            reader = csv.reader(readfile, delimiter=',')

            for row in reader:
                if invalid_entry(row):
                    continue
                hash = get_hash(row, year)
                winner_odds, loser_odds = row[30], row[31]
                if hash in match_data:
                    print('ERROR, hash already in dict', hash)
                match_data[hash] = {}
                match_data[hash]['w_odds'] = winner_odds
                match_data[hash]['l_odds'] = loser_odds

    return match_data


def get_hash(row, year):
    w_name, l_name = row[9], row[10]
    w_rank, l_rank = row[11], row[12]
    w_points, l_points = row[13], row[14]
    w_initial, l_initial = get_initial(w_name), get_initial(l_name)
    w_two, l_two = get_last_two(w_name), get_last_two(l_name)

    hash = year + w_initial.upper() + w_two + w_rank + l_initial.upper() + l_two + l_rank + w_points + l_points
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
    header_row.append('p1_odds')
    header_row.append('p2_odds')
    paired.append(header_row)

    for row in all_rows:
        match_hash = row[0]

        p1_win = row[-1]
        if match_hash in odds_dict:
            winner_odds, loser_odds = odds_dict[match_hash]['w_odds'], odds_dict[match_hash]['l_odds']
            if p1_win == '1':
                row.append(winner_odds)
                row.append(loser_odds)
            else:
                row.append(loser_odds)
                row.append(winner_odds)
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
         print(w_rank, l_rank)
         return True
    elif not w_rank or not l_rank:
        return True
    elif not w_points or not l_points or any(not c.isnumeric() for c in w_points) or any(not c.isnumeric() for c in l_points):
        return True
    elif '.' not in w_name or '.' not in l_name:
        return True
    return False

if __name__ == '__main__':
    # predictions_csv = f'data/test0.csv'
    # predictions = get_predictions(0,0,0,0)
    # add_predictions(predictions, predictions_csv)
    #  unpaired_csv = 'data/unpaired.csv'
    #  paired_csv = 'data/paired_odds.csv'
    #  get_data(2020, 2023, unpaired_csv)
    #  odds_dict = get_csv_info(source_csvs)
    #  pair_data(odds_dict, unpaired_csv, paired_csv)


    good_trials = []
    for hidden_layer in range(1000, 1301, 100):
        for learning_rate in range(3,7):
            learning_rate = learning_rate / 10000
            for int_dropout in range(45, 46):
                dropout = int_dropout / 100
                for trial in range(5):
                    predictions_csv = f'data/hidden{hidden_layer}lr{learning_rate}dropout{dropout}trial{trial}.csv'
                    # predictions = get_predictions(hidden_layer, learning_rate, dropout, trial)
                    # add_predictions(predictions, predictions_csv)
                    result = test(hidden_layer, learning_rate, dropout, trial)
                    good_trials.append((result, predictions_csv))
    
    good_trials.sort(reverse=True)
    for i in range(0, 15):
        print(good_trials[i])
                    

    # predictions_csv = f'data/test0.csv'
    # predictions = get_predictions(0,0,0,0)
    # add_predictions(predictions, predictions_csv)