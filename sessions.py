import os
from email.utils import parsedate_to_datetime
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

import fastf1
from fastf1.ergast import Ergast
import pandas as pd
import streamlit as st


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
