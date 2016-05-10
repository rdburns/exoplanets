"""
Extracts values from Open Exoplanet Catalog XML
"""
import time
import io
from lxml import etree
import gzip
import random

try:
    import requests
except ImportError:
    print "You need the requirements."
    print "pip install -r requirements.txt"
    sys.exit(1)


#Constants
JUPITER_IN_EARTH_MASSES = 317.828
NEPTUNE_IN_EARTH_MASSES = 17.147
JUPITER_IN_EARTH_RADII = 11.209 #equatorial
NEPTUNE_IN_EARTH_RADII = 3.883 #equatorial



def planet_radius(planet, multiple='jupiter'):
    """Returns planet radius as a float times Jupiter Radii

    :param planet: lxml etree node for <planet>
    :param multiple: String, either 'jupiter', 'neptune', or 'earth'. \
    If earth, will return number of earth masses, etc.
    """
    radius_node = planet.find('radius')
    if radius_node is None or radius_node.text is None:
        return None
    jup_radii = float(radius_node.text)
    if multiple == 'jupiter':
        return jup_radii
    elif multiple == 'neptune':
        return (jup_radii * JUPITER_IN_EARTH_RADII) / NEPTUNE_IN_EARTH_RADII
    elif multiple == 'earth':
        return jup_radii * JUPITER_IN_EARTH_RADII


def planet_mass(planet, multiple='jupiter'):
    """Returns planet mass as a float times mass of multiple.

    :param planet: lxml etree node for <planet>
    :param multiple: String, either 'jupiter', 'neptune', or 'earth'. \
    If earth, will return number of earth masses, etc.
    """
    massnode = planet.find('mass')
    if massnode is not None and massnode.text is not None:
        jup_mass = float(massnode.text)
    else:
        return None
    if multiple == 'jupiter':
        return jup_mass
    elif multiple == 'neptune':
        return (jup_mass * JUPITER_IN_EARTH_MASSES) / NEPTUNE_IN_EARTH_MASSES
    elif multiple == 'earth':
        return jup_mass * JUPITER_IN_EARTH_MASSES


def get_tree(url="https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"):
    """Retrieve exoplanets XML database using requests library."""
    r = requests.get(url)
    fo = io.BytesIO(r.content)
    tree = etree.parse(gzip.GzipFile(fileobj=fo))
    return tree


def find_system_by_name(tree, name):
    """Returns system node matching supplied name

    :param tree: etree object
    :param name: string containing desired system name.
    """
    system_name = name.replace('_',' ')
    target = tree.xpath('.//system/name[text()="'+system_name+'"]')
    if target == []:
        return None
    return parent_tag(target[0], 'system')


def random_system(tree):
    """Returns random system node.
    """
    systems = tree.xpath('.//system')
    idx = random.randrange(0,len(systems))
    return systems[idx]


def most_recent_planet(tree):
    """Returns planet node that has most recent update date.

    :param tree: lxml etree
    :returns: lxml etree
    """
    updates = tree.findall('.//lastupdate')
    update_time = [time.strptime(date.text,'%y/%m/%d') for date in updates]
    planet = updates[update_time.index(max(update_time))].getparent()
    return planet


def most_recent_system(tree):
    """Returns system with most recently updated planet.

    :param tree: lxml etree
    """
    planet = most_recent_planet(tree)
    return parent_tag(planet, 'system')


def parent_tag(node, tag):
    """Traverses up the tree from node until it finds tag and then returns that node.

    :param node: The child node to start the search from
    :param tag: String with tag type we're searching for.
    """
    if node.tag == tag:
        return node
    else:
        return parent_tag(node.getparent(), tag)


def num_planets(tree):
    """Returns the total number of planets in the tree

    :param tree: lxml etree
    :returns: integer representing number of planets.
    """
    return int(tree.xpath("count(.//planet)"))


def num_tags(tree, tag):
    """Returns the total number of tags in the tree of name tag

    Example, count planets: num_tags(tree, 'planet')

    :param tree: lxml etree
    :param tag: string containing <tag> name.
    :returns: integer representing number of tags found.
    """
    return int(tree.xpath("count(.//" + tag + ")"))


def max_value(tree, tag='semimajoraxis'):
    """Returns max value for all planets in tree.

    Default is to use Semi-Major Axis (AU) for all planets in tree.

    :param tree: An lxml etree
    :param tag: A string containing a tag name.
    """
    allsmas = [float(x.text) for x in tree.findall('.//'+tag)]
    if allsmas == []:
        return 0
    else:
        return max(allsmas)


def largest_system(tree):
    """Returns system node that has the largest number of planets.

    :param tree: lxml etree
    :returns: lxml etree centered on system with the mode planets.
    """
    system_size = [num_tags(system, 'planet') for system in tree.xpath(".//system")]
    largest_idx = system_size.index(max(system_size))
    root = tree.xpath("//systems")[0]
    return root[largest_idx]


def write_tree(tree,fn):
    xmlstr = etree.tostring(tree, pretty_print=True)
    with open(fn, 'w') as f:
        f.write(xmlstr)


def planet_name(planet):
    """Returns name of planet, just letter.
    """
    return planet.find('name').text[-1]
