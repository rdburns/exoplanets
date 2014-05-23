#!/usr/bin/python
from lxml import etree
import urllib
import gzip
import io
import time
import cmd

# TODO
# Some systems have more than one name
# Binaries don't work well.
# Alpha Centauri (not circumbinary)
# Kepler-47 (circumbinary)

try:
    from enum import Enum
except ImportError:
    print "You need the enum backport."
    print "pip install enum34"

    
class PlanetSize(Enum):
    """Defines fuzzy planet size labels.

    The enum value is an ASCII depiction."""
    terrestrial = '.'
    neptune = 'o'
    jupiter = '@'
    unknown = '?'
         

#Constants
JUPITER_IN_EARTH_MASSES = 317.828
NEPTUNE_IN_EARTH_MASSES = 17.147
JUPITER_IN_EARTH_RADII = 11.209 #equatorial
NEPTUNE_IN_EARTH_RADII = 3.883 #equatorial

SYMBOL = {'sun': u'\u2609',
          'earth': u'\u2295',
          'neptune': u'\u2646',
          'jupiter': u'\u2643'}


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


def get_planet_radius(planet, multiple='jupiter'):
    """Returns planet radius as a float times Jupiter Radii

    :param planet: lxml etree node for <planet>
    :param multiple: String, either 'jupiter', 'neptune', or 'earth'. \
    If earth, will return number of earth masses, etc.
    """
    radius_node = planet.find('radius')
    if radius_node is None:
        return None
    jup_radii = float(radius_node.text)
    if multiple == 'jupiter':
        return jup_radii
    elif multiple == 'neptune':
        return (jup_radii * JUPITER_IN_EARTH_RADII) / NEPTUNE_IN_EARTH_RADII
    elif multiple == 'earth':
        return jup_radii * JUPITER_IN_EARTH_RADII

    
def get_planet_mass(planet, multiple='jupiter'):
    """Returns planet mass as a float times mass of multiple.

    :param planet: lxml etree node for <planet>
    :param multiple: String, either 'jupiter', 'neptune', or 'earth'. \
    If earth, will return number of earth masses, etc.
    """
    jup_mass = float(planet.find('mass').text)
    if multiple == 'jupiter':
        return jup_mass
    elif multiple == 'neptune':
        return (jup_mass * JUPITER_IN_EARTH_MASSES) / NEPTUNE_IN_EARTH_MASSES
    elif multiple == 'earth':
        return jup_mass * JUPITER_IN_EARTH_MASSES

    
def get_planet_size(planet):
    """Returns PlanetSize enum for planet.

    Makes determination based on radius and mass criteria.
    :param planet: lxml etree node for <planet>
    """
    earth_radii = get_planet_radius(planet, 'earth')
    if earth_radii is not None:
        if earth_radii < 2:
            return PlanetSize.terrestrial
        elif earth_radii > 7:
            return PlanetSize.jupiter
        else:
            return PlanetSize.neptune
    else:
        earth_masses = get_planet_mass(planet, 'earth')
        if earth_masses < 10:
            return PlanetSize.terrestrial
        elif earth_masses > 30:
            return PlanetSize.jupiter
        else:
            return PlanetSize.neptune
    return PlanetSize.unknown    
    

def get_etree():
    url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
    fo = io.BytesIO(urllib.urlopen(url).read())
    tree = etree.parse(gzip.GzipFile(fileobj=fo))
    return tree


def find_system_by_name(name):
    """Returns system node matching supplied name

    :param name: string containing desired system name.
    """
    systems = tree.findall('.//system')
    names = [system.find('name').text for system in systems]
    return systems[names.index(name.replace('_',' '))]
    

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
    return get_parent_tag(planet, 'system')


def get_parent_tag(node, tag):
    """Traverses up the tree from node until it finds tag and then returns that node.

    :param node: The child node to start the search from
    :param tag: String with tag type we're searching for.
    """
    if node.tag == tag:
        return node
    else:
        return get_parent_tag(node.getparent(), tag)
    

def num_planets(tree):
    """Returns the total number of planets in the tree

    :param tree: lxml etree
    :returns: integer representing number of planets.
    """
    return int(tree.xpath("count(.//planet)"))


def num_stars(tree):
    """Returns the total number of stars in the tree

    :param tree: lxml etree
    :returns: integer representing number of planets.
    """
    return int(tree.xpath("count(.//star)"))


