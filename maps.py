from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
import OSMPythonTools.api
from geopy.geocoders import Nominatim
import tqdm
import OSMPythonTools
import os
import pickle
import time
import random

CACHE_ONLY = False

def load_cache(filename='cache.pickle') -> dict:
    if os.path.isfile(filename):
        try:
            cff = pickle.load(open(filename, 'rb'))
            return cff
        except EOFError: return {}
    else:
        return {}

def save_cache(cache : dict, filename='cache.pickle'):
    if os.path.exists(f"{filename}.bak"):
        os.remove(f"{filename}.bak")
    if os.path.exists(filename):
        os.rename(filename, f"{filename}.bak")
    dmp = pickle.dumps(cache)
    open(filename, 'wb').write(dmp)

elem_cache = load_cache()

def public_save_cache(filename='cache.pickle'):
    #print(elem_cache.keys()*, sep='\n')
    save_cache(elem_cache, filename=filename)

geolocatior = Nominatim(user_agent="Sophies_Art_Maps_maxlicatenby@gmail.com", timeout=60)
overpass = Overpass()

def raw_lookup(location):
    try:
        loc = geolocatior.geocode(location).raw["osm_id"]
    except AttributeError as ex:
        print(location)
        raise ex
    return loc

def lookup(location):
    global elem_cache
    key = f"Location - {location}"
    if key in elem_cache.keys() and random.random() < 0.9999:
        return elem_cache[key]
    result = raw_lookup(location)
    elem_cache[key] = result
    return result

def load_roads(area="Rockingham, NH", element='"highway"="motorway"'):
    osmid = lookup(area)
    areaId = osmid + 3600000000

    if type(element) == str:
        element = element.replace('[', '').replace(']', '').replace('(', '').replace(')', '')
        if ',' in element:
            element = element.split(',')
        else:
            element = [element]
    try:
        query = overpassQueryBuilder(area=areaId, elementType='way', selector=element)
        result = overpass.query(query)
        #print(f"Passed with element {element}, type {type(element)}")
    except Exception as ex:
        print(f"Failed with element {element}, type {type(element)}")
        exit()
    roads = []
    #print(f"{element}, {area}", file=sys.stderr)
    for element in tqdm.tqdm(result.elements(), desc=f"{area}, {element}"):

        try:
            geo = element.geometry()["coordinates"]
            if isinstance(geo[0][0], list):
                geo = [x for xs in geo for x in xs]
            #print(type(geo[0][0]))
            roads.append(geo)
        except Exception as ex:
            print(str(ex))
            if "HTTP Error 410" in str(ex):
                continue
            elif "Expected object or value" in str(ex):
                print(f"Weirdness, {ex}")
                continue
            else:
                raise ex
    #print(len(roads))
    return roads

def cached_load_roads(area="Rockingham, NH", element='"highway"="motorway"'):
    global elem_cache
    key = f"{area}-{element}"
    if key in elem_cache.keys() and random.random() < 0.9999: #cache hit, random invalidation
        return elem_cache[key]
    #cache miss
    if CACHE_ONLY: return []
    roads = load_roads(area=area, element=element)
    elem_cache[key] = roads
    return roads

def load_nodes(element='"railway"="station"', area="Rockingham, NH"):
    osmid = lookup(area)
    areaId = osmid + 3600000000

    if type(element) == str:
        element = element.replace('[','').replace(']','').replace('(','').replace(')','')
        if ',' in element:
            element = element.split(',')
        else:
            element = [element]

    query = overpassQueryBuilder(area=areaId, elementType='node', selector=element)

    result = overpass.query(query)
    for point in result.elements():
        yield point.geometry()['coordinates']

def elements_from_relation(relation : OSMPythonTools.element.Element, level=0):
    assert relation.type() == 'relation'
    if level == -1: it = tqdm.tqdm(relation.members(), position=level+1, leave=False)
    else:
        try:
            it = relation.members()
        except Exception as ex:
            if "Expected object or value" in str(ex):
                return
            else:
                raise ex
    for member in it:
        if member.type() == 'way':
            yield member
        elif member.type() == 'node':
            continue
        else:
            print(level, member.type())
            for e in elements_from_relation(member, level + 1):
                yield e

