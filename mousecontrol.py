__author__ = 'DJ'
#Script to control mouse movement let's see what we can do
import pyautogui
import random
from selenium import webdriver
from matplotlib import pyplot as plt
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from math import sqrt
from numpy import concatenate, linalg
import numpy
from skimage.color import rgb2gray


def start_game(browser, size):
    browser.maximize_window()
    print(browser.get_window_size())
    browser.get('http://agar.io')
    browser.maximize_window()
    element = browser.find_element_by_id("nick")
    element.send_keys("Bad Bot")
    browser.find_element_by_class_name('btn-settings').click()
    box_list = browser.find_elements_by_xpath("//input[@type='checkbox']")
    i=0
    for box in box_list:
        if i != 27:
            box_list[i].click()
        i+=1
    print(box_list)
    browser.find_element_by_class_name('btn-play-guest').click()


def find_blobs(key):
    image = data.load("/Users/DJ/Documents/Development/Agarbot/images/test_image")
    image_gray = rgb2gray(image)

    if key == 'doh':
        big_blobs = blob_doh(image_gray, max_sigma=200, min_sigma=50,num_sigma=10, threshold=.05)
        small_blobs = blob_doh(image_gray, max_sigma=20, min_sigma=1, num_sigma=10,threshold=.01)
        print("found blobs!")
        print(big_blobs)
        print(small_blobs)

    if big_blobs.any() and small_blobs.any():
        blobs = concatenate((big_blobs,small_blobs),axis=0)
    elif big_blobs.any():
        blobs = big_blobs
    elif small_blobs.any():
        blobs = small_blobs
    else:
        blobs = []
    draw(image,blobs)
    return(blobs)

def draw(image,blobs):
    color = 'lime'
    fig, ax = plt.subplots(1, 1)
    ax.imshow(image, interpolation='nearest')
    for blob in blobs:
        y, x, r = blob
        c = plt.Circle((x, y), r, color=color, linewidth=2, fill=False)
        ax.add_patch(c)
    y,x,r = find_me(blobs,(820,1440))
    c = plt.Circle((x,y),r,color='blue',linewidth=2,fill=False)
    ax.add_patch(c)
    plt.show()

def find_me(blobs, size):
    min_dist = 10000000
    for blob in blobs:
        x, y, r = blob
        distance = linalg.norm(numpy.array((x,y,0))-numpy.array((size[0]/2,size[1]/2,0)))
        if distance < min_dist:
            min_dist = distance - r
            maybe_me = blob
        print(distance)
    return maybe_me

def main():
    size = pyautogui.size()
    browser = webdriver.Firefox()
    start_game(browser, size)
    browser.save_screenshot("./images/test_image")
    blobs = find_blobs('doh')
    me = find_me(blobs,size)
    print(me)

main()