def num_systems(tree):
    """Returns the total number of systems in the tree

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


def planet_name(planet):
    """Returns name of planet, just letter.
    """
    return planet.find('name').text.split(' ')[-1]
    

def summarize_star(star):
    """return one line summary of star"""
    if star.find('name').text[-2] == ' ':
        name = star.find('name').text[-1]
    else:
        name = ' '
    return u'{0} {1} {2}{3}'.format(name, star.find('spectraltype').text, star.find('mass').text, 'M'+SYMBOL['sun'])


def format_planet_mass_str(planet):
    """Takes float multiple of Jupiter mass, and returns it rounded and prefixed.

    Uses J2.3 for jupiter masses.
    Uses E3.4 for earth masses if under 0.05 jupiter masses.
    """
    jup_mass = get_planet_mass(planet, 'jupiter')
    planet_size = get_planet_size(planet)
    flt_mass = float(planet.find('mass').text)
    if planet_size.name == 'terrestrial':
        use_mass = get_planet_mass(planet, 'earth')
        symbol = SYMBOL['earth']
    else:
        use_mass = jup_mass
        symbol = SYMBOL['jupiter']
    return u'{:0.3f}M{}'.format(round(use_mass, 3), symbol)
    
def summarize_planet(planet):
    """Return one line summary of planet"""
    if planet.find('list').text == "Confirmed planets":
        reliable = ' '
    else:
        reliable = '?'

    letter = planet_name(planet)

    mass = format_planet_mass_str(planet)
    return u'{0} {1} {2}'.format(reliable, letter, mass)


def summarize_system(system):
    """Prints concise summary of system represented by tree

    :param system: lxml etree based on <system> tag.
    """
    s = []
    s.append(system.find('name').text + ' - ' + str(num_stars(system)) + ' stars - ' + str(num_planets(system)) + ' planets')
    s.append(ascii_system(system))
    for star in system.iterfind('star'):
        s.append(' ' + summarize_star(star))
        for planet in star.iterfind('planet'):
            s.append('   ' + summarize_planet(planet))
#    for planet in system.iterfind('planet')
    return '\n'.join(s)


def get_max_sma(tree):
    """Returns max Semi-Major Axis (AU) for all planets in tree.

    :param tree: An lxml etree
    """
    allsmas = [float(x.text) for x in tree.findall('.//semimajoraxis')]
    return max(allsmas)


def ascii_system(system):
    """Return an ASCII graphic of the system.

    :param system: lxml etree based on <system> tag.
    """
    dots = []
    names = []
    maxsma = get_max_sma(system)
    for star in system.iterfind('star'):
        t = [' ']*80
        d = [' ']*80
        d[0] = '*'
        for planet in star.iterfind('planet'):
            sma = float(planet.find('semimajoraxis').text)
            loc = int((sma / maxsma) * 78) + 1
            while t[loc] != ' ':
                loc += 1
            t[loc] = planet_name(planet)
            d[loc] = get_planet_size(planet).value
        names.append(''.join(t))
        dots.append(''.join(d))
    result = []
    for idx in range(len(dots)):
        result.append(dots[idx])
        result.append(names[idx])
        result.append('')
    return '\n'.join(result)


def tweet_system(system):
    """Return system summary suitable for a twitter message.

    :param system: lxml etree based on <system> tag.
    """
    s = []
    for star in system.iterfind('star'):
        s.append(star.find('name').text)
        for planet in star.iterfind('planet'):
            planet_size = get_planet_size(planet)
            s.append('  ' + planet_size.value + ' ' + planet_name(planet))
    return '\n'.join(s)


def get_system_names(tree):
    """Returns list of all system names.

    :param tree: Tree to find systems in.
    """
    names = [n.replace(' ','_') for n in tree.xpath('./system/name/text()')]
    return names


class PlanetCmd(cmd.Cmd):
    def __init__(self, system_names):
        cmd.Cmd.__init__(self)
        self.prompt = '> '
        self.intro = "Exoplanet Explorer (type help commands):"
        self.system_names = system_names

    def do_most_recent_planet(self, args):
        planet = most_recent_planet(tree)
        print "Most recently updated planet is " + str(planet.find('name').text)
        print "  updated on " + planet.find('lastupdate').text
        print ""
        print planet.find('description').text

    def do_most_recent_system(self, args):
        print "Most recently updated system is:"
        most_recent = most_recent_system(tree)
        print summarize_system(most_recent)

    def do_stats(self, args):
        print "Catalog contains " + str(num_planets(tree)) + " planets in " + str(num_systems(tree)) + " systems."

    def do_largest_system(self, args):
        print "Largest system is:"
        largest = largest_system(tree)
        #write_tree(largest,'largest.xml')
        print summarize_system(largest)

    def do_system(self, system_name):
        print summarize_system(find_system_by_name(system_name))

    def do_tweet(self, system_name):
        print tweet_system(find_system_by_name(system_name))

    def complete_tweet(self, text, line, begidx, endidx):
        return self.complete_system(text, line, begidx, endidx)
    
    def complete_system(self, text, line, begidx, endidx):
        if not text:
            completions = self.system_names[:]
        else:
            completions = [ f
                            for f in self.system_names
                            if f.startswith(text)
                            ]
        return completions
        
    def do_exit(self, args):
        exit()
        

if __name__ == '__main__':
    tree = get_etree()
    system_names = get_system_names(tree)
    PlanetCmd(system_names).cmdloop()
    

