import streamlit as st
import wikipedia
import pandas as pd
import matplotlib.pyplot as plt
from fastf1.exceptions import DataNotLoadedError

from circuit_map import render_circuit_map
from design import render_standings_bar_card
from fps import render_fp_sessions
from qualifying import render_qualifying_session
from races import render_race_session
from sessions import (
    get_event_sessions,
    get_driver_standings,
    get_constructor_standings,
    get_schedule,
    load_session_data,
)
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


def render_track_condition_overlay(year, race_name) -> None:
    with st.container(border=True, key="dialog_track_condition_overlay"):
        st.markdown("<p class='section-kicker'>Track Condition Overlay</p>", unsafe_allow_html=True)
        st.markdown("<h2>Weather, Pace & Incident Windows</h2>", unsafe_allow_html=True)

        session, results, laps = load_session_data(year, race_name, "Race")
        if session is None or laps is None or laps.empty:
            session, results, laps = load_session_data(year, race_name, "Sprint")

        if session is None or laps is None or laps.empty:
            st.warning("Track-condition overlay unavailable for this event.")
            return

        try:
            weather = session.weather_data
        except DataNotLoadedError:
            weather = None
        except Exception:
            weather = None
        lap_pace = laps.dropna(subset=["LapNumber", "LapTime"]).copy()
        if lap_pace.empty:
            st.warning("Lap pace data unavailable for this session.")
            return

        lap_pace["LapSec"] = lap_pace["LapTime"].dt.total_seconds()
        lap_pace = (
            lap_pace.groupby("LapNumber", as_index=False)["LapSec"]
            .median()
            .sort_values("LapNumber")
        )

        incident_df = pd.DataFrame(columns=["Lap", "Category", "Message"])
        try:
            msgs = session.race_control_messages
            if msgs is not None and not msgs.empty and "Message" in msgs:
                msg_map = [
                    ("RED FLAG", "Red Flag"),
                    ("VIRTUAL SAFETY CAR", "VSC"),
                    ("SAFETY CAR", "Safety Car"),
                    ("PENALTY", "Penalty"),
                    ("INVESTIGATION", "Investigation"),
                ]
                frames = []
                for keyword, label in msg_map:
                    subset = msgs[msgs["Message"].str.contains(keyword, case=False, na=False)].copy()
                    if subset.empty:
                        continue
                    subset["Category"] = label
                    frames.append(subset)

                if frames:
                    incident_df = pd.concat(frames, ignore_index=True)
                    if "Lap" not in incident_df:
                        incident_df["Lap"] = pd.NA
                    incident_df = incident_df[["Lap", "Category", "Message"]].copy()
        except Exception:
            pass

        # Weather summary (text-first, no weather graph)
        weather_line = "On-track weather data unavailable for this session."
        if weather is not None and not weather.empty:
            details = []
            if "TrackTemp" in weather and not weather["TrackTemp"].dropna().empty:
                details.append(f"Track {weather['TrackTemp'].dropna().mean():.1f} C avg")
            if "AirTemp" in weather and not weather["AirTemp"].dropna().empty:
                details.append(f"Air {weather['AirTemp'].dropna().mean():.1f} C avg")
            if "WindSpeed" in weather and not weather["WindSpeed"].dropna().empty:
                details.append(f"Wind {weather['WindSpeed'].dropna().mean():.1f} m/s avg")
            if "Rainfall" in weather and not weather["Rainfall"].dropna().empty:
                raining = weather["Rainfall"].fillna(False).astype(bool).any()
                details.append("Wet conditions reported" if raining else "Dry running")
            if details:
                weather_line = " | ".join(details)

        st.info(f"On-track weather: {weather_line}")

        fig, ax_pace = plt.subplots(1, 1, figsize=(10.5, 3.9), constrained_layout=True)
        fig.patch.set_facecolor("#211d18")
        ax_pace.set_facecolor("#211d18")

        # Lap pace panel
        ax_pace.plot(
            lap_pace["LapNumber"], lap_pace["LapSec"],
            color="#e5dccb", linewidth=1.8, label="Median Lap Pace (s)"
        )

        incident_colors = {
            "Red Flag": "#d81f2e",
            "Safety Car": "#f4d03f",
            "VSC": "#ff9f1a",
            "Penalty": "#6fa8ff",
            "Investigation": "#9b8cff",
        }
        if not incident_df.empty:
            for _, row in incident_df.dropna(subset=["Lap"]).iterrows():
                try:
                    lap = float(row["Lap"])
                except Exception:
                    continue
                color = incident_colors.get(row["Category"], "#8f9cb0")
                ax_pace.axvspan(lap - 0.5, lap + 0.5, color=color, alpha=0.18)

        ax_pace.set_title("Lap Pace vs Incident Windows", color="#fbf7ee", fontsize=11)
        ax_pace.set_xlabel("Lap", color="#e5dccb")
        ax_pace.set_ylabel("Lap Time (s)", color="#e5dccb")
        ax_pace.tick_params(colors="#e5dccb")
        for spine in ax_pace.spines.values():
            spine.set_color("#6f675b")
        ax_pace.grid(color="#2a3146", alpha=0.35, linewidth=0.6)
        ax_pace.legend(facecolor="#211d18", edgecolor="#6f675b", labelcolor="#e5dccb", fontsize="small")

        st.pyplot(fig)

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric("Median Race Pace", f"{lap_pace['LapSec'].median():.2f} s")
        with metric_col2:
            if weather is not None and not weather.empty and "TrackTemp" in weather:
                st.metric("Avg Track Temp", f"{weather['TrackTemp'].dropna().mean():.1f} C")
            else:
                st.metric("Avg Track Temp", "N/A")
        with metric_col3:
            if weather is not None and not weather.empty and "WindSpeed" in weather:
                st.metric("Avg Wind Speed", f"{weather['WindSpeed'].dropna().mean():.1f} m/s")
            else:
                st.metric("Avg Wind Speed", "N/A")

        if incident_df.empty:
            st.caption("No major race-control incident windows detected in this overlay.")

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

