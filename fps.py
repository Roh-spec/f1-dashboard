import streamlit as st

from ui import anime_loading_box, get_team_color
from sessions import SESSION_LABELS, best_driver_name, format_timing_value, load_session_data


def build_fastest_lap_table(laps, results):
    if laps is None or laps.empty or "LapTime" not in laps:
        return None

    quick_laps = laps.pick_quicklaps() if hasattr(laps, "pick_quicklaps") else laps
    if quick_laps is None or quick_laps.empty:
        quick_laps = laps
    quick_laps = quick_laps.dropna(subset=["LapTime"])
    if quick_laps.empty:
        return None

    fastest_indexes = quick_laps.groupby("Driver")["LapTime"].idxmin()
    table = quick_laps.loc[fastest_indexes].sort_values("LapTime").reset_index(drop=True)
    table["POS"] = table.index + 1

    driver_names = {}
    if results is not None and not results.empty:
        for _, row in results.iterrows():
            code = row.get("Abbreviation") or row.get("Driver")
            name = best_driver_name(row)
            if code:
                driver_names[str(code)] = name

    table["DRIVER"] = table["Driver"].map(driver_names).fillna(table["Driver"])
    table["FASTEST LAP"] = table["LapTime"].map(format_timing_value)

    output_columns = ["POS", "DRIVER", "Team", "FASTEST LAP", "LapNumber", "Compound"]
    available = [column for column in output_columns if column in table]
    table = table[available].rename(
        columns={
            "Team": "TEAM",
            "LapNumber": "LAP",
            "Compound": "TYRE",
        }
    )
    return table


def render_fp_card(session_name, results, laps, year=None):
    label = SESSION_LABELS.get(session_name, session_name)
    table = build_fastest_lap_table(laps, results)

    if table is None or table.empty:
        driver_count = 0 if results is None or results.empty else len(results)
        detail = (
            f"{driver_count} Drivers Registered"
            if driver_count
            else "Session Archive Unavailable"
        )
        timing_status = (
            "Pre-2018 Digital Telemetry Limit"
            if year and int(year) < 2018
            else "Session Concluded (Digital Timing Offline)"
        )
        st.markdown(
            f"""
            <div class="practice-card" style="border-top: 3px solid #e10600; box-shadow: 0 4px 18px rgba(0, 0, 0, 0.45);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span class="practice-title">{label}</span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; font-weight: 700; color: #8b949e; background: rgba(255,255,255,0.04); border: 1px solid #262c36; padding: 2px 7px; text-transform: uppercase;">ENTRY ARCHIVE</span>
                </div>
                <p class="practice-stat">
                    <span class="practice-label" style="color: #8b949e; font-weight: 700;">Status</span>
                    <strong style="color: #f0f3f6; font-size: 1.0rem;">Official Session Archive</strong>
                </p>
                <p class="practice-stat">
                    <span class="practice-label" style="color: #8b949e; font-weight: 700;">Entry List</span>
                    <span style="font-family: 'JetBrains Mono', monospace; color: #f0f3f6; font-weight: 700; font-size: 1.0rem;">{detail}</span>
                </p>
                <p class="practice-stat">
                    <span class="practice-label" style="color: #8b949e; font-weight: 700;">Telemetry Feed</span>
                    <span style="color: #8b949e; font-size: 0.85rem;">{timing_status}</span>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    fastest = table.iloc[0]
    driver_name = fastest.get("DRIVER", "-")
    team_name = fastest.get("TEAM", "-")
    lap_time = fastest.get("FASTEST LAP", "-")
    lap_num = fastest.get("LAP", "-")
    tyre_comp = fastest.get("TYRE", "-")

    # Dynamic team color for the fastest driver
    team_col = get_team_color(team_name or driver_name)

    st.markdown(
        f"""
        <div class="practice-card" style="border-top: 3px solid {team_col}; box-shadow: 0 4px 18px rgba(0, 0, 0, 0.45);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span class="practice-title">{label}</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.70rem; font-weight: 700; color: {team_col}; background: rgba(255,255,255,0.04); border: 1px solid {team_col}; padding: 2px 7px; text-transform: uppercase;">{team_name}</span>
            </div>
            <p class="practice-stat">
                <span class="practice-label" style="color: {team_col}; font-weight: 700;">Fastest</span>
                <strong style="color: #f0f3f6; font-size: 1.05rem;">{driver_name}</strong>
            </p>
            <p class="practice-stat">
                <span class="practice-label" style="color: {team_col}; font-weight: 700;">Lap Time</span>
                <span style="font-family: 'JetBrains Mono', monospace; color: {team_col}; font-weight: 700; font-size: 1.05rem;">{lap_time}</span>
            </p>
            <p class="practice-stat">
                <span class="practice-label" style="color: {team_col}; font-weight: 700;">Team / Lap / Tyre</span>
                <span style="color: #c9d1d9;">{team_name} / Lap {lap_num} / {tyre_comp}</span>
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_fp_sessions(year, race_name, practice_sessions, round_num=None):
    if not practice_sessions:
        return

    with st.container(border=True, key="dialog_practice_sessions"):
        st.markdown("<h2>Practice Sessions</h2>", unsafe_allow_html=True)
        st.markdown(
            "<p class='session-kicker'>FP1, FP2, and FP3 fastest-lap readouts.</p>",
            unsafe_allow_html=True,
        )

        columns = st.columns(len(practice_sessions))
        for column, session_name in zip(columns, practice_sessions):
            with column:
                with anime_loading_box(f"Loading {SESSION_LABELS.get(session_name, session_name).upper()} data..."):
                    session, results, laps = load_session_data(year, race_name, session_name)
                render_fp_card(session_name, results, laps, year=year)
