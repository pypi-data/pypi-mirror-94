## About

This library encodes all of the information provided in the handouts Coefficient Data and Ephemeris_Meeus from ASEN 6008 (CU Boudler). This library was created in Spring 2021 when the course was taught by Professor Kate Davis.

## Installation

```
pip install asen_6008
```

## API

This library provides 10 classes (the 8 planets, Pluto, and the Sun) and 2 constants, AU and Days_per_year.

The classes are all instances of the class Planet which has the following layout (note this is pseudocode)

```
class Planet:
	L # deg
    a # AU
    e
    i #deg
    Omega # deg
    Pi  # deg
    mu  # km3/s2
    r # km
```

Elements L, a, e, i, Omega, and Pi are of type OrbitalElement which has the following layout
```
class OrbitalElement:
	a0
	a1
	a2
	a3
```

Elements mu and r are simply floating point values.

To access any of the data for a planet would look something like this

```
import asen_6008

print(asen_6008.Mars.L)
print(asen_6008.Earth.e.a1)
print(asen_6008.Sun.mu)
```

The names of all the classes and constants provided are listed below

```
AU
Days_per_year
Sun
Mercury
Venus
Earth
Mars
Jupiter
Saturn
Uranus
Neptune
Pluto
```

Also, both the Planet and OrbitalElement class have overridden the `__repr__` class attribute, so they can be printed directly, for example:

```
>>> import asen_6008
>>> print(asen_6008.Jupiter)
L (deg): 34.351484, 3034.9056746, -8.501e-05, 4e-09
a (AU): 5.202603191, 1.913e-07, 0, 0
e: 0.04849485, 0.000163244, -4.719e-07, -1.97e-09
i (deg): 1.30327, -0.0019872, 3.318e-05, 9.2e-08
Ω (deg): 100.464441, 0.1766828, 0.00090387, -7.032e-06
Π (deg): 14.331309, 0.2155525, 0.00072252, -4.59e-06
μ (km3/s2): 126686536.1
r (km): 71492
```


## Usage

Because the professor requested that no equations be placed in the library, only constants, the user will have to supply their own equations for calculating the ephemeris information as a function of time. There are many ways to do this, but one way which leads to a fairly clean API is to wrap the classes provided in your own class, like this

```
import asen_6008

class MyPlanet():
	def __init__(self, planet):
		self.planet = planet

	def e(self, t):
		return self.planet.e.a0 + self.planet.e.a1 * t + self.planet.e.a2 * t**2 + self.planet.e.a3 * t**3

Earth = MyPlanet(asen_6008.Earth)
Mars = MyPlanet(asen_6008.Mars)

print(Mars.e(some_julian_date))
```

You'll want to put this class and the instance of it in a separate file that you then import into your main Python project.

This way you can access various properties of the planet with a simple interface that accepts a time value. But you can also reach in directly to the underlying class provided by the asen_6008 library, as follows:

```
print(Earth.planet.e) # Here Earth is the same instance that was defined above.
```
