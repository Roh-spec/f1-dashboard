import streamlit as st
import pandas as pd


# -----------------------------------------------------------------------------
# CHAMPIONSHIP DRIVERS DATABASE (Organized by Layers / Championship Count)
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
                "years": "2008, 2014, 2015, 2017, 2018, 2019, 2020",
                "color": "#00a0dd",
                "key_teams": "McLaren, Mercedes, Ferrari",
            },
            {
                "name": "Michael Schumacher",
                "country": "GER",
                "titles": 7,
                "wins": 91,
                "poles": 68,
                "podiums": 155,
                "points": "1,566.0",
                "years": "1994, 1995, 2000, 2001, 2002, 2003, 2004",
                "color": "#e80020",
                "key_teams": "Benetton, Ferrari, Mercedes",
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
                "years": "1951, 1954, 1955, 1956, 1957",
                "color": "#f5a623",
                "key_teams": "Alfa Romeo, Maserati, Mercedes, Ferrari",
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
                "years": "1985, 1986, 1989, 1993",
                "color": "#0093cc",
                "key_teams": "Renault, McLaren, Ferrari, Williams",
            },
            {
                "name": "Sebastian Vettel",
                "country": "GER",
                "titles": 4,
                "wins": 53,
                "poles": 57,
                "podiums": 122,
                "points": "3,098.0",
                "years": "2010, 2011, 2012, 2013",
                "color": "#1e41ff",
                "key_teams": "Toro Rosso, Red Bull, Ferrari, Aston Martin",
            },
            {
                "name": "Max Verstappen",
                "country": "NED",
                "titles": 4,
                "wins": 63,
                "poles": 40,
                "podiums": 111,
                "points": "3,014.5",
                "years": "2021, 2022, 2023, 2024",
                "color": "#3671c6",
                "key_teams": "Toro Rosso, Red Bull Racing",
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
                "years": "1988, 1990, 1991",
                "color": "#ff8000",
                "key_teams": "Toleman, Lotus, McLaren, Williams",
            },
            {
                "name": "Nelson Piquet",
                "country": "BRA",
                "titles": 3,
                "wins": 23,
                "poles": 24,
                "podiums": 60,
                "points": "485.5",
                "years": "1981, 1983, 1987",
                "color": "#64c4ff",
                "key_teams": "Brabham, Williams, Lotus, Benetton",
            },
            {
                "name": "Niki Lauda",
                "country": "AUT",
                "titles": 3,
                "wins": 25,
                "poles": 24,
                "podiums": 54,
                "points": "420.5",
                "years": "1975, 1977, 1984",
                "color": "#e80020",
                "key_teams": "March, BRM, Ferrari, Brabham, McLaren",
            },
            {
                "name": "Jackie Stewart",
                "country": "GBR",
                "titles": 3,
                "wins": 27,
                "poles": 17,
                "podiums": 43,
                "points": "360.0",
                "years": "1969, 1971, 1973",
                "color": "#00594f",
                "key_teams": "BRM, Matra, Tyrrell",
            },
            {
                "name": "Jack Brabham",
                "country": "AUS",
                "titles": 3,
                "wins": 14,
                "poles": 13,
                "podiums": 31,
                "points": "261.0",
                "years": "1959, 1960, 1966",
                "color": "#00a651",
                "key_teams": "Cooper, Brabham",
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
                "years": "2005, 2006",
                "color": "#229971",
                "key_teams": "Renault, McLaren, Ferrari, Alpine, Aston Martin",
            },
            {
                "name": "Mika Häkkinen",
                "country": "FIN",
                "titles": 2,
                "wins": 20,
                "poles": 26,
                "podiums": 51,
                "points": "420.0",
                "years": "1998, 1999",
                "color": "#ff8000",
                "key_teams": "Lotus, McLaren",
            },
            {
                "name": "Emerson Fittipaldi",
                "country": "BRA",
                "titles": 2,
                "wins": 14,
                "poles": 6,
                "podiums": 35,
                "points": "281.0",
                "years": "1972, 1974",
                "color": "#ff8000",
                "key_teams": "Lotus, McLaren, Fittipaldi",
            },
            {
                "name": "Graham Hill",
                "country": "GBR",
                "titles": 2,
                "wins": 14,
                "poles": 13,
                "podiums": 36,
                "points": "289.0",
                "years": "1962, 1968",
                "color": "#1f4068",
                "key_teams": "BRM, Lotus, Brabham, Shadow, Hill",
            },
            {
                "name": "Jim Clark",
                "country": "GBR",
                "titles": 2,
                "wins": 25,
                "poles": 33,
                "podiums": 32,
                "points": "274.0",
                "years": "1963, 1965",
                "color": "#00594f",
                "key_teams": "Team Lotus",
            },
            {
                "name": "Alberto Ascari",
                "country": "ITA",
                "titles": 2,
                "wins": 13,
                "poles": 14,
                "podiums": 17,
                "points": "140.1",
                "years": "1952, 1953",
                "color": "#e80020",
                "key_teams": "Ferrari, Maserati, Lancia",
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
                "years": "2007",
                "color": "#e80020",
                "key_teams": "Sauber, McLaren, Ferrari, Lotus, Alfa Romeo",
            },
            {
                "name": "Nico Rosberg",
                "country": "GER",
                "titles": 1,
                "wins": 23,
                "poles": 30,
                "podiums": 57,
                "points": "1,594.5",
                "years": "2016",
                "color": "#00a0dd",
                "key_teams": "Williams, Mercedes",
            },
            {
                "name": "Jenson Button",
                "country": "GBR",
                "titles": 1,
                "wins": 15,
                "poles": 8,
                "podiums": 50,
                "points": "1,235.0",
                "years": "2009",
                "color": "#f5a623",
                "key_teams": "Williams, Benetton, BAR, Honda, Brawn GP, McLaren",
            },
            {
                "name": "Nigel Mansell",
                "country": "GBR",
                "titles": 1,
                "wins": 31,
                "poles": 32,
                "podiums": 59,
                "points": "482.0",
                "years": "1992",
                "color": "#64c4ff",
                "key_teams": "Lotus, Williams, Ferrari, McLaren",
            },
            {
                "name": "Damon Hill",
                "country": "GBR",
                "titles": 1,
                "wins": 22,
                "poles": 20,
                "podiums": 42,
                "points": "360.0",
                "years": "1996",
                "color": "#64c4ff",
                "key_teams": "Brabham, Williams, Arrows, Jordan",
            },
            {
                "name": "Jacques Villeneuve",
                "country": "CAN",
                "titles": 1,
                "wins": 11,
                "poles": 13,
                "podiums": 23,
                "points": "235.0",
                "years": "1997",
                "color": "#64c4ff",
                "key_teams": "Williams, BAR, Renault, Sauber",
            },
            {
                "name": "Alan Jones",
                "country": "AUS",
                "titles": 1,
                "wins": 12,
                "poles": 6,
                "podiums": 24,
                "points": "206.0",
                "years": "1980",
                "color": "#64c4ff",
                "key_teams": "Hesketh, Hill, Surtees, Shadow, Williams, Haas Lola",
            },
            {
                "name": "Mario Andretti",
                "country": "USA",
                "titles": 1,
                "wins": 12,
                "poles": 18,
                "podiums": 19,
                "points": "180.0",
                "years": "1978",
                "color": "#00594f",
                "key_teams": "Lotus, March, Ferrari, Parnelli, Alfa Romeo, Williams",
            },
            {
                "name": "Jody Scheckter",
                "country": "RSA",
                "titles": 1,
                "wins": 10,
                "poles": 3,
                "podiums": 33,
                "points": "255.0",
                "years": "1979",
                "color": "#e80020",
                "key_teams": "McLaren, Tyrrell, Wolf, Ferrari",
            },
            {
                "name": "James Hunt",
                "country": "GBR",
                "titles": 1,
                "wins": 10,
                "poles": 14,
                "podiums": 23,
                "points": "179.0",
                "years": "1976",
                "color": "#ff8000",
                "key_teams": "Hesketh, McLaren, Wolf",
            },
            {
                "name": "Keke Rosberg",
                "country": "FIN",
                "titles": 1,
                "wins": 5,
                "poles": 5,
                "podiums": 17,
                "points": "159.5",
                "years": "1982",
                "color": "#64c4ff",
                "key_teams": "Theodore, ATS, Wolf, Fittipaldi, Williams, McLaren",
            },
            {
                "name": "Denny Hulme",
                "country": "NZL",
                "titles": 1,
                "wins": 8,
                "poles": 1,
                "podiums": 33,
                "points": "248.0",
                "years": "1967",
                "color": "#ff8000",
                "key_teams": "Brabham, McLaren",
            },
            {
                "name": "Jochen Rindt",
                "country": "AUT",
                "titles": 1,
                "wins": 6,
                "poles": 10,
                "podiums": 13,
                "points": "109.0",
                "years": "1970",
                "color": "#00594f",
                "key_teams": "Cooper, Brabham, Lotus",
            },
            {
                "name": "John Surtees",
                "country": "GBR",
                "titles": 1,
                "wins": 6,
                "poles": 8,
                "podiums": 24,
                "points": "180.0",
                "years": "1964",
                "color": "#e80020",
                "key_teams": "Lotus, Cooper, Lola, Ferrari, Honda, BRM, Surtees",
            },
            {
                "name": "Giuseppe Farina",
                "country": "ITA",
                "titles": 1,
                "wins": 5,
                "poles": 5,
                "podiums": 20,
                "points": "127.3",
                "years": "1950",
                "color": "#9b111e",
                "key_teams": "Alfa Romeo, Ferrari",
            },
            {
                "name": "Phil Hill",
                "country": "USA",
                "titles": 1,
                "wins": 3,
                "poles": 6,
                "podiums": 16,
                "points": "98.0",
                "years": "1961",
                "color": "#e80020",
                "key_teams": "Maserati, Ferrari, ATS, Cooper, Eagle",
            },
            {
                "name": "Mike Hawthorn",
                "country": "GBR",
                "titles": 1,
                "wins": 3,
                "poles": 4,
                "podiums": 18,
                "points": "127.6",
                "years": "1958",
                "color": "#e80020",
                "key_teams": "Ferrari, Vanwall, BRM",
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
        "era": "1951-1961",
        "color": "#00a0dd",
        "key_teams": "Maserati, Mercedes, Vanwall, Cooper, Lotus",
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
        "era": "1994-2008",
        "color": "#64c4ff",
        "key_teams": "Williams, McLaren, Red Bull",
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
        "era": "1972-1982",
        "color": "#e80020",
        "key_teams": "Brabham, Ferrari, Lotus, Williams",
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
        "era": "2002-2017",
        "color": "#e80020",
        "key_teams": "Sauber, Ferrari, Williams",
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
        "era": "1993-2011",
        "color": "#e80020",
        "key_teams": "Jordan, Stewart, Ferrari, Honda, Brawn GP, Williams",
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
        "era": "2013-Present",
        "color": "#00a0dd",
        "key_teams": "Williams, Mercedes, Alfa Romeo / Sauber",
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
        "era": "1970-1978",
        "color": "#00594f",
        "key_teams": "March, Lotus, Tyrrell",
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
        "era": "2002-2013",
        "color": "#1e41ff",
        "key_teams": "Minardi, Jaguar, Williams, Red Bull",
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
        "era": "2018-Present",
        "color": "#e80020",
        "key_teams": "Sauber, Scuderia Ferrari",
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
        "era": "2011-2024",
        "color": "#1e41ff",
        "key_teams": "HRT, Toro Rosso, Red Bull, Renault, McLaren, RB",
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
        "era": "1967-1979",
        "color": "#e80020",
        "key_teams": "Cooper, Ferrari, Brabham, McLaren, Lotus, Ensign, Ligier",
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
        "era": "1978-1989",
        "color": "#0093cc",
        "key_teams": "Martini, Surtees, Renault, Ferrari, Ligier",
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
        "era": "2001-2006",
        "color": "#64c4ff",
        "key_teams": "Williams, McLaren",
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
        "era": "2011-Present",
        "color": "#1e41ff",
        "key_teams": "Sauber, McLaren, Force India / Racing Point, Red Bull",
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
        "era": "1977-1982",
        "color": "#e80020",
        "key_teams": "McLaren, Ferrari",
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
        "era": "2015-Present",
        "color": "#e80020",
        "key_teams": "Toro Rosso, Renault, McLaren, Ferrari, Williams",
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
        "era": "2019-Present",
        "color": "#ff8000",
        "key_teams": "McLaren",
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
        "era": "2019-Present",
        "color": "#00a0dd",
        "key_teams": "Williams, Mercedes",
    },
]


