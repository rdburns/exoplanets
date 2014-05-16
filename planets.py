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
    """Returns planet node that has most recent update date.

    :param tree: lxml etree
    :returns: lxml etree
    """
    updates = tree.findall('.//lastupdate')
    update_time = [time.strptime(date.text,'%y/%m/%d') for date in updates]
    planet = updates[update_time.index(max(update_time))].getparent()
    return planet


def num_planets(tree):
    """Returns the total number of planets in the database

    :param tree: lxml etree
    :returns: integer representing number of planets.
    """
    return int(tree.xpath("count(.//planet)"))


def num_systems(tree):
    """Returns the total number of systems in the database

    :param tree: lxml etree
    :returns: integer representing number of planets.
    """
    return int(tree.xpath("count(.//system)"))


def largest_system(tree):
    """Returns system node that has the largest number of planets.

    :param tree: lxml etree
    :returns: lxml etree centered on system with the mode planets.
    """
    system_size = [num_planets(system) for system in tree.xpath(".//system")]
    largest_idx = system_size.index(max(system_size))
    root = tree.xpath("//systems")[0]
    return root[largest_idx]


def write_tree(tree,fn):
    xmlstr = etree.tostring(tree, pretty_print=True)
    with open(fn, 'w') as f:
        f.write(xmlstr)


def summarize_system(system):
    """Prints concise summary of system represented by tree

    :param system: lxml etree based on <system> tag.
    """
    s = []
    s.append(system.find('name').text)
    return '\n'.join(s)


if __name__ == '__main__':
    tree = get_etree()
    planet = most_recent(tree)



    print "Most recently updated planet is " + str(planet.find('name').text)
    print "  updated on " + planet.find('lastupdate').text
    print ""
    print planet.find('description').text
    print ""
    print "Catalog contains " + str(num_planets(tree)) + " planets in " + str(num_systems(tree)) + " systems."
    print ""
    print "Largest system is:"
    print summarize_system(largest_system(tree))
