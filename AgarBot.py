__author__ = 'DJ'
from tkinter import *
from tkinter import ttk
from selenium import webdriver
from matplotlib import pyplot as plt
from math import (acos, sqrt, radians, cos, sin, degrees,pi,atan,fabs,hypot)
import numpy as np
import time
import os.path
from Blob import Blob, Mouse
import cv2
home = os.path.expanduser("~")
import os
import tkinter

class App(ttk.Frame):

    @classmethod
    def main(cls):
        NoDefaultRoot()
        root = Tk()
        app = cls(root)
        app.grid(sticky=NSEW)
        root.grid_columnconfigure(0,weight=1)
        root.grid_rowconfigure(0,weight=1)
        root.resizable(True, False)
        root.title("AgarBot")
        root.mainloop()

    def __init__(self,root):
        super().__init__(root)
        width = 300
        height=300
        x = 580
        y = 0
        root.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self._root().minsize(width=width,height=height)
        self._root().maxsize(width=width,height=height)
        self.create_variables()
        self.create_widgets()
        self.grid_widgets()
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def create_variables(self):
        self.browser_box_value = StringVar(self)
        self.header_text ="Choose your desired browser and press start".strip()
        self.browser_box_values = ('Chrome', 'Firefox')
        self.browser_size = (580,320)

    def create_widgets(self):
        self.browser_box_label = ttk.Label(self, text="Select browser")
        self.browser_box = ttk.Combobox(self,width=10, textvariable=self.browser_box_value, state='readonly')
        self.browser_box['values'] = self.browser_box_values
        self.browser_box.current(1)
        self.update_idletasks()
        self.header = ttk.Label(self, text=self.header_text,wraplength=self._root().winfo_width())
        self.start_button = ttk.Button(self,text='Start',command=lambda: start_game(get_browser(self.browser_box_value.get()),self.browser_size))
        self.exit_button = ttk.Button(self,text='Exit',command=self._root().destroy)

    def grid_widgets(self):
        options = dict(padx=5,pady=5)
        self.browser_box_label.grid(column=0,row=1,**options)
        self.browser_box.grid(column=1,row=1, **options)
        self.header.grid(column=0,row=0,columnspan=2, **options)
        self.start_button.grid(column=0,row=3, **options)
        self.exit_button.grid(column=1,row=3, **options)

    def label_width(self):
        window_width = self.winfo_width()
        self.wrap_len = window_width/2
        width = self.wrap_len / 400 * 55
        return width

def get_browser(browser_str):
    if browser_str == 'Firefox':
        browser = webdriver.Firefox()
        top_bar = 80
        print(type(browser))
    elif browser_str == 'Chrome':
        browser = webdriver.Chrome()
        top_bar = 95
        print(type(browser))
    browser.set_window_size(580,320+top_bar)
    browser.set_window_position(0,0)
    return browser

def start_game(browser,size):
    if type(browser) == webdriver.Firefox:
        browser_str = "Firefox"
    if type(browser) == webdriver.Chrome:
        browser_str = "Chrome"
    mouse = Mouse(browser=browser_str)
    mouse.set_center(size[0]/2,size[1]/2)
    mouse.set_position(0,0)
    browser.get('http://agar.io')
    element = 0
    while not element:
        try:
            element = browser.find_element_by_id("nick")
            #element.send_keys("Bad Bot")
            browser.find_element_by_class_name('btn-settings').click()
            box_list = browser.find_elements_by_xpath("//input[@type='checkbox']")
            i = 0
            for box in box_list:
                if i != 3:
                    box_list[i].click()
                i += 1
            browser.find_element_by_class_name('btn-play-guest').click()
        except:
            continue
        play_game(browser,size)


def find_blobs(image,size):
    center_x = size[0]/2
    center_y = size[1]/2
    params = cv2.SimpleBlobDetector_Params()
    params.filterByCircularity = True
    params.minCircularity = 0
    params.maxCircularity = 1
    params.minDistBetweenBlobs = 5
    params.filterByArea = True
    params.minArea = 1
    params.maxArea = 500000
    params.filterByInertia = True
    params.minInertiaRatio = 0
    params.maxInertiaRatio = 1
    params.filterByConvexity = True
    params.minConvexity = 0
    params.maxConvexity = 1
    detector = cv2.SimpleBlobDetector_create(params)
    found_blobs = detector.detect(image)
    blobs = []
    for blob in found_blobs:
        blob = Blob(blob.pt[0]-20, blob.pt[1]-20, blob.size/2)
        blob.set_center(center_x, center_y)
        if not is_score(blob, size):
            blobs.append(blob)
    #image = cv2.drawKeypoints(image, found_blobs, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
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
        distance = blob.dist_from_center()
        if distance is not False and distance < min_dist and blob.radius() > 3:
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


def classify(blobs, me):
    threats = []
    food = []
    for blob in blobs:
        if blob.type() != "me":
            if blob.area() > me.area():
                threats.append(blob)
                blob.set_type('threat')
            elif blob.area() < me.area() / 2:
                food.append(blob)
                blob.set_type("food")
    return threats, food


