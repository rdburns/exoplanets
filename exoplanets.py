#!/usr/bin/env python
"""Open Exoplanet Catalog Explorer

Ryan Burns
rdburns@gmail.com
http://twitter.com/ryanburns
"""

import sys
import cmd
from pprint import pprint

from exoplanets import extract

# TODO
# There's something weird with the system name autocomplete

try:
    from enum import Enum
    import inflect
except ImportError:
    print "You need the requirements."
    print "pip install -r requirements.txt"
    sys.exit(1)

try: 
    from colorama import Fore, Back, Style, init
    init()
except ImportError:
    # colorama support is optional.
    print "pip install colorama to get colors for stellar classes, etc."

    
inf = inflect.engine()

    
class PlanetSize(Enum):
    """Defines fuzzy planet size labels.

    The enum value is an ASCII depiction."""
    terrestrial = '.'
    neptune = 'o'
    jupiter = '@'
    unknown = '?'
    
def get_planet_size(planet):
    """Returns PlanetSize enum for planet.

    Makes determination based on radius and mass criteria.
    :param planet: lxml etree node for <planet>
    """
    earth_radii = extract.planet_radius(planet, 'earth')
    if earth_radii is not None:
        if earth_radii < 2:
            return PlanetSize.terrestrial
        elif earth_radii > 7:
            return PlanetSize.jupiter
        else:
            return PlanetSize.neptune
    else:
        earth_masses = extract.planet_mass(planet, 'earth')
        if earth_masses < 10:
            return PlanetSize.terrestrial
        elif earth_masses > 30:
            return PlanetSize.jupiter
        else:
            return PlanetSize.neptune
    return PlanetSize.unknown
         

SYMBOL = {'sun': u'\u2609',
          'mercury': u'\u263F',
          'venus':u'\u2640',
          'earth': u'\u2295',
          'mars': u'\u2642',
          'neptune': u'\u2646',
          'jupiter': u'\u2643',
          'saturn': u'\u2644',
          'uranus': u'\u26E2',
          'ellipsis': u'\u2026',
          'degrees': u'\u00B0',
          'eccentricity': u"\U0001D452"
          }

# In AUs:
SMA = {'mercury': 0.387,
       'venus':0.727,
       'earth': 1.0,
       'mars': 1.524,
       'neptune': 30.104,
       'jupiter': 5.204,
       'saturn': 9.582,
       'uranus': 19.299}


if not sys.modules.has_key('colorama'):
    # Doesn't wreck things if colorama isn't installed.
    STARCOLOR = {'O': '',
                 'B': '',
                 'A': '',
                 'F': '',
                 'G': '',
                 'K': '',
                 'M': ''}
    RSTCOLOR = ''
else:
    STARCOLOR = {'O': Fore.MAGENTA + Style.BRIGHT,
                 'B': Fore.BLUE + Style.BRIGHT,
                 'A': Fore.WHITE + Style.BRIGHT,
                 'F': Fore.YELLOW + Style.BRIGHT,
                 'G': Fore.YELLOW + Style.BRIGHT, 
                 'K': Fore.YELLOW,
                 'M': Fore.RED + Style.BRIGHT}
    RSTCOLOR = Fore.RESET + Style.RESET_ALL


def spectral_colorize(s, star):
    """Returns string s with spectral color colorama codes
    """
    spectral = star.find('spectraltype')
    if spectral is None:
        return s
    stellarclass = spectral.text[0]
    if stellarclass in STARCOLOR.keys():
        return STARCOLOR[stellarclass] + s + RSTCOLOR
    else:
        return s


def format_spectral_name(star):
    """Retruns string containing spectral name of star, with colorama color

    Doesn't include ANSII code if colorama is not installed.
    :param star: lxml etree on <star> node
    """
    spectral = star.find('spectraltype')
    if spectral is not None:
        return spectral_colorize(spectral.text, star)
    else:
        return ''


def format_body_temp_str(body):
    """Returns temperature string 273K for any body with a temperature
    tag.
    """
    temp = body.find('temperature')
    if temp is not None:
        return temp.text + 'K'
    else:
        return ''


