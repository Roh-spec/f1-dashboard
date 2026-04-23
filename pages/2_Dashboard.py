import streamlit as st
import wikipedia

from circuit_map import render_circuit_map
from fps import render_fp_sessions
from qualifying import render_qualifying_session
from races import render_race_session
from sessions import get_event_sessions
from track_analysis import render_circuit_winners, render_track_analysis

def _format_summary_card(label: str, value: str, note: str) -> str:
    return (
        f"<div class='summary-card'>"
        f"<div class='summary-label'>{label}</div>"
        f"<div class='summary-value'>{value}</div>"
        f"<p class='summary-note'>{note}</p>"
        f"</div>"
    )

def render_event_snapshot(event, event_sessions) -> None:
    practice_sessions = [name for name in event_sessions if name.startswith("Practice")]
    result_sessions = [name for name in event_sessions if not name.startswith("Practice")]
    session_count = len(event_sessions)

    with st.container(border=True, key="dialog_event_snapshot"):
        st.markdown("<p class='section-kicker'>Race Briefing</p>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='section-ribbon'><span>SESSION ARCHIVE</span><span>{session_count} AVAILABLE</span><span>{len(practice_sessions)} PRACTICE</span><span>{len(result_sessions)} RESULTS</span></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='summary-strip'>\n"
            f"{_format_summary_card('Season', str(event['EventDate'].year), f'Round {event['RoundNumber']}')}\n"
            f"{_format_summary_card('Venue', event['EventName'], f'{event['Location']}, {event['Country']}')}\n"
            f"{_format_summary_card('Date', str(event['EventDate'].date()), f'{session_count} archived sessions')}\n"
            f"{_format_summary_card('Format', str(event.get('EventFormat', 'race')).title(), f'{len(practice_sessions)} practice and {len(result_sessions)} result sessions')}\n"
            f"</div>",
            unsafe_allow_html=True,
        )

def render_track_details(year, race_name, event) -> None:
    with st.container(border=True, key="dialog_track_details"):
        st.markdown("<p class='section-kicker'>Circuit Intelligence</p>", unsafe_allow_html=True)
        st.markdown(f"<h2>Stage: {event['Location']}</h2>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='section-ribbon'><span>{event['EventName']}</span><span>{event['Country']}</span><span>ROUND {event['RoundNumber']}</span></div>",
            unsafe_allow_html=True,
        )

        col_track1, col_track2 = st.columns([2, 1])

        with col_track1:
            with st.container(border=True, key="track_archive_panel"):
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

                render_track_analysis(event)

        with col_track2:
            with st.container(border=True, key="circuit_map_panel"):
                render_circuit_map(year, race_name, event)
                render_circuit_winners(event)

def render_stage_stats(event, event_sessions) -> None:
    with st.container(border=True, key="dialog_stage_stats"):
        practice_sessions = [name for name in event_sessions if name.startswith("Practice")]
        result_sessions = [name for name in event_sessions if not name.startswith("Practice")]

        st.markdown("<p class='section-kicker'>Grid Notes</p>", unsafe_allow_html=True)
        st.markdown("<h2>Stage Stats</h2>", unsafe_allow_html=True)
        st.markdown(
            f"<div class='summary-strip'>\n"
            f"{_format_summary_card('Round', str(event['RoundNumber']), f'Season {event['EventDate'].year}')}\n"
            f"{_format_summary_card('Circuit', event['EventName'], event['Location'])}\n"
            f"{_format_summary_card('Country', event['Country'], f'{len(practice_sessions)} practice sessions')}\n"
            f"{_format_summary_card('Sessions', str(len(event_sessions)), f'{len(result_sessions)} result sessions')}\n"
            f"</div>",
            unsafe_allow_html=True,
        )

def render_sessions(year, race_name, event) -> None:
    event_sessions = get_event_sessions(event)
    practice_sessions = [name for name in event_sessions if name.startswith("Practice")]
    result_sessions = [name for name in event_sessions if not name.startswith("Practice")]

    st.markdown(
        "<div class='section-ribbon'><span>SESSION PANELS</span><span>FASTEST LAPS</span><span>QUALIFYING</span><span>RACE RESULTS</span></div>",
        unsafe_allow_html=True,
    )
    render_fp_sessions(year, race_name, practice_sessions)

    for session_name in result_sessions:
        if session_name in {"Qualifying", "Sprint Qualifying", "Sprint Shootout"}:
            render_qualifying_session(year, race_name, session_name)
        elif session_name in {"Race", "Sprint"}:
            render_race_session(year, race_name, session_name)

if "selected_event" not in st.session_state:
    st.warning("No archive selected. Please select a race from the Race Select page.")
    if st.button("Go to Race Select"):
        st.switch_page("pages/1_Race_Select.py")
else:
    event = st.session_state.selected_event
    selected_year = st.session_state.selected_year
    selected_race = st.session_state.selected_race
    
    event_sessions = get_event_sessions(event)
    
    if st.button("← RETURN TO RACE SELECT"):
        st.switch_page("pages/1_Race_Select.py")
        
    render_event_snapshot(event, event_sessions)
    render_track_details(selected_year, selected_race, event)
    render_stage_stats(event, event_sessions)
    render_sessions(selected_year, selected_race, event)
