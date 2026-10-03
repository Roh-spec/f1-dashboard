import streamlit as st
import pandas as pd


ACTIVE_PADDOCK_DRIVERS = {
    "Lewis Hamilton",
    "Max Verstappen",
    "Fernando Alonso",
    "Charles Leclerc",
    "Lando Norris",
    "George Russell",
    "Carlos Sainz",
    "Valtteri Bottas",
    "Sergio Pérez",
    "Pierre Gasly",
    "Esteban Ocon",
    "Yuki Tsunoda",
    "Alexander Albon",
    "Nico Hülkenberg",
    "Lance Stroll",
    "Kevin Magnussen",
    "Zhou Guanyu",
    "Liam Lawson",
    "Jack Doohan",
    "Oliver Bearman",
    "Andrea Kimi Antonelli",
    "Gabriel Bortoleto",
    "Isack Hadjar",
}

# -----------------------------------------------------------------------------
# CHAMPIONSHIP DRIVERS DATABASE (Layered by Titles)
# -----------------------------------------------------------------------------

CHAMPIONS_DATA = [
    # Layer: 7 World Championships
    {
        "tier": 7,
        "tier_title": "7 World Championships",
        "tier_badge": "7x WORLD CHAMPIONS",
        "drivers": [
            {
                "name": "Lewis Hamilton",
                "country": "GBR",
                "titles": 7,
                "wins": 105,
                "poles": 104,
                "podiums": 201,
                "points": "4,829.5",
                "points_num": 4829.5,
                "starts": 356,
                "win_rate": 29.5,
                "podium_rate": 56.5,
                "debut": "2007 Australian GP",
                "first_win": "2007 Canadian GP",
                "years": "2008, 2014, 2015, 2017, 2018, 2019, 2020",
                "color": "#00a0dd",
                "key_teams": "McLaren, Mercedes, Ferrari",
                "honors": ["Grand Slam (x6)", "Centurion 200+ Podiums", "Monaco Master (x3)"],
            },
            {
                "name": "Michael Schumacher",
                "country": "GER",
                "titles": 7,
                "wins": 91,
                "poles": 68,
                "podiums": 155,
                "points": "1,566.0",
                "points_num": 1566.0,
                "starts": 308,
                "win_rate": 29.5,
                "podium_rate": 50.3,
                "debut": "1991 Belgian GP",
                "first_win": "1992 Belgian GP",
                "years": "1994, 1995, 2000, 2001, 2002, 2003, 2004",
                "color": "#e80020",
                "key_teams": "Benetton, Ferrari, Mercedes",
                "honors": ["Grand Slam (x5)", "100% Season Podiums (2002)", "7x World Champion"],
            },
        ],
    },
    # Layer: 5 World Championships
    {
        "tier": 5,
        "tier_title": "5 World Championships",
        "tier_badge": "5x WORLD CHAMPION",
        "drivers": [
            {
                "name": "Juan Manuel Fangio",
                "country": "ARG",
                "titles": 5,
                "wins": 24,
                "poles": 29,
                "podiums": 35,
                "points": "277.6",
                "points_num": 277.6,
                "starts": 52,
                "win_rate": 46.2,
                "podium_rate": 67.3,
                "debut": "1950 British GP",
                "first_win": "1950 Monaco GP",
                "years": "1951, 1954, 1955, 1956, 1957",
                "color": "#f5a623",
                "key_teams": "Alfa Romeo, Maserati, Mercedes, Ferrari",
                "honors": ["All-Time Win Rate Record (46.2%)", "Titles with 4 Different Teams"],
            },
        ],
    },
    # Layer: 4 World Championships
    {
        "tier": 4,
        "tier_title": "4 World Championships",
        "tier_badge": "4x WORLD CHAMPIONS",
        "drivers": [
            {
                "name": "Alain Prost",
                "country": "FRA",
                "titles": 4,
                "wins": 51,
                "poles": 33,
                "podiums": 106,
                "points": "798.5",
                "points_num": 798.5,
                "starts": 202,
                "win_rate": 25.2,
                "podium_rate": 52.5,
                "debut": "1980 Argentine GP",
                "first_win": "1981 French GP",
                "years": "1985, 1986, 1989, 1993",
                "color": "#0093cc",
                "key_teams": "Renault, McLaren, Ferrari, Williams",
                "honors": ["The Professor", "51 Grand Prix Victories", "4x World Champion"],
            },
            {
                "name": "Sebastian Vettel",
                "country": "GER",
                "titles": 4,
                "wins": 53,
                "poles": 57,
                "podiums": 122,
                "points": "3,098.0",
                "points_num": 3098.0,
                "starts": 300,
                "win_rate": 17.7,
                "podium_rate": 40.7,
                "debut": "2007 US GP",
                "first_win": "2008 Italian GP",
                "years": "2010, 2011, 2012, 2013",
                "color": "#1e41ff",
                "key_teams": "Toro Rosso, Red Bull, Ferrari, Aston Martin",
                "honors": ["Youngest World Champion (23y 134d)", "9 Consecutive Wins (2013)"],
            },
            {
                "name": "Max Verstappen",
                "country": "NED",
                "titles": 4,
                "wins": 63,
                "poles": 40,
                "podiums": 111,
                "points": "3,014.5",
                "points_num": 3014.5,
                "starts": 209,
                "win_rate": 30.1,
                "podium_rate": 53.1,
                "debut": "2015 Australian GP",
                "first_win": "2016 Spanish GP",
                "years": "2021, 2022, 2023, 2024",
                "color": "#3671c6",
                "key_teams": "Toro Rosso, Red Bull Racing",
                "honors": ["19 Wins in a Season (2023 Record)", "10 Straight Wins Record", "Youngest Winner"],
            },
        ],
    },
    # Layer: 3 World Championships
    {
        "tier": 3,
        "tier_title": "3 World Championships",
        "tier_badge": "3x WORLD CHAMPIONS",
        "drivers": [
            {
                "name": "Ayrton Senna",
                "country": "BRA",
                "titles": 3,
                "wins": 41,
                "poles": 65,
                "podiums": 80,
                "points": "614.0",
                "points_num": 614.0,
                "starts": 162,
                "win_rate": 25.3,
                "podium_rate": 49.4,
                "debut": "1984 Brazilian GP",
                "first_win": "1985 Portuguese GP",
                "years": "1988, 1990, 1991",
                "color": "#ff8000",
                "key_teams": "Toleman, Lotus, McLaren, Williams",
                "honors": ["King of Monaco (6 Wins)", "65 Pole Positions", "Grand Slam (x4)"],
            },
            {
                "name": "Nelson Piquet",
                "country": "BRA",
                "titles": 3,
                "wins": 23,
                "poles": 24,
                "podiums": 60,
                "points": "485.5",
                "points_num": 485.5,
                "starts": 207,
                "win_rate": 11.1,
                "podium_rate": 29.0,
                "debut": "1978 German GP",
                "first_win": "1980 US West GP",
                "years": "1981, 1983, 1987",
                "color": "#64c4ff",
                "key_teams": "Brabham, Williams, Lotus, Benetton",
                "honors": ["3x World Champion", "First Turbo Champion (1983)"],
            },
            {
                "name": "Niki Lauda",
                "country": "AUT",
                "titles": 3,
                "wins": 25,
                "poles": 24,
                "podiums": 54,
                "points": "420.5",
                "points_num": 420.5,
                "starts": 177,
                "win_rate": 14.1,
                "podium_rate": 30.5,
                "debut": "1971 Austrian GP",
                "first_win": "1974 Spanish GP",
                "years": "1975, 1977, 1984",
                "color": "#e80020",
                "key_teams": "March, BRM, Ferrari, Brabham, McLaren",
                "honors": ["Comeback Legend", "Ferrari & McLaren Champion", "25 Wins"],
            },
            {
                "name": "Jackie Stewart",
                "country": "GBR",
                "titles": 3,
                "wins": 27,
                "poles": 17,
                "podiums": 43,
                "points": "360.0",
                "points_num": 360.0,
                "starts": 99,
                "win_rate": 27.3,
                "podium_rate": 43.4,
                "debut": "1965 South African GP",
                "first_win": "1965 Italian GP",
                "years": "1969, 1971, 1973",
                "color": "#00594f",
                "key_teams": "BRM, Matra, Tyrrell",
                "honors": ["Flying Scot", "27 Wins in 99 Starts", "3x World Champion"],
            },
            {
                "name": "Jack Brabham",
                "country": "AUS",
                "titles": 3,
                "wins": 14,
                "poles": 13,
                "podiums": 31,
                "points": "261.0",
                "points_num": 261.0,
                "starts": 126,
                "win_rate": 11.1,
                "podium_rate": 24.6,
                "debut": "1955 British GP",
                "first_win": "1959 Monaco GP",
                "years": "1959, 1960, 1966",
                "color": "#00a651",
                "key_teams": "Cooper, Brabham",
                "honors": ["Only Champion in Own Car (1966)", "3x World Champion"],
            },
        ],
    },
    # Layer: 2 World Championships
    {
        "tier": 2,
        "tier_title": "2 World Championships",
        "tier_badge": "2x WORLD CHAMPIONS",
        "drivers": [
            {
                "name": "Fernando Alonso",
                "country": "ESP",
                "titles": 2,
                "wins": 32,
                "poles": 22,
                "podiums": 106,
                "points": "2,329.0",
                "points_num": 2329.0,
                "starts": 401,
                "win_rate": 8.0,
                "podium_rate": 26.4,
                "debut": "2001 Australian GP",
                "first_win": "2003 Hungarian GP",
                "years": "2005, 2006",
                "color": "#229971",
                "key_teams": "Renault, McLaren, Ferrari, Alpine, Aston Martin",
                "honors": ["Ironman 400+ Starts", "2x World Champion", "Le Mans Winner"],
            },
            {
                "name": "Mika Häkkinen",
                "country": "FIN",
                "titles": 2,
                "wins": 20,
                "poles": 26,
                "podiums": 51,
                "points": "420.0",
                "points_num": 420.0,
                "starts": 161,
                "win_rate": 12.4,
                "podium_rate": 31.7,
                "debut": "1991 US GP",
                "first_win": "1997 European GP",
                "years": "1998, 1999",
                "color": "#ff8000",
                "key_teams": "Lotus, McLaren",
                "honors": ["Flying Finn", "Back-to-Back Titles (1998-99)", "20 Wins"],
            },
            {
                "name": "Emerson Fittipaldi",
                "country": "BRA",
                "titles": 2,
                "wins": 14,
                "poles": 6,
                "podiums": 35,
                "points": "281.0",
                "points_num": 281.0,
                "starts": 144,
                "win_rate": 9.7,
                "podium_rate": 24.3,
                "debut": "1970 British GP",
                "first_win": "1970 US GP",
                "years": "1972, 1974",
                "color": "#ff8000",
                "key_teams": "Lotus, McLaren, Fittipaldi",
                "honors": ["Youngest Champion at the Time (1972)", "2x World Champion"],
            },
            {
                "name": "Graham Hill",
                "country": "GBR",
                "titles": 2,
                "wins": 14,
                "poles": 13,
                "podiums": 36,
                "points": "289.0",
                "points_num": 289.0,
                "starts": 176,
                "win_rate": 8.0,
                "podium_rate": 20.5,
                "debut": "1958 Monaco GP",
                "first_win": "1962 Dutch GP",
                "years": "1962, 1968",
                "color": "#1f4068",
                "key_teams": "BRM, Lotus, Brabham, Shadow, Hill",
                "honors": ["Triple Crown Winner (F1, Indy 500, Le Mans)", "Mr. Monaco (5 Wins)"],
            },
            {
                "name": "Jim Clark",
                "country": "GBR",
                "titles": 2,
                "wins": 25,
                "poles": 33,
                "podiums": 32,
                "points": "274.0",
                "points_num": 274.0,
                "starts": 72,
                "win_rate": 34.7,
                "podium_rate": 44.4,
                "debut": "1960 Dutch GP",
                "first_win": "1962 Belgian GP",
                "years": "1963, 1965",
                "color": "#00594f",
                "key_teams": "Team Lotus",
                "honors": ["Grand Slam Record (x8)", "34.7% Win Rate", "1965 Indy 500 Winner"],
            },
            {
                "name": "Alberto Ascari",
                "country": "ITA",
                "titles": 2,
                "wins": 13,
                "poles": 14,
                "podiums": 17,
                "points": "140.1",
                "points_num": 140.1,
                "starts": 32,
                "win_rate": 40.6,
                "podium_rate": 53.1,
                "debut": "1950 Monaco GP",
                "first_win": "1951 German GP",
                "years": "1952, 1953",
                "color": "#e80020",
                "key_teams": "Ferrari, Maserati, Lancia",
                "honors": ["40.6% Win Rate", "7 Consecutive Wins (1952-53)", "Ferrari Legend"],
            },
        ],
    },
    # Layer: 1 World Championship
    {
        "tier": 1,
        "tier_title": "1 World Championship",
        "tier_badge": "1x WORLD CHAMPIONS",
        "drivers": [
            {
                "name": "Kimi Räikkönen",
                "country": "FIN",
                "titles": 1,
                "wins": 21,
                "poles": 18,
                "podiums": 103,
                "points": "1,873.0",
                "points_num": 1873.0,
                "starts": 349,
                "win_rate": 6.0,
                "podium_rate": 29.5,
                "debut": "2001 Australian GP",
                "first_win": "2003 Malaysian GP",
                "years": "2007",
                "color": "#e80020",
                "key_teams": "Sauber, McLaren, Ferrari, Lotus, Alfa Romeo",
                "honors": ["The Iceman", "2007 World Champion", "Centurion 103 Podiums"],
            },
            {
                "name": "Nico Rosberg",
                "country": "GER",
                "titles": 1,
                "wins": 23,
                "poles": 30,
                "podiums": 57,
                "points": "1,594.5",
                "points_num": 1594.5,
                "starts": 206,
                "win_rate": 11.2,
                "podium_rate": 27.7,
                "debut": "2006 Bahrain GP",
                "first_win": "2012 Chinese GP",
                "years": "2016",
                "color": "#00a0dd",
                "key_teams": "Williams, Mercedes",
                "honors": ["2016 World Champion", "Monaco Hat-Trick (2013-15)"],
            },
            {
                "name": "Jenson Button",
                "country": "GBR",
                "titles": 1,
                "wins": 15,
                "poles": 8,
                "podiums": 50,
                "points": "1,235.0",
                "points_num": 1235.0,
                "starts": 306,
                "win_rate": 4.9,
                "podium_rate": 16.3,
                "debut": "2000 Australian GP",
                "first_win": "2006 Hungarian GP",
                "years": "2009",
                "color": "#f5a623",
                "key_teams": "Williams, Benetton, BAR, Honda, Brawn GP, McLaren",
                "honors": ["2009 Brawn GP Champion", "Montreal 2011 Miracle"],
            },
            {
                "name": "Nigel Mansell",
                "country": "GBR",
                "titles": 1,
                "wins": 31,
                "poles": 32,
                "podiums": 59,
                "points": "482.0",
                "points_num": 482.0,
                "starts": 187,
                "win_rate": 16.6,
                "podium_rate": 31.6,
                "debut": "1980 Austrian GP",
                "first_win": "1985 European GP",
                "years": "1992",
                "color": "#64c4ff",
                "key_teams": "Lotus, Williams, Ferrari, McLaren",
                "honors": ["Red 5", "1992 Dominant Champion", "31 Wins & 32 Poles"],
            },
            {
                "name": "Damon Hill",
                "country": "GBR",
                "titles": 1,
                "wins": 22,
                "poles": 20,
                "podiums": 42,
                "points": "360.0",
                "points_num": 360.0,
                "starts": 115,
                "win_rate": 19.1,
                "podium_rate": 36.5,
                "debut": "1992 Spanish GP",
                "first_win": "1993 Hungarian GP",
                "years": "1996",
                "color": "#64c4ff",
                "key_teams": "Brabham, Williams, Arrows, Jordan",
                "honors": ["1996 World Champion", "22 Grand Prix Wins"],
            },
            {
                "name": "Jacques Villeneuve",
                "country": "CAN",
                "titles": 1,
                "wins": 11,
                "poles": 13,
                "podiums": 23,
                "points": "235.0",
                "points_num": 235.0,
                "starts": 163,
                "win_rate": 6.7,
                "podium_rate": 14.1,
                "debut": "1996 Australian GP",
                "first_win": "1996 European GP",
                "years": "1997",
                "color": "#64c4ff",
                "key_teams": "Williams, BAR, Renault, Sauber",
                "honors": ["1997 World Champion", "Indy 500 Winner"],
            },
            {
                "name": "Alan Jones",
                "country": "AUS",
                "titles": 1,
                "wins": 12,
                "poles": 6,
                "podiums": 24,
                "points": "206.0",
                "points_num": 206.0,
                "starts": 116,
                "win_rate": 10.3,
                "podium_rate": 20.7,
                "debut": "1975 Spanish GP",
                "first_win": "1977 Austrian GP",
                "years": "1980",
                "color": "#64c4ff",
                "key_teams": "Hesketh, Hill, Surtees, Shadow, Williams, Haas Lola",
                "honors": ["1980 World Champion", "Williams' First WDC Title"],
            },
            {
                "name": "Mario Andretti",
                "country": "USA",
                "titles": 1,
                "wins": 12,
                "poles": 18,
                "podiums": 19,
                "points": "180.0",
                "points_num": 180.0,
                "starts": 128,
                "win_rate": 9.4,
                "podium_rate": 14.8,
                "debut": "1968 US GP",
                "first_win": "1971 South African GP",
                "years": "1978",
                "color": "#00594f",
                "key_teams": "Lotus, March, Ferrari, Parnelli, Alfa Romeo, Williams",
                "honors": ["1978 World Champion", "Indy 500 & Daytona 500 Winner"],
            },
            {
                "name": "Jody Scheckter",
                "country": "RSA",
                "titles": 1,
                "wins": 10,
                "poles": 3,
                "podiums": 33,
                "points": "255.0",
                "points_num": 255.0,
                "starts": 112,
                "win_rate": 8.9,
                "podium_rate": 29.5,
                "debut": "1972 US GP",
                "first_win": "1974 Swedish GP",
                "years": "1979",
                "color": "#e80020",
                "key_teams": "McLaren, Tyrrell, Wolf, Ferrari",
                "honors": ["1979 Ferrari Champion", "10 Grand Prix Wins"],
            },
            {
                "name": "James Hunt",
                "country": "GBR",
                "titles": 1,
                "wins": 10,
                "poles": 14,
                "podiums": 23,
                "points": "179.0",
                "points_num": 179.0,
                "starts": 92,
                "win_rate": 10.9,
                "podium_rate": 25.0,
                "debut": "1973 Monaco GP",
                "first_win": "1975 Dutch GP",
                "years": "1976",
                "color": "#ff8000",
                "key_teams": "Hesketh, McLaren, Wolf",
                "honors": ["1976 World Champion", "Fuji 1976 Decider"],
            },
            {
                "name": "Keke Rosberg",
                "country": "FIN",
                "titles": 1,
                "wins": 5,
                "poles": 5,
                "podiums": 17,
                "points": "159.5",
                "points_num": 159.5,
                "starts": 114,
                "win_rate": 4.4,
                "podium_rate": 14.9,
                "debut": "1978 South African GP",
                "first_win": "1982 Swiss GP",
                "years": "1982",
                "color": "#64c4ff",
                "key_teams": "Theodore, ATS, Wolf, Fittipaldi, Williams, McLaren",
                "honors": ["1982 World Champion", "First Finnish Champion"],
            },
            {
                "name": "Denny Hulme",
                "country": "NZL",
                "titles": 1,
                "wins": 8,
                "poles": 1,
                "podiums": 33,
                "points": "248.0",
                "points_num": 248.0,
                "starts": 112,
                "win_rate": 7.1,
                "podium_rate": 29.5,
                "debut": "1965 Monaco GP",
                "first_win": "1967 Monaco GP",
                "years": "1967",
                "color": "#ff8000",
                "key_teams": "Brabham, McLaren",
                "honors": ["1967 World Champion", "The Bear"],
            },
            {
                "name": "Jochen Rindt",
                "country": "AUT",
                "titles": 1,
                "wins": 6,
                "poles": 10,
                "podiums": 13,
                "points": "109.0",
                "points_num": 109.0,
                "starts": 60,
                "win_rate": 10.0,
                "podium_rate": 21.7,
                "debut": "1964 Austrian GP",
                "first_win": "1969 US GP",
                "years": "1970",
                "color": "#00594f",
                "key_teams": "Cooper, Brabham, Lotus",
                "honors": ["1970 Posthumous Champion", "Monaco 1970 Thriller"],
            },
            {
                "name": "John Surtees",
                "country": "GBR",
                "titles": 1,
                "wins": 6,
                "poles": 8,
                "podiums": 24,
                "points": "180.0",
                "points_num": 180.0,
                "starts": 111,
                "win_rate": 5.4,
                "podium_rate": 21.6,
                "debut": "1960 Monaco GP",
                "first_win": "1963 German GP",
                "years": "1964",
                "color": "#e80020",
                "key_teams": "Lotus, Cooper, Lola, Ferrari, Honda, BRM, Surtees",
                "honors": ["Only Champion on 2 Wheels & 4 Wheels"],
            },
            {
                "name": "Giuseppe Farina",
                "country": "ITA",
                "titles": 1,
                "wins": 5,
                "poles": 5,
                "podiums": 20,
                "points": "127.3",
                "points_num": 127.3,
                "starts": 33,
                "win_rate": 15.2,
                "podium_rate": 60.6,
                "debut": "1950 British GP",
                "first_win": "1950 British GP",
                "years": "1950",
                "color": "#9b111e",
                "key_teams": "Alfa Romeo, Ferrari",
                "honors": ["Inaugural 1950 F1 World Champion", "First GP Pole & Win"],
            },
            {
                "name": "Phil Hill",
                "country": "USA",
                "titles": 1,
                "wins": 3,
                "poles": 6,
                "podiums": 16,
                "points": "98.0",
                "points_num": 98.0,
                "starts": 47,
                "win_rate": 6.4,
                "podium_rate": 34.0,
                "debut": "1958 French GP",
                "first_win": "1960 Italian GP",
                "years": "1961",
                "color": "#e80020",
                "key_teams": "Maserati, Ferrari, ATS, Cooper, Eagle",
                "honors": ["1961 World Champion", "Le Mans 24h Winner"],
            },
            {
                "name": "Mike Hawthorn",
                "country": "GBR",
                "titles": 1,
                "wins": 3,
                "poles": 4,
                "podiums": 18,
                "points": "127.6",
                "points_num": 127.6,
                "starts": 45,
                "win_rate": 6.7,
                "podium_rate": 40.0,
                "debut": "1952 Belgian GP",
                "first_win": "1953 French GP",
                "years": "1958",
                "color": "#e80020",
                "key_teams": "Ferrari, Vanwall, BRM",
                "honors": ["1958 Britain's First Champion", "Reims 1953 Duel"],
            },
        ],
    },
]