def format_star_mass_str(star):
    """Returns string of form 1.324M{sunsymbol}
    """
    mass = star.find('mass')
    if mass is not None:
        mass = mass.text
    else:
        mass = '?'
    return u'{}{}'.format(mass, 'M'+SYMBOL['sun'])


def format_star_radius_str(star):
    """Returns string of form 1.324M{sunsymbol}
    """
    radius = star.find('radius')
    if radius is not None:
        radius = radius.text
    else:
        radius = '?'
    return u'{}{}'.format(radius, 'R'+SYMBOL['sun'])


def format_star_metal_str(star):
    """Returns metallicity value relative to Sol
    """
    metallicity = star.find('metallicity')
    if metallicity is not None:
        metallicity = metallicity.text + 'Z' + SYMBOL['sun']
    else:
        metallicity = ''
    return metallicity


def summarize_star(star):
    """return one line summary of star"""
    if star.find('name').text[-2] == ' ':
        name = star.find('name').text[-1]
    else:
        name = ' '
    mass = format_star_mass_str(star)
    radius = format_star_radius_str(star)
    temp = format_body_temp_str(star)
    metallicity = format_star_metal_str(star)
    return u'{} {} {:>8} {:>8} {:>8} {:>8} {:>8} {}'.format(name, format_spectral_name(star),
                                             mass, radius, '', '', temp, metallicity)


def format_planet_mass_str(planet):
    """Takes float multiple of Jupiter mass, and returns it rounded and prefixed.

    Uses J2.3 for jupiter masses.
    Uses E3.4 for earth masses if under 0.05 jupiter masses.
    """
    jup_mass = extract.planet_mass(planet, 'jupiter')
    if jup_mass is None:
        return u'  ?M{}'.format(SYMBOL['jupiter'])
    else:
        planet_size = get_planet_size(planet)
        flt_mass = float(planet.find('mass').text)
        if planet_size.name == 'terrestrial':
            use_mass = extract.planet_mass(planet, 'earth')
            symbol = SYMBOL['earth']
        else:
            use_mass = jup_mass
            symbol = SYMBOL['jupiter']
        return u'{:0.3f}M{}'.format(round(use_mass, 3), symbol)
    

def format_planet_radius_str(planet):
    """Takes float multiple of Jupiter radius, and returns it rounded and prefixed.

    """
    jup_radius = extract.planet_radius(planet, 'jupiter')
    if jup_radius is None:
        return u'  ?R{}'.format(SYMBOL['jupiter'])
    else:
        planet_size = get_planet_size(planet)
        flt_radius = float(planet.find('radius').text)
        if planet_size.name == 'terrestrial':
            use_radius = extract.planet_radius(planet, 'earth')
            symbol = SYMBOL['earth']
        else:
            use_radius = jup_radius
            symbol = SYMBOL['jupiter']
        return u'{:0.3f}R{}'.format(round(use_radius, 3), symbol)


def format_method_date(body):
    """Formats discovery method and date and returns string of form:
    2001rv, 2008trn"""
    mf = body.find('discoverymethod')
    if mf is not None:
        method = mf.text
    else:
        methos = '-'
    yf = body.find('discoveryyear')
    if yf is not None:
        year = yf.text
    else:
        year = '-'
    if method == 'transit':
        meth = 'trn'
    elif method == 'RV':
        meth =  'rv'
    elif method == 'microlensing':
        meth = u'\u03BC'+'lens'
    elif method == 'imaging':
        meth = 'img'
    elif method == 'timing':
        meth = 'tim'
    else:
        meth = ''
    return year + meth
    

def format_planet_sma_str(planet):
    """Returns string describing Orbit"""
    smanode = planet.find('semimajoraxis')
    if smanode is None:
        return ''
    else:
        sma = float(smanode.text)
        return '{:0.3f}AU'.format(sma)


def format_planet_period_str(planet):
    """Returns string describing Orbit"""
    pernode = planet.find('period')
    if pernode is None:
        return ''
    else:
        period = float(pernode.text)
    return '{:0.2f}d'.format(period)


def format_eccentricity_str(planet):
    """Returns string describing eccentricity"""
    eccnode = planet.find('eccentricity')
    if eccnode is None or eccnode.text is None:
        return ''
    else:
        return SYMBOL['eccentricity'] + '={:0.2f}'.format(float(eccnode.text))


