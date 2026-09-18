import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from fastf1.exceptions import DataNotLoadedError

from ui import render_standings_bar_card
from fps import render_fp_sessions
from qualifying import render_qualifying_session
from races import render_race_session
import sessions

get_event_sessions = sessions.get_event_sessions
get_driver_standings = sessions.get_driver_standings
get_constructor_standings = sessions.get_constructor_standings
get_schedule = sessions.get_schedule
get_track_wiki_summary = sessions.get_track_wiki_summary
load_session_data = sessions.load_session_data
get_openf1_weather = getattr(sessions, "get_openf1_weather", None)
get_openf1_race_control = getattr(sessions, "get_openf1_race_control", None)
from track_analysis import CIRCUIT_ALIASES, render_circuit_map, render_circuit_records, render_track_analysis
from charts import plot_driver_telemetry_comparison


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
        season_val = str(event["EventDate"].year)
        round_val = f"Round {event.get('RoundNumber', '')}"
        circuit_val = str(event.get("EventName", ""))
        loc_val = f"{event.get('Location', '')}, {event.get('Country', '')}"
        date_val = str(event["EventDate"].date())
        format_name = str(event.get("EventFormat", "race")).title()
        format_note = f"{format_name} Weekend"
        sessions_val = f"{session_count} Sessions"
        sessions_note = f"{len(practice_sessions)} Practice · {len(result_sessions)} Qual/Race"

        st.markdown(
            f"<div class='summary-strip'>\n"
            f"{_format_summary_card('Round & Season', round_val, f'{season_val} FIA Championship')}\n"
            f"{_format_summary_card('Venue & Stage', circuit_val, loc_val)}\n"
            f"{_format_summary_card('Date & Format', date_val, format_note)}\n"
            f"{_format_summary_card('Archived Sessions', sessions_val, sessions_note)}\n"
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
                loc_name = str(event.get("Location", "")).strip()
                event_name = str(event.get("EventName", "")).strip()
                primary_candidate = CIRCUIT_ALIASES.get(loc_name.lower()) or CIRCUIT_ALIASES.get(event_name.lower())
                if not primary_candidate:
                    primary_candidate = f"{loc_name} Circuit" if loc_name else event_name

                fallback_candidate = event_name if primary_candidate != event_name else f"{loc_name} Grand Prix"

                wiki_summary = get_track_wiki_summary(primary_candidate, fallback_candidate, sentences=4)
                if wiki_summary:
                    st.markdown(
                        f"<div class='track-archive-quote' style='background: #11151d; border-left: 3px solid #e10600; padding: 14px 18px; margin-bottom: 18px; color: #d0d7de; font-size: 0.90rem; line-height: 1.6; font-family: \"Inter\", sans-serif;'>"
                        f"{wiki_summary}"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        """
                        <div style="background: #11151d; border: 1px dashed #262c36; border-radius: 0px; padding: 22px 18px; text-align: center; margin-bottom: 18px;">
                            <div style="font-size: 1.35rem; color: #8b949e; margin-bottom: 6px; opacity: 0.75;">🏛️</div>
                            <div style="font-family: 'Titillium Web', sans-serif; font-size: 0.85rem; font-weight: 700; color: #8b949e; letter-spacing: 0.08em; text-transform: uppercase;">Track Archives Unavailable</div>
                            <div style="font-family: 'Inter', sans-serif; font-size: 0.78rem; color: #4b5563; margin-top: 4px;">Historical overview not indexed for this circuit.</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                render_track_analysis(event)

        with col_track2:
            with st.container(border=True, key="circuit_map_panel"):
                render_circuit_map(year, race_name, event)
                render_circuit_records(event)


def render_track_condition_overlay(year, race_name, *args, **kwargs) -> None:
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

        if weather is None or (hasattr(weather, "empty") and weather.empty):
            try:
                weather = get_openf1_weather(int(year), race_name, "Race")
            except Exception:
                weather = None

        lap_pace = laps.dropna(subset=["LapNumber", "LapTime"]).copy()
        if lap_pace.empty:
            st.warning("Lap pace data unavailable for this session.")
            return

        lap_pace["LapSec"] = pd.to_timedelta(lap_pace["LapTime"], errors="coerce").dt.total_seconds()
        lap_pace = lap_pace.dropna(subset=["LapSec"])
        if lap_pace.empty:
            st.warning("Lap pace data unavailable for this session.")
            return

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

        if incident_df.empty:
            try:
                openf1_rc = get_openf1_race_control(int(year), race_name, "Race")
                if openf1_rc is not None and not openf1_rc.empty:
                    incident_df = openf1_rc
            except Exception:
                pass

        weather_line = "On-track weather data unavailable for this session."
        if weather is not None and not weather.empty:
            details = []
            if "TrackTemp" in weather and not weather["TrackTemp"].dropna().empty:
                details.append(f"Track {weather['TrackTemp'].dropna().mean():.1f}°C avg")
            if "AirTemp" in weather and not weather["AirTemp"].dropna().empty:
                details.append(f"Air {weather['AirTemp'].dropna().mean():.1f}°C avg")
            if "WindSpeed" in weather and not weather["WindSpeed"].dropna().empty:
                details.append(f"Wind {weather['WindSpeed'].dropna().mean():.1f} m/s avg")
            if "Rainfall" in weather and not weather["Rainfall"].dropna().empty:
                raining = weather["Rainfall"].fillna(False).astype(bool).any()
                details.append("Wet conditions reported" if raining else "Dry running")
            if details:
                weather_line = " | ".join(details)
        weather_line = weather_line.replace("Â°C", " C").replace("°C", " C")

        st.info(f"On-track weather: {weather_line}")

        # Broadcast Telemetry Incident Key Strip
        st.markdown(
            """
            <div style="background: #11151d; border: 1px solid #262c36; border-left: 3px solid #e10600; border-radius: 0px; padding: 10px 14px; margin-bottom: 12px; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 10px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; font-weight: 700; color: #e10600; letter-spacing: 0.12em; text-transform: uppercase;">TELEMETRY KEY</span>
                    <span style="color: #262c36; font-family: 'JetBrains Mono', monospace;">//</span>
                    <span style="font-family: 'Inter', sans-serif; font-size: 0.78rem; color: #8b949e;">Incident window shading & pace curve</span>
                </div>
                <div style="display: flex; flex-wrap: wrap; align-items: center; gap: 14px;">
                    <div style="display: inline-flex; align-items: center; gap: 6px;">
                        <span style="display: inline-block; width: 16px; height: 3px; background: #e10600; border-radius: 1px;"></span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #f0f3f6; font-weight: 600;">Median Lap Pace</span>
                    </div>
                    <div style="display: inline-flex; align-items: center; gap: 6px;">
                        <span style="display: inline-block; width: 10px; height: 10px; background: rgba(225, 6, 0, 0.45); border: 1px solid #e10600;"></span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #f0f3f6; font-weight: 600;">Red Flag (Stoppage)</span>
                    </div>
                    <div style="display: inline-flex; align-items: center; gap: 6px;">
                        <span style="display: inline-block; width: 10px; height: 10px; background: rgba(245, 166, 35, 0.45); border: 1px solid #f5a623;"></span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #f0f3f6; font-weight: 600;">Safety Car (SC)</span>
                    </div>
                    <div style="display: inline-flex; align-items: center; gap: 6px;">
                        <span style="display: inline-block; width: 10px; height: 10px; background: rgba(234, 179, 8, 0.45); border: 1px solid #eab308;"></span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #f0f3f6; font-weight: 600;">Virtual Safety Car (VSC)</span>
                    </div>
                    <div style="display: inline-flex; align-items: center; gap: 6px;">
                        <span style="display: inline-block; width: 10px; height: 10px; background: rgba(56, 189, 248, 0.45); border: 1px solid #38bdf8;"></span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #f0f3f6; font-weight: 600;">Penalty</span>
                    </div>
                    <div style="display: inline-flex; align-items: center; gap: 6px;">
                        <span style="display: inline-block; width: 10px; height: 10px; background: rgba(168, 85, 247, 0.45); border: 1px solid #a855f7;"></span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #f0f3f6; font-weight: 600;">Under Investigation</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        fig, ax_pace = plt.subplots(1, 1, figsize=(10.5, 3.8), constrained_layout=True)
        fig.patch.set_facecolor("#161b22")
        ax_pace.set_facecolor("#161b22")

        # Lap pace curve
        ax_pace.plot(
            lap_pace["LapNumber"], lap_pace["LapSec"],
            color="#e10600", linewidth=2.0, label="Median Lap Pace (s)", zorder=4
        )

        incident_colors = {
            "Red Flag": "#e10600",
            "Safety Car": "#f5a623",
            "VSC": "#eab308",
            "Penalty": "#38bdf8",
            "Investigation": "#a855f7",
        }
        present_categories = set()
        if not incident_df.empty:
            for _, row in incident_df.dropna(subset=["Lap"]).iterrows():
                try:
                    lap = float(row["Lap"])
                except Exception:
                    continue
                cat = row["Category"]
                color = incident_colors.get(cat, "#8f9cb0")
                ax_pace.axvspan(
                    lap - 0.45, lap + 0.45,
                    facecolor=color, edgecolor=color, linewidth=0.5, alpha=0.30, zorder=2
                )
                present_categories.add(cat)

        ax_pace.set_title("Lap Pace vs Incident Windows", color="#f0f3f6", fontsize=10, weight="bold", fontfamily="monospace")
        ax_pace.set_xlabel("Lap", color="#8b949e", fontsize=9)
        ax_pace.set_ylabel("Lap Time (s)", color="#8b949e", fontsize=9)
        ax_pace.tick_params(colors="#8b949e", labelsize=8)
        for spine in ax_pace.spines.values():
            spine.set_color("#262c36")
        ax_pace.grid(color="#262c36", alpha=0.5, linewidth=0.6)

        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric("Median Race Pace", f"{lap_pace['LapSec'].median():.2f} s")
        with metric_col2:
            if weather is not None and not weather.empty and "TrackTemp" in weather and not weather["TrackTemp"].dropna().empty:
                st.metric("Avg Track Temp", f"{weather['TrackTemp'].dropna().mean():.1f} C")
            else:
                st.metric("Avg Track Temp", "N/A")
        with metric_col3:
            if weather is not None and not weather.empty and "WindSpeed" in weather and not weather["WindSpeed"].dropna().empty:
                st.metric("Avg Wind Speed", f"{weather['WindSpeed'].dropna().mean():.1f} m/s")
            else:
                st.metric("Avg Wind Speed", "N/A")

        if not incident_df.empty:
            with st.expander(f"RACE CONTROL INCIDENT LOG ({len(incident_df)} EVENTS)"):
                st.dataframe(
                    incident_df.sort_values(["Lap", "Category"], na_position="last").reset_index(drop=True),
                    use_container_width=True,
                    hide_index=True,
                )
        else:
            st.caption("No major race-control incident windows detected in this overlay.")


def render_standings(year, round_num) -> None:
    st.markdown("<div class='section-ribbon'><span>CHAMPIONSHIP STANDINGS</span><span>WDC & WCC</span></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("<h3>World Driver Championship</h3>", unsafe_allow_html=True)
            wdc = get_driver_standings(year, round_num)
            if not wdc.empty:
                wdc_display = wdc.copy()
                wdc_display['DRIVER'] = wdc_display['givenName'] + " " + wdc_display['familyName']
                if 'constructorNames' in wdc_display:
                    wdc_display['TEAM'] = wdc_display['constructorNames'].apply(
                        lambda x: x[0] if isinstance(x, list) and len(x) > 0 else (str(x) if pd.notna(x) else "")
                    )
                elif 'constructorName' in wdc_display:
                    wdc_display['TEAM'] = wdc_display['constructorName']
                else:
                    wdc_display['TEAM'] = ""
                wdc_display = wdc_display[['position', 'DRIVER', 'TEAM', 'points', 'wins']]
                wdc_display.rename(columns={'position': 'POS', 'points': 'PTS', 'wins': 'WINS'}, inplace=True)
                
                # Format POS without decimal (.0 removal)
                wdc_display['POS'] = wdc_display['POS'].apply(
                    lambda x: str(int(float(x))) if pd.notna(x) and str(x).replace('.0', '').isdigit() else str(x)
                )

                top_max_points = None
                try:
                    top_max_points = float(wdc_display['PTS'].iloc[0])
                except Exception:
                    top_max_points = None

                render_standings_bar_card(
                    wdc_display,
                    title="Driver Standings",
                    name_column="DRIVER",
                    points_column="PTS",
                    limit=10,
                )

                if len(wdc_display) > 10:
                    with st.expander(f"SHOW FULL GRID ({len(wdc_display)} DRIVERS)"):
                        render_standings_bar_card(
                            wdc_display.iloc[10:],
                            title="",
                            name_column="DRIVER",
                            points_column="PTS",
                            limit=len(wdc_display) - 10,
                            max_points_override=top_max_points,
                            as_card=False,
                        )
            else:
                st.warning("WDC Standings unavailable.")

    with col2:
        with st.container(border=True):
            st.markdown("<h3>World Constructor Championship</h3>", unsafe_allow_html=True)
            wcc = get_constructor_standings(year, round_num)
            if not wcc.empty:
                wcc_display = wcc[['position', 'constructorName', 'points', 'wins']].copy() if 'constructorName' in wcc else wcc[['position', 'constructorNames', 'points', 'wins']].copy()
                if 'constructorNames' in wcc_display:
                    wcc_display['TEAM'] = wcc_display['constructorNames'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else x)
                else:
                    wcc_display['TEAM'] = wcc_display['constructorName']

                wcc_display = wcc_display[['position', 'TEAM', 'points', 'wins']]
                wcc_display.rename(columns={'position': 'POS', 'points': 'PTS', 'wins': 'WINS'}, inplace=True)
                
                # Format POS without decimal (.0 removal)
                wcc_display['POS'] = wcc_display['POS'].apply(
                    lambda x: str(int(float(x))) if pd.notna(x) and str(x).replace('.0', '').isdigit() else str(x)
                )

                render_standings_bar_card(
                    wcc_display,
                    title="Constructor Standings",
                    name_column="TEAM",
                    points_column="PTS",
                    limit=len(wcc_display),
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

    with st.container(border=True, key="dialog_end_race_nav"):
        left_col, mid_col, right_col = st.columns([1.2, 4.6, 1.2], vertical_alignment="center")

        with mid_col:
            st.markdown(
                (
                    "<div style='text-align: center; color: #f0f3f6; font-family: \"Titillium Web\", sans-serif; font-weight: 800; font-size: 1.1rem; letter-spacing: 0.06em; text-transform: uppercase;'>"
                    f"<span>{event['Location']}</span>"
                    f"<span style='color: #262c36; margin: 0 12px; font-family: \"JetBrains Mono\", monospace;'>//</span>"
                    f"<span style='color: #f5a623; font-family: \"JetBrains Mono\", monospace;'>ROUND {event['RoundNumber']}</span>"
                    f"<span style='color: #262c36; margin: 0 12px; font-family: \"JetBrains Mono\", monospace;'>//</span>"
                    f"<span style='color: #e10600; font-family: \"JetBrains Mono\", monospace;'>{event['EventDate'].year}</span>"
                    "</div>"
                ),
                unsafe_allow_html=True,
            )

        with right_col:
            if next_event is not None:
                if st.button(
                    "NEXT RACE →",
                    key="race_analysis_next_race_link",
                    type="primary",
                    use_container_width=True,
                ):
                    st.session_state.selected_event = next_event
                    st.session_state.selected_race = str(next_event.get("EventName", ""))
                    st.session_state.selected_year = int(selected_year)
                    st.rerun()
            else:
                st.markdown(
                    "<div style='text-align: center; color: #8b949e; font-family: \"JetBrains Mono\", monospace; font-size: 0.75rem; letter-spacing: 0.12em; text-transform: uppercase; margin-top: 10px;'>// SEASON COMPLETE //</div>",
                    unsafe_allow_html=True,
                )


def render_qualifying_vs_race_pace_overlay(year, race_name, *args, **kwargs) -> None:
    with st.container(border=True, key="dialog_q_vs_r_pace"):
        st.markdown("<p class='section-kicker'>Pace Analysis</p>", unsafe_allow_html=True)
        st.markdown("<h2>Qualifying vs Race Pace (Top 3 Qualifiers)</h2>", unsafe_allow_html=True)

        q_session, _, _ = load_session_data(year, race_name, "Qualifying")
        if q_session is None:
            q_session, _, _ = load_session_data(year, race_name, "Sprint Qualifying")

        r_session, _, _ = load_session_data(year, race_name, "Race")
        if r_session is None:
            r_session, _, _ = load_session_data(year, race_name, "Sprint")

        q_results = None
        if q_session is not None and hasattr(q_session, 'results'):
            q_results = q_session.results

        if q_session is None or r_session is None or q_results is None or q_results.empty:
            st.warning("Insufficient data to compare qualifying and race pace.")
            return

        top_3 = q_results.head(3)
        if "Abbreviation" not in top_3:
            st.warning("Driver abbreviation missing from results.")
            return

        drivers = top_3["Abbreviation"].dropna().tolist()

        if not drivers:
            st.warning("No drivers found in qualifying top 3.")
            return

        tabs = st.tabs(drivers)
        for i, drv in enumerate(drivers):
            with tabs[i]:
                _, col, _ = st.columns([1, 6, 1])
                with col:
                    plot_driver_telemetry_comparison(drv, q_session, r_session, "Qualifying", "Race", compact=True)


def _split_event_sessions(event):
    event_sessions = get_event_sessions(event)
    practice_sessions = [name for name in event_sessions if name.startswith("Practice")]
    qualifying_sessions = [
        name
        for name in event_sessions
        if name in {"Qualifying", "Sprint Qualifying", "Sprint Shootout"}
    ]
    race_sessions = [name for name in event_sessions if name in {"Race", "Sprint"}]
    return event_sessions, practice_sessions, qualifying_sessions, race_sessions

def render_page_header_navigation(event, selected_year: int) -> None:
    prev_event = None
    next_event = None
    try:
        schedule = get_schedule(int(selected_year))
        season_races = schedule[schedule["EventFormat"] != "testing"].sort_values("RoundNumber")
        current_round = int(event["RoundNumber"])

        earlier = season_races[season_races["RoundNumber"] < current_round]
        later = season_races[season_races["RoundNumber"] > current_round]

        if not earlier.empty:
            prev_event = earlier.iloc[-1]
        if not later.empty:
            next_event = later.iloc[0]
    except Exception:
        prev_event = None
        next_event = None

    with st.container(border=True, key="dialog_page_header_nav"):
        left_col, mid_col, right_col = st.columns([1.2, 4.6, 1.2], vertical_alignment="center")

        with left_col:
            if prev_event is not None and st.button(
                "← PREV RACE",
                key="race_analysis_top_previous_race",
                use_container_width=True,
            ):
                st.session_state.selected_event = prev_event
                st.session_state.selected_race = str(prev_event.get("EventName", ""))
                st.session_state.selected_year = int(selected_year)
                st.rerun()

        with mid_col:
            st.markdown(
                (
                    "<div style='text-align: center; color: #f0f3f6; font-family: \"Titillium Web\", sans-serif; font-weight: 800; font-size: 1.1rem; letter-spacing: 0.06em; text-transform: uppercase;'>"
                    f"<span>{event['EventName']}</span>"
                    f"<span style='color: #262c36; margin: 0 12px; font-family: \"JetBrains Mono\", monospace;'>//</span>"
                    f"<span style='color: #f5a623; font-family: \"JetBrains Mono\", monospace;'>ROUND {event['RoundNumber']}</span>"
                    f"<span style='color: #262c36; margin: 0 12px; font-family: \"JetBrains Mono\", monospace;'>//</span>"
                    f"<span style='color: #e10600; font-family: \"JetBrains Mono\", monospace;'>{event['EventDate'].year}</span>"
                    "</div>"
                ),
                unsafe_allow_html=True,
            )

        with right_col:
            if next_event is not None and st.button(
                "NEXT RACE →",
                key="race_analysis_top_next_race",
                type="primary",
                use_container_width=True,
            ):
                st.session_state.selected_event = next_event
                st.session_state.selected_race = str(next_event.get("EventName", ""))
                st.session_state.selected_year = int(selected_year)
                st.rerun()


def render_session_tabs(selected_year, selected_race, event, event_sessions) -> None:
    practice_sessions = [name for name in event_sessions if name.startswith("Practice")]
    sprint_q_session = next((s for s in event_sessions if s in {"Sprint Qualifying", "Sprint Shootout"}), None)
    sprint_race_session = next((s for s in event_sessions if s == "Sprint"), None)
    event_format = str(event.get("EventFormat", "")).lower()
    is_sprint_weekend = bool(sprint_q_session or sprint_race_session or "sprint" in event_format)

    st.markdown(
        "<div class='section-ribbon'><span>WEEKEND SESSIONS</span><span>TIMING & RESULTS PANELS</span></div>",
        unsafe_allow_html=True,
    )

    tab_titles = ["Practice"]
    tab_keys = ["practice"]

    if is_sprint_weekend:
        sq_name = sprint_q_session if sprint_q_session else ("Sprint Shootout" if "shootout" in event_format else "Sprint Qualifying")
        sr_name = sprint_race_session if sprint_race_session else "Sprint"
        tab_titles.extend(["Sprint Qualifying", "Sprint Race"])
        tab_keys.extend([("sprint_qualifying", sq_name), ("sprint_race", sr_name)])

    tab_titles.extend(["Qualifying", "Race"])
    tab_keys.extend(["qualifying", "race"])

    tabs = st.tabs(tab_titles)

    for i, item in enumerate(tab_keys):
        with tabs[i]:
            if item == "practice":
                round_num = int(event["RoundNumber"]) if event is not None and "RoundNumber" in event else None
                if practice_sessions:
                    render_fp_sessions(selected_year, selected_race, practice_sessions, round_num=round_num)
                else:
                    st.info("No practice session data available for this event.")
            elif isinstance(item, tuple) and item[0] == "sprint_qualifying":
                render_qualifying_session(selected_year, selected_race, item[1])
            elif isinstance(item, tuple) and item[0] == "sprint_race":
                render_race_session(selected_year, selected_race, item[1])
            elif item == "qualifying":
                render_qualifying_session(selected_year, selected_race, "Qualifying")
            elif item == "race":
                render_race_session(selected_year, selected_race, "Race")


def render_telemetry_section(selected_year, selected_race, event) -> None:
    _, _, qualifying_sessions, race_sessions = _split_event_sessions(event)
    if qualifying_sessions and race_sessions:
        st.markdown(
            "<div class='section-ribbon'><span>TELEMETRY INTELLIGENCE</span><span>QUALIFYING VS RACE PACE OVERLAYS</span></div>",
            unsafe_allow_html=True,
        )
        render_qualifying_vs_race_pace_overlay(selected_year, selected_race)


if "selected_event" not in st.session_state:
    st.warning("No archive selected. Please select a race from the Race Select page.")
    if st.button("Go to Race Select"):
        st.switch_page("pages/1_Race_Select.py")
else:
    event = st.session_state.selected_event
    selected_year = st.session_state.selected_year
    selected_race = st.session_state.selected_race
    round_num = int(event["RoundNumber"]) if event is not None and "RoundNumber" in event else None

    event_sessions = get_event_sessions(event)

    # 1. Page Header & Navigation
    render_page_header_navigation(event, selected_year)

    # 2. Overview: Consolidated Race Briefing
    render_event_snapshot(event, event_sessions)

    # 3. Circuit Analysis
    render_track_details(selected_year, selected_race, event)

    # 4. Track Condition Overlay (Weather, Pace & Incident Windows)
    render_track_condition_overlay(selected_year, selected_race)

    # 5. Weekend Sessions in Tabs (Practice, [Sprint Q, Sprint Race], Qualifying, Race)
    render_session_tabs(selected_year, selected_race, event, event_sessions)

    # 6. Telemetry Analysis (Qualifying vs Race Pace Overlay)
    render_telemetry_section(selected_year, selected_race, event)

    # 7. Championship Standings (WDC & WCC)
    render_standings(selected_year, event["RoundNumber"])

    # 8. Bottom Navigation Footer (Next Race)
    render_end_race_bar(event, selected_year)