# -----------------------------------------------------------------------------
# NON-CHAMPIONSHIP WINNERS & RECORD HOLDERS
# -----------------------------------------------------------------------------

NON_CHAMPIONS_DATA = [
    {
        "name": "Stirling Moss",
        "country": "GBR",
        "titles": 0,
        "best_finish": "4x Runner-Up (P2)",
        "wins": 16,
        "poles": 16,
        "podiums": 24,
        "points": "186.6",
        "points_num": 186.6,
        "starts": 66,
        "win_rate": 24.2,
        "podium_rate": 36.4,
        "debut": "1951 Swiss GP",
        "first_win": "1955 British GP",
        "era": "1951-1961",
        "color": "#00a0dd",
        "key_teams": "Maserati, Mercedes, Vanwall, Cooper, Lotus",
        "honors": ["Greatest Driver Without a Title", "16 Wins", "4x Runner-Up"],
    },
    {
        "name": "David Coulthard",
        "country": "GBR",
        "titles": 0,
        "best_finish": "2001 Runner-Up (P2)",
        "wins": 13,
        "poles": 12,
        "podiums": 62,
        "points": "535.0",
        "points_num": 535.0,
        "starts": 246,
        "win_rate": 5.3,
        "podium_rate": 25.2,
        "debut": "1994 Spanish GP",
        "first_win": "1995 Portuguese GP",
        "era": "1994-2008",
        "color": "#64c4ff",
        "key_teams": "Williams, McLaren, Red Bull",
        "honors": ["62 Career Podiums", "13 Wins", "2001 WDC Runner-Up"],
    },
    {
        "name": "Carlos Reutemann",
        "country": "ARG",
        "titles": 0,
        "best_finish": "1981 Runner-Up (P2)",
        "wins": 12,
        "poles": 6,
        "podiums": 45,
        "points": "310.0",
        "points_num": 310.0,
        "starts": 146,
        "win_rate": 8.2,
        "podium_rate": 30.8,
        "debut": "1972 Argentine GP",
        "first_win": "1974 South African GP",
        "era": "1972-1982",
        "color": "#e80020",
        "key_teams": "Brabham, Ferrari, Lotus, Williams",
        "honors": ["12 Wins & 45 Podiums", "1981 Runner-Up by 1 Pt"],
    },
    {
        "name": "Felipe Massa",
        "country": "BRA",
        "titles": 0,
        "best_finish": "2008 Runner-Up (P2)",
        "wins": 11,
        "poles": 16,
        "podiums": 41,
        "points": "1,167.0",
        "points_num": 1167.0,
        "starts": 269,
        "win_rate": 4.1,
        "podium_rate": 15.2,
        "debut": "2002 Australian GP",
        "first_win": "2006 Turkish GP",
        "era": "2002-2017",
        "color": "#e80020",
        "key_teams": "Sauber, Ferrari, Williams",
        "honors": ["11 Wins & 16 Poles", "2008 Title Duel at Interlagos"],
    },
    {
        "name": "Rubens Barrichello",
        "country": "BRA",
        "titles": 0,
        "best_finish": "2x Runner-Up (P2)",
        "wins": 11,
        "poles": 14,
        "podiums": 68,
        "points": "658.0",
        "points_num": 658.0,
        "starts": 322,
        "win_rate": 3.4,
        "podium_rate": 21.1,
        "debut": "1993 South African GP",
        "first_win": "2000 German GP",
        "era": "1993-2011",
        "color": "#e80020",
        "key_teams": "Jordan, Stewart, Ferrari, Honda, Brawn GP, Williams",
        "honors": ["68 Podiums (Non-Champion Record)", "11 Wins", "Hockenheim 2000 Miracle"],
    },
    {
        "name": "Valtteri Bottas",
        "country": "FIN",
        "titles": 0,
        "best_finish": "2x Runner-Up (P2)",
        "wins": 10,
        "poles": 20,
        "podiums": 67,
        "points": "1,797.0",
        "points_num": 1797.0,
        "starts": 246,
        "win_rate": 4.1,
        "podium_rate": 27.2,
        "debut": "2013 Australian GP",
        "first_win": "2017 Russian GP",
        "era": "2013-Present",
        "color": "#00a0dd",
        "key_teams": "Williams, Mercedes, Alfa Romeo / Sauber",
        "honors": ["1,797 Points", "20 Poles & 67 Podiums", "2x Runner-Up"],
    },
    {
        "name": "Ronnie Peterson",
        "country": "SWE",
        "titles": 0,
        "best_finish": "2x Runner-Up (P2)",
        "wins": 10,
        "poles": 14,
        "podiums": 26,
        "points": "206.0",
        "points_num": 206.0,
        "starts": 123,
        "win_rate": 8.1,
        "podium_rate": 21.1,
        "debut": "1970 Monaco GP",
        "first_win": "1973 French GP",
        "era": "1970-1978",
        "color": "#00594f",
        "key_teams": "March, Lotus, Tyrrell",
        "honors": ["SuperSwede", "10 Wins & 14 Poles", "2x Runner-Up"],
    },
    {
        "name": "Mark Webber",
        "country": "AUS",
        "titles": 0,
        "best_finish": "3x 3rd Place (P3)",
        "wins": 9,
        "poles": 13,
        "podiums": 42,
        "points": "1,047.5",
        "points_num": 1047.5,
        "starts": 215,
        "win_rate": 4.2,
        "podium_rate": 19.5,
        "debut": "2002 Australian GP",
        "first_win": "2009 German GP",
        "era": "2002-2013",
        "color": "#1e41ff",
        "key_teams": "Minardi, Jaguar, Williams, Red Bull",
        "honors": ["9 Wins & 42 Podiums", "Monaco GP Winner (x2)"],
    },
    {
        "name": "Charles Leclerc",
        "country": "MON",
        "titles": 0,
        "best_finish": "2022 Runner-Up (P2)",
        "wins": 8,
        "poles": 26,
        "podiums": 43,
        "points": "1,430.0",
        "points_num": 1430.0,
        "starts": 146,
        "win_rate": 5.5,
        "podium_rate": 29.5,
        "debut": "2018 Australian GP",
        "first_win": "2019 Belgian GP",
        "era": "2018-Present",
        "color": "#e80020",
        "key_teams": "Sauber, Scuderia Ferrari",
        "honors": ["26 Pole Positions", "Monaco GP Winner (2024)", "Monza Winner (x2)"],
    },
    {
        "name": "Daniel Ricciardo",
        "country": "AUS",
        "titles": 0,
        "best_finish": "2x 3rd Place (P3)",
        "wins": 8,
        "poles": 3,
        "podiums": 32,
        "points": "1,329.0",
        "points_num": 1329.0,
        "starts": 257,
        "win_rate": 3.1,
        "podium_rate": 12.5,
        "debut": "2011 British GP",
        "first_win": "2014 Canadian GP",
        "era": "2011-2024",
        "color": "#1e41ff",
        "key_teams": "HRT, Toro Rosso, Red Bull, Renault, McLaren, RB",
        "honors": ["Honey Badger", "8 Grand Prix Wins", "Monaco GP Winner (2018)"],
    },
    {
        "name": "Jacky Ickx",
        "country": "BEL",
        "titles": 0,
        "best_finish": "2x Runner-Up (P2)",
        "wins": 8,
        "poles": 13,
        "podiums": 25,
        "points": "181.0",
        "points_num": 181.0,
        "starts": 114,
        "win_rate": 7.0,
        "podium_rate": 21.9,
        "debut": "1967 German GP",
        "first_win": "1968 French GP",
        "era": "1967-1979",
        "color": "#e80020",
        "key_teams": "Cooper, Ferrari, Brabham, McLaren, Lotus, Ensign, Ligier",
        "honors": ["6x Le Mans 24h Winner", "8 F1 Wins", "2x Runner-Up"],
    },
    {
        "name": "René Arnoux",
        "country": "FRA",
        "titles": 0,
        "best_finish": "1983 3rd Place (P3)",
        "wins": 7,
        "poles": 18,
        "podiums": 22,
        "points": "181.0",
        "points_num": 181.0,
        "starts": 149,
        "win_rate": 4.7,
        "podium_rate": 14.8,
        "debut": "1978 Belgian GP",
        "first_win": "1980 Brazilian GP",
        "era": "1978-1989",
        "color": "#0093cc",
        "key_teams": "Martini, Surtees, Renault, Ferrari, Ligier",
        "honors": ["18 Pole Positions", "Dijon 1979 Duel with Villeneuve"],
    },
    {
        "name": "Juan Pablo Montoya",
        "country": "COL",
        "titles": 0,
        "best_finish": "2x 3rd Place (P3)",
        "wins": 7,
        "poles": 13,
        "podiums": 30,
        "points": "307.0",
        "points_num": 307.0,
        "starts": 94,
        "win_rate": 7.4,
        "podium_rate": 31.9,
        "debut": "2001 Australian GP",
        "first_win": "2001 Italian GP",
        "era": "2001-2006",
        "color": "#64c4ff",
        "key_teams": "Williams, McLaren",
        "honors": ["Monaco GP & Indy 500 Winner", "Fastest Lap at Monza (2004)"],
    },
    {
        "name": "Sergio Pérez",
        "country": "MEX",
        "titles": 0,
        "best_finish": "2023 Runner-Up (P2)",
        "wins": 6,
        "poles": 3,
        "podiums": 39,
        "points": "1,638.0",
        "points_num": 1638.0,
        "starts": 281,
        "win_rate": 2.1,
        "podium_rate": 13.9,
        "debut": "2011 Australian GP",
        "first_win": "2020 Sakhir GP",
        "era": "2011-Present",
        "color": "#1e41ff",
        "key_teams": "Sauber, McLaren, Force India / Racing Point, Red Bull",
        "honors": ["King of the Streets", "6 Wins & 39 Podiums", "2023 Runner-Up"],
    },
    {
        "name": "Gilles Villeneuve",
        "country": "CAN",
        "titles": 0,
        "best_finish": "1979 Runner-Up (P2)",
        "wins": 6,
        "poles": 2,
        "podiums": 13,
        "points": "107.0",
        "points_num": 107.0,
        "starts": 67,
        "win_rate": 9.0,
        "podium_rate": 19.4,
        "debut": "1977 British GP",
        "first_win": "1978 Canadian GP",
        "era": "1977-1982",
        "color": "#e80020",
        "key_teams": "McLaren, Ferrari",
        "honors": ["Ferrari Icon", "1979 Runner-Up", "Dijon 1979 Legend"],
    },
    {
        "name": "Carlos Sainz",
        "country": "ESP",
        "titles": 0,
        "best_finish": "2024 5th Place (P5)",
        "wins": 4,
        "poles": 6,
        "podiums": 25,
        "points": "1,226.5",
        "points_num": 1226.5,
        "starts": 206,
        "win_rate": 1.9,
        "podium_rate": 12.1,
        "debut": "2015 Australian GP",
        "first_win": "2022 British GP",
        "era": "2015-Present",
        "color": "#e80020",
        "key_teams": "Toro Rosso, Renault, McLaren, Ferrari, Williams",
        "honors": ["Smooth Operator", "4 Wins & 6 Poles", "Singapore 2023 Masterclass"],
    },
    {
        "name": "Lando Norris",
        "country": "GBR",
        "titles": 0,
        "best_finish": "2024 Runner-Up (P2)",
        "wins": 4,
        "poles": 8,
        "podiums": 29,
        "points": "978.0",
        "points_num": 978.0,
        "starts": 128,
        "win_rate": 3.1,
        "podium_rate": 22.7,
        "debut": "2019 Australian GP",
        "first_win": "2024 Miami GP",
        "era": "2019-Present",
        "color": "#ff8000",
        "key_teams": "McLaren",
        "honors": ["2024 WDC Runner-Up", "4 Wins & 8 Poles", "29 Podiums"],
    },
    {
        "name": "George Russell",
        "country": "GBR",
        "titles": 0,
        "best_finish": "2022 4th Place (P4)",
        "wins": 3,
        "poles": 5,
        "podiums": 15,
        "points": "699.0",
        "points_num": 699.0,
        "starts": 128,
        "win_rate": 2.3,
        "podium_rate": 11.7,
        "debut": "2019 Australian GP",
        "first_win": "2022 São Paulo GP",
        "era": "2019-Present",
        "color": "#00a0dd",
        "key_teams": "Williams, Mercedes",
        "honors": ["Mr. Saturday", "3 Wins & 5 Poles", "15 Podiums"],
    },
]