def cached_elements_from_relation(relation):
    global elem_cache
    id = relation.id()

    if id in elem_cache.keys(): #cache hit
        for i in elem_cache[id]:
            yield i

    else: #cache miss
        mbrs = []
        for i in elements_from_relation(relation):
            yield i.geometry()['coordinates']
            mbrs.append(i.geometry()['coordinates'])
        elem_cache[id] = mbrs
        #save_cache(elem_cache)

def point_equality(a, b):
    return (abs(a[0] - b[0]) < 0.000000000002) and (abs(a[1] - b[1]) < 0.000000000002)

def get_water_relations(area='New Hampshire', selector=['"natural"="water"']):
    print(f"Water lookup {area}, {selector}")
    osmid = lookup(area)
    areaId = osmid + 3600000000
    query = overpassQueryBuilder(area=areaId, elementType='relation', selector=selector)
    results = overpass.query(query)
    lines = []
    print(results.countElements())
    for element in results.elements():
        print('---')
        ways = element.members(True, False, True)
        if len(ways) == 0: continue
        elif len(ways) == 1:
            try:
                yield ways[0].geometry()['coordinates']
            except Exception as ex:
                if "Cannot build geometry" in str(ex):
                    continue
                else:
                    raise ex
        else:
            line = ways[0].geometry()['coordinates']
            for way in ways[1:]:
                #print(f"{way.id()=}")
                #print(f'{len(line)=}')
                if way.type() != 'way':
                    continue

                next_segment = way.geometry()['coordinates']
                try:
                    if point_equality(next_segment[0], line[0]):
                        line = next_segment[::-1] + line
                        #print(f"{way.id()=}")
                    elif point_equality(next_segment[0], line[-1]):
                        line = line + next_segment
                        #print(f"{way.id()=}")
                    elif point_equality(next_segment[-1], line[0]):
                        line = next_segment + line
                        #print(f"{way.id()=}")
                    elif point_equality(next_segment[-1], line[-1]):
                        line = next_segment + line[::-1]
                        #print(f"{way.id()=}")
                    else:
                        #print(f"{line[0]=},{line[-1]=}, {next_segment[0]=},{next_segment[-1]=}, {element.id()=}, {way.id()=}, {line=}")
                        continue
                except TypeError as ex:
                    #print(f"{ex=}, https://openstreetmap.org/relation/{element.id()}")
                    pass
            yield line

def cached_get_water_relations(area="New Hampshire", selector=['"natural"="water"']):
    global elem_cache
    if selector[0] == '"natural"="water"':
        key = f"{area}-x-water-relation"
        cache = True
    else:
        key = f"{area}-x-{selector}"
        cache = False

    if key in elem_cache.keys() and random.random() < 0.9999 and cache: #cache hit
        #print(f"Water Cache Hit, {key}")
        return elem_cache[key]
    print(f"Water Cache Miss, {key}")
    result = [i for i in tqdm.tqdm(get_water_relations(area, selector=selector))]
    elem_cache[key] = result
    #print(f"{key=},")
    return result

def cached_load_relations(area="New Hampshire", element = '"natural"="water"'):
    osmid = lookup(area)
    areaId = osmid + 3600000000

    if type(element) == str:
        element = element.replace('[', '').replace(']', '').replace('(', '').replace(')', '')
        if ',' in element:
            element = element.split(',')
        else:
            element = [element]

    #print(f"{element=}")
    query = overpassQueryBuilder(area=areaId, elementType='relation', selector=element)
    results = overpass.query(query)
    lines = []
    for result in tqdm.tqdm(results.elements(), desc=f"{area}, {element}"):
        for member in cached_elements_from_relation(result):
            try:
                lines.append(member)
            except Exception as ex:
                if "Expected object or value" in str(ex):
                    continue
                else:
                    raise ex
    return lines

def double_cached_load_relations(area="New Hampshire", element = '"natural"="water"'):
    global elem_cache
    key = f"{area}xr{element}"
    if key in elem_cache.keys() and random.random() < 0.9999: #cache hit
        return elem_cache[key]
    #cache miss
    if CACHE_ONLY: return []
    geo = cached_load_relations(area=area, element=element)
    elem_cache[key] = geo
    return geo

if __name__ == "__main__":
    pass


