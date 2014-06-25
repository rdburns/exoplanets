Planets
=======

Commandline app for the Open Exoplanet Catalog.
http://www.openexoplanetcatalogue.com/

When you view a system it will show:
* key physical parameters.
* ascii art view of system with sol system symbols overlaid for scale.
* approriately colored spectral class

Requirements4
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

    Alpha Centauri - RA:14h39m14s DEC:-60°50'14" 1.3 pc / 4.4 ly
    2 stars - 1 planets
    ☉ ☿ ♀⊕ ♂               ♃                  ♄                                     
    *                                                                               
    A                                                                               
    *.                                                                              
    Bb                                                                              
     
     A G2 V  1.105M☉  1.227R☉                      5790K 
     B K1 V  0.934M☉  0.865R☉                      5260K 
         b  1.130M⊕      ?R♃  0.040AU    3.23d                        2012rv …


> largest_system

    Largest system is:
    HD 10180 - RA:01h37m01s DEC:-60°30'42" 39.4 pc / 128.5 ly
    1 stars - 9 planets
    ☉        ☿       ♀     ⊕           ♂                                            
    *.o.o  o.   o                   o                                              @
    bcid  ej   f                   g                                              h

       G1V   1.06M☉      ?R☉                    5911.0K 0.08Z☉
         b  1.300M⊕      ?R♃  0.022AU    1.18d  1915.3K 𝑒=0.05        2010rv …
         c  0.041M♃      ?R♃  0.064AU    5.76d  1128.3K 𝑒=0.07        2010rv …
       ? i  1.900M⊕      ?R♃  0.090AU    9.65d   950.0K 𝑒=0.05        2010rv …
         d  0.037M♃      ?R♃  0.128AU   16.35d   796.3K 𝑒=0.11        2010rv …
         e  0.079M♃      ?R♃  0.270AU   49.75d   549.9K 𝑒=0.01        2010rv …
       ? j  5.099M⊕      ?R♃  0.330AU   67.55d   497.2K 𝑒=0.07        2010rv …
         f  0.072M♃      ?R♃  0.494AU  122.88d   406.5K 𝑒=0.13        2010rv …
         g  0.069M♃      ?R♃  1.415AU  596.00d   239.0K 𝑒=0.03        2010rv …
         h  0.207M♃      ?R♃  3.490AU 2300.00d   154.9K 𝑒=0.18        2010rv …

> system Kepler-47

    Kepler-47 - RA:19h41m19s DEC:+46°55'13" 1189.0 pc / 3878.0 ly
    2 stars - 2 planets
    ☉                              ☿                          ♀                     
    *                                                                               
    A                                                                               
    *                                                                               
    B                                                                               
     
     A G  1.043M☉  0.964R☉                      5636K 
     B G  0.362M☉ 0.3506R☉                      3357K 
     (..) circumbinary planets:
         b      ?M♃  0.272R♃  0.296AU   49.51d   448.8K        89.59° 2012trn …
         c      ?M♃  0.420R♃  0.989AU  303.16d   245.3K        89.83° 2012trn …
