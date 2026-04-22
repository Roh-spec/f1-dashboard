import streamlit as st

from fps import build_fastest_lap_table
from sessions import SESSION_LABELS, format_columns, load_session_data


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
    ]
    available = [column for column in columns if column in results]
    table = results[available].copy()
    table = table.rename(
        columns={
            "Position": "POS",
            "BroadcastName": "DRIVER",
            "TeamName": "TEAM",
            "GridPosition": "GRID",
            "Time": "TIME/GAP",
            "Status": "STATUS",
            "Points": "PTS",
        }
    )
    return format_columns(table, ["TIME/GAP"])


def render_race_session(year, race_name, session_name):
    label = SESSION_LABELS.get(session_name, session_name)

    with st.spinner(f"LOADING {label.upper()} DATA..."):
        results, laps = load_session_data(year, race_name, session_name)

    with st.container(border=True):
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
