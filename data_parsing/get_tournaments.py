import csv


def main():
    tournament_dict = get_tournament_dict()
    names = get_tournament_names()
    write_tournament_names(names, tournament_dict)

def get_tournament_names():
    unique_names = set()
    get_atp_matches(unique_names)
    get_challenger_matches(unique_names)

    for name in unique_names:
        print(name)
    return unique_names

def get_atp_matches(unique_names):
    for year in range(2000, 2024):
        path = f'tennis_atp/atp_matches_{year}.csv'
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                tournament_name = row[1]
                if 'Davis Cup' in tournament_name:
                    continue
                unique_names.add(tournament_name)

def get_challenger_matches(unique_names):
    for year in range(2000, 2024):
        path = f'tennis_atp/atp_matches_qual_chall_{year}.csv'
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                tournament_name = row[1]
                unique_names.add(tournament_name)


def write_tournament_names(names, tournament_dict):
    header = ['tourney_name','tourney_country']
    done = []
    todo = []
    for name in names:
        if name in tournament_dict:
            done.append([f'{name},{tournament_dict[name]}'])
        else:
            todo.append([name, ''])
    with open('data/tournaments_test.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(header)
        for row in todo:
            writer.writerow(row)
        for row in done:
            writer.writerow(row)

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

if __name__ == '__main__':
    main()