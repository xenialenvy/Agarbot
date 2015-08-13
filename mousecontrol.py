__author__ = 'DJ'
#Script to control mouse movement let's see what we can do
import pyautogui
import random
from selenium import webdriver
from matplotlib import pyplot as plt
from skimage import data, novice
from skimage.feature import blob_dog, blob_log, blob_doh
from math import (acos, sqrt, radians, cos, sin, degrees)
from numpy import concatenate, linalg
import numpy
from skimage.color import rgb2gray


def start_game(browser):
    #browser.set_window_size(270,200)
    browser.set_window_size(580,400)
    browser.get('http://agar.io')
    element = 0
    while not element:
        try:
            element = browser.find_element_by_id("nick")
            element.send_keys("Bad Bot")
            browser.find_element_by_class_name('btn-settings').click()
            box_list = browser.find_elements_by_xpath("//input[@type='checkbox']")
            i=0
            for box in box_list:
             if i != 27:
                box_list[i].click()
                i+=1
            browser.find_element_by_class_name('btn-play-guest').click()
        except:
            continue


def find_blobs(key):
    image = novice.open("/Users/DJ/Documents/Development/Agarbot/images/test_image")
    image = data.load("/Users/DJ/Documents/Development/Agarbot/images/test_image")
    image_gray = rgb2gray(image)

    if key == 'doh':
        big_blobs = blob_doh(image_gray, max_sigma=60, min_sigma=1,num_sigma=20, threshold=.01)
        #small_blobs = blob_doh(image_gray, max_sigma=20, min_sigma=1, num_sigma=10,threshold=.01)
        small_blobs = numpy.array([])
        print("found blobs!")

    if big_blobs.any() and small_blobs.any():
        blobs = concatenate((big_blobs,small_blobs),axis=0)
    elif big_blobs.any():
        blobs = big_blobs
    elif small_blobs.any():
        blobs = small_blobs
    else:
        blobs = []
    #draw(image,blobs)
    return blobs


def draw(image,blobs):
    fig, ax = plt.subplots(1, 1)
    ax.imshow(image, interpolation='nearest')
    me = find_me(blobs,(580,320))
    y, x, r = me
    c = plt.Circle((x,y),r,color='blue',linewidth=2,fill=False)
    ax.add_patch(c)
    for blob in find_food(blobs,me):
        y, x, r = blob
        c = plt.Circle((x,y),r,color='green',linewidth=2,fill=False)
        ax.add_patch(c)
    for blob in find_threats(blobs,me):
        y, x, r = blob
        c = plt.Circle((x,y),r,color='red',linewidth=2,fill=False)
        ax.add_patch(c)
    plt.show()


def find_me(blobs, size):
    min_dist = 10000000
    for blob in blobs:
        y, x, r = blob
        distance = linalg.norm(numpy.array((x, y, 0))-numpy.array((size[0]/2,size[1]/2,0)))
        if distance < min_dist:
            min_dist = distance
            maybe_me = blob
    return maybe_me


def find_threats(blobs, me):
    threats = numpy.array([])
    i=0
    indexes = []
    for blob in blobs:
        if blob[2] * blob[2] > me[2] * me[2]:
            if threats.any():
                threats = concatenate((threats, numpy.array([blob])),axis=0)
            else:
                threats = numpy.array([blob])
    return threats


def find_food(blobs, me):
    food = numpy.array([])
    for blob in blobs:
        if blob[2] * blob[2] < me[2] * me[2]:
            if food.any():
                food = concatenate((food, numpy.array([blob])), axis=0)
            else:
                food = numpy.array([blob])
    return food


def angle(a):
    b = (1,0,0)
    dot = 0
    i = 0
    for c in a:
        dot += c * b[i]
        i += 1
    cosine = dot / (sqrt((a[0] * a[0]) + (a[1] * a[1]) + (a[2] * a[2])) * sqrt((b[0] * b[0]) + (b[1] * b[1]) + (b[2] * b[2])))
    acute = acos(cosine)
    if a[1] >= 0:
        angle_from_origin = acute
    if a[1] < 0:
        angle_from_origin = radians(360) - acute
    return angle_from_origin


def vec_from_angle(vec_angle):
    mag = 100
    vec = (mag * cos(vec_angle), mag * sin(vec_angle))
    return vec


def shift(angles, center):
    shift_angle = 20
    mouse = from_mouse(pyautogui.position())
    mouse_vector = (mouse[0] - center[0], mouse[1] - center[1], 0)
    normal = (1,0,0)
    mouse_angle = angle(mouse_vector)
    print("Mouse angle now", degrees(mouse_angle), "degrees")
    for threat_angle in angles:
        if threat_angle < radians(180):
            mouse_angle -= radians(shift_angle)
        else:
            mouse_angle += radians(shift_angle)
    vec = vec_from_angle(mouse_angle)
    new_mouse = to_mouse((vec[0] + center[0], vec[1] + center[1]))
    pyautogui.moveTo(new_mouse)


def avoid(threats, size):
    threat_limit = 90
    mouse = from_mouse(pyautogui.position())
    center = (size[0]/2,size[1]/2)
    angles = []
    for threat in threats:
        y, x, r = threat
        threat_vector = (x - center[0], y - center[1], 0)
        mouse_vector = (mouse[0] - center[0], mouse[1] - center[1], 0)
        mouse_angle = angle(mouse_vector)
        threat_angle_origin = angle(threat_vector)

        if mouse_angle <= threat_angle_origin:
            threat_angle = threat_angle_origin - mouse_angle
        if mouse_angle > threat_angle_origin:
            threat_angle = mouse_angle - threat_angle_origin

        if 0 < threat_angle < radians(threat_limit) or 0 < radians(360) - threat_angle < radians(threat_limit):
            angles.append(threat_angle)
    shift(angles, center)


def play_game(browser, size):
    browser.save_screenshot("./images/test_image")
    blobs = find_blobs('doh')
    me = find_me(blobs, size)
    threats = find_threats(blobs, me)
    if threats.any():
        avoid(threats, size)
    threats = numpy.array([])


def to_mouse(point):
    x, y = point
    mouse_x = x
    mouse_y = y + 100
    return mouse_x, mouse_y


def from_mouse(point):
    mouse_x, mouse_y = point
    x = mouse_x
    y = mouse_y - 100
    return x, y


def main():
    browser = webdriver.Firefox()
    start_game(browser)
    size = (browser.get_window_size()['width'],browser.get_window_size()['height']-80)
    while True:
        play_game(browser, size)

main()