def format_inclination_str(planet):
    """Returns string describing inclination"""
    incnode = planet.find('inclination')
    if incnode is None or incnode.text is None:
        return ''
    else:
        return u'{:0.2f}{}'.format(float(incnode.text), SYMBOL['degrees'])


def summarize_planet(planet):
    """Return one line summary of planet"""
    if planet.find('list').text == "Confirmed planets":
        reliable = ' '
    else:
        reliable = '?'

    letter = extract.planet_name(planet)

    mass = format_planet_mass_str(planet)
    radius = format_planet_radius_str(planet)
    temp = format_body_temp_str(planet)
    sma = format_planet_sma_str(planet)
    period = format_planet_period_str(planet)
    method = format_method_date(planet)
    if planet.find('description') is not None:
        desc = SYMBOL['ellipsis']
    else:
        desc = ' '
    eccentricity = format_eccentricity_str(planet)
    inclination = format_inclination_str(planet)
        
    fmt = u'{} {} {:>8} {:>8} {:>8} {:>8} {:>8} {:>6} {:>6} {} {}'
    return fmt.format(reliable, letter,
                      mass, radius, sma, period, temp,
                      eccentricity, inclination, 
                      method, desc)


def convert_pc_to_ly(pc):
    """Converts distance in parsecs into lightyears and returns integer."""
    return pc * 3.2615638


def system_coord_str(system):
    """Return String representing sky coordinates

    :param system: lxml etree at system node"""
    ranode = system.find('rightascension')
    if ranode is not None:
        ra = ranode.text.split(' ')
    else:
        ra = ['?','?','?']
    decnode = system.find('declination')
    if decnode is not None:
        dec = decnode.text.split(' ')
    else:
        dec = ['?','?','?']
    distance = system.find('distance')
    if distance is not None:
        dist_flt = float(distance.text)
        dist_str = '{:0.1f} pc / {:0.1f} ly'.format(dist_flt,
                                          convert_pc_to_ly(dist_flt))
    else:
        dist_str = ''
        
    return ('RA:' + ra[0] + 'h' + ra[1] + 'm' + ra[0] + 's' +
            ' DEC:' + dec[0] + SYMBOL['degrees'] + dec[1] + "'" + dec[2] + '"' +
            ' ' + dist_str
            )


def summarize_system(system):
    """Prints concise summary of system represented by tree

    :param system: ommi clxml etree based on <system> tag.
    """
    s = []
    s.append(system.find('name').text + ' - ' + system_coord_str(system))
    num_stars = extract.num_tags(system, 'star')
    num_planets = extract.num_tags(system, 'planet')
    s.append('{} {} - {} {}'.format(num_stars,
                                    inf.plural('star',num_stars),
                                    num_planets,
                                    inf.plural('planet',num_planets)
                                    ))
    s.append(ascii_system(system))
    s.append('')
    binary = system.find('binary')
    if binary is not None:
        system = binary
    for star in system.iterfind('star'):
        s.append(' ' + summarize_star(star))
        for planet in star.iterfind('planet'):
            s.append('   ' + summarize_planet(planet))
    if system.find('planet') is not None:
        s.append(' (..) circumbinary planets:')
    for planet in system.iterfind('planet'):
        s.append('   ' + summarize_planet(planet))
    return '\n'.join(s)


