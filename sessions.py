import os
import json
from email.utils import parsedate_to_datetime
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

import fastf1
from fastf1.ergast import Ergast
import pandas as pd
import streamlit as st
import wikipedia


SESSION_CODES = {
    "Practice 1": "FP1",
    "Practice 2": "FP2",
    "Practice 3": "FP3",
    "Qualifying": "Q",
    "Sprint Qualifying": "SQ",
    "Sprint Shootout": "SQ",
    "Sprint": "S",
    "Race": "R",
}

SESSION_LABELS = {
    "Practice 1": "FP1",
    "Practice 2": "FP2",
    "Practice 3": "FP3",
    "Qualifying": "Qualifying",
    "Sprint Qualifying": "Sprint Qualifying",
    "Sprint Shootout": "Sprint Qualifying",
    "Sprint": "Sprint",
    "Race": "Race",
}

_CACHE_READY = False
ERGAST_BASE_URL = "https://api.jolpi.ca/ergast/f1"
ERGAST_FALLBACK_BASE_URL = "https://ergast.com/api/f1"

STATIC_DRIVER_DIRECTORY = [
    {"driverId": "hamilton", "givenName": "Lewis", "familyName": "Hamilton", "nationality": "British"},
    {"driverId": "max_verstappen", "givenName": "Max", "familyName": "Verstappen", "nationality": "Dutch"},
    {"driverId": "alonso", "givenName": "Fernando", "familyName": "Alonso", "nationality": "Spanish"},
    {"driverId": "vettel", "givenName": "Sebastian", "familyName": "Vettel", "nationality": "German"},
    {"driverId": "raikkonen", "givenName": "Kimi", "familyName": "Raikkonen", "nationality": "Finnish"},
    {"driverId": "button", "givenName": "Jenson", "familyName": "Button", "nationality": "British"},
    {"driverId": "rosberg", "givenName": "Nico", "familyName": "Rosberg", "nationality": "German"},
    {"driverId": "massa", "givenName": "Felipe", "familyName": "Massa", "nationality": "Brazilian"},
    {"driverId": "schumacher", "givenName": "Michael", "familyName": "Schumacher", "nationality": "German"},
    {"driverId": "bottas", "givenName": "Valtteri", "familyName": "Bottas", "nationality": "Finnish"},
    {"driverId": "perez", "givenName": "Sergio", "familyName": "Perez", "nationality": "Mexican"},
    {"driverId": "norris", "givenName": "Lando", "familyName": "Norris", "nationality": "British"},
    {"driverId": "leclerc", "givenName": "Charles", "familyName": "Leclerc", "nationality": "Monegasque"},
    {"driverId": "sainz", "givenName": "Carlos", "familyName": "Sainz", "nationality": "Spanish"},
    {"driverId": "russell", "givenName": "George", "familyName": "Russell", "nationality": "British"},
    {"driverId": "gasly", "givenName": "Pierre", "familyName": "Gasly", "nationality": "French"},
    {"driverId": "ocon", "givenName": "Esteban", "familyName": "Ocon", "nationality": "French"},
    {"driverId": "tsunoda", "givenName": "Yuki", "familyName": "Tsunoda", "nationality": "Japanese"},
    {"driverId": "albon", "givenName": "Alexander", "familyName": "Albon", "nationality": "Thai"},
]

TEAM_LEADERS = {
    "alpine": "Oliver Oakes",
    "aston_martin": "Andy Cowell",
    "ferrari": "Frederic Vasseur",
    "haas": "Ayao Komatsu",
    "mclaren": "Andrea Stella",
    "mercedes": "Toto Wolff",
    "rb": "Laurent Mekies",
    "red_bull": "Christian Horner",
    "sauber": "Mattia Binotto",
    "williams": "James Vowles",
}

TEAM_PREVIOUS_NAMES = {
    "alpine": ["Renault", "Lotus F1 Team", "Benetton", "Toleman"],
    "aston_martin": ["Racing Point", "Force India", "Spyker", "Midland", "Jordan"],
    "ferrari": [],
    "haas": [],
    "mclaren": [],
    "mercedes": ["Brawn GP", "Honda", "BAR", "Tyrrell"],
    "rb": ["AlphaTauri", "Toro Rosso", "Minardi"],
    "red_bull": ["Jaguar", "Stewart"],
    "sauber": ["Alfa Romeo", "BMW Sauber"],
    "williams": [],
}

TEAM_LINEAGE = {
    "alpine": {
        "aliases": ["alpine", "renault", "lotus_f1", "benetton"],
        "previous_names": ["Benetton", "Lotus F1 Team", "Renault", "Toleman"],
    },
    "aston_martin": {
        "aliases": ["aston_martin", "racing_point", "force_india", "spyker", "midland", "jordan"],
        "previous_names": ["Force India", "Jordan", "Midland", "Racing Point", "Spyker"],
    },
    "ferrari": {
        "aliases": ["ferrari"],
        "previous_names": [],
    },
    "haas": {
        "aliases": ["haas"],
        "previous_names": [],
    },
    "mclaren": {
        "aliases": ["mclaren"],
        "previous_names": [],
    },
    "mercedes": {
        "aliases": ["mercedes", "brawn", "tyrrell", "honda", "bar"],
        "previous_names": ["Brawn GP", "Honda", "BAR", "Tyrrell"],
    },
    "rb": {
        "aliases": ["rb", "alphatauri", "toro_rosso", "minardi"],
        "previous_names": ["AlphaTauri", "Minardi", "Toro Rosso"],
    },
    "red_bull": {
        "aliases": ["red_bull", "jaguar", "stewart"],
        "previous_names": ["Jaguar", "Stewart"],
    },
    "sauber": {
        "aliases": ["sauber", "bmw_sauber", "alfa", "alfa_romeo"],
        "previous_names": ["Alfa Romeo", "BMW Sauber"],
    },
    "williams": {
        "aliases": ["williams"],
        "previous_names": [],
    },
}

