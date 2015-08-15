__author__ = 'DJ'
from math import pi


class Blob:
    def __init__(self, x=0, y=0, r=0, blob_type='unclassified'):
        self._x = x
        self._y = y
        self._radius = r
        self._type = blob_type

    def coords(self):
        return self._x,self._y

    def radius(self):
        return self._radius

    def area(self):
        return pi * self._radius * self._radius

    def set_type(self, blob_type):
        self._type = blob_type

    def type(self):
        return self._type

    def __str__(self):
        return "Point:(" + str(round(self._x, 2)) + "," + str(round(self._y, 2)) + ")\nRadius: " + str(round(self._radius, 2))

    def __repr__(self):
        return "Point:(" + str(round(self._x, 2)) + "," + str(round(self._y, 2)) + ")\nRadius: " + str(round(self._radius, 2))
