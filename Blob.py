__author__ = 'DJ'
from math import pi
from pyautogui import moveTo,position
from math import cos, sin, atan, sqrt, hypot

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


class Blob:
    def __init__(self, x=0, y=0, r=0, blob_type='unclassified'):
        self.__x = x
        self.__y = y
        self.__radius = r
        self.__type = blob_type
        self.__center = False

    def coord(self):
        return self.__x, self.__y

    def set_center(self, center_x,center_y):
        self.__center = (center_x, center_y)

    def coord_from_center(self):
        if self.__center is not False:
            return self.__x - self.__center[0], self.__y - self.__center[1]
        else:
            return False

    def angle_from_center(self):
        if self.__center is not False:
            x, y = self.coord_from_center()
            a = arc_tan(x, y)
            return a

    def dist_from_center(self):
        if self.__center:
            x, y = self.coord_from_center()
            return hypot(x, y)

    def radius(self):
        return self.__radius

    def area(self):
        return pi * self.__radius * self.__radius

    def set_type(self, blob_type):
        self.__type = blob_type

    def type(self):
        return self.__type

    def unit_from_center(self):
        if self.__center:
            d = self.dist_from_center()
            v = self.coord_from_center()
            return v[0]/d, v[1]/d

    def angle_from_center(self):
        if self.__center is not False:
            x, y = self.unit_from_center()
            return arc_tan(x,y)

    def __str__(self):
        return "Point:(" + str(round(self.__x, 2)) + "," + str(round(self.__y, 2)) + ")\nRadius: " + str(round(self.__radius, 2))

    def __repr__(self):
        return "Point:(" + str(round(self.__x, 2)) + "," + str(round(self.__y, 2)) + ")\nRadius: " + str(round(self.__radius, 2))


class Mouse:
    def __init__(self,mag=100, browser='firefox'):
        top_bar = {'firefox':100}
        self.__x, self.__y = position()
        self.__top_bar = top_bar[browser]
        self.__y -= top_bar[browser]
        self.__center = False
        self.__mag = mag

    def set_center(self, center_x, center_y):
        if type(center_x) in [int, float] and type(center_y) in [int, float]:
            self.__center = (center_x, center_y)

    def coord_from_center(self):
        if self.__center is not False:
            return self.__x - self.__center[0], self.__y - self.__center[1]
        else:
            return False

    def set_angle(self, angle):
        mag = self.__mag
        vec = (mag * cos(angle), mag * sin(angle))
        vec = (vec[0]+self.__center[0], vec[1] + self.__center[1])
        moveTo(vec[0], self.__top_bar+vec[1])

    def set_position(self, x, y):
        mag = self.__mag
        current_mag = hypot(x,y)
        if current_mag:
            vec = (x/current_mag, y/current_mag)
        else:
            vec = (0,0)
        vec = ((mag * vec[0])+self.__center[0], (mag * vec[1]) + self.__center[1])
        moveTo(vec[0], vec[1] + self.__top_bar)