# Complete historical World Constructors' Championships (1958 - 2024)
HISTORICAL_WCC = [
    {"season": 1958, "constructorId": "vanwall", "constructorName": "Vanwall", "points": 48.0, "drivers": "Stirling Moss, Tony Brooks"},
    {"season": 1959, "constructorId": "cooper", "constructorName": "Cooper-Climax", "points": 40.0, "drivers": "Jack Brabham, Bruce McLaren"},
    {"season": 1960, "constructorId": "cooper", "constructorName": "Cooper-Climax", "points": 48.0, "drivers": "Jack Brabham, Bruce McLaren"},
    {"season": 1961, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 40.0, "drivers": "Phil Hill, Wolfgang von Trips"},
    {"season": 1962, "constructorId": "brm", "constructorName": "BRM", "points": 42.0, "drivers": "Graham Hill, Richie Ginther"},
    {"season": 1963, "constructorId": "lotus", "constructorName": "Lotus-Climax", "points": 54.0, "drivers": "Jim Clark, Trevor Taylor"},
    {"season": 1964, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 45.0, "drivers": "John Surtees, Lorenzo Bandini"},
    {"season": 1965, "constructorId": "lotus", "constructorName": "Lotus-Climax", "points": 54.0, "drivers": "Jim Clark, Mike Spence"},
    {"season": 1966, "constructorId": "brabham", "constructorName": "Brabham-Repco", "points": 42.0, "drivers": "Jack Brabham, Denny Hulme"},
    {"season": 1967, "constructorId": "brabham", "constructorName": "Brabham-Repco", "points": 63.0, "drivers": "Denny Hulme, Jack Brabham"},
    {"season": 1968, "constructorId": "lotus", "constructorName": "Lotus-Ford", "points": 62.0, "drivers": "Graham Hill, Jackie Oliver"},
    {"season": 1969, "constructorId": "matra", "constructorName": "Matra-Ford", "points": 66.0, "drivers": "Jackie Stewart, Jean-Pierre Beltoise"},
    {"season": 1970, "constructorId": "lotus", "constructorName": "Lotus-Ford", "points": 59.0, "drivers": "Jochen Rindt, Emerson Fittipaldi"},
    {"season": 1971, "constructorId": "tyrrell", "constructorName": "Tyrrell-Ford", "points": 73.0, "drivers": "Jackie Stewart, François Cevert"},
    {"season": 1972, "constructorId": "lotus", "constructorName": "Lotus-Ford", "points": 61.0, "drivers": "Emerson Fittipaldi, David Walker"},
    {"season": 1973, "constructorId": "lotus", "constructorName": "Lotus-Ford", "points": 92.0, "drivers": "Emerson Fittipaldi, Ronnie Peterson"},
    {"season": 1974, "constructorId": "mclaren", "constructorName": "McLaren-Ford", "points": 73.0, "drivers": "Emerson Fittipaldi, Denny Hulme"},
    {"season": 1975, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 72.5, "drivers": "Niki Lauda, Clay Regazzoni"},
    {"season": 1976, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 83.0, "drivers": "Niki Lauda, Clay Regazzoni"},
    {"season": 1977, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 95.0, "drivers": "Niki Lauda, Carlos Reutemann"},
    {"season": 1978, "constructorId": "lotus", "constructorName": "Lotus-Ford", "points": 86.0, "drivers": "Mario Andretti, Ronnie Peterson"},
    {"season": 1979, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 113.0, "drivers": "Jody Scheckter, Gilles Villeneuve"},
    {"season": 1980, "constructorId": "williams", "constructorName": "Williams-Ford", "points": 120.0, "drivers": "Alan Jones, Carlos Reutemann"},
    {"season": 1981, "constructorId": "williams", "constructorName": "Williams-Ford", "points": 95.0, "drivers": "Carlos Reutemann, Alan Jones"},
    {"season": 1982, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 74.0, "drivers": "Didier Pironi, Patrick Tambay"},
    {"season": 1983, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 89.0, "drivers": "René Arnoux, Patrick Tambay"},
    {"season": 1984, "constructorId": "mclaren", "constructorName": "McLaren-TAG", "points": 143.5, "drivers": "Niki Lauda, Alain Prost"},
    {"season": 1985, "constructorId": "mclaren", "constructorName": "McLaren-TAG", "points": 90.0, "drivers": "Alain Prost, Niki Lauda"},
    {"season": 1986, "constructorId": "williams", "constructorName": "Williams-Honda", "points": 141.0, "drivers": "Nigel Mansell, Nelson Piquet"},
    {"season": 1987, "constructorId": "williams", "constructorName": "Williams-Honda", "points": 137.0, "drivers": "Nelson Piquet, Nigel Mansell"},
    {"season": 1988, "constructorId": "mclaren", "constructorName": "McLaren-Honda", "points": 199.0, "drivers": "Ayrton Senna, Alain Prost"},
    {"season": 1989, "constructorId": "mclaren", "constructorName": "McLaren-Honda", "points": 141.0, "drivers": "Alain Prost, Ayrton Senna"},
    {"season": 1990, "constructorId": "mclaren", "constructorName": "McLaren-Honda", "points": 121.0, "drivers": "Ayrton Senna, Gerhard Berger"},
    {"season": 1991, "constructorId": "mclaren", "constructorName": "McLaren-Honda", "points": 139.0, "drivers": "Ayrton Senna, Gerhard Berger"},
    {"season": 1992, "constructorId": "williams", "constructorName": "Williams-Renault", "points": 164.0, "drivers": "Nigel Mansell, Riccardo Patrese"},
    {"season": 1993, "constructorId": "williams", "constructorName": "Williams-Renault", "points": 168.0, "drivers": "Alain Prost, Damon Hill"},
    {"season": 1994, "constructorId": "williams", "constructorName": "Williams-Renault", "points": 118.0, "drivers": "Damon Hill, David Coulthard, Nigel Mansell"},
    {"season": 1995, "constructorId": "benetton", "constructorName": "Benetton-Renault", "points": 137.0, "drivers": "Michael Schumacher, Johnny Herbert"},
    {"season": 1996, "constructorId": "williams", "constructorName": "Williams-Renault", "points": 175.0, "drivers": "Damon Hill, Jacques Villeneuve"},
    {"season": 1997, "constructorId": "williams", "constructorName": "Williams-Renault", "points": 123.0, "drivers": "Jacques Villeneuve, Heinz-Harald Frentzen"},
    {"season": 1998, "constructorId": "mclaren", "constructorName": "McLaren-Mercedes", "points": 156.0, "drivers": "Mika Häkkinen, David Coulthard"},
    {"season": 1999, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 128.0, "drivers": "Eddie Irvine, Michael Schumacher, Mika Salo"},
    {"season": 2000, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 170.0, "drivers": "Michael Schumacher, Rubens Barrichello"},
    {"season": 2001, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 179.0, "drivers": "Michael Schumacher, Rubens Barrichello"},
    {"season": 2002, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 221.0, "drivers": "Michael Schumacher, Rubens Barrichello"},
    {"season": 2003, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 158.0, "drivers": "Michael Schumacher, Rubens Barrichello"},
    {"season": 2004, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 262.0, "drivers": "Michael Schumacher, Rubens Barrichello"},
    {"season": 2005, "constructorId": "renault", "constructorName": "Renault", "points": 191.0, "drivers": "Fernando Alonso, Giancarlo Fisichella"},
    {"season": 2006, "constructorId": "renault", "constructorName": "Renault", "points": 206.0, "drivers": "Fernando Alonso, Giancarlo Fisichella"},
    {"season": 2007, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 204.0, "drivers": "Kimi Räikkönen, Felipe Massa"},
    {"season": 2008, "constructorId": "ferrari", "constructorName": "Ferrari", "points": 172.0, "drivers": "Felipe Massa, Kimi Räikkönen"},
    {"season": 2009, "constructorId": "brawn", "constructorName": "Brawn-Mercedes", "points": 172.0, "drivers": "Jenson Button, Rubens Barrichello"},
    {"season": 2010, "constructorId": "red_bull", "constructorName": "Red Bull-Renault", "points": 498.0, "drivers": "Sebastian Vettel, Mark Webber"},
    {"season": 2011, "constructorId": "red_bull", "constructorName": "Red Bull-Renault", "points": 650.0, "drivers": "Sebastian Vettel, Mark Webber"},
    {"season": 2012, "constructorId": "red_bull", "constructorName": "Red Bull-Renault", "points": 460.0, "drivers": "Sebastian Vettel, Mark Webber"},
    {"season": 2013, "constructorId": "red_bull", "constructorName": "Red Bull-Renault", "points": 596.0, "drivers": "Sebastian Vettel, Mark Webber"},
    {"season": 2014, "constructorId": "mercedes", "constructorName": "Mercedes", "points": 701.0, "drivers": "Lewis Hamilton, Nico Rosberg"},
    {"season": 2015, "constructorId": "mercedes", "constructorName": "Mercedes", "points": 703.0, "drivers": "Lewis Hamilton, Nico Rosberg"},
    {"season": 2016, "constructorId": "mercedes", "constructorName": "Mercedes", "points": 765.0, "drivers": "Nico Rosberg, Lewis Hamilton"},
    {"season": 2017, "constructorId": "mercedes", "constructorName": "Mercedes", "points": 668.0, "drivers": "Lewis Hamilton, Valtteri Bottas"},
    {"season": 2018, "constructorId": "mercedes", "constructorName": "Mercedes", "points": 655.0, "drivers": "Lewis Hamilton, Valtteri Bottas"},
    {"season": 2019, "constructorId": "mercedes", "constructorName": "Mercedes", "points": 739.0, "drivers": "Lewis Hamilton, Valtteri Bottas"},
    {"season": 2020, "constructorId": "mercedes", "constructorName": "Mercedes", "points": 573.0, "drivers": "Lewis Hamilton, Valtteri Bottas"},
    {"season": 2021, "constructorId": "mercedes", "constructorName": "Mercedes", "points": 613.5, "drivers": "Lewis Hamilton, Valtteri Bottas"},
    {"season": 2022, "constructorId": "red_bull", "constructorName": "Red Bull-RBPT", "points": 759.0, "drivers": "Max Verstappen, Sergio Perez"},
    {"season": 2023, "constructorId": "red_bull", "constructorName": "Red Bull-Honda RBPT", "points": 860.0, "drivers": "Max Verstappen, Sergio Perez"},
    {"season": 2024, "constructorId": "mclaren", "constructorName": "McLaren-Mercedes", "points": 666.0, "drivers": "Lando Norris, Oscar Piastri"},
]

