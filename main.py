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
    '"highway"="primary"',
    '"highway"="secondary"',
    '"highway"="tertiary"',
    '"highway"="unclassified"',
    '"highway"="residential"',
    '"highway"="service"',
    '"highway"="path"',
    '"highway"="footway"',
    '"highway"="track"',
    '"natural"="coastline"',
    '"railway"="rail"',
    '"route"="ferry"',
)

road_sizes = (
    5, #motorway
    4, #link
    4, #trunk
    3, #primary
    2, #secondary
    1, #tertiary
    1, #unclassified
    1, #residential
    1, #service
    1, #path
    1, #footway
    1, #track
    5, #coastline
    1, #railway
    1, #ferry
)
road_colors = (
    (50,0,0),      #motorway
    (50,0,0),      #motorway link
    (0,0,0),       #trunk
    (0,0,0),       #primary
    (0,0,0),       #secondary
    (0,0,0),       #tertiary
    (50,50,50),    #unclassified
    (75,75,75),    #residential
    (125,125,125), #service
    (0,87,0),     #path
    (0,87,0),     #footway
    (63,87,0),   #track
    (0,0,0),    #coastline
    (50,0,0),     #railway
    (0, 255, 255),  # ferry
)
road_colors_b = (
    (200,200,200),      #motorway
    (200,200,200),      #motorway link
    (205,205,205),       #trunk
    (205,205,205),       #primary
    (210,210,210),       #secondary
    (210,210,210),       #tertiary
    (215,215,215),    #unclassified
    (215,215,215),    #residential
    (225,225,225), #service
    (0,87,0),     #path
    (0,87,0),     #footway
    (63,87,0),   #track
    (0,0,0),    #coastline
    (250,200,200),     #railway
    (0, 255, 255),  # ferry
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
    (0,0,0), #island
    (0,0,0), #islet
    (0,0,0), #water
)

route_types = (
    '"route"="train"',
    '"route"="bus"',
    '"route"="ferry"',
    '"route"="bicycle"',
)

route_sizes = (
    4, #train
    3, #bus
    2, #ferry
    2, #bike
)

route_colors = (
    (255,0,0),   #train
    (0,0,255),   #bus
    (0,255,255), #ferry
    (0,175,0),   #bike
)

stop_types = (
    ('"railway"="stop"','"operator"!~"Scenic"'),
    '"highway"="bus_stop"',
    '"amenity"="ferry_terminal"',
)

stop_sizes = (
    20, #train
    10, #bus
    15, #ferry
)

stop_colors = (
    (255, 0, 0),  # train
    (0, 0, 255),  # bus
    (0, 255, 255),  # ferry
)

def buildlist(location):
    roads = [{"points": maps.load_roads(area=location, element='"highway"="motorway"'),        "width": 5, "color": (10, 0, 0)},
             {"points": maps.load_roads(area=location, element='"highway"="motorway_link"'),   "width": 4, "color": (10, 0, 0)},
             {"points": maps.load_roads(area=location, element='"highway"="trunk"'),           "width": 4},
             {"points": maps.load_roads(area=location, element='"highway"="primary"'),         "width": 3},
             {"points": maps.load_roads(area=location, element='"highway"="secondary"'),       "width": 2},
             {"points": maps.load_roads(area=location, element='"highway"="tertiary"'),        "width": 1},
             {"points": maps.load_roads(area=location, element='"highway"="unclassified"'),    "width": 1, "color": (175, 175, 175)},
             {"points": maps.load_roads(area=location, element='"highway"="residential"'),     "width": 1, "color": (125, 125, 125)},
             {"points": maps.load_roads(area=location, element='"highway"="path"'),            "width": 1, "color": (0, 175, 0)},
             {"points": maps.load_roads(area=location, element='"highway"="footway"'),         "width": 1, "color": (0, 175, 0)},
             {"points": maps.load_roads(area=location, element='"highway"="track"'),           "width": 1, "color": (125, 175, 0)},
             {"points": maps.load_roads(area="New Hampshire", element='"boundary"="administrative"'), "width": 3, "color":(255,0,0)}
             ]
    return roads

def build_lists(locations, features, colors=((0,0,0),), widths=(1,)):
    roads = []
    for location in locations:
        for feature, color, width in zip(features, itertools.cycle(colors), itertools.cycle(widths)):
            roads.append({"points":maps.cached_load_roads(area=location, element=feature), "width":width, "color":color})
    time.sleep(.25)
    maps.public_save_cache()
    time.sleep(.25)
    return roads

def build_list_nodes(locations, features, colors=((0, 0, 0),), sizes=(10,)):
    nodes = []
    for location in locations:
        for feature, color, size in zip(features, itertools.cycle(colors), itertools.cycle(sizes)):
            nodes.append({"points": maps.load_nodes(area=location, element=feature), "size": size, "color": color})
    return nodes

def build_lists_relations(locations, features, colors=((0, 0, 0),), widths=(1,)):
    lines = []
    for location in locations:
        for feature, color, width in zip(features, itertools.cycle(colors), itertools.cycle(widths)):
            lines.append({"points":maps.cached_load_relations(area=location, element=feature), "width":width, "color":color})
    return lines

states  = ("New Hampshire", "Maine", "Massachusetts", "Vermont", "Rhode Island")
counties = ("Essex County, MA", "Rockingham, NH", "Strafford, NH", "York County, ME", "Cumberland County, ME", "Oxford County, ME", "Carroll County, NH", "Belknap County, NH", "Merrimack County, NH",)# "Maine", "New Hampshire", "Massachusetts")
nh_counties = ("Belknap County, NH", "Carroll County, NH", "Cheshire County, NH", "Coos County, NH", "Hillsborough County, NH","Merrimack County, NH", "Rockingham County, NH","Strafford County, NH", "Sullivan County, NH", "Grafton County, NH")


if __name__ == '__main__':
    start = time.time()
    img, drw = draw.setup(*SIZE)

    state_lines = build_lists_relations(("New England", ), ('"border_type"="state"',), widths=(5,))


    routes = build_lists_relations(("New Hampshire", "Maine"),
                                   route_types, widths=route_sizes, colors=route_colors)
    stations = build_list_nodes(("New Hampshire", "Maine"),
                                stop_types, colors=stop_colors, sizes=stop_sizes)

    for i in range(1000):
        try:
            roads = build_lists(counties, road_types, widths=road_sizes, colors=road_colors_b)
            break
        except:
            time.sleep(i)
            print(f"Error, {i} times")
            continue

    waters = build_lists(counties, container_types, widths=container_sizes, colors=container_edge)
    waters2 = build_lists_relations(counties, ('"natural"="water"',), colors=((0, 0, 0),))
    maps.public_save_cache()


    draw.drawCollectionLines(waters2, drw, projection=projections.cartesian, projection_args=[SIZE])
    draw.drawCollectionLines(waters, drw, projection=projections.cartesian, projection_args=[SIZE])
    draw.drawCollectionLines(roads , drw, projection=projections.cartesian, projection_args=[SIZE])
    draw.drawCollectionLines(routes , drw, projection=projections.cartesian, projection_args=[SIZE])
    draw.drawCollectionLines(state_lines , drw, projection=projections.cartesian, projection_args=[SIZE])
    draw.drawCollectionPoints(stations[::-1] , drw, projection=projections.cartesian, projection_args=[SIZE])
    img.show()
    img.save("map.png")
    stop = time.time()
    print(f"Took {stop - start} seconds")