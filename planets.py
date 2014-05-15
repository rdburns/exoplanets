#!/usr/bin/python
import xml.etree.ElementTree as ET, urllib, gzip, io
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.urlopen(url).read())))

# Output mass and radius of all planets 
for planet in oec.findall(".//planet"):
    print [planet.findtext("mass"), planet.findtext("radius")]

# Find all circumbinary planets 
for planet in oec.findall(".//binary/planet"):
    print planet.findtext("name")

# Output distance to planetary system (in pc, if known) and number of planets in system
for system in oec.findall(".//system"):
    print system.findtext("distance"), len(system.findall(".//planet"))