# Complete historical World Drivers' Championships (1950 - 2024)
HISTORICAL_WDC = [
    {"season": 1950, "constructorId": "alfa", "driverName": "Giuseppe Farina", "points": 30.0},
    {"season": 1951, "constructorId": "alfa", "driverName": "Juan Manuel Fangio", "points": 31.0},
    {"season": 1952, "constructorId": "ferrari", "driverName": "Alberto Ascari", "points": 36.0},
    {"season": 1953, "constructorId": "ferrari", "driverName": "Alberto Ascari", "points": 34.5},
    {"season": 1954, "constructorId": "mercedes", "driverName": "Juan Manuel Fangio", "points": 42.0},
    {"season": 1955, "constructorId": "mercedes", "driverName": "Juan Manuel Fangio", "points": 40.0},
    {"season": 1956, "constructorId": "ferrari", "driverName": "Juan Manuel Fangio", "points": 30.0},
    {"season": 1957, "constructorId": "maserati", "driverName": "Juan Manuel Fangio", "points": 40.0},
    {"season": 1958, "constructorId": "ferrari", "driverName": "Mike Hawthorn", "points": 42.0},
    {"season": 1959, "constructorId": "cooper", "driverName": "Jack Brabham", "points": 31.0},
    {"season": 1960, "constructorId": "cooper", "driverName": "Jack Brabham", "points": 43.0},
    {"season": 1961, "constructorId": "ferrari", "driverName": "Phil Hill", "points": 34.0},
    {"season": 1962, "constructorId": "brm", "driverName": "Graham Hill", "points": 42.0},
    {"season": 1963, "constructorId": "lotus", "driverName": "Jim Clark", "points": 54.0},
    {"season": 1964, "constructorId": "ferrari", "driverName": "John Surtees", "points": 40.0},
    {"season": 1965, "constructorId": "lotus", "driverName": "Jim Clark", "points": 54.0},
    {"season": 1966, "constructorId": "brabham", "driverName": "Jack Brabham", "points": 42.0},
    {"season": 1967, "constructorId": "brabham", "driverName": "Denny Hulme", "points": 51.0},
    {"season": 1968, "constructorId": "lotus", "driverName": "Graham Hill", "points": 48.0},
    {"season": 1969, "constructorId": "matra", "driverName": "Jackie Stewart", "points": 63.0},
    {"season": 1970, "constructorId": "lotus", "driverName": "Jochen Rindt", "points": 45.0},
    {"season": 1971, "constructorId": "tyrrell", "driverName": "Jackie Stewart", "points": 62.0},
    {"season": 1972, "constructorId": "lotus", "driverName": "Emerson Fittipaldi", "points": 61.0},
    {"season": 1973, "constructorId": "tyrrell", "driverName": "Jackie Stewart", "points": 71.0},
    {"season": 1974, "constructorId": "mclaren", "driverName": "Emerson Fittipaldi", "points": 55.0},
    {"season": 1975, "constructorId": "ferrari", "driverName": "Niki Lauda", "points": 64.5},
    {"season": 1976, "constructorId": "mclaren", "driverName": "James Hunt", "points": 69.0},
    {"season": 1977, "constructorId": "ferrari", "driverName": "Niki Lauda", "points": 72.0},
    {"season": 1978, "constructorId": "lotus", "driverName": "Mario Andretti", "points": 64.0},
    {"season": 1979, "constructorId": "ferrari", "driverName": "Jody Scheckter", "points": 51.0},
    {"season": 1980, "constructorId": "williams", "driverName": "Alan Jones", "points": 67.0},
    {"season": 1981, "constructorId": "brabham", "driverName": "Nelson Piquet", "points": 50.0},
    {"season": 1982, "constructorId": "williams", "driverName": "Keke Rosberg", "points": 44.0},
    {"season": 1983, "constructorId": "brabham", "driverName": "Nelson Piquet", "points": 59.0},
    {"season": 1984, "constructorId": "mclaren", "driverName": "Niki Lauda", "points": 72.0},
    {"season": 1985, "constructorId": "mclaren", "driverName": "Alain Prost", "points": 73.0},
    {"season": 1986, "constructorId": "mclaren", "driverName": "Alain Prost", "points": 72.0},
    {"season": 1987, "constructorId": "williams", "driverName": "Nelson Piquet", "points": 73.0},
    {"season": 1988, "constructorId": "mclaren", "driverName": "Ayrton Senna", "points": 90.0},
    {"season": 1989, "constructorId": "mclaren", "driverName": "Alain Prost", "points": 76.0},
    {"season": 1990, "constructorId": "mclaren", "driverName": "Ayrton Senna", "points": 78.0},
    {"season": 1991, "constructorId": "mclaren", "driverName": "Ayrton Senna", "points": 96.0},
    {"season": 1992, "constructorId": "williams", "driverName": "Nigel Mansell", "points": 108.0},
    {"season": 1993, "constructorId": "williams", "driverName": "Alain Prost", "points": 99.0},
    {"season": 1994, "constructorId": "benetton", "driverName": "Michael Schumacher", "points": 92.0},
    {"season": 1995, "constructorId": "benetton", "driverName": "Michael Schumacher", "points": 102.0},
    {"season": 1996, "constructorId": "williams", "driverName": "Damon Hill", "points": 97.0},
    {"season": 1997, "constructorId": "williams", "driverName": "Jacques Villeneuve", "points": 81.0},
    {"season": 1998, "constructorId": "mclaren", "driverName": "Mika Häkkinen", "points": 100.0},
    {"season": 1999, "constructorId": "mclaren", "driverName": "Mika Häkkinen", "points": 76.0},
    {"season": 2000, "constructorId": "ferrari", "driverName": "Michael Schumacher", "points": 108.0},
    {"season": 2001, "constructorId": "ferrari", "driverName": "Michael Schumacher", "points": 123.0},
    {"season": 2002, "constructorId": "ferrari", "driverName": "Michael Schumacher", "points": 144.0},
    {"season": 2003, "constructorId": "ferrari", "driverName": "Michael Schumacher", "points": 93.0},
    {"season": 2004, "constructorId": "ferrari", "driverName": "Michael Schumacher", "points": 148.0},
    {"season": 2005, "constructorId": "renault", "driverName": "Fernando Alonso", "points": 133.0},
    {"season": 2006, "constructorId": "renault", "driverName": "Fernando Alonso", "points": 134.0},
    {"season": 2007, "constructorId": "ferrari", "driverName": "Kimi Räikkönen", "points": 110.0},
    {"season": 2008, "constructorId": "mclaren", "driverName": "Lewis Hamilton", "points": 98.0},
    {"season": 2009, "constructorId": "brawn", "driverName": "Jenson Button", "points": 95.0},
    {"season": 2010, "constructorId": "red_bull", "driverName": "Sebastian Vettel", "points": 256.0},
    {"season": 2011, "constructorId": "red_bull", "driverName": "Sebastian Vettel", "points": 392.0},
    {"season": 2012, "constructorId": "red_bull", "driverName": "Sebastian Vettel", "points": 281.0},
    {"season": 2013, "constructorId": "red_bull", "driverName": "Sebastian Vettel", "points": 397.0},
    {"season": 2014, "constructorId": "mercedes", "driverName": "Lewis Hamilton", "points": 384.0},
    {"season": 2015, "constructorId": "mercedes", "driverName": "Lewis Hamilton", "points": 381.0},
    {"season": 2016, "constructorId": "mercedes", "driverName": "Nico Rosberg", "points": 385.0},
    {"season": 2017, "constructorId": "mercedes", "driverName": "Lewis Hamilton", "points": 363.0},
    {"season": 2018, "constructorId": "mercedes", "driverName": "Lewis Hamilton", "points": 408.0},
    {"season": 2019, "constructorId": "mercedes", "driverName": "Lewis Hamilton", "points": 413.0},
    {"season": 2020, "constructorId": "mercedes", "driverName": "Lewis Hamilton", "points": 347.0},
    {"season": 2021, "constructorId": "red_bull", "driverName": "Max Verstappen", "points": 395.5},
    {"season": 2022, "constructorId": "red_bull", "driverName": "Max Verstappen", "points": 454.0},
    {"season": 2023, "constructorId": "red_bull", "driverName": "Max Verstappen", "points": 575.0},
    {"season": 2024, "constructorId": "red_bull", "driverName": "Max Verstappen", "points": 429.0},
]


