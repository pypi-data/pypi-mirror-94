#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 12:40:48 2021

@author: nbelakovski
"""

__version__ = "2.0.0"

AU = 1.49597870700e8 # km
Days_per_year =  365.242189


class OrbitalElement(object):
    def __init__(self, a0, a1, a2, a3):
        self.a0 = a0
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3

    def __repr__(self):
        return "{}, {}, {}, {}".format(self.a0, self.a1, self.a2, self.a3)


class Planet(object):
    def __init__(self, L, a, e, i, Omega, Pi, mu, r):
        self.L = L # deg
        self.a = a # AU
        self.e = e
        self.i = i #deg
        self.Omega = Omega # deg
        self.Pi = Pi # deg
        self.mu = mu # km3/s2
        self.r = r # km

    def __repr__(self):
        return '''L (deg): {}
a (AU): {}
e: {}
i (deg): {}
Ω (deg): {}
Π (deg): {}
μ (km3/s2): {}
r (km): {}'''.format(self.L, self.a, self.e, self.i, self.Omega, self.Pi, self.mu, self.r)


Sun = Planet(L=None,
                 a=None,
                 e=None,
                 i=None,
                 Omega=None,
                 Pi=None,
                 mu=1.32712440018e11,
                 r=None
                 )


Mercury = Planet(L=OrbitalElement(252.250906, 149472.6746358, -0.00000535, 0.000000002),
                 a=OrbitalElement(0.387098310, 0, 0, 0),
                 e=OrbitalElement(0.20563175, 0.000020406, -0.0000000284, -0.00000000017),
                 i=OrbitalElement(7.004986, -0.0059516, 0.00000081, 0.000000041),
                 Omega=OrbitalElement(48.330893, -0.1254229, -0.00008833, -0.000000196),
                 Pi=OrbitalElement(77.456119, 0.1588643, -0.00001343, 0.000000039),
                 # Values for mu and r for Mercury were not specified in the handout.
                 # Override them in your own code if you like

                 mu=None,
                 r=None
                 )

Venus = Planet(L=OrbitalElement(181.979801, 58517.8156760, 0.00000165, -0.000000002),
                 a=OrbitalElement(0.72332982, 0, 0, 0),
                 e=OrbitalElement(0.00677188, -0.000047766, 0.0000000975, 0.00000000044),
                 i=OrbitalElement(3.394662, -0.0008568, -0.00003244, 0.000000010),
                 Omega=OrbitalElement(76.679920, -0.2780080, -0.00014256, -0.000000198),
                 Pi=OrbitalElement(131.563707, 0.0048646, -0.00138232, -0.000005332),
                 mu=3.24858599e5,
                 r=6051.8
                 )


Earth = Planet(L=OrbitalElement(100.466449, 35999.3728519, -0.00000568, 0.0),
                 a=OrbitalElement(1.000001018, 0, 0, 0),
                 e=OrbitalElement(0.01670862, -0.000042037, -0.0000001236, 0.00000000004),
                 i=OrbitalElement(0, 0.0130546, -0.00000931, -0.000000034),
                 Omega=OrbitalElement(174.873174, -0.2410908, 0.00004067, -0.000001327),
                 Pi=OrbitalElement(102.937348, 0.3225557, 0.00015026, 0.000000478),
                 mu=3.98600433e5,
                 r=6378.14
                 )

Mars = Planet(L=OrbitalElement(355.433275, 19140.2993313, 0.00000261, -0.000000003),
                 a=OrbitalElement(1.523679342, 0, 0, 0),
                 e=OrbitalElement(0.09340062, 0.000090483, -0.0000000806, -0.00000000035),
                 i=OrbitalElement(1.849726, -0.0081479, -0.00002255, -0.000000027),
                 Omega=OrbitalElement(49.558093, -0.2949846, -0.00063993, -0.000002143),
                 Pi=OrbitalElement(336.060234, 0.4438898, -0.00017321, 0.000000300),
                 mu=4.28283100e4,
                 r=3396.19
                 )

Jupiter = Planet(L=OrbitalElement(34.351484, 3034.9056746, -0.00008501, 0.000000004),
                 a=OrbitalElement(5.202603191, 0.0000001913, 0, 0),
                 e=OrbitalElement(0.04849485, 0.000163244, -0.0000004719, -0.00000000197),
                 i=OrbitalElement(1.303270, -0.0019872, 0.00003318, 0.000000092),
                 Omega=OrbitalElement(100.464441, 0.1766828, 0.00090387, -0.000007032),
                 Pi=OrbitalElement(14.331309, 0.2155525, 0.00072252, -0.000004590),
                 mu=1.266865361e8,
                 r=71492
                 )




Saturn = Planet(L=OrbitalElement(50.077471, 1222.1137943, 0.00021004, -0.000000019),
                 a=OrbitalElement(9.554909596, -0.0000021389, 0, 0),
                 e=OrbitalElement(0.05550862, -0.000346818, -0.0000006456, 0.00000000338),
                 i=OrbitalElement(2.488878, 0.0025515, -0.00004903, 0.000000018),
                 Omega=OrbitalElement(113.665524, -0.2566649, -0.00018345, 0.000000357),
                 Pi=OrbitalElement(93.056787, 0.5665496, 0.00052809, 0.000004882),
                 mu=3.7931208e7,
                 r=60268
                 )



Uranus = Planet(L=OrbitalElement(314.055005, 429.8640561, 0.00030434, 0.000000026),
                 a=OrbitalElement(19.218446062, -0.0000000372, 0.00000000098, 0.0),
                 e=OrbitalElement(0.04629590, -0.000027337, 0.0000000790, 0.00000000025),
                 i=OrbitalElement(0.773196, 0.0007744, 0.00003749, -0.000000092),
                 Omega=OrbitalElement(74.005947, 0.5211258, 0.00133982, 0.000018516),
                 Pi=OrbitalElement(173.005159, 1.4863784, 0.0021450, 0.000000433),
                 mu=5.7939513e6,
                 r=25559
                 )



Neptune = Planet(L=OrbitalElement(304.348665, 219.8833092, 0.00030926, 0.000000018),
                 a=OrbitalElement(30.110386869, -0.0000001663, 0.00000000069, 0.0),
                 e=OrbitalElement(0.00898809, 0.000006408, -0.0000000008, -0.00000000005),
                 i=OrbitalElement(1.769952, -0.0093082, -0.00000708, 0.000000028),
                 Omega=OrbitalElement(131.784057, 1.1022057, 0.00026006, -0.000000636),
                 Pi=OrbitalElement(48.123691, 1.4262677, 0.00037918, -0.000000003),
                 mu=6.835100e6,
                 r=24764
                 )



Pluto = Planet(L=OrbitalElement(238.92903833, 145.20780515, 0.0, 0.0),
                 a=OrbitalElement(39.48211675, -0.00031596, 0.0, 0.0),
                 e=OrbitalElement(0.24882730, 0.00005170, 0.0, 0.0),
                 i=OrbitalElement(17.14001206, 0.00004818, 0.0, 0.0),
                 Omega=OrbitalElement(110.30393684, -0.01183482, 0.0, 0.0),
                 Pi=OrbitalElement(224.06891629, -0.04062942, 0.0, 0.0),
                 mu=8.71e2,
                 r=1188.3
                 )
