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


@st.cache_data
def get_driver_standings(year, round_num):
    try:
        ergast = Ergast()
        standings = ergast.get_driver_standings(season=year, round=round_num).content[0]
        return standings
    except Exception:
        return pd.DataFrame()


@st.cache_data
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


def _fetch_ergast_path(path):
    for base_url in (ERGAST_BASE_URL, ERGAST_FALLBACK_BASE_URL):
        payload = _fetch_json(f"{base_url}/{path}")
        if payload:
            return payload
    return {}


@st.cache_data(ttl=86400)
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


@st.cache_data(ttl=86400)
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


@st.cache_data(ttl=86400)
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


@st.cache_data(ttl=86400)
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


@st.cache_data(ttl=604800)
def get_driver_history_blurb(driver_name):
    try:
        return wikipedia.summary(f"{driver_name} Formula One", sentences=3, auto_suggest=False)
    except Exception:
        try:
            return wikipedia.summary(driver_name, sentences=3, auto_suggest=False)
        except Exception:
            return "History unavailable right now."
