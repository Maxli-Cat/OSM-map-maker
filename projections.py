
def cartesian(points):
    WORLD_MIN_Y = -71.2
    WORLD_MAX_Y = -71.0
    WORLD_MIN_X = 43.1
    WORLD_MAX_X = 43.0

    DRAW_MIN_X = 0
    DRAW_MAX_X = 1200
    DRAW_MIN_Y = 0
    DRAW_MAX_Y = 1200

    worldx = WORLD_MAX_X - WORLD_MIN_X
    worldy = WORLD_MAX_Y - WORLD_MIN_Y
    mapx = DRAW_MAX_X - DRAW_MIN_X
    mapy = DRAW_MAX_Y - DRAW_MIN_Y

    print(f"{worldx=}, {worldy=}, {mapx=}, {mapy=}")

    newpoints = []
    for point in points:
        x, y = point
        x = ((x - WORLD_MIN_X) / worldx) * mapx
        y = ((y - WORLD_MIN_Y) / worldy) * mapy
        newpoints.append((y,x))

    return newpoints