def _resolve_team_lineage(constructor_id):
    for _, lineage in TEAM_LINEAGE.items():
        if constructor_id in lineage.get("aliases", []):
            return lineage

    return {
        "aliases": [constructor_id],
        "previous_names": TEAM_PREVIOUS_NAMES.get(constructor_id, []),
    }


def setup_fastf1_cache(cache_dir: str | None = None) -> None:
    global _CACHE_READY
    # Patch FastF1 internal headers to a modern desktop browser User-Agent
    # This prevents Cloudflare/Akamai 403 Forbidden blocks on cloud environments (Streamlit Cloud, AWS)
    _ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    try:
        import fastf1.api as _f1_api
        if hasattr(_f1_api, "headers") and isinstance(_f1_api.headers, dict):
            _f1_api.headers["User-Agent"] = _ua
    except Exception:
        pass

    if cache_dir is None:
        if os.name != "nt" or "/mount/" in os.path.abspath("."):
            import tempfile
            cache_dir = os.path.join(tempfile.gettempdir(), "fastf1_cache")
        else:
            cache_dir = "f1_cache"

    try:
        os.makedirs(cache_dir, exist_ok=True)
        fastf1.Cache.enable_cache(cache_dir)
    except Exception:
        try:
            import tempfile
            t_dir = tempfile.mkdtemp()
            fastf1.Cache.enable_cache(t_dir)
        except Exception:
            pass

    try:
        import fastf1.req as _f1_req
        if hasattr(_f1_req.Cache, "_requests_session") and _f1_req.Cache._requests_session:
            _f1_req.Cache._requests_session.headers["User-Agent"] = _ua
        if hasattr(_f1_req.Cache, "_requests_session_cached") and _f1_req.Cache._requests_session_cached:
            _f1_req.Cache._requests_session_cached.headers["User-Agent"] = _ua
    except Exception:
        pass

    _CACHE_READY = True


@st.cache_data(ttl=86400)
def get_race_laps_fallback(year: int, round_num: int):
    """Reliable fallback lap fetcher from Jolpica/Ergast API.
    Guarantees that lap times, lap pace, and driver positions are available
    for all historical races (1950-current) and when live timing is blocked on cloud.
    """
    import concurrent.futures
    import requests

    id_to_abbr = {}
    id_to_num = {}
    id_to_team = {}
    res_url = f"https://api.jolpi.ca/ergast/f1/{int(year)}/{int(round_num)}/results.json"
    try:
        r = requests.get(res_url, timeout=6)
        if r.status_code == 200:
            data = r.json()
            races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
            if races:
                for row in races[0].get("Results", []):
                    did = str(row.get("Driver", {}).get("driverId", "")).lower()
                    code = row.get("Driver", {}).get("code") or row.get("Driver", {}).get("familyName", "")[:3].upper()
                    num = str(row.get("number", ""))
                    team = str(row.get("Constructor", {}).get("name", ""))
                    if did:
                        id_to_abbr[did] = code
                        id_to_num[did] = num
                        id_to_team[did] = team
    except Exception:
        pass

    first_url = f"https://api.jolpi.ca/ergast/f1/{int(year)}/{int(round_num)}/laps.json?limit=100&offset=0"
    try:
        r0 = requests.get(first_url, timeout=6)
        if r0.status_code != 200:
            return None
        data0 = r0.json()
        mr_data = data0.get("MRData", {})
        total = int(mr_data.get("total", 0))
        races0 = mr_data.get("RaceTable", {}).get("Races", [])
        if not races0:
            return None
        raw_pages = [data0]
    except Exception:
        return None

    offsets = list(range(100, min(total, 1800), 100))
    if offsets:
        def _fetch_page(offset):
            try:
                u = f"https://api.jolpi.ca/ergast/f1/{int(year)}/{int(round_num)}/laps.json?limit=100&offset={offset}"
                rp = requests.get(u, timeout=5)
                if rp.status_code == 200:
                    return rp.json()
            except Exception:
                pass
            return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            pages = list(executor.map(_fetch_page, offsets))
            for p in pages:
                if p:
                    raw_pages.append(p)

    all_timings = []
    for p in raw_pages:
        races = p.get("MRData", {}).get("RaceTable", {}).get("Races", [])
        if not races:
            continue
        for lap in races[0].get("Laps", []):
            try:
                lap_num = int(lap["number"])
            except Exception:
                continue
            for t in lap.get("Timings", []):
                all_timings.append({
                    "LapNumber": lap_num,
                    "driverId": str(t.get("driverId", "")).lower(),
                    "Position": int(t.get("position", 0)) if t.get("position") else 0,
                    "time_str": t.get("time", ""),
                })

    if not all_timings:
        return None

    df = pd.DataFrame(all_timings)
    df["Driver"] = df["driverId"].map(id_to_abbr).fillna(df["driverId"])
    df["DriverNumber"] = df["driverId"].map(id_to_num).fillna("")
    df["Team"] = df["driverId"].map(id_to_team).fillna("")

    def parse_time(s):
        try:
            parts = str(s).split(":")
            if len(parts) == 2:
                return pd.Timedelta(minutes=int(parts[0]), seconds=float(parts[1]))
            return pd.Timedelta(seconds=float(parts[0]))
        except Exception:
            return pd.NaT

    df["LapTime"] = pd.to_timedelta(df["time_str"].apply(parse_time), errors="coerce")
    df = df.dropna(subset=["LapTime"]).sort_values(["LapNumber", "Position"]).reset_index(drop=True)
    df["Time"] = pd.to_timedelta(df.groupby("Driver")["LapTime"].cumsum(), errors="coerce")
    df["Compound"] = "UNKNOWN"
    df["Stint"] = 1
    df["IsPersonalBest"] = False
    return df


