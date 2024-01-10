import itertools
import time
import draw
import maps
import projections

from constants import SIZE

road_types = (
    '"highway"="motorway"',
    '"highway"="motorway_link"',
    '"highway"="trunk"',
    '"highway"="trunk_link"',
    '"highway"="primary"',
    '"highway"="secondary"',
    '"highway"="tertiary"',
    '"highway"="unclassified"',
    '"highway"="residential"',
   # '"highway"="service"',
    '"highway"="path"',
    ['"highway"="footway"','"footway"!="sidewalk"','"footway"!="crossing"', '"footway"!="traffic_island"','"footway"!="link"'],
    '"highway"="track"',
    '"natural"="coastline"',
    '"railway"="rail"',
    '"route"="ferry"',
    '"highway"="cycleway"',
)

road_sizes = (
    5, #motorway
    4, #link
    4, #trunk
    3, #trunk_link
    3, #primary
    2, #secondary
    1, #tertiary
    1, #unclassified
    1, #residential
   # 1, #service
    1, #path
    1, #footway
    1, #track
    5, #coastline
    1, #railway
    1, #ferry
    1, #cycleway
)
road_colors = (
    (50,0,0),      #motorway
    (50,0,0),      #motorway link
    (0,0,0),       #trunk
    (0,0,0),       #trunk_link
    (0,0,0),       #primary
    (0,0,0),       #secondary
    (0,0,0),       #tertiary
    (50,50,50),    #unclassified
    (75,75,75),    #residential
   # (125,125,125), #service
    (0,87,0),     #path
    (0,87,0),     #footway
    (63,87,0),   #track
    (0,0,0),    #coastline
    (50,0,0),     #railway
    (0, 255, 255),  # ferry
    (0,175,0),   #bike
)
road_colors_b = (
    (200,200,200),      #motorway
    (200,200,200),      #motorway link
    (205,205,205),       #trunk
    (205,205,205),       #trunk_link
    (205,205,205),       #primary
    (210,210,210),       #secondary
    (210,210,210),       #tertiary
    (215,215,215),    #unclassified
   # (215,215,215),    #residential
    (225,225,225), #service
    (0,87,0),     #path
    (0,87,0),     #footway
    (159,171,127),   #track
    (0,0,0),    #coastline
    (250,200,200),     #railway
    (0, 255, 255),  # ferry
    (0,175,0),   #bike
)

container_types = (
    '"place"="island"',
    '"place"="islet"',
    '"natural"="water"',
)

container_sizes = (
    1, #island
    1, #islet
    1, #water
)

container_edge = (
    ((255,255,255), (255,255,255)), #island
    ((255,255,255), (255,255,255)), #islet
    ((225,240,255), (225,240,255)) #water
)

route_types = (
    '"route"="subway"',
    '"route"="light_rail"',
    '"route"="train"',
    '"route"="bus"',
    '"route"="ferry"',
    '"route"="bicycle"',
)

route_sizes = (
    3, #subway
    3, #light rail
    4, #train
    3, #bus
    2, #ferry
    2, #bike
)

route_colors = (
    (255,0,255), #subway
    (127,0,255), #light rail
    (255,0,0),   #train
    (0,0,255),   #bus
    (0,255,255), #ferry
    (0,175,0),   #bike
)

stop_types = (
    ['"railway"="station"','"train"="yes"', '"station"!="light_rail"','!"subway"'],
    ['"railway"="station"','"subway"="yes"'],
    ['"railway"="station"','"train"="yes"', '"station"="light_rail"'],
    '"highway"="bus_stop"',
    '"amenity"="ferry_terminal"',
)

stop_sizes = (
    10, #train
    7, #subway
    7, #light rail
    5, #bus
    7, #ferry
)

stop_colors = (
    (255, 0, 0),  # train
    (255, 0, 255),  # subway
    (127, 0, 255),  # light rail
    (0, 0, 255),  # bus
    (0, 255, 255),  # ferry
)

def build_lists(locations, features, colors=((0,0,0),), widths=(1,)):
    roads = []
    for location in locations:
        for feature, color, width in zip(features, itertools.cycle(colors), itertools.cycle(widths)):
            roads.append({"points":maps.cached_load_roads(area=location, element=feature), "width":width, "color":color})
    return roads

