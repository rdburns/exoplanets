ExoPlanets
==========

Commandline app for the Open Exoplanet Catalog.
http://www.openexoplanetcatalogue.com/

When you view a system it will show:
* key physical parameters.
* ascii art view of system with sol system symbols overlaid for scale.
* approriately colored spectral class

Setup
-----

This is under development, so I recommend you install it via GitHub,
rather than PyPi.

```bash
git clone git@github.com:rdburns/exoplanets.git
cd exoplanets
python setup.py install
```

Usage
-----

There are two entry points.

### Exosummary

This app shows the summary for one system. You can supply the
system name as an argument, no quotes required:

```bash
exosummary HD 10180
```

You can also get the most recently updated system, which can
be fun to put in your .bashrc when you open a new terminal:
```bash
exosummary --freshest
```

You can also pipe a system name directly into exosummary:
```bash
echo "HD 10180" | exosummary
```

### Exoplanet_browser

```bash
exoplanet_browser
```

This provides a more interactive way to browse the catalag.
You can display system summaries with auto-complete on system
names, which can be convenient. You can also display random systems,
and run other commands.

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

> system Kepler-229

```
Kepler-229 - RA:19h07m19s DEC:+48°22'32" 949.1 pc / 3095.6 ly
1 star - 3 planets
☉☿♀♂      ♃        ♄                 ⛢                    ♆
*           o                  o                                               o
            b                  c                                               d

    0.7940M☉  0.728R☉                      5120K
     c      ?M♃  0.448R♃            16.07d                        2014trn …
     d      ?M♃  0.351R♃            41.19d                        2014trn …
     b      ?M♃  0.200R♃             6.25d                        2014trn …
```
