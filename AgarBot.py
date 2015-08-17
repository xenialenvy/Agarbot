__author__ = 'DJ'
#Script to control mouse movement let's see what we can do
from selenium import webdriver
#from matplotlib import pyplot as plt
from math import (acos, sqrt, radians, cos, sin, degrees,pi,atan)
import numpy as np
import time
import os.path
from os import mkdir
from Blob import Blob, Mouse
import cv2
home = os.path.expanduser("~")

def start_game(browser,size):
    browser.set_window_size(size[0],size[1])
    mouse = Mouse()
    mouse.set_center(size[0]/2,size[1]/2-40)
    mouse.set_angle(0)
    browser.get('http://agar.io')
    element = 0
    while not element:
        try:
            element = browser.find_element_by_id("nick")
            element.send_keys("Bad Bot")
            browser.find_element_by_class_name('btn-settings').click()
            box_list = browser.find_elements_by_xpath("//input[@type='checkbox']")
            i = 0
            for box in box_list:
                if i != 27:
                    box_list[i].click()
                i += 1
            browser.find_element_by_class_name('btn-play-guest').click()
        except:
            continue


def find_blobs(image):
    params = cv2.SimpleBlobDetector_Params()
    params.filterByCircularity = True
    params.minCircularity = 0
    params.maxCircularity = 1
    params.minDistBetweenBlobs = 5
    params.filterByArea = True
    params.minArea = 1
    params.maxArea = 50000
    params.filterByInertia = True
    params.minInertiaRatio = 0
    params.maxInertiaRatio = 1
    detector = cv2.SimpleBlobDetector_create(params)
    found_blobs = detector.detect(image)
    blobs = []
    for blob in found_blobs:
        blob = Blob(blob.pt[0]-20, blob.pt[1]-20, blob.size/2)
        blobs.append(blob)
    image = cv2.drawKeypoints(image, found_blobs, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    #cv2.imshow("Keypoints", image)
    #cv2.waitKey(0)
    return blobs


def draw(image, blobs):
    fig, ax = plt.subplots(1, 1)
    ax.imshow(image, cmap='Greys', interpolation='nearest')
    colors = {'unclassified': 'orange', 'threat': 'red', 'food': 'green', 'me': 'blue'}
    for blob in blobs:
        x, y = blob.coord()
        r = blob.radius()
        color = colors[blob.type()]
        c = plt.Circle((x+20, y+20), r, color=color, linewidth=2, fill=False)
        ax.add_patch(c)
    plt.show()


def find_me(blobs, size):
    min_dist = 1000
    for blob in blobs:
        blob.set_center(size[0]/2,size[1]/2)
        distance = blob.dist_from_center()
        if distance is not False and distance < min_dist:
            min_dist = distance
            maybe_me = blob
    maybe_me.set_type("me")
    return maybe_me


def find_biggest_threat(blobs):
    biggest_blob = Blob()
    for blob in blobs:
        if blob[2] > biggest_blob[2]:
            biggest_blob = blob
    return biggest_blob


def is_me(blob):
    center_radius = 10


def classify(blobs, me):
    threats = []
    food = []
    for blob in blobs:
        if blob.type() != "me":
            if blob.area() > me.area():
                threats.append(blob)
                blob.set_type('threat')
                #print('threat at ',degrees(blob.angle_from_center()),"degrees")
            elif blob.area() < me.area() / 2:
                food.append(blob)
                blob.set_type("food")
    return threats, food


# def find_threats(blobs, me):
#     threats = []
#     for blob in blobs:
#         if blob.area() > me.area():
#                 threats.append(blob)
#                 blob.set_type('threat')
#     return threats
#
#
# def find_food(blobs, me):
#     food = []
#     for blob in blobs:
#         if blob.area() < me.area() / 2:
#             food.append(blob)
#             blob.set_type("food")
#     return food


# def angle(a):
#     b = (1,0,0)
#     dot = 0
#     i = 0
#     for c in a:
#         dot += c * b[i]
#         i += 1
#     cosine = dot / (sqrt((a[0] * a[0]) + (a[1] * a[1]) + (a[2] * a[2])) * sqrt((b[0] * b[0]) + (b[1] * b[1]) + (b[2] * b[2])))
#     acute = acos(cosine)
#     if a[1] >= 0:
#         angle_from_origin = acute
#     if a[1] < 0:
#         angle_from_origin = radians(360) - acute
#     return angle_from_origin


def vec_from_angle(vec_angle):
    mag = 100
    vec = (mag * cos(vec_angle), mag * sin(vec_angle))
    return vec


def threat_function(dist):
    return 1


# def avoid(threats, size):
#     mouse = Mouse()
#     mouse.set_center(size[0]/2, size[1]/2)
#     vec = [0, 0]
#     for threat in threats:
#         threat.set_center(size[0]/2, size[1]/2)
#         threat_angle = threat.angle_from_center()
#         print("Threat at", degrees(threat_angle),"degrees")
#         threat_distance = threat.dist_from_center()
#         multiplier = threat_function(threat_distance)
#         vec[0] += multiplier * cos(threat_angle + pi)
#         vec[1] += multiplier * sin(threat_angle + pi)
#     #print("setting position to", (vec[0],vec[1]))
#     mouse.set_position(vec[0], vec[1])





# def shift(angles, center):
#     shift_angle = radians(5)
#     threat_limit = radians(30)
#     mouse = from_mouse(pyautogui.position())
#     mouse_vector = (mouse[0] - center[0], mouse[1] - center[1], 0)
#     mouse_angle = angle(mouse_vector)
#     #print("Mouse angle now", degrees(mouse_angle), "degrees")
#     added = False
#     while True:
#         #print("mouse angle changed",mouse_angle)
#         if mouse_angle >= radians(180):
#             mouse_angle -= radians(180)
#         for threat_angle in angles:
#             if mouse_angle - threat_limit >= 0 and mouse_angle + threat_limit <= radians(360):
#                 if mouse_angle - threat_limit <= threat_angle < mouse_angle + threat_limit:
#                     mouse_angle += shift_angle
#                     continue
#             elif mouse_angle - threat_limit < 0:
#                 if radians(180) + mouse_angle - threat_limit <= threat_angle <= radians(180) or 0 <= threat_angle <= mouse_angle + threat_limit:
#                     mouse_angle += shift_angle
#                     continue
#             elif mouse_angle + threat_limit >= radians(180):
#                 if mouse_angle - threat_limit <= threat_angle <= radians(180) or 0 <= threat_angle <= mouse_angle + threat_limit - radians(180):
#                     mouse_angle += shift_angle
#                     continue
#         break
#     vec = vec_from_angle(mouse_angle)
#     new_mouse = to_mouse((vec[0] + center[0], vec[1] + center[1]))
#     pyautogui.moveTo(new_mouse)


# def shift(angles, center):
#     shift_angle = 20
#     mouse = from_mouse(pyautogui.position())
#     mouse_vector = (mouse[0] - center[0], mouse[1] - center[1], 0)
#     normal = (1,0,0)
#     mouse_angle = angle(mouse_vector)
#     print("Mouse angle now", degrees(mouse_angle), "degrees")
#     for threat_angle in angles:
#         if threat_angle < radians(180):
#             mouse_angle -= radians(shift_angle)
#         else:
#             mouse_angle += radians(shift_angle)
#     vec = vec_from_angle(mouse_angle)
#     new_mouse = to_mouse((vec[0] + center[0], vec[1] + center[1]))
#     pyautogui.moveTo(new_mouse)


# def avoid(threats, size):
#     threat_limit = 90
#     mouse = from_mouse(pyautogui.position())
#     center = (size[0]/2,size[1]/2)
#     angles = []
#     for threat in threats:
#         y, x, r = threat
#         threat_vector = (x - center[0], y - center[1], 0)
#         mouse_vector = (mouse[0] - center[0], mouse[1] - center[1], 0)
#         mouse_angle = angle(mouse_vector)
#         threat_angle_origin = angle(threat_vector)
#
#         if mouse_angle <= threat_angle_origin:
#             threat_angle = threat_angle_origin - mouse_angle
#         if mouse_angle > threat_angle_origin:
#             threat_angle = mouse_angle - threat_angle_origin
#
#         if 0 < threat_angle < radians(threat_limit) or 0 < radians(360) - threat_angle < radians(threat_limit):
#             angles.append(threat_angle)
#     shift(angles, center)


def play_game(browser, size):
    timeout = time.time() + 60
    border = 20
    c = 0
    if not os.path.exists(home + "/AgarBot"):
        os.mkdir(home + "/AgarBot")
    if not os.path.isdir(home + "/AgarBot/images"):
        os.mkdir(home + "/AgarBot/images")
    browser.save_screenshot(home + "/AgarBot/images/image.png")
    image = cv2.bitwise_not(cv2.imread(home + "/AgarBot/images/image.png", cv2.IMREAD_GRAYSCALE))
    image = cv2.copyMakeBorder(image,border,border,border,border,borderType=cv2.BORDER_CONSTANT,value=(512,521,3))
    c += 1
    blobs = find_blobs(image)
    me = find_me(blobs,size)
    threats, food = classify(blobs,me)
    if threats:
        avoid(threats,size)
    else:
        eat(food,size)
    #draw(image,blobs)
    # me = find_me(blobs, size)
    # threats = find_threats(blobs, me)
    #food = find_food(blobs,me)
    # if threats
    #     avoid(threats, size)
    # threats = np.array([])


def eat(food,size):
    mouse = Mouse()
    center_x = size[0]/2
    center_y = size[1]/2
    mouse.set_center(center_x,center_y)
    d_min = 10000
    v_final = [0,0]
    for blob in food:
        blob.set_center(center_x,center_y)
        if blob.dist_from_center() < d_min:
            d_min = blob.dist_from_center()
            v = blob.coord_from_center()
            v_final = [v[0]/d_min,v[1]/d_min]
    x = v_final[0]
    y = v_final[1]
    angle = arc_tan(x,y)
    mouse.set_angle(angle)
    # coord = vec_from_angle(angle)
    # coord = [coord[0]+center_x,coord[1]+center_y]
    # coord = to_mouse(coord)
    # pyautogui.moveTo(coord)


def arc_tan(x, y):
    if x>0 and y>=0:
        a=atan(y/x)
    elif x>0 and y<0:
        a = 2*pi + atan(y/x)
    elif x<0 and y<=0:
        a = pi + atan(y/x)
    elif x<0 and y>0:
        a = pi + atan(y/x)
    elif x==0 and y>0:
        a = pi/2
    elif x==0 and y<0:
        a = 3*pi/2
    else:
        a = 0
    return a


def avoid(threats, size):
    mouse = Mouse()
    center_x = size[0]/2
    center_y = size[1]/2
    mouse.set_center(center_x,center_y)
    v_final = [0,0]
    for blob in threats:
        blob.set_center(center_x,center_y)
        v = blob.coord_from_center()
        v_mag = blob.dist_from_center()
        v_unit = [v[0]/v_mag,v[1]/v_mag]
        v_final[0]-=v_unit[0]
        v_final[1]-=v_unit[1]
    x=v_final[0]
    y=v_final[1]
    angle = arc_tan(x, y)
    mouse.set_angle(angle)
    # coord = vec_from_angle(angle)
    # coord = [coord[0]+center_x,coord[1]+center_y]
    # coord = to_mouse(coord)
    # pyautogui.moveTo(coord)





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
    size = (580,400)
    start_game(browser,size)
    size = (browser.get_window_size()['width'],browser.get_window_size()['height']-80)
    while True:
        play_game(browser, size)

main()