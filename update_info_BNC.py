#!/usr/bin/python3

from bs4 import BeautifulSoup as bs
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

import datetime

driver = webdriver.Firefox()

INFO = dict()

def set_viewport_size(driver, width, height):
    window_size = driver.execute_script("""
        return [window.outerWidth - window.innerWidth + arguments[0],
          window.outerHeight - window.innerHeight + arguments[1]];
        """, width, height)
    driver.set_window_size(*window_size)

# set_viewport_size(driver, 800, 600)


url = "https://auth.sketchengine.eu/#login"
PASSWORD = ""
USERNAME = ""

driver.get(url)


sleep(5)

# locate email form by_name
username = driver.find_element(By.CSS_SELECTOR, ".loginColumns  .leftColumn .input-field  #r_0")

username.send_keys(f"{USERNAME}")

# locate password form by_name
password = driver.find_element(By.CSS_SELECTOR, ".loginColumns .leftColumn .input-field #r_1")

password.send_keys(f"{PASSWORD}")


log_in_button = driver.find_element(By.ID, "btnLogin")

# locate submit button by_xpath
#log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')

# .click() to mimic button click
log_in_button.click()

sleep(2)

# WORDS = [
# "barman",
# "barmaid",
# "bartender",
# "cab driver",
# "cabbie",
# "caregiver",
# "caretaker",
# "carer",
# "chaperon",
# "hobo",
# "janitor",
# "porter",
# "professor",
# "solicitor",
# ]


NOT_FOUND = []


def get_total_frequency(word):

    if ' ' in word:
        word_split = word.split(' ')
        word1 = word_split[0]
        word2 = word_split[-1]
        link = f"https://app.sketchengine.eu/#wordlist?corpname=preloaded%2Fbnc2_tt31&tab=advanced&wlattr=lc&wlminfreq=0&criteria=%5B%7B%22filter%22%3A%22startingWith%22%2C%22value%22%3A%22{word1}%22%7D%2C%7B%22filter%22%3A%22endingWith%22%2C%22value%22%3A%22{word2}%22%7D%5D&include_nonwords=1&itemsPerPage=50&showresults=1&cols=%5B%22frq%22%5D&showtimelines=1&diaattr=bncdoc.year&showtimelineabs=0&timelinesthreshold=5"

    else:
        link = f"https://app.sketchengine.eu/#wordlist?corpname=preloaded%2Fbnc2_tt31&tab=advanced&keyword=%5E{word}(s*)%24&filter=matchingRegex&wlattr=lc&include_nonwords=1&itemsPerPage=50&showresults=1&cols=%5B%22frq%22%5D&showtimelines=1&diaattr=bncdoc.year&showtimelineabs=0&timelinesthreshold=5"
    # link_word = f"https://app.sketchengine.eu/#wordlist?corpname=preloaded%2Fbnc2_tt31&tab=advanced&keyword={word}&filter=containing&wlattr=lc&include_nonwords=1&itemsPerPage=50&showresults=1&cols=%5B%22frq%22%5D&showtimelines=1&diaattr=bncdoc.year&showtimelineabs=0&timelinesthreshold=5"


    driver.get(link)

    sleep(2)
    
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")

    soup = bs(html, "html5lib")
    try:
        text = soup.select(".totalItems span:nth-child(3)")[0].text
    except:
        NOT_FOUND.append(word)
        # print("NOT_FOUND", word)
        return

    first_split = text.split(' ')[0]
    split = first_split.split('\xa0')[0]
    number = split.replace(',', '')


    INFO[word] = number

    print(f"'{word}': {number}")

    # parent_class:nth-child(1)
    # driver.get()


for word in WORDS:
    get_total_frequency(word)
    sleep(2)

print(INFO)
print(NOT_FOUND)

