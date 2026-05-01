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
ERGAST_BASE_URL = "https://ergast.com/api/f1"
ERGAST_FALLBACK_BASE_URL = "https://api.jolpi.ca/ergast/f1"

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
    {"driverId": "alonso", "givenName": "Fernando", "familyName": "Alonso", "nationality": "Spanish"},
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
    "sauber": "Alessandro Alunni Bravi",
    "williams": "James Vowles",
}

TEAM_PREVIOUS_NAMES = {
    "alpine": ["Renault", "Lotus F1 Team", "Benetton"],
    "aston_martin": ["Racing Point", "Force India", "Spyker", "Midland", "Jordan"],
    "ferrari": [],
    "haas": [],
    "mclaren": [],
    "mercedes": ["Brawn GP", "Tyrrell"],
    "rb": ["AlphaTauri", "Toro Rosso", "Minardi"],
    "red_bull": ["Jaguar", "Stewart"],
    "sauber": ["Alfa Romeo", "BMW Sauber"],
    "williams": [],
}

TEAM_LINEAGE = {
    "alpine": {
        "aliases": ["alpine", "renault", "lotus_f1", "benetton"],
        "previous_names": ["Benetton", "Lotus F1 Team", "Renault"],
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
        "aliases": ["mercedes", "brawn", "tyrrell"],
        "previous_names": ["Brawn GP", "Tyrrell"],
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


def _resolve_team_lineage(constructor_id):
    for _, lineage in TEAM_LINEAGE.items():
        if constructor_id in lineage.get("aliases", []):
            return lineage

    return {
        "aliases": [constructor_id],
        "previous_names": TEAM_PREVIOUS_NAMES.get(constructor_id, []),
    }


def setup_fastf1_cache(cache_dir: str = "f1_cache") -> None:
    global _CACHE_READY
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    fastf1.Cache.enable_cache(cache_dir)
    _CACHE_READY = True


@st.cache_data
def get_schedule(year):
    return fastf1.get_event_schedule(year)


@st.cache_data
def load_session_data(year, race_name, session_name):
    if not _CACHE_READY:
        setup_fastf1_cache()

    session_code = SESSION_CODES.get(session_name, session_name)
    session_identifiers = [session_code]

    if session_name != session_code:
        session_identifiers.append(session_name)
    if session_name == "Sprint Qualifying":
        session_identifiers.append("Sprint Shootout")
    if session_name == "Sprint Shootout":
        session_identifiers.extend(["SS", "Sprint Qualifying"])

    for session_identifier in session_identifiers:
        try:
            session = fastf1.get_session(year, race_name, session_identifier)
            session.load(laps=True, telemetry=True, weather=False, messages=True)
        except Exception:
            continue

        results = None
        laps = None

        try:
            results = session.results
        except Exception:
            results = None

        try:
            laps = session.laps
        except Exception:
            laps = None

        if results is not None or laps is not None:
            return session, results, laps

    return None, None, None


@st.cache_data(ttl=3600)
def get_driver_standings(year, round_num):
    try:
        ergast = Ergast()
        standings = ergast.get_driver_standings(season=year, round=round_num).content[0]
        return standings
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def get_constructor_standings(year, round_num):
    try:
        ergast = Ergast()
        standings = ergast.get_constructor_standings(season=year, round=round_num).content[0]
        return standings
    except Exception:
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
        if payload:
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


@st.cache_data(ttl=3600)
def get_all_wcc_titles():
    payload = _fetch_ergast_path("constructorStandings/1.json?limit=1000")
    standings_lists = payload.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
    if not standings_lists:
        return pd.DataFrame(columns=["season", "constructorId", "constructorName", "points"])

    rows = []
    for season_row in standings_lists:
        season = int(season_row.get("season", 0) or 0)
        standings = season_row.get("ConstructorStandings", [])
        if not standings:
            continue
        winner = standings[0]
        constructor = winner.get("Constructor", {})
        try:
            points = float(winner.get("points", 0.0))
        except (TypeError, ValueError):
            points = 0.0

        rows.append(
            {
                "season": season,
                "constructorId": constructor.get("constructorId", ""),
                "constructorName": constructor.get("name", ""),
                "points": points,
            }
        )

    if not rows:
        return pd.DataFrame(columns=["season", "constructorId", "constructorName", "points"])

    titles = pd.DataFrame(rows)
    titles = titles.sort_values("season").reset_index(drop=True)
    return titles


@st.cache_data(ttl=3600)
def get_all_wdc_titles():
    payload = _fetch_ergast_path("driverStandings/1.json?limit=1000")
    standings_lists = payload.get("MRData", {}).get("StandingsTable", {}).get("StandingsLists", [])
    if not standings_lists:
        return pd.DataFrame(columns=["season", "constructorId", "driverName", "points"])

    rows = []
    for season_row in standings_lists:
        season = int(season_row.get("season", 0) or 0)
        standings = season_row.get("DriverStandings", [])
        if not standings:
            continue

        winner = standings[0]
        driver = winner.get("Driver", {})
        constructors = winner.get("Constructors", [])
        constructor = constructors[0] if constructors else {}
        driver_name = f"{driver.get('givenName', '')} {driver.get('familyName', '')}".strip()

        try:
            points = float(winner.get("points", 0.0))
        except (TypeError, ValueError):
            points = 0.0

        rows.append(
            {
                "season": season,
                "constructorId": constructor.get("constructorId", ""),
                "driverName": driver_name or "Unknown Driver",
                "points": points,
            }
        )

    if not rows:
        return pd.DataFrame(columns=["season", "constructorId", "driverName", "points"])

    titles = pd.DataFrame(rows)
    titles = titles.sort_values("season").reset_index(drop=True)
    return titles


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
            season = int(row["season"])
            winning_constructor_id = row.get("constructorId", constructor_id)
            drivers_df = get_constructor_season_driver_points(winning_constructor_id, season)
            if drivers_df.empty:
                drivers_text = "Drivers unavailable"
            else:
                drivers_text = ", ".join(
                    [f"{drow['driverName']} ({drow['points']:.1f})" for _, drow in drivers_df.iterrows()]
                )

            wcc_entries.append(
                {
                    "season": season,
                    "points": float(row["points"]),
                    "drivers": drivers_text,
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
        # Safe fallback: if season calendar endpoint is unavailable,
        # derive rounds from season results so chart data can still render.
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

    # Fallback when standings endpoint is unavailable: cumulative race points.
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

        # Break safely if endpoint stops advancing or all pages are consumed.
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
