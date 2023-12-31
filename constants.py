import math

SIZE = (2500*5, 1800*2)
CART_BOUNDS = (43.7, 41.4, -72.25, -69.8)
#CART_BOUNDS = (43.1, 42.9, -71, -70.6)

run = abs(CART_BOUNDS[0] - CART_BOUNDS[1]) * 111.32
rise = abs(CART_BOUNDS[2] - CART_BOUNDS[3]) * (40075 * math.cos(math.radians(CART_BOUNDS[0])) / 360)
aspect = run / rise
SIZE = (SIZE[0], int(SIZE[0] * aspect))

if __name__ == "__main__":
    print(rise, run, aspect)
    print(SIZE)