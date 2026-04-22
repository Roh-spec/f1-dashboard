import streamlit as st

from sessions import SESSION_LABELS, best_driver_name, format_timing_value, load_session_data


def build_fastest_lap_table(laps, results):
    if laps is None or laps.empty or "LapTime" not in laps:
        return None

    quick_laps = laps.pick_quicklaps() if hasattr(laps, "pick_quicklaps") else laps
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


def render_fp_card(session_name, results, laps):
    label = SESSION_LABELS.get(session_name, session_name)
    table = build_fastest_lap_table(laps, results)

    if table is None or table.empty:
        driver_count = 0 if results is None or results.empty else len(results)
        detail = (
            f"{driver_count} drivers loaded"
            if driver_count
            else "Session archive unavailable"
        )
        st.markdown(
            f"""
            <div class="practice-card">
                <p class="practice-title">{label}</p>
                <p class="practice-stat">
                    <span class="practice-label">Timing</span>
                    Unsupported archive
                </p>
                <p class="practice-stat">
                    <span class="practice-label">Entry List</span>
                    {detail}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    fastest = table.iloc[0]
    st.markdown(
        f"""
        <div class="practice-card">
            <p class="practice-title">{label}</p>
            <p class="practice-stat">
                <span class="practice-label">Fastest</span>
                {fastest.get("DRIVER", "-")}
            </p>
            <p class="practice-stat">
                <span class="practice-label">Lap Time</span>
                {fastest.get("FASTEST LAP", "-")}
            </p>
            <p class="practice-stat">
                <span class="practice-label">Team / Lap / Tyre</span>
                {fastest.get("TEAM", "-")} / {fastest.get("LAP", "-")} / {fastest.get("TYRE", "-")}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_fp_sessions(year, race_name, practice_sessions):
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
                with st.spinner(f"LOADING {SESSION_LABELS.get(session_name, session_name).upper()} DATA..."):
                    results, laps = load_session_data(year, race_name, session_name)
                render_fp_card(session_name, results, laps)