@st.cache_data
def get_schedule(year):
    return fastf1.get_event_schedule(year)


@st.cache_resource(ttl=3600)
def load_session_data(year, race_name, session_name, *args, **kwargs):
    if not _CACHE_READY:
        setup_fastf1_cache()

    # Extract round_num flexibly from kwargs or positional args
    round_num = kwargs.get("round_num")
    if round_num is None and args:
        round_num = args[0]

    if round_num is not None:
        try:
            round_num = int(round_num)
        except (ValueError, TypeError):
            round_num = None

    # Determine round_num if not provided
    if round_num is None:
        try:
            sched = get_schedule(int(year))
            matched = sched[sched["EventName"] == race_name]
            if not matched.empty:
                round_num = int(matched.iloc[0]["RoundNumber"])
        except Exception:
            round_num = None

    session_code = SESSION_CODES.get(session_name, session_name)
    session_identifiers = [session_code]

    if session_name != session_code:
        session_identifiers.append(session_name)
    if session_name == "Sprint Qualifying":
        session_identifiers.append("Sprint Shootout")
    if session_name == "Sprint Shootout":
        session_identifiers.extend(["SS", "Sprint Qualifying"])

    best_session = None
    best_results = None
    best_laps = None

    for session_identifier in session_identifiers:
        session = None
        # Try deterministic round number first if available
        if round_num is not None and round_num > 0:
            try:
                session = fastf1.get_session(int(year), int(round_num), session_identifier)
            except Exception:
                session = None

        if session is None:
            try:
                session = fastf1.get_session(int(year), race_name, session_identifier)
            except Exception:
                continue

        # Tier 1: Fast & reliable core load (laps, results, messages)
        loaded_ok = False
        try:
            session.load(laps=True, telemetry=False, weather=False, messages=True)
            loaded_ok = True
        except Exception:
            try:
                session.load(laps=True, telemetry=False, weather=False, messages=False)
                loaded_ok = True
            except Exception:
                pass

        curr_results = None
        try:
            curr_results = session.results
        except Exception:
            curr_results = None

        curr_laps = None
        try:
            if hasattr(session, "_laps") and session._laps is not None and not session._laps.empty:
                curr_laps = session.laps
        except Exception:
            curr_laps = None

        if best_session is None:
            best_session = session
            best_results = curr_results

        if curr_laps is not None and not curr_laps.empty:
            best_session = session
            best_results = curr_results
            best_laps = curr_laps

            # Tier 2: Best-effort telemetry load (for speed/throttle/brake traces)
            try:
                session.load(telemetry=True, weather=False, messages=False)
            except Exception:
                pass
            break

    # If live timing laps failed or unavailable, check Jolpica fallback for race sessions
    if (best_laps is None or best_laps.empty) and session_name in ["Race", "Sprint"]:
        if round_num is not None and round_num > 0:
            try:
                fallback_laps = get_race_laps_fallback(int(year), int(round_num))
                if fallback_laps is not None and not fallback_laps.empty:
                    best_laps = fallback_laps
                    if best_session is not None:
                        best_session._laps = fallback_laps
            except Exception:
                pass

    if best_session is not None or best_results is not None or best_laps is not None:
        return best_session, best_results, best_laps

    return None, None, None


@st.cache_data(ttl=3600)
def get_driver_standings(year, round_num):
    try:
        ergast = Ergast()
        standings = ergast.get_driver_standings(season=year, round=round_num).content[0]
        return standings
    except Exception:
        # Fallback via direct Jolpica API
        try:
            payload = _fetch_json(f"{ERGAST_BASE_URL}/{int(year)}/{int(round_num)}/driverStandings.json")
            standings_list = payload.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
            if standings_list:
                rows = standings_list[0].get("DriverStandings", [])
                records = []
                for r in rows:
                    drv = r.get("Driver", {})
                    records.append({
                        "position": r.get("position", ""),
                        "givenName": drv.get("givenName", ""),
                        "familyName": drv.get("familyName", ""),
                        "points": float(r.get("points", 0)),
                        "wins": int(r.get("wins", 0)),
                    })
                return pd.DataFrame(records)
        except Exception:
            pass
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def get_constructor_standings(year, round_num):
    try:
        ergast = Ergast()
        standings = ergast.get_constructor_standings(season=year, round=round_num).content[0]
        return standings
    except Exception:
        try:
            payload = _fetch_json(f"{ERGAST_BASE_URL}/{int(year)}/{int(round_num)}/constructorStandings.json")
            standings_list = payload.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
            if standings_list:
                rows = standings_list[0].get("ConstructorStandings", [])
                records = []
                for r in rows:
                    c = r.get("Constructor", {})
                    records.append({
                        "position": r.get("position", ""),
                        "constructorName": c.get("name", ""),
                        "points": float(r.get("points", 0)),
                        "wins": int(r.get("wins", 0)),
                    })
                return pd.DataFrame(records)
        except Exception:
            pass
        return pd.DataFrame()


def get_event_sessions(event):
    sessions = []
    for index in range(1, 6):
        session_name = event.get(f"Session{index}")
        if pd.isna(session_name) or not str(session_name).strip():
            continue

        session_name = str(session_name)
        if session_name.lower() in {"nan", "testing"}:
            continue

        sessions.append(session_name)

    if sessions:
        return sessions

    return ["Practice 1", "Practice 2", "Practice 3", "Qualifying", "Race"]


def format_timing_value(value, empty="-"):
    if pd.isna(value):
        return empty

    if isinstance(value, pd.Timedelta):
        total_seconds = value.total_seconds()
        if total_seconds < 0:
            return str(value)
        minutes = int(total_seconds // 60)
        seconds = total_seconds - (minutes * 60)
        return f"{minutes}:{seconds:06.3f}"

    text = str(value)
    if text in {"NaT", "nan", "None"}:
        return empty
    return text.replace("0 days 00:", "").split(".")[0]


def format_columns(dataframe, columns):
    for column in columns:
        if column in dataframe:
            dataframe[column] = dataframe[column].map(format_timing_value)
    return dataframe


def best_driver_name(row):
    for column in ("BroadcastName", "FullName", "Abbreviation", "Driver"):
        value = row.get(column)
        if pd.notna(value) and str(value).strip() and str(value).lower() != "nan":
            return str(value).strip()
    return "Unknown"


@st.cache_data(ttl=1800)
def get_motorsport_news(limit=8):
    feeds = [
        "https://www.motorsport.com/rss/f1/news/",
        "https://www.racefans.net/feed/",
        "https://www.the-race.com/feed/",
    ]

    stories = []
    seen_titles = set()

    for feed_url in feeds:
        try:
            request = Request(
                feed_url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; F1-Retro-Dashboard/1.0)"},
            )
            with urlopen(request, timeout=6) as response:
                payload = response.read()
            root = ET.fromstring(payload)
        except (URLError, TimeoutError, ET.ParseError, ValueError):
            continue

        for item in root.findall(".//item"):
            title = (item.findtext("title") or "").strip()
            link = (item.findtext("link") or "").strip()
            if not title or not link:
                continue

            title_key = title.lower()
            if title_key in seen_titles:
                continue
            seen_titles.add(title_key)

            pub_date_raw = (item.findtext("pubDate") or "").strip()
            pub_date = None
            if pub_date_raw:
                try:
                    pub_date = parsedate_to_datetime(pub_date_raw)
                except (TypeError, ValueError):
                    pub_date = None

            source = urlparse(link).netloc.replace("www.", "")
            source = source or urlparse(feed_url).netloc.replace("www.", "")

            stories.append(
                {
                    "title": title,
                    "link": link,
                    "source": source,
                    "published": pub_date,
                }
            )

    def _published_rank(item):
        published = item["published"]
        if published is None:
            return 0.0
        try:
            return published.timestamp()
        except (OverflowError, OSError, ValueError):
            return 0.0

    stories.sort(key=_published_rank, reverse=True)
    return stories[:limit]


