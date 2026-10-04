import streamlit as st

from charts import (
    compute_corner_telemetry_matrix,
    plot_micro_sector_dominance,
    plot_top_2_telemetry,
)
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


def render_qualifying_telemetry(session, results):
    st.markdown("<br><h3>QUALIFYING TELEMETRY & RACE INTELLIGENCE</h3>", unsafe_allow_html=True)
    mode_options = [
        "🗺️ Track Map Dominance",
        "🎯 Corner Telemetry Inspector",
        "⚡ Waveform Telemetry",
    ]
    s_id = str(getattr(session, "name", "Q")).lower().replace(" ", "_")
    selected_mode = st.pills(
        "Telemetry Mode",
        mode_options,
        default=mode_options[0],
        key=f"qual_telem_pill_{s_id}",
        label_visibility="collapsed",
    )

    if not selected_mode:
        selected_mode = mode_options[0]

    if selected_mode == "🗺️ Track Map Dominance":
        dom_res = plot_micro_sector_dominance(session)
        if dom_res:
            d1 = dom_res["driver_1"]
            d2 = dom_res["driver_2"]
            c1 = dom_res["color_1"]
            c2 = dom_res["color_2"]
            n1 = dom_res["count_1"]
            n2 = dom_res["count_2"]
            p1 = dom_res["pct_1"]
            p2 = dom_res["pct_2"]
            t1 = dom_res["d1_lap_time"]
            t2 = dom_res["d2_lap_time"]
            unit = dom_res.get("unit_label", "SECTORS")
            st.markdown(
                f"""
                <div style="background: #161b22; border: 1px solid #262c36; padding: 12px 18px; margin-top: 6px; margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="display: inline-block; width: 12px; height: 12px; background: {c1}; border-radius: 2px;"></span>
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 1rem; font-weight: 700; color: #f0f3f6;">{d1}</span>
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #8b949e;">{t1}</span>
                            <span style="background: rgba(255,255,255,0.06); padding: 2px 7px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: {c1}; font-weight: 700;">{n1} {unit} ({p1}%)</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="background: rgba(255,255,255,0.06); padding: 2px 7px; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: {c2}; font-weight: 700;">{n2} {unit} ({p2}%)</span>
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #8b949e;">{t2}</span>
                            <span style="font-family: 'JetBrains Mono', monospace; font-size: 1rem; font-weight: 700; color: #f0f3f6;">{d2}</span>
                            <span style="display: inline-block; width: 12px; height: 12px; background: {c2}; border-radius: 2px;"></span>
                        </div>
                    </div>
                    <div style="width: 100%; height: 8px; background: #262c36; display: flex; overflow: hidden; border-radius: 1px;">
                        <div style="width: {p1}%; background: {c1}; height: 100%;"></div>
                        <div style="width: {p2}%; background: {c2}; height: 100%;"></div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    elif selected_mode == "🎯 Corner Telemetry Inspector":
        c_res = compute_corner_telemetry_matrix(session)
        if c_res and not c_res["dataframe"].empty:
            d1 = c_res["driver_1"]
            d2 = c_res["driver_2"]
            c1 = c_res["color_1"]
            c2 = c_res["color_2"]
            w1 = c_res["d1_wins"]
            w2 = c_res["d2_wins"]
            tot = c_res["total_corners"]

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric(
                    label=f"{d1} vs {d2} Corner Advantage",
                    value=f"{w1} - {w2}",
                    delta=f"{d1} +{w1-w2}" if w1 > w2 else (f"{d2} +{w2-w1}" if w2 > w1 else "Tied"),
                )
            with col_b:
                st.metric(
                    label="Corners Analyzed",
                    value=f"{tot} Turns",
                    delta="Apex & Braking Zones",
                )
            with col_c:
                st.metric(
                    label="Telemetry Sampling",
                    value="10 Hz Precision",
                    delta="GPS Aligned",
                )

            display_cols = [c for c in c_res["dataframe"].columns if not c.startswith("_")]
            st.dataframe(
                c_res["dataframe"][display_cols].set_index("Turn"),
                use_container_width=True,
            )
        else:
            st.info("Corner-by-corner braking and throttle telemetry is unavailable for this session archive.")

    elif selected_mode == "⚡ Waveform Telemetry":
        _, col, _ = st.columns([1, 6, 1])
        with col:
            plot_top_2_telemetry(session)



def render_qualifying_incidents(session, results):
    st.markdown("<br><h3>SESSION INTELLIGENCE</h3>", unsafe_allow_html=True)
    has_intel = False
    blocks = []

    if results is not None and not results.empty and "Position" in results:
        q1_elim = results[(results["Position"] > 15) & (results["Position"] <= 22)]
        q2_elim = results[(results["Position"] > 10) & (results["Position"] <= 15)]
        
        if not q2_elim.empty:
            drivers = ", ".join(q2_elim["Abbreviation"].dropna().tolist())
            blocks.append((st.warning, "!", f"**Q2 Eliminated:**\n- {drivers}"))

        if not q1_elim.empty:
            drivers = ", ".join(q1_elim["Abbreviation"].dropna().tolist())
            blocks.append((st.error, "X", f"**Q1 Eliminated:**\n- {drivers}"))

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
                blocks.append((st.warning, "!", pen_text))
                
            invs = msgs[msgs['Message'].str.contains('INVESTIGATION', case=False, na=False)]
            if not invs.empty:
                inv_text = "**Investigations:**\n"
                for _, row in invs.iterrows():
                    inv_text += f"- {row['Message']} ({format_time(row.get('Time'))})\n"
                blocks.append((st.info, "i", inv_text))
                
            reds = msgs[msgs['Message'].str.contains('RED FLAG', case=False, na=False)]
            if not reds.empty:
                red_text = "**Red Flags:**\n"
                for _, row in reds.iterrows():
                    red_text += f"- {row['Message']} ({format_time(row.get('Time'))})\n"
                blocks.append((st.error, "!", red_text))

    except Exception:
        pass

    if blocks:
        has_intel = True
        cols = st.columns(min(3, len(blocks)))
        for i, (st_func, _icon, text) in enumerate(blocks):
            with cols[i % len(cols)]:
                st_func(text)

    if not has_intel:
        st.success("Clean session. No major incidents.")


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

        render_qualifying_telemetry(session, results)
        render_qualifying_incidents(session, results)

