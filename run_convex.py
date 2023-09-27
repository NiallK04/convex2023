#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Void

f = Void()

print("¬ведите три точки треугольника:")
triangle = Polygon(R2Point(), R2Point(), R2Point())

try:
    while True:
        f = f.add(R2Point())
        print(
            f"S = {f.area()}, P = {f.perimeter()}, Partial perimeter P = {f.partial_perimeter(triangle)}\n")
        print()
except(EOFError, KeyboardInterrupt):
    print("\nStop")
