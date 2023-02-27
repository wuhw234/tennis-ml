from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

from webdriver_manager.chrome import ChromeDriverManager

from get_matches import standardize_name

def get_odds(fanduel_url, betmgm_url, bovada_url):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    match_odds = {}

    if fanduel_url:
        fanduel_html = get_fanduel_html(driver, fanduel_url)
        get_fanduel_matches(fanduel_html, match_odds)
    if betmgm_url:
        betmgm_html = get_mgm_html(driver, betmgm_url)
        get_mgm_matches(betmgm_html, match_odds)
    if bovada_url:
        bovada_html = get_bovada_html(driver, bovada_url)
        get_bovada_matches(bovada_html, match_odds)

    return match_odds

def get_fanduel_matches(fanduel_html, match_odds):
    soup = BeautifulSoup(fanduel_html, 'html.parser')
    list = soup.find_all('ul')
    all_matches = None
    for item in list:
        if 'Upcoming' in item.text:
            all_matches = item
            break

    # f = open("newfile.txt", "w")
    # f.write(all_matches.prettify())
    # f.close()
    for match in all_matches:
        is_live = match.find(attrs={'aria-label': 'live event'})
        spans = match.find_all('span')

        if len(spans) != 5 or is_live: #if match has started or betting not allowed
            continue
        is_doubles = '/' in spans[0].text
        if is_doubles:
            continue

        player1, player2 = spans[0].text, spans[1].text
        player1, player2 = standardize_name(player1), standardize_name(player2)
        player1_odds, player2_odds = int(spans[2].text), int(spans[3].text)
        if player1 > player2: #alphabetically smaller player is p1
            player1, player2 = player2, player1
            player1_odds, player2_odds = player2_odds, player1_odds
        p1_prob, p2_prob = moneyline_to_probability(player1_odds), moneyline_to_probability(player2_odds)
        
        hash = hash_match(player1, player2)
        # print(player1, player1_odds, player2, player2_odds, hash)
        if hash not in match_odds:
            match_odds[hash] = {}
            match_odds[hash]['p1_prob'] = []
            match_odds[hash]['p2_prob'] = []

        match_odds[hash]['p1_prob'].append((p1_prob, 'Fanduel'))
        match_odds[hash]['p2_prob'].append((p2_prob, 'Fanduel'))
    
def get_mgm_matches(mgm_html, match_odds):
    soup = BeautifulSoup(mgm_html, 'html.parser')
    all_matches = soup.select('ms-event.grid-event')

    for match in all_matches:
        is_live = match.select('i.live-icon')
        if is_live:
            continue
        players = match.select('div.participant')
        player1, player2 = players[0].find(text=True, recursive=False), players[1].find(text=True, recursive=False)
        player1, player2 = standardize_name(player1), standardize_name(player2)
        
        odds = match.find_all('ms-font-resizer')
        player1_odds, player2_odds = int(odds[0].text), int(odds[1].text)

        if player1 > player2:
            player1, player2 = player2, player1
            player1_odds, player2_odds = player2_odds, player1_odds
        p1_prob, p2_prob = moneyline_to_probability(player1_odds), moneyline_to_probability(player2_odds)

        hash = hash_match(player1, player2)
        if hash not in match_odds:
            match_odds[hash] = {}
            match_odds[hash]['p1_prob'] = []
            match_odds[hash]['p2_prob'] = []

        match_odds[hash]['p1_prob'].append((p1_prob, 'BetMGM'))
        match_odds[hash]['p2_prob'].append((p2_prob, 'BetMGM'))

def get_bovada_matches(bovada_html, match_odds):
    soup = BeautifulSoup(bovada_html, 'html.parser')
    container = soup.select('div.next-events-bucket')[0]
    matches_container = container.select('div.grouped-events')[0]
    matches = matches_container.select('section.coupon-content.more-info')
    for match in matches:
        competitors = match.select('div.competitors')[0]
        spans = competitors.select('span.name')
        p1, p2 = standardize_name(spans[0].text), standardize_name(spans[1].text)
        odds_container = match.select('sp-outcomes.markets-container')[0]
        moneyline = odds_container.select('sp-two-way-vertical')[1]
        odds = moneyline.select('span.bet-price')
        p1_odds, p2_odds = odds[0].text, odds[1].text
        if 'EVEN' in p1_odds:
            p1_odds = 100
        else:
            p1_odds = int(p1_odds)
        if 'EVEN' in p2_odds:
            p2_odds = 100
        else:
            p2_odds = int(p2_odds)

        if p1 > p2:
            p1, p2 = p2, p1
            p1_odds, p2_odds = p2_odds, p1_odds
        p1_prob, p2_prob = moneyline_to_probability(p1_odds), moneyline_to_probability(p2_odds)
        hash = hash_match(p1, p2)
        if hash not in match_odds:
            match_odds[hash] = {}
            match_odds[hash]['p1_prob'] = []
            match_odds[hash]['p2_prob'] = []

        match_odds[hash]['p1_prob'].append((p1_prob, 'Bovada'))
        match_odds[hash]['p2_prob'].append((p2_prob, 'Bovada'))

def moneyline_to_probability(odds):
    if odds < 0:
        return ((-odds) / (-odds + 100))
    else:
        return (100 / (odds+100))
    
def get_fanduel_html(driver, url):
    driver.get(url)
    WebDriverWait(driver, timeout=15).until(EC.url_to_be(url))
    curr_url = driver.current_url
    page_source = None
    if curr_url == url:
        page_source = driver.page_source

    return page_source

def get_mgm_html(driver, url):
    driver.get(url)
    WebDriverWait(driver, timeout=15).until(EC.presence_of_element_located((By.CLASS_NAME, 'event-group')))

    return driver.page_source

def get_bovada_html(driver, url):
    driver.get(url)
    WebDriverWait(driver, timeout=15).until(EC.presence_of_element_located((By.CLASS_NAME, 'next-events-bucket')))

    return driver.page_source


def hash_match(player1, player2):
    return player1 + '/' + player2


if __name__ == '__main__':
    get_odds()