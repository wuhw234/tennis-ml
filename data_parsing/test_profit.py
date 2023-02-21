import csv
import matplotlib.pyplot as plt
import numpy as np

def test(hidden_layer, learning_rate, dropout, trial):
    all_rows = []
    with open(f'data/hidden{hidden_layer}lr{learning_rate}dropout{dropout}trial{trial}.csv', newline='') as readfile:
    # with open(f'data/good1.csv', newline='') as readfile:
        reader = csv.reader(readfile, delimiter=',')
        next(reader)
        for row in reader:
            all_rows.append(row)

    bet_results = []
    total = 0
    losses = []
    wins = []
    loss_prob = []
    win_prob = []

    for i, row in enumerate(all_rows):
        if i < 2500: #first year 2010, unstable ratings
            continue
        p1_win = float(row[-4])
        p1_prediction = float(row[-1])
        p2_prediction = 1 - p1_prediction
        p2_prob = float(row[-2])
        p1_prob = float(row[-3])

        if p1_prediction > p1_prob:
        # if p1_prediction > p1_prob and p1_prediction > 0.8:
            bet_size = kelly(200, p1_prob, p1_prediction)
            if p1_win:
                decimal_odds = 1 / p1_prob
                gain = (bet_size * decimal_odds) - bet_size
                total += gain
                wins.append(p1_prob)
                win_prob.append(p1_prediction)
            else:
                total -= bet_size
                losses.append(p1_prob)
                loss_prob.append(p1_prediction)


            bet_results.append(total)
        elif p2_prediction > p2_prob:
        # elif p2_prediction > p2_prob and p2_prediction > 0.8:
            bet_size = kelly(200, p2_prob, p2_prediction)
            if not p1_win:
                decimal_odds = 2 / p2_prob
                gain = (bet_size * decimal_odds) - bet_size
                wins.append(p2_prob)
                win_prob.append(p2_prediction)

            else:
                total -= bet_size
                losses.append(p2_prob)
                loss_prob.append(p2_prediction)

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
    theta_squared = 0.3
    decimal_odds = 1/odds
    p = predicted
    b = decimal_odds - 1
    fraction = (((b+1) * (p) - 1) ** 2) / (((b+1)*(p) - 1) ** 2 + (b+1) ** 2 * theta_squared)
    proportion_gained = decimal_odds - 1
    kelly_percentage = predicted - ((1 - predicted) / proportion_gained)
    return fraction * balance * kelly_percentage

def calculate_win():
    pass

if __name__ == '__main__':
    test(600, 0.031, 0.35, 2)
    # test(600, 0.011, 0.25, 1) 
    # test(600, 0.031, 0.15, 0)
    # test(600, 0.031, 0.25, 2) 4
    # test(600, 0.021, 0.15, 0) 5
    # test(600, 0.021, 0.25, 2) 6