def _render_driver_card(drv: dict, is_champion: bool = True, rank_num: int | None = None) -> str:
    color = drv.get("color", "#e10600")
    country = drv.get("country", "F1")
    name = drv.get("name", "Unknown Driver")
    titles = drv.get("titles", 0)
    wins = drv.get("wins", 0)
    poles = drv.get("poles", 0)
    podiums = drv.get("podiums", 0)
    points = drv.get("points", "0.0")
    starts = drv.get("starts", 0)
    win_rate = drv.get("win_rate", 0.0)
    podium_rate = drv.get("podium_rate", 0.0)
    debut = drv.get("debut", "-")
    first_win = drv.get("first_win", "-")
    honors = drv.get("honors", [])

    is_active = name in ACTIVE_PADDOCK_DRIVERS
    if is_active:
        active_badge = '<span style="font-family: \'JetBrains Mono\', monospace; font-size: 0.60rem; font-weight: 700; color: #10b981; background: rgba(16,185,129,0.12); border: 1px solid #10b981; padding: 2px 6px; border-radius: 2px;"><span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#10b981; margin-right:4px;"></span>ACTIVE PADDOCK</span>'
    else:
        active_badge = '<span style="font-family: \'JetBrains Mono\', monospace; font-size: 0.60rem; font-weight: 700; color: #8e929b; background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.1); padding: 2px 6px; border-radius: 2px;">🏛️ HALL OF FAME</span>'

    if is_champion:
        badge_text = f"{titles}x WORLD CHAMPION" if titles > 1 else "WORLD CHAMPION"
        footer_label = "CHAMPIONSHIP SEASONS"
        footer_val = drv.get("years", "-")
    else:
        badge_text = drv.get("best_finish", "GRAND PRIX WINNER")
        footer_label = "ACTIVE ERA"
        footer_val = f"{drv.get('era', '-')} &bull; Teams: {drv.get('key_teams', '-')}"

    rank_html = f"<span style=\"font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 800; color: #f5a623; margin-right: 8px;\">#{rank_num:02d}</span>" if rank_num else ""

    honors_html = ""
    for h in honors:
        honors_html += f"<span style=\"font-family: 'JetBrains Mono', monospace; font-size: 0.60rem; color: #f5a623; border: 1px solid rgba(245,166,35,0.3); background: rgba(245,166,35,0.05); padding: 1px 6px; border-radius: 2px; margin-right: 4px; display: inline-block; margin-bottom: 2px;\">{h}</span>"

    return f"""
    <div style="background: #161b22; border: 1px solid rgba(255,255,255,0.08); border-top: 3px solid {color}; border-radius: 6px; padding: 14px 16px; margin-bottom: 8px; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <div style="display: flex; align-items: center;">
                    {rank_html}
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 700; color: #8e929b; letter-spacing: 0.06em; text-transform: uppercase;">{badge_text}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 6px;">
                    {active_badge}
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 700; color: {color}; background: rgba(255,255,255,0.04); border: 1px solid {color}; padding: 1px 6px; border-radius: 2px;">{country}</span>
                </div>
            </div>
            <div style="font-family: 'Titillium Web', sans-serif; font-size: 1.25rem; font-weight: 700; color: #f0f3f6; letter-spacing: 0.02em; margin-bottom: 8px;">{name}</div>

            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; background: rgba(0,0,0,0.25); padding: 8px 6px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.04); margin-bottom: 8px;">
                <div style="text-align: center;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #8e929b; text-transform: uppercase;">TITLES</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 800; color: #f5a623;">{titles}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #8e929b; text-transform: uppercase;">WINS</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 800; color: #00e5ff;">{wins}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #8e929b; text-transform: uppercase;">POLES</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 800; color: #a855f7;">{poles}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #8e929b; text-transform: uppercase;">PODIUMS</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 800; color: #10b981;">{podiums}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #8e929b; text-transform: uppercase;">POINTS</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.95rem; font-weight: 800; color: #ffffff; white-space: nowrap;">{points}</div>
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.04); border-radius: 4px; padding: 4px 8px; margin-bottom: 8px; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem;">
                <span style="color: #8e929b;">Starts: <strong style="color: #ffffff;">{starts}</strong></span>
                <span style="color: #8e929b;">Win Rate: <strong style="color: #00e5ff;">{win_rate:.1f}%</strong></span>
                <span style="color: #8e929b;">Podium Rate: <strong style="color: #10b981;">{podium_rate:.1f}%</strong></span>
            </div>

            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #8e929b; margin-bottom: 6px;">
                Debut: <span style="color: #c9d1d9;">{debut}</span> &bull; 1st Win: <span style="color: #c9d1d9;">{first_win}</span>
            </div>

            <div style="margin-bottom: 8px;">
                {honors_html}
            </div>
        </div>

        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #8e929b; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 6px; line-height: 1.4;">
            <span style="color: #6b7280;">{footer_label}:</span> <span style="color: #c9d1d9;">{footer_val}</span>
        </div>
    </div>
    """


