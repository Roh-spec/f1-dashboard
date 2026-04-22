import os

import fastf1
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


def setup_fastf1_cache(cache_dir: str = "f1_cache") -> None:
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    fastf1.Cache.enable_cache(cache_dir)


@st.cache_data
def get_schedule(year):
    return fastf1.get_event_schedule(year)


@st.cache_data
def load_session_data(year, race_name, session_name):
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
            session.load(laps=True, telemetry=False, weather=False, messages=False)
            return session.results, session.laps
        except Exception:
            continue

    return None, None


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
