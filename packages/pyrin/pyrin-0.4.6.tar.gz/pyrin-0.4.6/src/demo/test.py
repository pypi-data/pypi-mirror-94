import time

from pyrin.caching.decorators import cached_property, cached_class_property


class Car:
    @cached_property
    def fuel(self):
        return time.time() * 10

    @cached_class_property
    def speed(cls):
        return time.time() * 100


class Plane:
    @cached_property
    def fuel(self):
        return time.time() * 10

    @cached_class_property
    def speed(cls):
        return time.time() * 100


bmw = Car()
f1 = bmw.fuel
s1 = bmw.speed

f2 = bmw.fuel
s2 = bmw.speed


boeing = Plane()
f11 = boeing.fuel
s11 = boeing.speed

f22 = boeing.fuel
s22 = boeing.speed

v = 4