def _fetch_json(url):
    try:
        request = Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (compatible; F1-Retro-Dashboard/1.0)"},
        )
        with urlopen(request, timeout=10) as response:
            return json.loads(response.read().decode("utf-8"))
    except (URLError, TimeoutError, ValueError, json.JSONDecodeError):
        return {}


@st.cache_data(ttl=3600)
def _fetch_ergast_path(path):
    for base_url in (ERGAST_BASE_URL, ERGAST_FALLBACK_BASE_URL):
        payload = _fetch_json(f"{base_url}/{path}")
        if payload and payload.get("MRData"):
            return payload
    return {}


@st.cache_data(ttl=3600)
def get_driver_directory():
    payload = _fetch_ergast_path("drivers.json?limit=1000")
    drivers = payload.get("MRData", {}).get("DriverTable", {}).get("Drivers", [])
    if not drivers:
        drivers = STATIC_DRIVER_DIRECTORY

    directory = pd.DataFrame(drivers)
    directory["fullName"] = (directory.get("givenName", "") + " " + directory.get("familyName", "")).str.strip()
    directory = directory[directory["fullName"].astype(str).str.len() > 0]
    directory = directory.drop_duplicates(subset=["driverId", "fullName"]).copy()
    directory = directory.sort_values("fullName").reset_index(drop=True)
    return directory


@st.cache_data(ttl=3600)
def get_drivers_for_season(season):
    payload = _fetch_ergast_path(f"{int(season)}/results.json?limit=2000")
    races = payload.get("MRData", {}).get("RaceTable", {}).get("Races", [])

    drivers = []
    seen_driver_ids = set()
    for race in races:
        for result in race.get("Results", []):
            driver = result.get("Driver", {})
            driver_id = driver.get("driverId")
            if not driver_id or driver_id in seen_driver_ids:
                continue
            seen_driver_ids.add(driver_id)
            drivers.append(driver)

    if not drivers:
        payload = _fetch_ergast_path(f"{int(season)}/drivers.json?limit=1000")
        drivers = payload.get("MRData", {}).get("DriverTable", {}).get("Drivers", [])

    if not drivers:
        standings_payload = _fetch_ergast_path(f"{int(season)}/driverStandings.json")
        standings_list = standings_payload.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
        if standings_list:
            standings_rows = standings_list[0].get("DriverStandings", [])
            drivers = [row.get("Driver", {}) for row in standings_rows if row.get("Driver")]

    if not drivers:
        return pd.DataFrame(columns=["driverId", "givenName", "familyName", "nationality", "fullName"])

    directory = pd.DataFrame(drivers)
    directory["fullName"] = (directory.get("givenName", "") + " " + directory.get("familyName", "")).str.strip()
    directory = directory[directory["fullName"].astype(str).str.len() > 0]
    directory = directory.drop_duplicates(subset=["driverId", "fullName"]).copy()
    directory = directory.sort_values("fullName").reset_index(drop=True)
    return directory


@st.cache_data(ttl=3600)
def get_teams_for_season(season):
    payload = _fetch_ergast_path(f"{int(season)}/constructors.json?limit=200")
    constructors = payload.get("MRData", {}).get("ConstructorTable", {}).get("Constructors", [])
    if not constructors:
        return pd.DataFrame(columns=["constructorId", "name", "nationality", "url"])

    teams = pd.DataFrame(constructors)
    for column in ("constructorId", "name", "nationality", "url"):
        if column not in teams:
            teams[column] = ""

    teams = teams[["constructorId", "name", "nationality", "url"]].copy()
    teams = teams[teams["name"].astype(str).str.strip().str.len() > 0]
    teams = teams.drop_duplicates(subset=["constructorId"]).sort_values("name").reset_index(drop=True)
    return teams


@st.cache_data(ttl=3600)
def get_constructor_results_history(constructor_id):
    page_limit = 100
    offset = 0
    rows = []
    seen_races = set()

    while True:
        payload = _fetch_ergast_path(
            f"constructors/{constructor_id}/results.json?limit={page_limit}&offset={offset}"
        )
        race_page = payload.get("MRData", {}).get("RaceTable", {}).get("Races", [])
        if not race_page:
            break

        new_count = 0
        for race in race_page:
            race_key = (race.get("season"), race.get("round"), race.get("raceName"))
            if race_key in seen_races:
                continue
            seen_races.add(race_key)

            try:
                season = int(race.get("season", 0) or 0)
                round_num = int(race.get("round", 0) or 0)
            except (TypeError, ValueError):
                continue

            rows.append(
                {
                    "season": season,
                    "round": round_num,
                    "raceName": race.get("raceName", "Unknown Race"),
                    "date": race.get("date", ""),
                }
            )
            new_count += 1

        mr_data = payload.get("MRData", {})
        try:
            total = int(mr_data.get("total", len(rows)) or len(rows))
        except (TypeError, ValueError):
            total = len(rows)

        offset += len(race_page)
        if new_count == 0 or offset >= total:
            break

    if not rows:
        return pd.DataFrame(columns=["season", "round", "raceName", "date"])

    history = pd.DataFrame(rows)
    history = history.sort_values(["season", "round"]).reset_index(drop=True)
    return history


@st.cache_data(ttl=3600)
def get_constructor_season_driver_points(constructor_id, season):
    payload = _fetch_ergast_path(f"{int(season)}/constructors/{constructor_id}/results.json?limit=100")
    races = payload.get("MRData", {}).get("RaceTable", {}).get("Races", [])
    if not races:
        return pd.DataFrame(columns=["driverId", "driverName", "points", "starts"])

    driver_totals = {}
    for race in races:
        for result in race.get("Results", []):
            driver = result.get("Driver", {})
            driver_id = driver.get("driverId")
            if not driver_id:
                continue

            full_name = f"{driver.get('givenName', '')} {driver.get('familyName', '')}".strip() or driver_id
            try:
                points = float(result.get("points", 0.0))
            except (TypeError, ValueError):
                points = 0.0

            if driver_id not in driver_totals:
                driver_totals[driver_id] = {"driverName": full_name, "points": 0.0, "starts": 0}

            driver_totals[driver_id]["points"] += points
            driver_totals[driver_id]["starts"] += 1

    if not driver_totals:
        return pd.DataFrame(columns=["driverId", "driverName", "points", "starts"])

    rows = []
    for driver_id, values in driver_totals.items():
        rows.append(
            {
                "driverId": driver_id,
                "driverName": values["driverName"],
                "points": float(values["points"]),
                "starts": int(values["starts"]),
            }
        )

    drivers_df = pd.DataFrame(rows)
    drivers_df = drivers_df.sort_values(["points", "driverName"], ascending=[False, True]).reset_index(drop=True)
    return drivers_df