def _render_driver_card(drv: dict, is_champion: bool = True) -> str:
    color = drv.get("color", "#e10600")
    country = drv.get("country", "F1")
    name = drv.get("name", "Unknown Driver")
    titles = drv.get("titles", 0)
    wins = drv.get("wins", 0)
    poles = drv.get("poles", 0)
    podiums = drv.get("podiums", 0)
    points = drv.get("points", "0.0")

    if is_champion:
        badge_text = f"{titles}x WORLD CHAMPION" if titles > 1 else "WORLD CHAMPION"
        footer_label = "CHAMPIONSHIP SEASONS"
        footer_val = drv.get("years", "-")
    else:
        badge_text = drv.get("best_finish", "GRAND PRIX WINNER")
        footer_label = "ACTIVE ERA"
        footer_val = f"{drv.get('era', '-')} &bull; Teams: {drv.get('key_teams', '-')}"

    return f"""
    <div style="background: #161b22; border: 1px solid rgba(255,255,255,0.08); border-top: 3px solid {color}; border-radius: 6px; padding: 14px 16px; margin-bottom: 12px; height: 100%; display: flex; flex-direction: column; justify-content: space-between;">
        <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 700; color: #8e929b; letter-spacing: 0.06em; text-transform: uppercase;">{badge_text}</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; font-weight: 700; color: {color}; background: rgba(255,255,255,0.04); border: 1px solid {color}; padding: 1px 6px; border-radius: 2px;">{country}</span>
            </div>
            <div style="font-family: 'Titillium Web', sans-serif; font-size: 1.22rem; font-weight: 700; color: #f0f3f6; letter-spacing: 0.02em; margin-bottom: 10px;">{name}</div>
            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px; background: rgba(0,0,0,0.25); padding: 8px 6px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.04); margin-bottom: 10px;">
                <div style="text-align: center;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #8e929b; text-transform: uppercase;">TITLES</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.12rem; font-weight: 800; color: #f5a623;">{titles}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #8e929b; text-transform: uppercase;">WINS</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.12rem; font-weight: 800; color: #00e5ff;">{wins}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #8e929b; text-transform: uppercase;">POLES</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.12rem; font-weight: 800; color: #a855f7;">{poles}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #8e929b; text-transform: uppercase;">PODIUMS</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.12rem; font-weight: 800; color: #10b981;">{podiums}</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.58rem; color: #8e929b; text-transform: uppercase;">POINTS</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.95rem; font-weight: 800; color: #ffffff; white-space: nowrap;">{points}</div>
                </div>
            </div>
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #8e929b; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 6px; line-height: 1.4;">
            <span style="color: #6b7280;">{footer_label}:</span> <span style="color: #c9d1d9;">{footer_val}</span>
        </div>
    </div>
    """


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
        col_scope, col_search = st.columns([1, 2])
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
        with col_search:
            search_query = st.text_input("SEARCH RACER", placeholder="Filter by driver name, nationality, or era...")

    # -------------------------------------------------------------------------
    # LAYERED WORLD CHAMPIONS SECTION
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

            # Determine column count based on number of drivers
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


render_page()
