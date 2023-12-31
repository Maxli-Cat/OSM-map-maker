
def cartesian(points, bounds=(600,600)):
    WORLD_MIN_Y = -71.2
    WORLD_MAX_Y = -71.0
    WORLD_MIN_X = 43.1
    WORLD_MAX_X = 43.0

    DRAW_MIN_X = 0
    DRAW_MIN_Y = 0
    DRAW_MAX_Y, DRAW_MAX_X = bounds

    worldx = WORLD_MAX_X - WORLD_MIN_X
    worldy = WORLD_MAX_Y - WORLD_MIN_Y
    mapx = DRAW_MAX_X - DRAW_MIN_X
    mapy = DRAW_MAX_Y - DRAW_MIN_Y

    newpoints = []
    for point in points:
        try:
            y, x = point
        except ValueError as ex:
            #print(point)
            continue
        x = ((x - WORLD_MIN_X) / worldx) * mapx
        y = ((y - WORLD_MIN_Y) / worldy) * mapy
        newpoints.append((y,x))

    return newpoints