def vec_from_angle(vec_angle):
    mag = 100
    vec = (mag * cos(vec_angle), mag * sin(vec_angle))
    return vec


def threat_function(dist,size):
    center_x,center_y = size
    max_d = hypot(center_x,center_y)
    f = 1 - dist/max_d
    return f


def get_image(browser):
        border = 20
        if not os.path.exists(home + "/AgarBot"):
            os.mkdir(home + "/AgarBot")
        if not os.path.isdir(home + "/AgarBot/images"):
            os.mkdir(home + "/AgarBot/images")
        browser.save_screenshot(home + "/AgarBot/images/image.png")
        image = cv2.bitwise_not(cv2.imread(home + "/AgarBot/images/image.png", cv2.IMREAD_GRAYSCALE))
        image = cv2.copyMakeBorder(image, border, border, border, border, borderType=cv2.BORDER_CONSTANT,
                                   value=(512, 521, 3))
        return image


def play_game(browser, size):
    i = 0
    while True:
        mouse = Mouse()
        mouse.set_center(size[0]/2, size[1]/2)
        angle = None
        safe = True
        image = get_image(browser)
        #cv2.imwrite(home + "/AgarBot/images/image"+str(i)+".png",image)
        blobs = find_blobs(image,size)
        if not blobs:
            continue
        me = find_me(blobs,size)
        remove_name(blobs,me)
        threats, food = classify(blobs,me)
        #if menu(image):
            #print("menu")
        if threats:
            angle = avoid(threats,size)
            safe = False
        wall_list = walls(blobs, me)
        angle = avoid_walls(wall_list, angle)
        angle = eat(food, size, angle, safe)
        if angle:
            mouse.set_angle(angle)
        i+=1
        #draw(image,blobs)


def eat(food, size, angle,safe):
    d_min = 10000
    d_theta = 5
    if angle is not None:
        if safe:
            d_theta = radians(25)
        if not safe:
            d_theta = radians(10)
        for blob in food:
            if fabs(blob.angle_from_center() - angle) <= d_theta:
                if blob.dist_from_center() < d_min:
                    d_min = blob.dist_from_center()
                    angle = blob.angle_from_center()

    else:
        for blob in food:
            if blob.dist_from_center() < d_min:
                d_min = blob.dist_from_center()
                angle = blob.angle_from_center()
    return angle


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
    v_final = [0, 0]
    for blob in threats:
        v = blob.coord_from_center()
        v_mag = blob.dist_from_center()
        m = threat_function(v_mag,size)
        v_unit = [v[0]/v_mag,v[1]/v_mag]
        v_final[0] -= (v_unit[0] * m)
        v_final[1] -= (v_unit[1] * m)
    x = v_final[0]
    y = v_final[1]
    angle = arc_tan(x, y)
    return angle


def avoid_walls(wall_list, angle):
    if wall_list:
        directions = {'left': [1, 0], 'right': [-1, 0], 'down': [0, -1], 'up': [0,1]}
        if angle is not None:
            vec = [cos(angle), sin(angle)]
        else:
            vec = [0, 0]
        for wall in wall_list:
            print(wall)
            vec[0] += directions[wall][0]
            vec[1] += directions[wall][1]
        return arc_tan(vec[0], vec[1])
    else:
        return angle


def walls(blobs, me):
    wall_list = []
    if not blobs_left(blobs, me):
        wall_list.append("left")
    if not blobs_right(blobs, me):
        wall_list.append("right")
    if not blobs_up(blobs, me):
        wall_list.append("up")
    if not blobs_down(blobs,me):
        wall_list.append("down")
    return wall_list


def blobs_left(blobs, me):
    for blob in blobs:
        if blob.type() == "me":
            continue
        if blob.coord_from_center()[0] < 0 and fabs(blob.coord_from_center()[0]) >= me.radius() + 50:
            return True
    return False


def blobs_right(blobs, me):
    for blob in blobs:
        if blob.coord_from_center()[0] >= me.radius() + 50:
            return True
    return False


def blobs_up(blobs, me):
    for blob in blobs:
        if blob.coord_from_center()[1] < 0 and fabs(blob.coord_from_center()[1]) >= me.radius() + 50:
            return True
    return False


def blobs_down(blobs, me):
    for blob in blobs:
        if blob.coord_from_center()[1] >= me.radius() + 50:
            return True
    return False


def is_score(blob, size):
    x, y = blob.coord()
    if .9 * size[1] <= y <= size[1] and 0 <= x <= .22 * size[0]:
        return True
    else:
        return False

def remove_name(blobs,me):
    i = 0
    for blob in blobs:
        if blob.dist_from_center() < me.radius() and blob.type() != 'me':
            blobs.pop(i)
        i+=1


def menu(image):
    menu_classifier = cv2.CascadeClassifier('./Classifiers/MenuClassifier.xml')
    menu_found = menu_classifier.detectMultiScale(image)
    x,y,w,h = None,None,0,0
    for menu_item in menu_found:
        if menu_item.any():
            print(menu_found)
            (x,y,w,h) = menu_found[0]
        if w > 400 and h > 200:
            return True
    return False

if __name__ == '__main__':
    App.main()