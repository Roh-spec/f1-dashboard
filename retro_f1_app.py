import streamlit as st
import wikipedia

from design import inject_retro_css
from fps import render_fp_sessions
from qualifying import render_qualifying_session
from races import render_race_session
from sessions import get_event_sessions, get_schedule, setup_fastf1_cache


st.set_page_config(page_title="F1 RETRO DASH", layout="wide")
inject_retro_css()
setup_fastf1_cache()


def render_header() -> None:
    st.markdown("<h1>F1 RETRO DASH</h1>", unsafe_allow_html=True)
    st.markdown("<p>INSERT COIN TO START...</p>", unsafe_allow_html=True)
    st.divider()


def render_controls():
    col1, col2 = st.columns(2)

    with col1:
        selected_year = st.selectbox("SELECT YEAR:", list(range(2025, 2017, -1)))

    schedule = get_schedule(selected_year)
    races = schedule[schedule["EventFormat"] != "testing"]

    with col2:
        selected_race = st.selectbox("SELECT STAGE (RACE):", races["EventName"].tolist())

    event = races[races["EventName"] == selected_race].iloc[0]
    return selected_year, selected_race, event


def render_track_details(event) -> None:
    with st.container(border=True):
        st.markdown(f"<h2>Stage: {event['Location']}</h2>", unsafe_allow_html=True)

        col_track1, col_track2 = st.columns([2, 1])

        with col_track1:
            st.markdown("<h3>Track Archives</h3>", unsafe_allow_html=True)
            circuit_name = event["Location"] + " Grand Prix"
            try:
                wiki_summary = wikipedia.summary(circuit_name, sentences=4)
                st.write(f"> {wiki_summary}")
            except Exception:
                try:
                    wiki_summary = wikipedia.summary(event["EventName"], sentences=4)
                    st.write(f"> {wiki_summary}")
                except Exception:
                    st.write("> Data unavailable. Unable to load track history.")

        with col_track2:
            st.markdown("<h3>Stage Stats</h3>", unsafe_allow_html=True)
            st.write(f"**ROUND:** {event['RoundNumber']}")
            st.write(f"**CIRCUIT:** {event['EventName']}")
            st.write(f"**LOCATION:** {event['Location']}, {event['Country']}")
            st.write(f"**DATE:** {event['EventDate'].date()}")

    st.divider()


def render_sessions(year, race_name, event) -> None:
    event_sessions = get_event_sessions(event)
    practice_sessions = [name for name in event_sessions if name.startswith("Practice")]
    result_sessions = [name for name in event_sessions if not name.startswith("Practice")]

    render_fp_sessions(year, race_name, practice_sessions)

    for session_name in result_sessions:
        if session_name in {"Qualifying", "Sprint Qualifying", "Sprint Shootout"}:
            render_qualifying_session(year, race_name, session_name)
        elif session_name in {"Race", "Sprint"}:
            render_race_session(year, race_name, session_name)


def main() -> None:
    render_header()
    selected_year, selected_race, event = render_controls()
    render_track_details(event)
    render_sessions(selected_year, selected_race, event)


main()