def render_standings(year, round_num) -> None:
    st.markdown("<div class='section-ribbon'><span>CHAMPIONSHIP STANDINGS</span><span>WDC & WCC</span></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("<h3>World Driver Championship</h3>", unsafe_allow_html=True)
            wdc = get_driver_standings(year, round_num)
            if not wdc.empty:
                wdc_display = wdc[['position', 'givenName', 'familyName', 'points', 'wins']].copy()
                wdc_display['DRIVER'] = wdc_display['givenName'] + " " + wdc_display['familyName']
                wdc_display = wdc_display[['position', 'DRIVER', 'points', 'wins']]
                wdc_display.rename(columns={'position': 'POS', 'points': 'PTS', 'wins': 'WINS'}, inplace=True)
                render_standings_bar_card(
                    wdc_display,
                    title="Driver Standings",
                    name_column="DRIVER",
                    points_column="PTS",
                    limit=20,
                )
            else:
                st.warning("WDC Standings unavailable.")

    with col2:
        with st.container(border=True):
            st.markdown("<h3>World Constructor Championship</h3>", unsafe_allow_html=True)
            wcc = get_constructor_standings(year, round_num)
            if not wcc.empty:
                # The ergast data for constructors actually returns 'constructorName' based on my earlier check
                wcc_display = wcc[['position', 'constructorName', 'points', 'wins']].copy() if 'constructorName' in wcc else wcc[['position', 'constructorNames', 'points', 'wins']].copy()
                if 'constructorNames' in wcc_display:
                    wcc_display['TEAM'] = wcc_display['constructorNames'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x)
                else:
                    wcc_display['TEAM'] = wcc_display['constructorName']
                    
                wcc_display = wcc_display[['position', 'TEAM', 'points', 'wins']]
                wcc_display.rename(columns={'position': 'POS', 'points': 'PTS', 'wins': 'WINS'}, inplace=True)
                render_standings_bar_card(
                    wcc_display,
                    title="Constructor Standings",
                    name_column="TEAM",
                    points_column="PTS",
                    limit=20,
                    highlight_top=True,
                )
            else:
                st.warning("WCC Standings unavailable.")


def render_end_race_bar(event, selected_year) -> None:
    next_event = None
    try:
        schedule = get_schedule(int(selected_year))
        if schedule is not None and not schedule.empty and "RoundNumber" in schedule:
            next_events = schedule[schedule["RoundNumber"] > int(event["RoundNumber"])].sort_values("RoundNumber")
            if not next_events.empty:
                next_event = next_events.iloc[0]
    except Exception:
        next_event = None

    left_col, right_col = st.columns([4.2, 1.8], vertical_alignment="center")
    with left_col:
        st.markdown(
            (
                "<div class='section-ribbon'>"
                f"<span>{event['Location']}</span>"
                f"<span>ROUND {event['RoundNumber']}</span>"
                f"<span>{event['EventDate'].year}</span>"
                "</div>"
            ),
            unsafe_allow_html=True,
        )
    with right_col:
        if next_event is not None:
            next_label = str(next_event.get("EventName", "Next Race")).upper()
            if st.button(
                f"NEXT RACE: {next_label} ➜",
                key="race_analysis_next_race_link",
                type="tertiary",
                use_container_width=True,
            ):
                st.session_state.selected_event = next_event
                st.session_state.selected_race = str(next_event.get("EventName", ""))
                st.session_state.selected_year = int(selected_year)
                st.rerun()
        else:
            st.markdown(
                "<div class='section-ribbon'><span>SEASON COMPLETE</span></div>",
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

    top_nav_col1, top_nav_col2, _ = st.columns([1.2, 1.2, 4])
    with top_nav_col1:
        if st.button("🏁 RACE SELECT", key="race_analysis_top_race_select"):
            st.switch_page("pages/1_Race_Select.py")
    with top_nav_col2:
        if st.button("🔄 CHANGE RACE", key="race_analysis_top_change_race"):
            st.switch_page("pages/1_Race_Select.py")
        
    render_event_snapshot(event, event_sessions)
    render_track_details(selected_year, selected_race, event)
    render_track_condition_overlay(selected_year, selected_race)
    render_stage_stats(event, event_sessions)
    render_sessions(selected_year, selected_race, event)
    render_standings(selected_year, event['RoundNumber'])
    render_end_race_bar(event, selected_year)
