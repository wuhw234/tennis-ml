import csv


def main():
    names = get_tournament_names()
    write_tournament_names(names)

def get_tournament_names():
    unique_names = set()
    for year in range(2010, 2024):
        get_atp_matches(unique_names)
        get_challenger_matches(unique_names)
        # get_itf_matches(unique_names)

    for name in unique_names:
        print(name)
    return unique_names

def get_atp_matches(unique_names):
    for year in range(2010, 2024):
        path = f'tennis_atp/atp_matches_{year}.csv'
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                tournament_name = row[1]
                if 'Davis Cup' in tournament_name:
                    continue
                unique_names.add(tournament_name)

def get_challenger_matches(unique_names):
    for year in range(2010, 2024):
        path = f'tennis_atp/atp_matches_qual_chall_{year}.csv'
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                tournament_name = row[1]
                unique_names.add(tournament_name)

def get_itf_matches(unique_names):
    for year in range(2010, 2024):
        path = f'tennis_atp/atp_matches_futures_{year}.csv'
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                tournament_name = row[1]
                unique_names.add(tournament_name)


def write_tournament_names(names):
    header = ['tourney_name','tourney_country']
    with open('data/tournaments.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(header)
        for name in names:
            writer.writerow([name, ''])



if __name__ == '__main__':
    main()