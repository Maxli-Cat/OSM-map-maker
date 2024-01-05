from OSMPythonTools.api import Api
from OSMPythonTools.nominatim import Nominatim as Nomtm
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from geopy.geocoders import Nominatim
from joblib import Memory
import tqdm
import sys
import OSMPythonTools
mem = Memory("./cache")
import os
import pickle

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
    #print(elem_cache)
    save_cache(elem_cache, filename=filename)

geolocatior = Nominatim(user_agent="Sophies_Art_Maps_maxlicatenby@gmail.com")
overpass = Overpass()
nom = Nomtm(userAgent="Sophies_Art_Maps_maxlicatenby@gmail.com")

def old_lookup(location):
    return nom.query(location)

def raw_lookup(location):
    return geolocatior.geocode(location).raw["osm_id"]

lookup = mem.cache(raw_lookup)

def load_roads(area="Rockingham, NH", element='"highway"="motorway"'):
    osmid = lookup(area)
    areaId = osmid + 3600000000
    query = overpassQueryBuilder(area=areaId, elementType='way', selector=[f'{element}'])
    result = overpass.query(query)
    roads = []
    #print(f"{element}, {area}", file=sys.stderr)
    for element in tqdm.tqdm(result.elements(), desc=f"{area}, {element}"):

        geo = element.geometry()["coordinates"]
        if isinstance(geo[0][0], list):
            geo = [x for xs in geo for x in xs]
        #print(type(geo[0][0]))
        roads.append(geo)
    #print(len(roads))
    return roads

def cached_load_roads(area="Rockingham, NH", element='"highway"="motorway"'):
    global elem_cache
    key = f"{area}-{element}"
    if key in elem_cache.keys(): #cache hit
        return elem_cache[key]
    #cache miss
    if CACHE_ONLY: return []
    roads = load_roads(area=area, element=element)
    elem_cache[key] = roads
    return roads

def load_nodes(area="Rockingham, NH", element='"railway"="stop"'):
    osmid = lookup(area)
    areaId = osmid + 3600000000
    query = overpassQueryBuilder(area=areaId, elementType='node', selector=[f'{element}'])
    result = overpass.query(query)
    for point in result.elements():
        yield point.geometry()['coordinates']

def elements_from_relation(relation : OSMPythonTools.element.Element, level=0):
    assert relation.type() == 'relation'
    if level == -1: it = tqdm.tqdm(relation.members(), position=level+1, leave=False)
    else: it = relation.members()
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

def load_relations(area="New Hampshire", element = '"natural"="water"'):
    osmid = lookup(area)
    areaId = osmid + 3600000000
    query = overpassQueryBuilder(area=areaId, elementType='relation', selector=[f'{element}'])
    results = overpass.query(query)
    lines = []
    for result in tqdm.tqdm(results.elements(), desc=f"{area}, {element}"):
        for member in cached_elements_from_relation(result):
            lines.append(member.geometry()['coordinates'])
    return lines

def cached_load_relations(area="New Hampshire", element = '"natural"="water"'):
    osmid = lookup(area)
    areaId = osmid + 3600000000
    query = overpassQueryBuilder(area=areaId, elementType='relation', selector=[f'{element}'])
    results = overpass.query(query)
    lines = []
    for result in tqdm.tqdm(results.elements(), desc=f"{area}, {element}"):
        for member in cached_elements_from_relation(result):
            lines.append(member)
    return lines

if __name__ == "__main__":
    area = "New Hampshire"
    element = '"natural"="water"'
    osmid = lookup(area)
    areaId = osmid + 3600000000
    query = overpassQueryBuilder(area=areaId, elementType='relation', selector=[f'{element}'])
    results = overpass.query(query)

