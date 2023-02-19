import csv
import matplotlib.pyplot as plt
import numpy as np

def test(hidden_layer, learning_rate, dropout, trial):
    all_rows = []
    with open(f'data/hidden{hidden_layer}lr{learning_rate}dropout{dropout}trial{trial}.csv', newline='') as readfile:
    # with open(f'data/test1.csv', newline='') as readfile:
        reader = csv.reader(readfile, delimiter=',')
        next(reader)
        for row in reader:
            all_rows.append(row)

    bet_results = []
    total = 50
    losses = 0
    wins = 0

    for row in all_rows:
        p1_win = float(row[-4])
        p1_prediction = float(row[-1])
        p2_prediction = 1 - p1_prediction
        p2_prob = float(row[-2])
        p1_prob = float(row[-3])

        if p1_prediction > p1_prob:
            bet_size = kelly(2, p1_prob, p1_prediction)
            if p1_win:
                decimal_odds = 1 / p1_prob
                gain = (bet_size * decimal_odds) - bet_size
                total += gain
                wins += 1
            else:
                total -= bet_size
                losses += 1
            bet_results.append(total)
        elif p2_prediction > p2_prob:
            bet_size = kelly(2, p2_prob, p2_prediction)
            if not p1_win:
                decimal_odds = 2 / p2_prob
                gain = (bet_size * decimal_odds) - bet_size
                wins += 1
            else:
                total -= bet_size
                losses += 1
            bet_results.append(total)
            
        else:
            continue

    min_balance = min(bet_results)
    # print('max balance', max(bet_results))
    # print('min_balance', min(bet_results))
    # print('end', bet_results[-1])

    # plt.rcParams["figure.figsize"] = [7.50, 3.50]
    # plt.rcParams["figure.autolayout"] = True

    # x = np.array(bet_results)

    # plt.title("Line graph")
    # plt.plot(x, color="red")

    # plt.show()

    return min_balance


        

def kelly(balance, odds, predicted):
    # theta = 0.3
    # decimal_odds = 1/odds
    # p = predicted
    # b = decimal_odds - 1
    # fraction = (((b+1) * (p) - 1) ** 2) / (((b+1)*(p) - 1) ** 2 + (b+1) ** 2 *theta)
    # return fraction * balance
    decimal_odds = 1/odds
    proportion_gained = decimal_odds - 1
    percentage = predicted - ((1 - predicted) / proportion_gained)
    return balance * percentage

def calculate_win():
    pass

if __name__ == '__main__':
    test(0.03, 1)