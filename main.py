import draw
import maps
import projections

SIZE = (2500,1800)

if __name__ == '__main__':
    img, drw = draw.setup(*SIZE)
    roads = maps.load_roads()
    roads += maps.load_roads(area="Rockingham, NH", element='"highway"="trunk"')
    roads += maps.load_roads(area="Rockingham, NH", element='"highway"="primary"')
    roads += maps.load_roads(area="Rockingham, NH", element='"highway"="secondary"')
    roads += maps.load_roads(area="Rockingham, NH", element='"highway"="tertiary"')
    roads += maps.load_roads(area="Rockingham, NH", element='"highway"="unclassified"')
    roads += maps.load_roads(area="Rockingham, NH", element='"highway"="residential"')
    roads += maps.load_roads(area="Epping, NH", element='"highway"')
    roads += maps.load_roads(area="Freemont, NH", element='"highway"')
    roads += maps.load_roads(area="Lee, NH", element='"highway"')
    #roads = maps.load_roads(area="New Hampshire", element='"boundary"="administrative"')
    map_roads = [projections.cartesian(i, bounds=SIZE) for i in roads]
    for road in map_roads:
        draw.drawLines(road, drw, width=1)
    img.show()