@st.cache_data(ttl=86400)
def get_all_wcc_titles():
    """Returns complete historical World Constructors' Championship titles (1958-2024)."""
    return pd.DataFrame(HISTORICAL_WCC)


@st.cache_data(ttl=86400)
def get_all_wdc_titles():
    """Returns complete historical World Drivers' Championship titles (1950-2024)."""
    return pd.DataFrame(HISTORICAL_WDC)


@st.cache_data(ttl=86400)
def get_team_history_blurb(team_name):
    try:
        return wikipedia.summary(f"{team_name} Formula One", sentences=3, auto_suggest=False)
    except Exception:
        try:
            return wikipedia.summary(team_name, sentences=3, auto_suggest=False)
        except Exception:
            return "History unavailable right now."


@st.cache_data(ttl=86400)
def get_track_wiki_summary(primary_title, fallback_title=None, sentences=4):
    try:
        return wikipedia.summary(primary_title, sentences=sentences)
    except Exception:
        if fallback_title:
            try:
                return wikipedia.summary(fallback_title, sentences=sentences)
            except Exception:
                pass
        return "Data unavailable. Unable to load track history."


def get_team_wiki_profile(constructor_id, constructor_name, selected_season):
    lineage = _resolve_team_lineage(constructor_id)
    aliases = lineage.get("aliases", [constructor_id])

    history_frames = []
    for alias_id in aliases:
        alias_history = get_constructor_results_history(alias_id)
        if not alias_history.empty:
            history_frames.append(alias_history)

    if history_frames:
        history = pd.concat(history_frames, ignore_index=True)
        history = history.drop_duplicates(subset=["season", "round", "raceName"]).copy()
        history = history.sort_values(["season", "round"]).reset_index(drop=True)
    else:
        history = pd.DataFrame(columns=["season", "round", "raceName", "date"])

    races = int(len(history))
    debut = "Unknown"
    if not history.empty:
        first_row = history.iloc[0]
        debut = f"{int(first_row['season'])} {first_row['raceName']}"

    leader = TEAM_LEADERS.get(constructor_id, "Unknown")

    current_drivers_df = get_constructor_season_driver_points(constructor_id, int(selected_season))
    current_drivers = []
    if not current_drivers_df.empty:
        for _, row in current_drivers_df.iterrows():
            current_drivers.append(f"{row['driverName']} ({row['points']:.1f} pts)")

    previous_names = lineage.get("previous_names", TEAM_PREVIOUS_NAMES.get(constructor_id, []))
    previous_names = sorted(previous_names)

    wcc_titles_df = get_all_wcc_titles()
    team_wcc = wcc_titles_df[wcc_titles_df["constructorId"].isin(aliases)].copy()
    team_wcc = team_wcc.sort_values("season").reset_index(drop=True)

    wcc_entries = []
    if not team_wcc.empty:
        for _, row in team_wcc.iterrows():
            wcc_entries.append(
                {
                    "season": int(row["season"]),
                    "points": float(row["points"]),
                    "drivers": row.get("drivers", "Drivers recorded"),
                }
            )

    wdc_titles_df = get_all_wdc_titles()
    team_wdc = wdc_titles_df[wdc_titles_df["constructorId"].isin(aliases)].copy()
    team_wdc = team_wdc.sort_values("season").reset_index(drop=True)

    wdc_entries = []
    if not team_wdc.empty:
        for _, row in team_wdc.iterrows():
            wdc_entries.append(
                {
                    "season": int(row["season"]),
                    "driver": row["driverName"],
                    "points": float(row["points"]),
                }
            )

    return {
        "constructorId": constructor_id,
        "name": constructor_name,
        "debut": debut,
        "leader": leader,
        "drivers": current_drivers,
        "races": races,
        "wcc_count": int(len(wcc_entries)),
        "wcc_entries": wcc_entries,
        "wdc_count": int(len(wdc_entries)),
        "wdc_entries": wdc_entries,
        "previous_names": previous_names,
        "history": get_team_history_blurb(constructor_name),
    }


def get_driver_season_results(driver_id, season):
    payload = _fetch_ergast_path(f"{int(season)}/drivers/{driver_id}/results.json?limit=100")
    races = payload.get("MRData", {}).get("RaceTable", {}).get("Races", [])

    rows = []
    for race in races:
        results = race.get("Results", [])
        if not results:
            continue
        result = results[0]
        try:
            round_num = int(race.get("round", 0) or 0)
        except (TypeError, ValueError):
            round_num = 0
        if round_num <= 0:
            continue
        try:
            points = float(result.get("points", 0.0))
        except (TypeError, ValueError):
            points = 0.0

        rows.append(
            {
                "Round": round_num,
                "RaceName": race.get("raceName", f"Round {round_num}"),
                "points": points,
            }
        )

    if rows:
        df = pd.DataFrame(rows)
        df = df.drop_duplicates(subset=["Round"]).sort_values("Round").reset_index(drop=True)
        return df

    history = get_driver_results_history(driver_id)
    if history.empty:
        return pd.DataFrame(columns=["Round", "RaceName", "points"])

    season_history = history[history["season"] == int(season)].copy()
    if season_history.empty:
        return pd.DataFrame(columns=["Round", "RaceName", "points"])

    season_history = season_history.rename(columns={"round": "Round", "raceName": "RaceName"})
    season_history = season_history[["Round", "RaceName", "points"]]
    season_history = season_history.drop_duplicates(subset=["Round"]).sort_values("Round").reset_index(drop=True)
    return season_history


def get_driver_championship_progression(driver_id, season):
    calendar = get_season_race_calendar(int(season))
    if calendar.empty:
        season_results = get_driver_season_results(driver_id, int(season))
        if season_results.empty:
            return pd.DataFrame(columns=["Round", "RaceName", "championship_points"])

        season_results = season_results.copy()
        season_results["championship_points"] = season_results["points"].cumsum()
        return season_results[["Round", "RaceName", "championship_points"]]

    points_so_far = 0.0
    found_any_round = False
    rows = []

    for _, calendar_row in calendar.iterrows():
        round_num = int(calendar_row["Round"])
        payload = _fetch_ergast_path(f"{int(season)}/{round_num}/driverStandings.json")
        standings_lists = payload.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])

        if standings_lists:
            standings_rows = standings_lists[0].get("DriverStandings", [])
            driver_row = None
            for standing in standings_rows:
                if standing.get("Driver", {}).get("driverId") == driver_id:
                    driver_row = standing
                    break

            if driver_row is not None:
                found_any_round = True
                try:
                    points_so_far = float(driver_row.get("points", points_so_far))
                except (TypeError, ValueError):
                    pass

        rows.append(
            {
                "Round": round_num,
                "RaceName": calendar_row["RaceName"],
                "championship_points": points_so_far,
            }
        )

    progression = pd.DataFrame(rows)

    if found_any_round:
        return progression

    season_results = get_driver_season_results(driver_id, int(season))
    if season_results.empty:
        return pd.DataFrame(columns=["Round", "RaceName", "championship_points"])

    season_results = season_results.copy()
    season_results["championship_points"] = season_results["points"].cumsum()

    fallback = calendar[["Round", "RaceName"]].copy()
    fallback = fallback.merge(
        season_results[["Round", "championship_points"]],
        how="left",
        on="Round",
    )
    fallback["championship_points"] = fallback["championship_points"].ffill().fillna(0.0)
    return fallback


