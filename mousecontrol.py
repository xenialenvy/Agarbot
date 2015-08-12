__author__ = 'DJ'
#Script to control mouse movement let's see what we can do
import pyautogui
import random
from selenium import webdriver


def start_game(browser, size):
    browser.maximize_window()
    browser.get('http://agar.io')
    browser.maximize_window()
    element = browser.find_element_by_id("nick")
    element.send_keys("Bad Bot")
    browser.find_element_by_class_name('btn-play-guest').click()


def play_game(size):
    while True:
        delta = [random.randint(-100,100),random.randint(-100,100)]
        current_position = pyautogui.position()
        proposed_x = current_position[0] + delta[0]
        proposed_y = current_position[1] + delta[1]
        if 0 <= proposed_x <= size[0] and 0 <= proposed_y <= size[1]:
            pyautogui.moveRel(delta)

def main():
    size = pyautogui.size()
    browser = webdriver.Firefox()
    start_game(browser, size)
    play_game(size)

main()