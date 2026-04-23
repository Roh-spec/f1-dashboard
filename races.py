import streamlit as st

from charts import plot_lap_times, plot_top_2_telemetry
from fps import build_fastest_lap_table
from sessions import SESSION_LABELS, best_driver_name, format_columns, load_session_data


def build_race_table(results):
    if results is None or results.empty:
        return None

    columns = [
        "Position",
        "BroadcastName",
        "TeamName",
        "GridPosition",
        "Time",
        "Status",
        "Points",
        "Laps",
    ]
    available = [column for column in columns if column in results]
    table = results[available].copy()
    table["DRIVER_NAME"] = results.apply(best_driver_name, axis=1)
    table = table.rename(
        columns={
            "Position": "POS",
            "BroadcastName": "DRIVER",
            "TeamName": "TEAM",
            "GridPosition": "GRID",
            "Time": "TIME/GAP",
            "Status": "STATUS",
            "Points": "PTS",
            "Laps": "LAPS",
        }
    )
    driver_text = table["DRIVER"].astype(str).str.strip()
    table["DRIVER"] = table["DRIVER"].where(
        (driver_text != "") & (driver_text.str.lower() != "nan"),
        table["DRIVER_NAME"],
    )
    table = table.drop(columns=["DRIVER_NAME"])
    return format_columns(table, ["TIME/GAP"])


def render_race_session(year, race_name, session_name):
    label = SESSION_LABELS.get(session_name, session_name)

    with st.spinner(f"LOADING {label.upper()} DATA..."):
        session, results, laps = load_session_data(year, race_name, session_name)

    with st.container(border=True, key=f"dialog_{session_name.lower().replace(' ', '_')}"):
        st.markdown(f"<h2>{label} Results</h2>", unsafe_allow_html=True)
        st.markdown(
            f"<p class='session-kicker'>Session loaded from the {session_name} archive.</p>",
            unsafe_allow_html=True,
        )

        table = build_race_table(results)
        if table is None or table.empty:
            table = build_fastest_lap_table(laps, results)

        if table is None or table.empty:
            st.warning("Session not completed yet or data unavailable.")
            return

        st.dataframe(table.set_index("POS"), use_container_width=True)
        if "DRIVER" in table:
            st.success(f"Winner: {table.iloc[0]['DRIVER']}")

        st.markdown("<h3>Race Telemetry & Lap Times</h3>", unsafe_allow_html=True)
        plot_top_2_telemetry(session)
        plot_lap_times(session)
