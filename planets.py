#!/usr/bin/python
from lxml import etree
import urllib
import gzip
import io
import time


def demo():
    # Output mass and radius of all planets 
    for planet in oec.findall(".//planet"):
        print [planet.findtext("mass"), planet.findtext("radius")]

    # Find all circumbinary planets 
    for planet in oec.findall(".//binary/planet"):
        print planet.findtext("name")

    # Output distance to planetary system (in pc, if known) and number of planets in system
    for system in oec.findall(".//system"):
        print system.findtext("distance"), len(system.findall(".//planet"))


def get_etree():
    url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
    fo = io.BytesIO(urllib.urlopen(url).read())
    tree = etree.parse(gzip.GzipFile(fileobj=fo))
    return tree


def most_recent(tree):
    """Returns system containing the most rececntly updated planet.

    :param tree: lxml etree
    :returns: lxml etree
    """
    updates = tree.findall('.//lastupdate')
    update_time = [time.strptime(date.text,'%y/%m/%d') for date in updates]
    planet = updates[update_time.index(max(update_time))].getparent()
    return planet


def write_tree(tree,fn):
    xmlstr = etree.tostring(tree, pretty_print=True)
    with open(fn, 'w') as f:
        f.write(xmlstr)

        
if __name__ == '__main__':
    tree = get_etree()
    planet = most_recent(tree)
    print etree.tostring(planet, pretty_print=True)
