import math

DPI = 600
SIZE_INCH = (24, 36)
SIZE = (SIZE_INCH[0] * DPI, SIZE_INCH[1] * DPI)

#SIZE = (2500*5, 1800*2)
CART_BOUNDS = (45.0, 40.48, -74.35, -68.63)
#CART_BOUNDS = (43.1, 42.9, -71, -70.6)

run = abs(CART_BOUNDS[0] - CART_BOUNDS[1]) * 111.32
rise = abs(CART_BOUNDS[2] - CART_BOUNDS[3]) * (40075 * math.cos(math.radians(CART_BOUNDS[0])) / 360)
aspect = run / rise
SIZE = (SIZE[0], int(SIZE[0] * aspect))
SIZE_INCH = (SIZE[0] / DPI, SIZE[1] / DPI)

if __name__ == "__main__":
    print(rise, run, aspect)
    print(SIZE)
    print(SIZE_INCH)