#!/usr/bin/env python
"""Open Exoplanet Catalog Explorer

Ryan Burns
rdburns@gmail.com
http://twitter.com/ryanburns
"""

import cmd
from pprint import pprint

from exoplanets import extract, formatters

# TODO
# There's something weird with the system name autocomplete


class PlanetCmd(cmd.Cmd):
    def __init__(self, tree):
        cmd.Cmd.__init__(self)
        self.prompt = '> '
        self.intro = "Exoplanet Explorer (type help, tab autocompletes commmands and system names):"
        self.system_names = formatters.system_names(tree)
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
        print formatters.summarize_system(most_recent)

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
        print formatters.summarize_system(largest)

    def help_largest_system(self):
        print "Shows summary of system with most plenets."

    def do_system(self, system_name):
        system = extract.find_system_by_name(self.tree, system_name)
        if system is None:
            print "Supply system name as argument, you can use tab to autocomplete."
        else:
            print formatters.summarize_system(system)

    def help_system(self):
        print "system <systen_name>"
        print "Will print system summary of supplied system, will autocomplete system names with tab."

    def do_random(self, args):
        system = extract.random_system(self.tree)
        print system.find('name').text
        print formatters.summarize_system(system)
        
    def help_random(self):
        print "Show random system"
        
    def do_tweet(self, system_name):
        system = extract.find_system_by_name(self.tree, system_name)
        if system is None:
            print "Supplyj system name as argument, you can use tab to autocomplete."
        else:
            print formatters.tweet_system(system)

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
    tree = extract.get_tree()
    PlanetCmd(tree).cmdloop()
    

