#!/usr/bin/python3

from bs4 import BeautifulSoup as bs
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import datetime

driver = webdriver.Firefox()

INFO = dict()

ACCOUNTS = [
]


def re_register(account):
    # driver.quit()
    # driver = webdriver.Firefox()
    driver.delete_all_cookies()
    
    sleep(2)

    url = "https://www.english-corpora.org/coca/login1.asp"
    driver.get(url)


    sleep(3)

    # locate email form by_name
    # username = driver.find_element(By.CLASS_NAME, 'email')
    username = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]')
    username.send_keys(account[0])

    # locate password form by_name
    password = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    password.send_keys(account[1])

    log_in_button = driver.find_element(By.CSS_SELECTOR, 'input[name="B1"]')
    log_in_button.click()

    sleep(2)

    # return driver

re_register(ACCOUNTS[0])


WORDS = [
# "apartment",
# "apartment block",
# "apartment building",
# "apartment house",
# "attics",
# "backyard",
# "bar",
# "block of flats",
# "box-house",
# "box junction",
# "bungalow",
# "club",
# "condominium",
# "dormitory ",
# "duplex",
# "entryway",
# "estate",
# "false-front building",
# "flat",
# "foyer",
# "front room",
# "garden",
# "grocery store",
# "hall",
# "hallway",
# "honky-tonk",
# "housing project",
# "living room",
# "lobby",
# "lodge",
# "loft apartment",
# "lounge",
# "lounge bar",
# "lunchroom",
# "mobile home",
# "parlour",
# "porch",
# "public house",
# "pub",
# "ranch house",
# "rooming house",
# "row house",
# "saloon",
# "semi-skyscraper",
# "shop",
# "store",
# "subdivision",
# "sun lounge",
# "sun porch",
# "tavern",
# "terraced house",
# "townhouse",
# "yard", # END_OF_FIRST_GROUP
# "auto shop",
# "avenue",
# "beltway",
# "blacktop",
# "block",
# "boulevard",
# "bus",
# "bus station",
# "bypass",
# "byroad",
# "byway",
# "car park",
# "caravan",
# "come down the pike",
# "couch",
# "curb",
# "dead end",
# "detour",
# "dirt road",
# "dirt track",
# "divided highway",
# "driveway",
# "dual carriageway",
# "estate car",
# "expressway",
# "fender",
# "filling station",
# "fly-over",
# "footpath",
# "freeway",
# "garage",
# "gas station",
# "highroad",
# "highway",
# "hold-up",
# "interstate",
# "intersection",
# "main road",
# "main street",
# "motorway",
# "off-ramp",
# "overpass",
# "parking lot",
# "parkway",
# "pavement",
# "public highway",
# "rat run",
# "relief road",
# "right up/down someone’s alley",
# "right up/down someone’s street",
# "ring road",
# "road diversion",
# "roadhouse",
# "rotary",
# "roundabout",
# "saloon car",
# "schedule",
# "sedan",
# "service road",
# "shoulder",
# "sidewalk",
# "slip road",
# "subway",
# "superhighway",
# "the m25",
# "thruway",
# "tie-up",
# "tarmac",
# "tollway",
# "traffic circle",
# "trail",
# "trailer",
# "tram",
# "trolley",
# "trunk road",
# "turnpike",
# "underground",
# "verge", #END_OF_SECOND_SECTION
# "barman",
# "barmaid",
# "bartender",
# "cab driver",
# "cabbie",
# "caregiver",
# "caretaker",
# "carer",
"chaperon",
"hobo",
"janitor",
"porter",
"professor",
"solicitor",
]

NOT_FOUND = []


def get_total_frequency(word, attempt_counter = 1):

    if attempt_counter > 4:
        print(f"SOMETHING WENT WRONG WITH THIS WORD: {word}")
        return

    link = "https://www.english-corpora.org/coca/"
    driver.get(link)
    # driver.refresh()

    sleep(2)

    # print all of the page source that was loaded
    # print(driver.page_source.encode("utf-8"))

    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR ,'frame[name="x1"]')))

    query = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
    query.send_keys(word)


    # query = driver.find_element(By.CSS_SELECTOR, 'input[name="p"]')
    # query.send_keys(word)

    search_button = driver.find_element(By.CSS_SELECTOR, 'input#submit1')
    search_button.click()

    sleep(2)

    driver.switch_to.default_content()

    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR ,'frame[name="x2"]')))
    
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

    soup = bs(html, "html5lib")
    try:
        text = soup.select(".flexRow td:nth-child(6) font")[0].text
    except:
        get_total_frequency(word, attempt_counter + 1)
        return
        
        # NOT_FOUND.append(word)
        # # print("NOT_FOUND", word)
        # return
    
    number = text.strip().replace('\n', '')
    # first_split = text.split(' ')[0]
    # split = first_split.split('\xa0')[0]
    # number = split.replace(',', '')


    INFO[word] = number

    print(f"'{word}': '{number}',")

    # parent_class:nth-child(1)
    # driver.get()

count = 0
account_number = 1

for word in WORDS:
    if count >= 19:
        re_register(ACCOUNTS[account_number])
        account_number += 1
        count = 0

    get_total_frequency(word)
    sleep(2)

    count += 1

print(INFO)