def _get_all_drivers_list() -> list[dict]:
    all_drvs = []
    for layer in CHAMPIONS_DATA:
        for d in layer["drivers"]:
            d_copy = dict(d)
            d_copy["is_champion"] = True
            all_drvs.append(d_copy)
    for d in NON_CHAMPIONS_DATA:
        d_copy = dict(d)
        d_copy["is_champion"] = False
        all_drvs.append(d_copy)
    return all_drvs


def render_page() -> None:
    # -------------------------------------------------------------------------
    # HEADER
    # -------------------------------------------------------------------------
    with st.container(border=True, key="dialog_racers_wiki_header"):
        st.markdown("<p class='section-kicker'>Paddock Intelligence</p>", unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>RACERS WIKI</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p class='hero-subtitle'>Historical encyclopedia of Formula 1 drivers tiered by World Championships, Grand Prix victories, pole positions, podiums, and career points.</p>",
            unsafe_allow_html=True,
        )

    # Filter / Search controls
    with st.container(border=True, key="dialog_racers_wiki_filter"):
        st.markdown("<p class='section-kicker'>Filter & Browse</p>", unsafe_allow_html=True)
        st.markdown("<h2>Driver Hall of Fame Scope</h2>", unsafe_allow_html=True)
        col_scope, col_sort, col_search = st.columns([1.2, 1.2, 1.6])
        with col_scope:
            tier_options = [
                "All Layers (Complete Encyclopedia)",
                "7 World Championships",
                "5 World Championships",
                "4 World Championships",
                "3 World Championships",
                "2 World Championships",
                "1 World Championship",
                "Non-Championship Winners",
            ]
            selected_tier = st.selectbox("SELECT TIER", tier_options)
        with col_sort:
            sort_options = [
                "Championship Layers (Default)",
                "Most Grand Prix Wins",
                "Most Pole Positions",
                "Highest Career Win Rate (%)",
                "Most Career Podiums",
                "Most Career Points",
            ]
            selected_sort = st.selectbox("SORT BY", sort_options)
        with col_search:
            search_query = st.text_input("SEARCH RACER", placeholder="Filter by driver name, nationality, or era...")

    # -------------------------------------------------------------------------
    # IF CUSTOM SORT IS CHOSEN (OVERALL LEADERBOARD VIEW)
    # -------------------------------------------------------------------------
    if selected_sort != "Championship Layers (Default)":
        all_drivers = _get_all_drivers_list()

        # Apply search query
        if search_query:
            q = search_query.lower().strip()
            all_drivers = [
                d for d in all_drivers
                if q in d["name"].lower() or q in d["country"].lower() or q in str(d.get("years", "")).lower() or q in str(d.get("era", "")).lower() or q in d.get("key_teams", "").lower()
            ]

        # Apply tier filter if not "All Layers"
        if selected_tier == "Non-Championship Winners":
            all_drivers = [d for d in all_drivers if not d.get("is_champion")]
        elif selected_tier != "All Layers (Complete Encyclopedia)":
            tier_num = int(selected_tier.split()[0])
            all_drivers = [d for d in all_drivers if d.get("titles") == tier_num]

        # Sort based on selected metric
        if selected_sort == "Most Grand Prix Wins":
            all_drivers.sort(key=lambda x: (x.get("wins", 0), x.get("podiums", 0)), reverse=True)
            sort_label = "Grand Prix Wins"
        elif selected_sort == "Most Pole Positions":
            all_drivers.sort(key=lambda x: (x.get("poles", 0), x.get("wins", 0)), reverse=True)
            sort_label = "Pole Positions"
        elif selected_sort == "Highest Career Win Rate (%)":
            all_drivers.sort(key=lambda x: (x.get("win_rate", 0.0), x.get("wins", 0)), reverse=True)
            sort_label = "Win Rate (%)"
        elif selected_sort == "Most Career Podiums":
            all_drivers.sort(key=lambda x: (x.get("podiums", 0), x.get("wins", 0)), reverse=True)
            sort_label = "Career Podiums"
        elif selected_sort == "Most Career Points":
            all_drivers.sort(key=lambda x: (x.get("points_num", 0.0), x.get("wins", 0)), reverse=True)
            sort_label = "Career Points"

        with st.container(border=True, key="dialog_racers_sorted_view"):
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 10px;">
                    <div>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; font-weight: 700; color: #00e5ff; letter-spacing: 0.08em; text-transform: uppercase;">ALL-TIME LEADERBOARD</span>
                        <h2 style="margin: 2px 0 0 0; color: #f0f3f6;">Ranked by {sort_label}</h2>
                    </div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 700; color: #00e5ff; background: rgba(0,229,255,0.08); border: 1px solid #00e5ff; padding: 2px 10px; border-radius: 3px;">
                        {len(all_drivers)} DRIVERS RANKED
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            cols = st.columns(3)
            for idx, drv in enumerate(all_drivers):
                col_idx = idx % 3
                with cols[col_idx]:
                    st.markdown(_render_driver_card(drv, is_champion=drv.get("is_champion", True), rank_num=idx + 1), unsafe_allow_html=True)
                    if st.button("VS COMPARE", key=f"btn_sort_comp_{drv['name']}_{idx}", use_container_width=True):
                        st.session_state.compare_driver_prefill = drv["name"]
                        st.switch_page("pages/3_Driver_Compare.py")
                    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

        return

    # -------------------------------------------------------------------------
    # DEFAULT VIEW: LAYERED WORLD CHAMPIONS SECTION
    # -------------------------------------------------------------------------
    for layer in CHAMPIONS_DATA:
        tier_title = layer["tier_title"]
        tier_badge = layer["tier_badge"]
        drivers = layer["drivers"]

        # Filter by selected tier
        if selected_tier != "All Layers (Complete Encyclopedia)":
            if selected_tier != tier_title:
                continue

        # Filter by search query
        if search_query:
            q = search_query.lower().strip()
            drivers = [
                d for d in drivers
                if q in d["name"].lower() or q in d["country"].lower() or q in d["years"].lower() or q in d.get("key_teams", "").lower()
            ]
            if not drivers:
                continue

        with st.container(border=True, key=f"dialog_racers_tier_{layer['tier']}"):
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 10px;">
                    <div>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; font-weight: 700; color: #f5a623; letter-spacing: 0.08em; text-transform: uppercase;">CHAMPIONSHIP TIER</span>
                        <h2 style="margin: 2px 0 0 0; color: #f0f3f6;">{tier_title}</h2>
                    </div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 700; color: #f5a623; background: rgba(245,166,35,0.08); border: 1px solid #f5a623; padding: 2px 10px; border-radius: 3px;">
                        {tier_badge}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            num_drivers = len(drivers)
            if num_drivers == 1:
                cols = st.columns(1)
            elif num_drivers == 2:
                cols = st.columns(2)
            else:
                cols = st.columns(3)

            for idx, drv in enumerate(drivers):
                col_idx = idx % len(cols)
                with cols[col_idx]:
                    st.markdown(_render_driver_card(drv, is_champion=True), unsafe_allow_html=True)
                    if st.button("VS COMPARE", key=f"btn_champ_comp_{drv['name']}_{layer['tier']}_{idx}", use_container_width=True):
                        st.session_state.compare_driver_prefill = drv["name"]
                        st.switch_page("pages/3_Driver_Compare.py")
                    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # SEPARATE PART: NON-CHAMPIONSHIP WINNERS
    # -------------------------------------------------------------------------
    show_non_champions = (
        selected_tier == "All Layers (Complete Encyclopedia)" or selected_tier == "Non-Championship Winners"
    )

    if show_non_champions:
        non_champs = NON_CHAMPIONS_DATA
        if search_query:
            q = search_query.lower().strip()
            non_champs = [
                d for d in non_champs
                if q in d["name"].lower() or q in d["country"].lower() or q in d["era"].lower() or q in d.get("key_teams", "").lower()
            ]

        with st.container(border=True, key="dialog_racers_non_champions"):
            st.markdown(
                """
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 10px;">
                    <div>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; font-weight: 700; color: #00e5ff; letter-spacing: 0.08em; text-transform: uppercase;">DISTINGUISHED FORMULA 1 RACERS</span>
                        <h2 style="margin: 2px 0 0 0; color: #f0f3f6;">Non-Championship Winners & Record Holders</h2>
                    </div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 700; color: #00e5ff; background: rgba(0,229,255,0.08); border: 1px solid #00e5ff; padding: 2px 10px; border-radius: 3px;">
                        NON-CHAMPION LEGENDS
                    </span>
                </div>
                <p style="font-size: 0.88rem; color: #8e929b; margin-bottom: 16px;">
                    Formula 1 icons who never captured a World Championship title, yet amassed extraordinary Grand Prix victories, pole positions, podiums, and championship points.
                </p>
                """,
                unsafe_allow_html=True,
            )

            # 4 Category Leaderboards for Non-Champions
            st.markdown("<p class='section-kicker'>Non-Champion Leaderboards</p>", unsafe_allow_html=True)
            leader_categories = [
                {
                    "title": "🏁 Most GP Wins",
                    "accent": "#00e5ff",
                    "drivers": [
                        ("Stirling Moss", "16 wins"),
                        ("David Coulthard", "13 wins"),
                        ("Carlos Reutemann", "12 wins"),
                        ("Felipe Massa", "11 wins"),
                        ("Rubens Barrichello", "11 wins"),
                    ],
                },
                {
                    "title": "⏱️ Most Pole Positions",
                    "accent": "#a855f7",
                    "drivers": [
                        ("Charles Leclerc", "26 poles"),
                        ("Valtteri Bottas", "20 poles"),
                        ("René Arnoux", "18 poles"),
                        ("Stirling Moss", "16 poles"),
                        ("Felipe Massa", "16 poles"),
                    ],
                },
                {
                    "title": "🎯 Most Career Points",
                    "accent": "#f5a623",
                    "drivers": [
                        ("Valtteri Bottas", "1,797.0 pts"),
                        ("Sergio Pérez", "1,638.0 pts"),
                        ("Charles Leclerc", "1,430.0 pts"),
                        ("Daniel Ricciardo", "1,329.0 pts"),
                        ("Carlos Sainz", "1,226.5 pts"),
                    ],
                },
                {
                    "title": "🍾 Most Podiums",
                    "accent": "#10b981",
                    "drivers": [
                        ("Rubens Barrichello", "68 podiums"),
                        ("Valtteri Bottas", "67 podiums"),
                        ("David Coulthard", "62 podiums"),
                        ("Carlos Reutemann", "45 podiums"),
                        ("Charles Leclerc", "43 podiums"),
                    ],
                },
            ]

            b_cols = st.columns(4)
            for col, cat in zip(b_cols, leader_categories):
                with col:
                    items_html = ""
                    for idx, (drv_name, stat_val) in enumerate(cat["drivers"]):
                        rank_str = f"0{idx + 1}"
                        border_bottom = "border-bottom: 1px solid rgba(255,255,255,0.05);" if idx < 4 else ""
                        items_html += f"""
                        <div style="display: flex; justify-content: space-between; align-items: center; padding: 5px 0; {border_bottom}">
                            <div style="display: flex; align-items: center; gap: 6px;">
                                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; color: #8e929b;">{rank_str}</span>
                                <span style="font-family: 'Titillium Web', sans-serif; font-size: 0.86rem; font-weight: 600; color: #f0f3f6;">{drv_name}</span>
                            </div>
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 700; color: {cat['accent']};">{stat_val}</span>
                        </div>
                        """
                    st.markdown(
                        f"""
                        <div style="background: #161b22; border: 1px solid rgba(255,255,255,0.08); border-left: 3px solid {cat['accent']}; border-radius: 6px; padding: 10px 14px; margin-bottom: 14px;">
                            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; font-weight: 700; color: #f0f3f6; text-transform: uppercase; margin-bottom: 8px;">{cat['title']}</div>
                            {items_html}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            # Driver boxes for non-championship winners
            st.markdown("<p class='section-kicker'>Driver Dossiers</p>", unsafe_allow_html=True)
            st.markdown("<h3>Non-Champion Driver Profiles</h3>", unsafe_allow_html=True)

            nc_cols = st.columns(3)
            for idx, drv in enumerate(non_champs):
                col_idx = idx % 3
                with nc_cols[col_idx]:
                    st.markdown(_render_driver_card(drv, is_champion=False), unsafe_allow_html=True)
                    if st.button("VS COMPARE", key=f"btn_nc_comp_{drv['name']}_{idx}", use_container_width=True):
                        st.session_state.compare_driver_prefill = drv["name"]
                        st.switch_page("pages/3_Driver_Compare.py")
                    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)


render_page()
