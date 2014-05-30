Planets
=======

Commandline app for the Open Exoplanet Catalog.
http://www.openexoplanetcatalogue.com/

When you view a system it will show:
* key physical parameters.
* ascii art view of system with sol system symbols overlaid for scale.
* approriately colored spectral class

Requirements
------------

* pip install enum34
* pip install colorama (optional, but nice!)

Usage
-----

> python planets.py

Uses Python Cmd module to let you query exoplanet catalog.
Try:

> help

> system Alpha_Centauri

    Kepler-47 - RA:19h41m19s DEC:+46°55'13" 1189.0 pc / 3878.0 ly
    2 stars - 2 planets
    ☉                              ☿                          ♀                     
    *                                                                               
    A                                                                               
    *                                                                               
    B                                                                               
     
     A G 1.043M☉
     B G 0.362M☉
     (..) circumbinary planets:
         b      ?M♃  0.272R♃  0.296AU   49.51d   448.8K trn
         c      ?M♃  0.420R♃  0.989AU  303.16d   245.3K trn


> largest_system

    Largest system is:
    HD 10180 - RA:01h37m01s DEC:-60°30'42" 39.4 pc / 128.5 ly
    1 stars - 9 planets
    ☉        ☿       ♀     ⊕           ♂                                            
    *.o.o  o.   o                   o                                              @
     bcid  ej   f                   g                                              h
     
       G1V 1.06M☉
         b  1.300M⊕      ?R♃  0.022AU    1.18d  1915.3K rv
         c  0.041M♃      ?R♃  0.064AU    5.76d  1128.3K rv
       ? i  1.900M⊕      ?R♃  0.090AU    9.65d   950.0K rv
         d  0.037M♃      ?R♃  0.128AU   16.35d   796.3K rv
         e  0.079M♃      ?R♃  0.270AU   49.75d   549.9K rv
       ? j  5.099M⊕      ?R♃  0.330AU   67.55d   497.2K rv
         f  0.072M♃      ?R♃  0.494AU  122.88d   406.5K rv
         g  0.069M♃      ?R♃  1.415AU  596.00d   239.0K rv
         h  0.207M♃      ?R♃  3.490AU 2300.00d   154.9K rv