def ascii_system(system):
    """Return an ASCII graphic of the system.

    :param system: lxml etree based on <system> tag.
    """
    def check_sol(maxsma, planet_str, sol):
        """Inserts planet symbol into ascii art list 'sol' and returns it.
        """
        if maxsma > SMA[planet_str]:
            loc = int((SMA[planet_str] / maxsma) * 78) + 1
            sol[loc] = SYMBOL[planet_str]
        sol[0] = SYMBOL['sun']
        return sol

    def make_sol(maxsma):
        """Returns depiction of our solar system at same scale."""
        sol = [' ']*80
        for planet in SMA:
            sol = check_sol(maxsma, planet, sol)
        return ''.join(sol)
    

    dots = []
    names = []
    sorttag = 'semimajoraxis'
    maxsma = extract.max_value(system, sorttag)
    if maxsma == 0:
        sorttag = 'period'
        maxsma = extract.max_value(system, sorttag)
    if maxsma == 0:
        return ''

    sol = make_sol(maxsma)
    
    binary = system.find('binary')
    for star in system.xpath('.//star'):
        t = [' ']*80
        d = [' ']*80
        d[0] = spectral_colorize('*', star)
        if binary is not None:
            t[0] = star.find('name').text[-1]
        for planet in star.iterfind('planet'):
            smanode = planet.find(sorttag)
            if smanode is None:
                sma = 0
            else:
                sma = float(smanode.text)
            loc = int((sma / maxsma) * 78) + 1
            while t[loc] != ' ':
                # Makes sure we show all planets even if they're in the same bin.
                loc += 1
            t[loc] = extract.planet_name(planet)
            ps = get_planet_size(planet)
            d[loc] = ps.value
        names.append(''.join(t))
        dots.append(''.join(d))
    result = []
    result.append(sol)
    for idx in range(len(dots)):
        result.append(dots[idx])
        result.append(names[idx])
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
            s.append('  ' + planet_size.value + ' ' + \
                     extract.planet_name(planet))
    return '\n'.join(s)


def system_names(tree):
    """Returns list of all system names.

    :param tree: Tree to find systems in.
    """
    names = [n.replace(' ','_') for n in tree.xpath('./system/name/text()')]
    return names


class PlanetCmd(cmd.Cmd):
    def __init__(self, tree):
        cmd.Cmd.__init__(self)
        self.prompt = '> '
        self.intro = "Exoplanet Explorer (type help, tab autocompletes commmands and system names):"
        self.system_names = system_names(tree)
        self.tree = tree

    def do_most_recent_planet(self, args):
        planet = extract.most_recent_planet(tree)
        print "Most recently updated planet is " + str(planet.find('name').text)
        print "  updated on " + planet.find('lastupdate').text
        print ""
        print planet.find('description').text

    def do_most_recent_system(self, args):
        print "Most recently updated system is:"
        most_recent = extract.most_recent_system(self.tree)
        print summarize_system(most_recent)

    def help_most_recent_system(self):
        print "Shows most recently updated system."
        
    def do_stats(self, args):
        print str(extract.num_tags(self.tree, 'system')) + " systems"
        print str(extract.num_tags(self.tree, 'star')) + " stars"
        print str(extract.num_tags(self.tree, 'binary')) + " binaries"
        print str(extract.num_tags(self.tree, 'planet')) + " planets"
        
    def do_largest_system(self, args):
        print "Largest system is:"
        largest = extract.largest_system(self.tree)
        #extract.write_tree(largest,'largest.xml')
        print summarize_system(largest)

    def help_largest_system(self):
        print "Shows summary of system with most plenets."

    def do_system(self, system_name):
        system = extract.find_system_by_name(self.tree, system_name)
        if system is None:
            print "Supply system name as argument, you can use tab to autocomplete."
        else:
            print summarize_system(system)

    def help_system(self):
        print "system <systen_name>"
        print "Will print system summary of supplied system, will autocomplete system names with tab."

    def do_random(self, args):
        system = extract.random_system(self.tree)
        print system.find('name').text
        print summarize_system(system)
        
    def help_random(self):
        print "Show random system"
        
    def do_tweet(self, system_name):
        system = extract.find_system_by_name(self.tree, system_name)
        if system is None:
            print "Supply system name as argument, you can use tab to autocomplete."
        else:
            print tweet_system(system)

    def help_tweet(self):
        print "Shows twitter compatible (140 character) view of system, could "
        print "be used to tweet new systems or that kind of thing, still in development."

    def complete_tweet(self, text, line, begidx, endidx):
        return self.complete_system(text, line, begidx, endidx)
    
    def complete_system(self, text, line, begidx, endidx):
        if not text:
            completions = self.system_names[:]
        else:
            completions = [ f
                            for f in self.system_names
                            if f.lower().startswith(text.lower())
                            ]
        return completions
        
    def do_exit(self, args):
        exit()
        

if __name__ == '__main__':
    url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
    tree = extract.get_tree(url)
    PlanetCmd(tree).cmdloop()
    

