import draw
import projections

testpoints = ( (43.00864, -71.07462),
               (43.02628, -71.07298),
               (43.03702, -71.06808),
               (43.03812, -71.07300),
               (43.04101, -71.30804))

testmappoints = projections.cartesian(testpoints)

if __name__ == '__main__':
    img, drw = draw.setup(1200,1200)
    draw.drawLines(testmappoints, drw, width=3, color=(100,0,0))
    print(*testmappoints, sep='\n')

    img.show()

