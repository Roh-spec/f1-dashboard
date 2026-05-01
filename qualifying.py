import streamlit as st

from charts import plot_lap_times, plot_top_2_telemetry
from ui import anime_loading_box, render_top_podium_card
from fps import build_fastest_lap_table
from sessions import SESSION_LABELS, best_driver_name, format_columns, load_session_data


def build_qualifying_table(results):
    if results is None or results.empty:
        return None

    columns = ["Position", "BroadcastName", "TeamName", "Q1", "Q2", "Q3"]
    available = [column for column in columns if column in results]
    table = results[available].copy()
    table["DRIVER_NAME"] = results.apply(best_driver_name, axis=1)
    table = table.rename(
        columns={
            "Position": "POS",
            "BroadcastName": "DRIVER",
            "TeamName": "TEAM",
        }
    )
    driver_text = table["DRIVER"].astype(str).str.strip()
    table["DRIVER"] = table["DRIVER"].where(
        (driver_text != "") & (driver_text.str.lower() != "nan"),
        table["DRIVER_NAME"],
    )
    table = table.drop(columns=["DRIVER_NAME"])
    return format_columns(table, ["Q1", "Q2", "Q3"])


def render_qualifying_incidents(session, results):
    st.markdown("<br><h3>SESSION INTELLIGENCE</h3>", unsafe_allow_html=True)
    has_intel = False
    blocks = []

    if results is not None and not results.empty and "Position" in results:
        q1_elim = results[(results["Position"] > 15) & (results["Position"] <= 22)]
        q2_elim = results[(results["Position"] > 10) & (results["Position"] <= 15)]
        
        if not q2_elim.empty:
            drivers = ", ".join(q2_elim["Abbreviation"].dropna().tolist())
            blocks.append((st.warning, "🔻", f"**Q2 Eliminated:**\n- {drivers}"))

        if not q1_elim.empty:
            drivers = ", ".join(q1_elim["Abbreviation"].dropna().tolist())
            blocks.append((st.error, "❌", f"**Q1 Eliminated:**\n- {drivers}"))

    try:
        msgs = session.race_control_messages
        if msgs is not None and not msgs.empty:
            import pandas as pd
            def format_time(t):
                if pd.isna(t): return "Unknown"
                s = str(t).split('.')[0]
                return s.replace("0 days ", "") if "days" in s else s

            pens = msgs[msgs['Message'].str.contains('PENALTY', case=False, na=False)]
            if not pens.empty:
                pen_text = "**Penalties:**\n"
                for _, row in pens.iterrows():
                    pen_text += f"- {row['Message']} ({format_time(row.get('Time'))})\n"
                blocks.append((st.warning, "⏱️", pen_text))
                
            invs = msgs[msgs['Message'].str.contains('INVESTIGATION', case=False, na=False)]
            if not invs.empty:
                inv_text = "**Investigations:**\n"
                for _, row in invs.iterrows():
                    inv_text += f"- {row['Message']} ({format_time(row.get('Time'))})\n"
                blocks.append((st.info, "🔎", inv_text))
                
            reds = msgs[msgs['Message'].str.contains('RED FLAG', case=False, na=False)]
            if not reds.empty:
                red_text = "**Red Flags:**\n"
                for _, row in reds.iterrows():
                    red_text += f"- {row['Message']} ({format_time(row.get('Time'))})\n"
                blocks.append((st.error, "🚩", red_text))

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


def render_qualifying_session(year, race_name, session_name):
    label = SESSION_LABELS.get(session_name, session_name)

    with anime_loading_box(f"Loading {label.upper()} data..."):
        session, results, laps = load_session_data(year, race_name, session_name)

    with st.container(border=True, key=f"dialog_{session_name.lower().replace(' ', '_')}"):
        st.markdown(f"<h2>{label} Results</h2>", unsafe_allow_html=True)
        st.markdown(
            f"<p class='session-kicker'>Session loaded from the {session_name} archive.</p>",
            unsafe_allow_html=True,
        )

        table = build_qualifying_table(results)
        if table is None or table.empty:
            table = build_fastest_lap_table(laps, results)

        if table is None or table.empty:
            st.warning("Session not completed yet or data unavailable.")
            return

        render_top_podium_card(
            table,
            title=str(race_name),
            subtitle=f"{label} archive summary",
            badge="LAST SESSION",
            time_column="Q3",
        )

        st.dataframe(table.set_index("POS"), use_container_width=True)
        if "DRIVER" in table:
            st.info(f"Fastest qualifier: {table.iloc[0]['DRIVER']}")

        st.markdown("<h3>Qualifying Telemetry</h3>", unsafe_allow_html=True)
        _, col, _ = st.columns([1, 4, 1])
        with col:
            plot_top_2_telemetry(session)
            
        render_qualifying_incidents(session, results)