def build_list_nodes(locations, features, colors=((0, 0, 0),), sizes=(10,)):
    nodes = []
    for location in locations:
        for feature, color, size in zip(features, itertools.cycle(colors), itertools.cycle(sizes)):
            #print(f"{feature=}, {type(feature)}")
            nodes.append({"points": maps.load_nodes(area=location, element=feature), "size": size, "color": color})
    return nodes

def build_lists_relations(locations, features, colors=((0, 0, 0),), widths=(1,)):
    lines = []
    for location in locations:
        for feature, color, width in zip(features, itertools.cycle(colors), itertools.cycle(widths)):
            lines.append({"points":maps.double_cached_load_relations(area=location, element=feature), "width":width, "color":color})
    return lines

def build_lists_waters(locations):
    for location in locations:
        for water in maps.cached_get_water_relations(location):
            yield water


states  = ("New Hampshire", "Maine", "Massachusetts", "Vermont", "Rhode Island")
counties = ("Sullivan County, NH", "Rockingham, NH", "Strafford, NH","Hillsborough County, NH",  "Carroll County, NH", "Belknap County, NH", "Merrimack County, NH", "Grafton County, NH", "Coos County, NH", "Cheshire County, NH",
            "Maine", "Rhode Island",
            "Essex County, VT", "Caledonia County, VT", "Orange County, VT", "Windsor County, VT", "Windham County, VT", "Bennington County, VT", "Rutland County, VT", "Addison County, VT", "Washington County, VT", "Chittenden County, VT", "Lamoille County, VT", "Orleans County, VT", "Franklin County, VT",
            "Essex County, MA", "Middlesex County, MA", "Norfolk County, MA", "Plymouth County, MA", "Worcester County, MA", "Barnstable County, MA", "Nantucket County, MA", "Suffolk County, MA", "Bristol County, MA", "Hampden County,MA", "Hampshire County, MA", "Franklin County, MA", "Berkshire County, MA",
            "Windham County, CT", "New London County, CT", "Middlesex County, CT", "Tolland County, CT", #"Hartford County, CT", "New Haven County, CT", "Litchfield County, CT"
            #"Suffolk County, NY",
            )# "Massachusetts", "Connecticut")
nh_counties = ("Belknap County, NH", "Carroll County, NH", "Cheshire County, NH", "Coos County, NH", "Hillsborough County, NH","Merrimack County, NH", "Rockingham County, NH","Strafford County, NH", "Sullivan County, NH", "Grafton County, NH")


if __name__ == '__main__':
    start = time.time()
    img, drw = draw.setup(*SIZE)

    for i in range(1000):
        try:
            roads = build_lists(counties, road_types, widths=road_sizes, colors=road_colors_b)
            break
        except:
            time.sleep(i)
            print(f"Error, {i} times")
            continue

    state_lines = build_lists_relations(("New England",), ('"border_type"="state"',), widths=(5,))

    routes = build_lists_relations(counties,
                                   route_types, widths=route_sizes, colors=route_colors)
    stations = build_list_nodes(counties,
                                stop_types, colors=stop_colors, sizes=stop_sizes)

    waters = build_lists(counties, container_types, widths=container_sizes, colors=container_edge)
    #waters2 = build_lists_relations(counties, ('"natural"="water"',), colors=(((225,240,255), (225,240,255)),), outer_only=True)
    waters2 = build_lists_waters(counties)
    time.sleep(1)
    draw.drawCollectionWater(waters2, drw, projection=projections.cartesian, projection_args=[SIZE])
    maps.public_save_cache()
    draw.drawCollectionPoly(waters, drw, projection=projections.cartesian, projection_args=[SIZE])
    draw.drawCollectionLines(roads , drw, projection=projections.cartesian, projection_args=[SIZE])
    draw.drawCollectionLines(routes , drw, projection=projections.cartesian, projection_args=[SIZE])
    #draw.drawCollectionLines(state_lines , drw, projection=projections.cartesian, projection_args=[SIZE])
    draw.drawCollectionPoints(stations[::-1], drw, projection=projections.cartesian, projection_args=[SIZE])
    img.show()
    img.save("map.png")
    stop = time.time()
    print(f"Took {stop - start} seconds")