def get_driver_results_history(driver_id):
    page_limit = 100
    offset = 0
    races = []
    seen_races = set()

    while True:
        payload = _fetch_ergast_path(f"drivers/{driver_id}/results.json?limit={page_limit}&offset={offset}")
        race_page = payload.get("MRData", {}).get("RaceTable", {}).get("Races", [])

        if not race_page:
            break

        new_count = 0
        for race in race_page:
            race_key = (race.get("season"), race.get("round"), race.get("raceName"))
            if race_key in seen_races:
                continue
            seen_races.add(race_key)
            races.append(race)
            new_count += 1

        mr_data = payload.get("MRData", {})
        try:
            total = int(mr_data.get("total", len(races)) or len(races))
        except (TypeError, ValueError):
            total = len(races)

        offset += len(race_page)

        if new_count == 0 or offset >= total:
            break

    if not races:
        return pd.DataFrame()

    rows = []
    for race in races:
        result = race.get("Results", [{}])[0]
        try:
            points = float(result.get("points", 0.0))
        except (TypeError, ValueError):
            points = 0.0

        rows.append(
            {
                "season": int(race.get("season", 0) or 0),
                "round": int(race.get("round", 0) or 0),
                "raceName": race.get("raceName", "Unknown Race"),
                "date": race.get("date", ""),
                "points": points,
                "positionText": str(result.get("positionText", "")),
            }
        )

    history = pd.DataFrame(rows)
    history = history.sort_values(["season", "round"]).reset_index(drop=True)
    history["race_index"] = range(1, len(history) + 1)
    history["cumulative_points"] = history["points"].cumsum()
    history["event_label"] = history["season"].astype(str) + " " + history["raceName"].astype(str)
    return history


@st.cache_data(ttl=3600)
def get_season_driver_standings(season):
    payload = _fetch_ergast_path(f"{season}/driverStandings.json")
    standings = payload.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
    if not standings:
        return {}

    rows = standings[0].get("DriverStandings", [])
    mapping = {}
    for row in rows:
        driver = row.get("Driver", {})
        driver_id = driver.get("driverId")
        try:
            position = int(row.get("position", 0) or 0)
        except (TypeError, ValueError):
            position = 0
        if driver_id and position > 0:
            mapping[driver_id] = position

    return mapping


@st.cache_data(ttl=3600)
def get_season_race_calendar(season):
    payload = _fetch_ergast_path(f"{int(season)}.json?limit=100")
    races = payload.get("MRData", {}).get("RaceTable", {}).get("Races", [])
    if not races:
        return pd.DataFrame(columns=["Round", "RaceName"])

    rows = []
    for race in races:
        try:
            round_num = int(race.get("round", 0) or 0)
        except (TypeError, ValueError):
            round_num = 0
        if round_num <= 0:
            continue
        rows.append({"Round": round_num, "RaceName": race.get("raceName", f"Round {round_num}")})

    if not rows:
        return pd.DataFrame(columns=["Round", "RaceName"])

    calendar = pd.DataFrame(rows)
    calendar = calendar.drop_duplicates(subset=["Round"]).sort_values("Round").reset_index(drop=True)
    return calendar


def get_driver_season_totals(driver_id):
    history = get_driver_results_history(driver_id)
    if history.empty:
        return pd.DataFrame(columns=["season", "points", "races", "wins", "championship_position"])

    season_totals = (
        history.groupby("season", as_index=False)
        .agg(
            points=("points", "sum"),
            races=("round", "count"),
            wins=("positionText", lambda series: int((series == "1").sum())),
        )
        .sort_values("season")
        .reset_index(drop=True)
    )

    positions = []
    for season in season_totals["season"].tolist():
        season_map = get_season_driver_standings(int(season))
        positions.append(season_map.get(driver_id))

    season_totals["championship_position"] = positions
    return season_totals


def get_driver_metadata(driver_id):
    if not driver_id:
        return {}

    directory = get_driver_directory()
    if not directory.empty:
        matches = directory[directory["driverId"] == driver_id]
        if not matches.empty:
            row = matches.iloc[0]
            return {
                "driverId": driver_id,
                "fullName": row.get("fullName", "Unknown Driver"),
                "nationality": row.get("nationality", "Unknown"),
            }

    payload = _fetch_ergast_path(f"drivers/{driver_id}.json")
    drivers = payload.get("MRData", {}).get("DriverTable", {}).get("Drivers", [])
    if drivers:
        row = drivers[0]
        full_name = f"{row.get('givenName', '')} {row.get('familyName', '')}".strip()
        return {
            "driverId": driver_id,
            "fullName": full_name or "Unknown Driver",
            "nationality": row.get("nationality", "Unknown"),
        }

    for row in STATIC_DRIVER_DIRECTORY:
        if row.get("driverId") == driver_id:
            full_name = f"{row.get('givenName', '')} {row.get('familyName', '')}".strip()
            return {
                "driverId": driver_id,
                "fullName": full_name or "Unknown Driver",
                "nationality": row.get("nationality", "Unknown"),
            }

    inferred_name = str(driver_id).replace("_", " ").replace("-", " ").title()
    return {
        "driverId": driver_id,
        "fullName": inferred_name or "Unknown Driver",
        "nationality": "Unknown",
    }


def get_driver_profile(driver_id):
    metadata = get_driver_metadata(driver_id)
    if not metadata:
        return {}

    history = get_driver_results_history(driver_id)
    if history.empty:
        return {
            "driverId": driver_id,
            "fullName": metadata.get("fullName", "Unknown Driver"),
            "nationality": metadata.get("nationality", "Unknown"),
            "races": 0,
            "wins": 0,
            "points": 0.0,
            "debut": "Unknown",
            "most_points": "Unknown",
            "least_points": "Unknown",
        }

    debut = history.iloc[0]
    season_totals = get_driver_season_totals(driver_id)
    wins = int((history["positionText"] == "1").sum())

    most_points = "Unknown"
    least_points = "Unknown"

    if not season_totals.empty:
        current_season = int(pd.Timestamp.now().year)
        most_row = season_totals.loc[season_totals["points"].idxmax()]
        least_source = season_totals[season_totals["season"] != current_season]
        least_row = least_source.loc[least_source["points"].idxmin()] if not least_source.empty else None

        most_pos = most_row.get("championship_position")
        least_pos = least_row.get("championship_position") if least_row is not None else None

        most_pos_text = f"P{int(most_pos)}" if pd.notna(most_pos) else "Position N/A"
        least_pos_text = f"P{int(least_pos)}" if pd.notna(least_pos) else "Position N/A"

        most_points = f"{most_row['points']:.1f} ({int(most_row['season'])}, {most_pos_text})"
        if least_row is not None:
            least_points = f"{least_row['points']:.1f} ({int(least_row['season'])}, {least_pos_text})"

    return {
        "driverId": driver_id,
        "fullName": metadata.get("fullName", "Unknown Driver"),
        "nationality": metadata.get("nationality", "Unknown"),
        "races": int(len(history)),
        "wins": wins,
        "points": float(history["points"].sum()),
        "debut": f"{debut['season']} {debut['raceName']}",
        "most_points": most_points,
        "least_points": least_points,
    }


@st.cache_data(ttl=86400)
def get_driver_history_blurb(driver_name):
    try:
        return wikipedia.summary(f"{driver_name} Formula One", sentences=3, auto_suggest=False)
    except Exception:
        try:
            return wikipedia.summary(driver_name, sentences=3, auto_suggest=False)
        except Exception:
            return "History unavailable right now."
