import streamlit as st

from charts import plot_driver_positions, plot_lap_times, plot_top_2_telemetry
from design import anime_loading_box, render_top_podium_card
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


def render_race_incidents(session, results):
    st.markdown("<br><h3>SESSION INTELLIGENCE</h3>", unsafe_allow_html=True)
    has_intel = False
    blocks = []

    if results is not None and not results.empty and "Status" in results:
        dnfs = results[~results["Status"].str.contains("Finished|Lap", case=False, na=False)]
        if not dnfs.empty:
            dnf_text = "**Retirements:**\n"
            for _, row in dnfs.iterrows():
                drv = row.get("Abbreviation", "")
                status = row.get("Status", "DNF")
                laps = row.get("Laps", 0)
                import pandas as pd
                lap_str = f"Lap {int(laps) + 1}" if pd.notna(laps) else "Unknown Lap"
                dnf_text += f"- **{drv}**: {status} ({lap_str})\n"
            blocks.append((st.error, "💥", dnf_text))

    try:
        msgs = session.race_control_messages
        if msgs is not None and not msgs.empty:
            import pandas as pd
            def get_lap_str(lap):
                return f"Lap {int(lap)}" if pd.notna(lap) else "Unknown"

            reds = msgs[msgs['Message'].str.contains('RED FLAG', case=False, na=False)]
            if not reds.empty:
                red_text = "**Red Flags:**\n"
                for _, row in reds.iterrows():
                    red_text += f"- {row['Message']} ({get_lap_str(row['Lap'])})\n"
                blocks.append((st.error, "🚩", red_text))
                
            scs = msgs[msgs['Message'].str.contains('SAFETY CAR|VIRTUAL SAFETY CAR', case=False, na=False)]
            scs = scs[~scs['Message'].str.contains('IN THIS LAP|ENDING', case=False, na=False)]
            if not scs.empty:
                sc_text = "**Safety Cars:**\n"
                for _, row in scs.iterrows():
                    sc_text += f"- {row['Message']} ({get_lap_str(row['Lap'])})\n"
                blocks.append((st.warning, "🟨", sc_text))

            pens = msgs[msgs['Message'].str.contains('PENALTY', case=False, na=False)]
            if not pens.empty:
                pen_text = "**Penalties:**\n"
                for _, row in pens.iterrows():
                    pen_text += f"- {row['Message']} ({get_lap_str(row['Lap'])})\n"
                blocks.append((st.warning, "⏱️", pen_text))
                
            invs = msgs[msgs['Message'].str.contains('INVESTIGATION', case=False, na=False)]
            if not invs.empty:
                inv_text = "**Investigations:**\n"
                for _, row in invs.iterrows():
                    inv_text += f"- {row['Message']} ({get_lap_str(row['Lap'])})\n"
                blocks.append((st.info, "🔎", inv_text))
                
    except Exception:
        pass

    if blocks:
        has_intel = True
        cols = st.columns(min(3, len(blocks)))
        for i, (st_func, icon, text) in enumerate(blocks):
            with cols[i % len(cols)]:
                st_func(text, icon=icon)

    if not has_intel:
        st.success("Clean session. No major incidents.", icon="✅")


def render_race_session(year, race_name, session_name):
    label = SESSION_LABELS.get(session_name, session_name)

    with anime_loading_box(f"Loading {label.upper()} data..."):
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

        render_top_podium_card(
            table,
            title=str(race_name),
            subtitle=f"{label} archive summary",
            badge="LAST RACE",
            time_column="TIME/GAP",
        )

        st.dataframe(table.set_index("POS"), use_container_width=True)
        if "DRIVER" in table:
            st.success(f"Winner: {table.iloc[0]['DRIVER']}")

        st.markdown("<h3>Race Telemetry & Lap Times</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            plot_top_2_telemetry(session)
        with col2:
            plot_lap_times(session)
        
        st.markdown("<h3>Track Positions</h3>", unsafe_allow_html=True)
        _, col, _ = st.columns([1, 4, 1])
        with col:
            plot_driver_positions(session)
            
        render_race_incidents(session, results)
