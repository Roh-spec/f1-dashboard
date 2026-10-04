"""Shared FastF1 chart rendering helpers.

This module owns the app-wide Matplotlib/FastF1 chart style plus the reusable
data transformations for telemetry overlays, lap-time traces, position plots,
and tyre-stint timelines.
"""

import matplotlib.pyplot as plt
import fastf1.plotting
import streamlit as st
import pandas as pd
import numpy as np
from matplotlib.patches import Patch
from ui import get_team_color

# Setup fastf1 plotting styles
fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')


def _set_retro_style(fig, ax_list):
    fig.patch.set_facecolor('#161b22')
    for ax in ax_list:
        ax.set_facecolor('#161b22')
        ax.tick_params(colors='#8b949e', labelsize=8.5)
        for spine in ax.spines.values():
            spine.set_color('#262c36')
        ax.grid(color='#262c36', alpha=0.55, linewidth=0.7)


def _safe_laps(session):
    if session is None:
        return None
    try:
        laps = session.laps
        if laps is not None and not laps.empty and "LapTime" in laps:
            laps = laps.copy()
            laps["LapTime"] = pd.to_timedelta(laps["LapTime"], errors="coerce")
        return laps
    except Exception:
        return None


def _safe_results(session):
    if session is None:
        return None
    try:
        return session.results
    except Exception:
        return None


def _ensure_telemetry_loaded(session):
    if session is None:
        return False
    try:
        if not hasattr(session, '_car_data') or session._car_data is None:
            session.load(telemetry=True, weather=False, messages=False)
        return True
    except Exception:
        return False


def _pick_driver_laps(laps, drv):
    if laps is None:
        return pd.DataFrame()
    if hasattr(laps, "pick_driver"):
        try:
            res = laps.pick_driver(drv)
            if res is not None and not res.empty:
                return res
        except Exception:
            pass
    if isinstance(laps, pd.DataFrame) and "Driver" in laps:
        return laps[laps["Driver"] == drv]
    return pd.DataFrame()


def _pick_quicklaps(laps):
    if laps is None:
        return pd.DataFrame()
    if hasattr(laps, "pick_quicklaps"):
        try:
            res = laps.pick_quicklaps()
            if res is not None and not res.empty:
                return res
        except Exception:
            pass
    if isinstance(laps, pd.DataFrame) and "LapTime" in laps:
        valid = laps.dropna(subset=["LapTime"]).copy()
        if not valid.empty:
            if len(valid) >= 5:
                med = valid["LapTime"].median()
                return valid[valid["LapTime"] <= med * 1.15]
            return valid
    return laps


def _pick_fastest(laps):
    if laps is None or (hasattr(laps, "empty") and laps.empty):
        return None
    if hasattr(laps, "pick_fastest"):
        try:
            res = laps.pick_fastest()
            if res is not None and not pd.isna(res.get("LapTime")):
                return res
        except Exception:
            pass
    if isinstance(laps, pd.DataFrame) and "LapTime" in laps:
        valid = laps.dropna(subset=["LapTime"])
        if not valid.empty:
            return valid.loc[valid["LapTime"].idxmin()]
    return None


def plot_top_2_telemetry(session, compact=False):
    laps = _safe_laps(session)
    if laps is None or laps.empty:
        st.warning("No lap data available for telemetry.")
        return

    results = _safe_results(session)
    if results is not None and not results.empty and "Abbreviation" in results:
        top_2_drivers = results.iloc[:2]['Abbreviation'].dropna().tolist()
    else:
        top_laps = _pick_quicklaps(laps).sort_values(by='LapTime').dropna(subset=['LapTime'])
        if top_laps.empty:
            st.warning("No quick laps available.")
            return
        top_2_drivers = top_laps['Driver'].unique()[:2].tolist()

    if len(top_2_drivers) < 2:
        st.warning("Not enough drivers with data to compare telemetry.")
        return

    driver_1, driver_2 = top_2_drivers[0], top_2_drivers[1]

    try:
        color_d1 = get_team_color(driver_1, default="#ff8000")
        color_d2 = get_team_color(driver_2, default="#1e41ff")
        if str(color_d1).lower() == str(color_d2).lower():
            color_d2 = "#ffffff" if color_d1 != "#ffffff" else "#f5a623"

        laps_d1 = _pick_fastest(_pick_driver_laps(laps, driver_1))
        laps_d2 = _pick_fastest(_pick_driver_laps(laps, driver_2))

        if laps_d1 is None or laps_d2 is None or pd.isna(laps_d1['LapTime']) or pd.isna(laps_d2['LapTime']):
            raise ValueError("Could not find fastest lap for top drivers.")

        _ensure_telemetry_loaded(session)
        import fastf1.utils
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            delta_time, tel_d1, tel_d2 = fastf1.utils.delta_time(laps_d1, laps_d2)

        fig_size = (7.6, 6.8) if compact else (10, 8.5)
        fig, ax = plt.subplots(5, 1, figsize=fig_size, sharex=True, gridspec_kw={'height_ratios': [3, 1.5, 1.5, 1.5, 2]})
        _set_retro_style(fig, ax)

        ax[0].plot(tel_d1['Distance'], tel_d1['Speed'], color=color_d1, label=driver_1, linewidth=1.8)
        ax[0].plot(tel_d2['Distance'], tel_d2['Speed'], color=color_d2, label=driver_2, linewidth=1.8)
        ax[0].set_ylabel("Speed (km/h)", color='#f0f3f6', fontsize=9)
        ax[0].legend(facecolor='#161b22', edgecolor='#262c36', labelcolor='#f0f3f6', loc='upper right', fontsize='small')

        ax[1].plot(tel_d1['Distance'], tel_d1['Throttle'], color=color_d1, linewidth=1.5)
        ax[1].plot(tel_d2['Distance'], tel_d2['Throttle'], color=color_d2, linewidth=1.5)
        ax[1].set_ylabel("Throttle %", color='#f0f3f6', fontsize=9)

        ax[2].plot(tel_d1['Distance'], tel_d1['Brake'], color=color_d1, linewidth=1.5)
        ax[2].plot(tel_d2['Distance'], tel_d2['Brake'], color=color_d2, linewidth=1.5)
        ax[2].set_ylabel("Brake", color='#f0f3f6', fontsize=9)
        ax[2].set_yticks([0, 1])
        ax[2].set_yticklabels(['OFF', 'ON'], color='#f0f3f6', fontsize=8)

        ax[3].plot(tel_d1['Distance'], tel_d1['nGear'], color=color_d1, linewidth=1.5)
        ax[3].plot(tel_d2['Distance'], tel_d2['nGear'], color=color_d2, linewidth=1.5)
        ax[3].set_ylabel("Gear", color='#f0f3f6', fontsize=9)
        ax[3].set_yticks(range(1, 9))

        ax[4].plot(tel_d1['Distance'], delta_time, color='#e10600', alpha=0.9, linewidth=1.5)
        ax[4].axhline(0, color='#374151', linestyle='--', linewidth=0.8)
        ax[4].fill_between(tel_d1['Distance'], delta_time, 0, where=(delta_time < 0), color=color_d1, alpha=0.35)
        ax[4].fill_between(tel_d1['Distance'], delta_time, 0, where=(delta_time > 0), color=color_d2, alpha=0.35)
        ax[4].set_ylabel(f"Δ {driver_1}-{driver_2} (s)", color='#f0f3f6', fontsize=9)
        ax[4].set_xlabel("Distance (m)", color='#f0f3f6', fontsize=9)

        event_name = session.event.EventName if session.event is not None else "Session"
        fig.suptitle(f"{event_name} - {session.name}\n{driver_1} vs {driver_2} Fastest Lap Telemetry", color='#f0f3f6', family='monospace', fontsize=10, weight='bold')
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        return
    except Exception:
        # Fallback to head-to-head lap pace comparison across all race laps
        d1_laps = _pick_quicklaps(_pick_driver_laps(laps, driver_1)).dropna(subset=['LapTime', 'LapNumber'])
        d2_laps = _pick_quicklaps(_pick_driver_laps(laps, driver_2)).dropna(subset=['LapTime', 'LapNumber'])
        if not d1_laps.empty and not d2_laps.empty:
            fig_size = (7.6, 4.4) if compact else (10, 5.2)
            fig, ax = plt.subplots(figsize=fig_size)
            _set_retro_style(fig, [ax])
            c1 = get_team_color(driver_1, default="#ff8000")
            c2 = get_team_color(driver_2, default="#1e41ff")
            if str(c1).lower() == str(c2).lower():
                c2 = "#ffffff" if c1 != "#ffffff" else "#f5a623"
            ax.plot(d1_laps['LapNumber'], d1_laps['LapTime'].dt.total_seconds(), color=c1, label=f"{driver_1} Pace", linewidth=2.0, marker='o', markersize=3)
            ax.plot(d2_laps['LapNumber'], d2_laps['LapTime'].dt.total_seconds(), color=c2, label=f"{driver_2} Pace", linewidth=2.0, marker='s', markersize=3)
            ax.set_xlabel("Lap Number", color='#f0f3f6', fontsize=9)
            ax.set_ylabel("Lap Time (s)", color='#f0f3f6', fontsize=9)
            event_name = session.event.EventName if hasattr(session, 'event') and session.event is not None else "Session"
            ax.set_title(f"{event_name} - {driver_1} vs {driver_2} Head-to-Head Pace", color='#f0f3f6', family='monospace', fontsize=10, weight='bold')
            ax.legend(facecolor='#161b22', edgecolor='#262c36', labelcolor='#f0f3f6', loc='upper right')
            fig.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            return

        st.info("Detailed 10Hz telemetry overlay unavailable. Lap pace and race traces are displayed below.")
        return


def plot_lap_times(session, compact=False):
    laps = _safe_laps(session)
    if laps is None or laps.empty:
        st.warning("No lap time data available.")
        return

    results = _safe_results(session)
    if results is not None and not results.empty and "Abbreviation" in results:
        drivers = results['Abbreviation'].dropna().tolist()
    else:
        drivers = laps['Driver'].unique().tolist()

    fig_size = (7.6, 4.6) if compact else (10, 5.8)
    fig, ax = plt.subplots(figsize=fig_size)
    _set_retro_style(fig, [ax])

    for drv in drivers:
        drv_laps = _pick_quicklaps(_pick_driver_laps(laps, drv))
        if not drv_laps.empty:
            color = get_team_color(drv)
            ax.plot(drv_laps['LapNumber'], drv_laps['LapTime'].dt.total_seconds(), color=color, label=drv, alpha=0.85, linewidth=1.4)

    ax.set_xlabel("Lap Number", color='#f0f3f6', fontsize=9)
    ax.set_ylabel("Lap Time (s)", color='#f0f3f6', fontsize=9)

    event_name = session.event.EventName if hasattr(session, 'event') and session.event is not None else "Session"
    s_name = getattr(session, 'name', 'Race')
    fig.suptitle(f"{event_name} - {s_name} Lap Times", color='#f0f3f6', family='monospace', fontsize=10, weight='bold')

    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', facecolor='#161b22', edgecolor='#262c36', labelcolor='#f0f3f6', fontsize='x-small', framealpha=0.95)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def plot_driver_positions(session, compact=False):
    laps = _safe_laps(session)
    if laps is None or laps.empty:
        st.warning("No position data available.")
        return

    results = _safe_results(session)
    if results is not None and not results.empty and "Abbreviation" in results:
        drivers = results['Abbreviation'].dropna().tolist()
    else:
        drivers = laps['Driver'].unique().tolist()

    fig_size = (7.6, 5.2) if compact else (10, 7.5)
    fig, ax = plt.subplots(figsize=fig_size)
    _set_retro_style(fig, [ax])

    for drv in drivers:
        drv_laps = _pick_driver_laps(laps, drv)
        drv_laps = drv_laps.dropna(subset=['Position'])
        if not drv_laps.empty:
            color = get_team_color(drv)
            ax.plot(drv_laps['LapNumber'], drv_laps['Position'], color=color, label=drv, alpha=0.85, linewidth=1.8)

    max_pos = min(22, max(20, len(drivers)))
    ax.set_ylim(max_pos + 0.5, 0.5)
    ax.set_yticks(range(1, max_pos + 1))

    ax.set_xlabel("Lap Number", color='#f0f3f6', fontsize=9)
    ax.set_ylabel("Position", color='#f0f3f6', fontsize=9)

    event_name = session.event.EventName if hasattr(session, 'event') and session.event is not None else "Session"
    s_name = getattr(session, 'name', 'Race')
    fig.suptitle(f"{event_name} - {s_name} Track Positions", color='#f0f3f6', family='monospace', fontsize=10, weight='bold')

    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', facecolor='#161b22', edgecolor='#262c36', labelcolor='#f0f3f6', fontsize='x-small', framealpha=0.95)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def plot_tyre_strategy_timeline(session, max_drivers=20, compact=False):
    source_laps = _safe_laps(session)
    if source_laps is None or source_laps.empty:
        st.warning("No lap data available for tyre strategy.")
        return

    laps = source_laps.copy()
    required = {"Driver", "Stint", "Compound", "LapNumber"}

    openf1_stints = None
    if not required.issubset(set(laps.columns)) or (laps["Compound"] == "UNKNOWN").all():
        try:
            import sessions
            get_openf1_stints = getattr(sessions, "get_openf1_stints", None)
            if get_openf1_stints is not None:
                ev = getattr(session, "event", None)
                year = getattr(session, "event", {}).get("Year") if hasattr(session, "event") and isinstance(session.event, dict) else (getattr(ev, "Year", None) if ev is not None else None)
                r_name = getattr(session, "event", {}).get("EventName") if hasattr(session, "event") and isinstance(session.event, dict) else (getattr(ev, "EventName", None) if ev is not None else None)
                if not year and hasattr(session, "date"):
                    year = session.date.year
                if not r_name and hasattr(session, "name"):
                    r_name = session.name
                if year and r_name:
                    openf1_stints = get_openf1_stints(int(year), str(r_name), "Race")
        except Exception:
            openf1_stints = None

    if (not required.issubset(set(laps.columns)) or (laps["Compound"] == "UNKNOWN").all()) and (openf1_stints is None or openf1_stints.empty):
        st.markdown(
            """
            <div style="background: #161b22; border: 1px solid #262c36; border-left: 3px solid #e10600; padding: 14px 18px; margin-top: 8px;">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #f5a623; font-weight: 700; letter-spacing: 0.08em;">STRATEGY ARCHIVE // NOTICE</span>
                <p style="color: #c9d1d9; font-size: 0.88rem; margin: 4px 0 0 0;">Tyre compound telemetry is recorded for 2018+ digital live timing sessions. Lap times and driver position traces are fully displayed above.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        return

    if openf1_stints is None or openf1_stints.empty:
        laps = laps.dropna(subset=["Driver", "Stint", "LapNumber"]).copy()
        if laps.empty:
            st.warning("Tyre strategy data unavailable for this session.")
            return

    compound_colors = {
        "SOFT": "#e10600",
        "MEDIUM": "#f5a623",
        "HARD": "#f0f3f6",
        "INTERMEDIATE": "#39b54a",
        "WET": "#38bdf8",
        "UNKNOWN": "#6b7280",
    }

    results = _safe_results(session)
    if results is not None and not results.empty and "Abbreviation" in results:
        driver_order = results["Abbreviation"].dropna().astype(str).tolist()
    elif openf1_stints is not None and not openf1_stints.empty:
        driver_order = openf1_stints["Driver"].dropna().astype(str).unique().tolist()
    else:
        driver_order = laps["Driver"].dropna().astype(str).unique().tolist()

    if compact:
        max_drivers = min(max_drivers, 14)
    driver_order = driver_order[:max_drivers]

    fig_height = max(3.8, min(8.0, 0.32 * len(driver_order) + 1.8))
    fig_width = 8.0 if compact else 10.5

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    _set_retro_style(fig, [ax])

    y_positions = list(range(len(driver_order)))
    y_map = {drv: idx for idx, drv in enumerate(driver_order)}
    bar_height = 0.65

    for drv in driver_order:
        if openf1_stints is not None and not openf1_stints.empty:
            stint_groups = openf1_stints[openf1_stints["Driver"] == drv].sort_values("lap_start")
            if stint_groups.empty:
                continue
        else:
            drv_laps = laps[laps["Driver"] == drv].copy()
            if drv_laps.empty:
                continue

            stint_groups = (
                drv_laps.groupby("Stint", as_index=False)
                .agg(
                    lap_start=("LapNumber", "min"),
                    lap_end=("LapNumber", "max"),
                    compound=("Compound", "last"),
                )
                .sort_values("lap_start")
            )

        y = y_map[drv]
        for _, stint in stint_groups.iterrows():
            lap_start = int(stint["lap_start"])
            lap_end = int(stint["lap_end"])
            width = max(0.85, (lap_end - lap_start) + 1)
            compound = str(stint.get("compound", "UNKNOWN")).upper()
            color = compound_colors.get(compound, compound_colors["UNKNOWN"])

            ax.broken_barh(
                [(lap_start - 0.5, width)],
                (y - bar_height / 2, bar_height),
                facecolors=color,
                edgecolors="#0d1117",
                linewidth=0.8,
            )

        # Mark pit-stop points at stint boundaries
        pit_laps = stint_groups["lap_start"].tolist()[1:]
        if pit_laps:
            ax.scatter(
                [float(l) - 0.5 for l in pit_laps],
                [y] * len(pit_laps),
                s=22,
                color="#f5a623",
                edgecolors="#0d1117",
                linewidths=0.8,
                zorder=5,
            )

    if openf1_stints is not None and not openf1_stints.empty:
        max_lap = int(openf1_stints["lap_end"].max()) if not openf1_stints["lap_end"].dropna().empty else 57
    else:
        max_lap = int(laps["LapNumber"].max()) if not laps["LapNumber"].dropna().empty else 0
    ax.set_xlim(0.5, max(5.5, max_lap + 1))
    ax.set_ylim(-0.8, len(driver_order) - 0.2)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(driver_order, color="#f0f3f6", fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Lap Number", color="#f0f3f6", fontsize=9)
    ax.set_ylabel("Driver", color="#f0f3f6", fontsize=9)

    legend_items = [
        Patch(facecolor=compound_colors["SOFT"], edgecolor="none", label="Soft"),
        Patch(facecolor=compound_colors["MEDIUM"], edgecolor="none", label="Medium"),
        Patch(facecolor=compound_colors["HARD"], edgecolor="none", label="Hard"),
        Patch(facecolor=compound_colors["INTERMEDIATE"], edgecolor="none", label="Inter"),
        Patch(facecolor=compound_colors["WET"], edgecolor="none", label="Wet"),
    ]
    ax.legend(
        handles=legend_items,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.08),
        ncol=5,
        frameon=True,
        facecolor="#161b22",
        edgecolor="#262c36",
        labelcolor="#f0f3f6",
        fontsize="x-small",
    )

    event_name = session.event.EventName if session.event is not None else "Session"
    fig.suptitle(f"{event_name} - {session.name} Tyre Strategy Timeline", color="#f0f3f6", family="monospace", fontsize=10, weight="bold")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def plot_driver_telemetry_comparison(driver, session1, session2, name1="Qualifying", name2="Race", compact=False):
    laps1 = _safe_laps(session1)
    laps2 = _safe_laps(session2)

    if laps1 is None or laps1.empty or laps2 is None or laps2.empty:
        st.warning(f"Lap data missing for {driver}.")
        return

    try:
        lap1 = _pick_fastest(_pick_driver_laps(laps1, driver))
        lap2 = _pick_fastest(_pick_driver_laps(laps2, driver))

        if lap1 is None or lap2 is None or pd.isna(lap1['LapTime']) or pd.isna(lap2['LapTime']):
            st.warning(f"Could not find valid fastest lap for {driver} in both sessions.")
            return

        _ensure_telemetry_loaded(session1)
        _ensure_telemetry_loaded(session2)
        import fastf1.utils
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            delta_time, tel1, tel2 = fastf1.utils.delta_time(lap1, lap2)
    except Exception as e:
        st.info(f"Detailed 10Hz telemetry comparison unavailable for {driver} ({e}).")
        return

    try:
        color1 = fastf1.plotting.get_driver_color(driver, session1)
    except Exception:
        color1 = None
    if not color1:
        color1 = get_team_color(driver, default="#ff8000")

    color2 = "#ffffff" if color1 != "#ffffff" else "#f5a623"

    fig_size = (7.6, 6.8) if compact else (10, 8.5)
    fig, ax = plt.subplots(5, 1, figsize=fig_size, sharex=True, gridspec_kw={'height_ratios': [3, 1.5, 1.5, 1.5, 2]})
    _set_retro_style(fig, ax)

    ax[0].plot(tel1['Distance'], tel1['Speed'], color=color1, label=f"{name1} Fastest", linewidth=1.8)
    ax[0].plot(tel2['Distance'], tel2['Speed'], color=color2, label=f"{name2} Fastest", linewidth=1.8)
    ax[0].set_ylabel("Speed (km/h)", color='#f0f3f6', fontsize=9)
    ax[0].legend(facecolor='#161b22', edgecolor='#262c36', labelcolor='#f0f3f6', loc='upper right', fontsize='small')

    ax[1].plot(tel1['Distance'], tel1['Throttle'], color=color1, linewidth=1.5)
    ax[1].plot(tel2['Distance'], tel2['Throttle'], color=color2, linewidth=1.5)
    ax[1].set_ylabel("Throttle %", color='#f0f3f6', fontsize=9)

    ax[2].plot(tel1['Distance'], tel1['Brake'], color=color1, linewidth=1.5)
    ax[2].plot(tel2['Distance'], tel2['Brake'], color=color2, linewidth=1.5)
    ax[2].set_ylabel("Brake", color='#f0f3f6', fontsize=9)
    ax[2].set_yticks([0, 1])
    ax[2].set_yticklabels(['OFF', 'ON'], color='#f0f3f6', fontsize=8)

    ax[3].plot(tel1['Distance'], tel1['nGear'], color=color1, linewidth=1.5)
    ax[3].plot(tel2['Distance'], tel2['nGear'], color=color2, linewidth=1.5)
    ax[3].set_ylabel("Gear", color='#f0f3f6', fontsize=9)
    ax[3].set_yticks(range(1, 9))

    ax[4].plot(tel1['Distance'], delta_time, color='#e10600', alpha=0.9, linewidth=1.5)
    ax[4].axhline(0, color='#374151', linestyle='--', linewidth=0.8)
    ax[4].fill_between(tel1['Distance'], delta_time, 0, where=(delta_time < 0), color=color1, alpha=0.35)
    ax[4].fill_between(tel1['Distance'], delta_time, 0, where=(delta_time > 0), color=color2, alpha=0.35)
    ax[4].set_ylabel(f"Δ {name1}-{name2} (s)", color='#f0f3f6', fontsize=9)
    ax[4].set_xlabel("Distance (m)", color='#f0f3f6', fontsize=9)

    event_name = session1.event.EventName if session1.event is not None else "Session"
    fig.suptitle(f"{event_name}\n{driver} - {name1} vs {name2} Fastest Lap Telemetry", color='#f0f3f6', family='monospace', fontsize=10, weight='bold')
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def _get_top_2_drivers(session, laps=None):
    results = _safe_results(session)
    if results is not None and not results.empty and "Abbreviation" in results:
        top_2 = results.iloc[:2]["Abbreviation"].dropna().tolist()
        if len(top_2) >= 2:
            return str(top_2[0]), str(top_2[1])
    if laps is None:
        laps = _safe_laps(session)
    if laps is not None and not laps.empty:
        top_laps = _pick_quicklaps(laps).sort_values(by="LapTime").dropna(subset=["LapTime"])
        if not top_laps.empty:
            drivers = [str(d) for d in top_laps["Driver"].unique().tolist()]
            if len(drivers) >= 2:
                return drivers[0], drivers[1]
            elif len(drivers) == 1:
                return drivers[0], None
    return None, None


def plot_micro_sector_dominance(session, p1_drv=None, p2_drv=None, num_sectors=25, compact=False):
    """Calculates and renders track map dominance broken down into micro-sectors.
    Color codes each circuit segment according to which driver set the faster split time.
    """
    laps = _safe_laps(session)
    if laps is None or laps.empty:
        st.info("Lap telemetry data unavailable for micro-sector dominance map.")
        return None

    if not p1_drv or not p2_drv:
        d1_cand, d2_cand = _get_top_2_drivers(session, laps)
        driver_1 = p1_drv or d1_cand
        driver_2 = p2_drv or d2_cand
    else:
        driver_1, driver_2 = p1_drv, p2_drv

    if not driver_1 or not driver_2:
        st.info("Insufficient driver data to render micro-sector dominance.")
        return None

    try:
        color_d1 = get_team_color(driver_1, default="#ff8000")
        color_d2 = get_team_color(driver_2, default="#1e41ff")
        if str(color_d1).lower() == str(color_d2).lower():
            color_d2 = "#ffffff" if color_d1 != "#ffffff" else "#f5a623"

        laps_d1 = _pick_fastest(_pick_driver_laps(laps, driver_1))
        laps_d2 = _pick_fastest(_pick_driver_laps(laps, driver_2))

        if laps_d1 is None or laps_d2 is None or pd.isna(laps_d1.get("LapTime")) or pd.isna(laps_d2.get("LapTime")):
            st.info("Could not extract clean fastest laps for both drivers.")
            return None

        _ensure_telemetry_loaded(session)
        tel_d1 = laps_d1.get_telemetry()
        tel_d2 = laps_d2.get_telemetry()

        if tel_d1 is None or tel_d2 is None or "X" not in tel_d1.columns or "Y" not in tel_d1.columns or "Distance" not in tel_d1.columns:
            st.info("High-precision GPS coordinates unavailable for this session.")
            return None

        # Clean telemetry
        tel_d1 = tel_d1.dropna(subset=["X", "Y", "Distance", "Time"]).copy()
        tel_d2 = tel_d2.dropna(subset=["Distance", "Time"]).copy()

        if len(tel_d1) < 50 or len(tel_d2) < 50:
            st.info("Telemetry point density too low for micro-sector calculation.")
            return None

        max_dist = min(tel_d1["Distance"].max(), tel_d2["Distance"].max())
        if max_dist <= 500:
            st.info("Track distance range invalid.")
            return None

        # Fetch circuit info for rotation and corner turn boundaries
        rot = 0.0
        circuit_info = None
        try:
            circuit_info = session.get_circuit_info()
            if circuit_info is not None:
                rot = getattr(circuit_info, "rotation", 0.0) or 0.0
        except Exception:
            rot = 0.0
            circuit_info = None

        corners_df = None
        if circuit_info is not None and hasattr(circuit_info, "corners") and circuit_info.corners is not None and not circuit_info.corners.empty:
            c_valid = circuit_info.corners.dropna(subset=["Distance"]).sort_values("Distance")
            c_valid = c_valid[(c_valid["Distance"] > 0) & (c_valid["Distance"] < max_dist)]
            if len(c_valid) >= 3:
                corners_df = c_valid

        # Segment lap path by actual circuit turns
        if corners_df is not None and len(corners_df) >= 3:
            c_dists = corners_df["Distance"].to_numpy()
            midpoints = (c_dists[:-1] + c_dists[1:]) / 2.0
            bins = np.concatenate(([0.0], midpoints, [max_dist]))
            num_segments = len(bins) - 1
            unit_label = "TURNS"
        else:
            num_segments = num_sectors
            bins = np.linspace(0, max_dist, num_segments + 1)
            unit_label = "TURNS"

        t1_sec = tel_d1["Time"].dt.total_seconds().to_numpy()
        t2_sec = tel_d2["Time"].dt.total_seconds().to_numpy()
        d1 = tel_d1["Distance"].to_numpy()
        d2 = tel_d2["Distance"].to_numpy()

        t1_bins = np.interp(bins, d1, t1_sec)
        t2_bins = np.interp(bins, d2, t2_sec)

        dt1 = np.diff(t1_bins)
        dt2 = np.diff(t2_bins)
        winners = np.where(dt1 <= dt2, driver_1, driver_2)

        count_1 = int(np.sum(winners == driver_1))
        count_2 = int(np.sum(winners == driver_2))
        pct_1 = round((count_1 / num_segments) * 100, 1)
        pct_2 = round((count_2 / num_segments) * 100, 1)

        def _rotate_points(xy, deg):
            if deg == 0:
                return xy[:, 0], xy[:, 1]
            theta = np.radians(deg)
            c, s = np.cos(theta), np.sin(theta)
            r_mat = np.array(((c, -s), (s, c)))
            rot_xy = np.dot(xy, r_mat)
            return rot_xy[:, 0], rot_xy[:, 1]

        xy_raw = tel_d1[["X", "Y"]].to_numpy()
        x_rot, y_rot = _rotate_points(xy_raw, rot)

        fig_size = (7.5, 5.8) if compact else (9.5, 6.8)
        fig, ax = plt.subplots(figsize=fig_size)
        fig.patch.set_facecolor("#161b22")
        ax.set_facecolor("#161b22")

        # Track shadow/base line
        ax.plot(x_rot, y_rot, color="#0d1117", linewidth=7.5, zorder=2, alpha=0.95)

        # Plot turn segments with seamless overlap
        for i in range(num_segments):
            start_idx = np.searchsorted(d1, bins[i], side="left")
            end_idx = min(len(d1), np.searchsorted(d1, bins[i + 1], side="right") + 1)
            if start_idx >= end_idx:
                continue
            seg_x = x_rot[start_idx:end_idx]
            seg_y = y_rot[start_idx:end_idx]
            seg_color = color_d1 if winners[i] == driver_1 else color_d2
            ax.plot(seg_x, seg_y, color=seg_color, linewidth=4.2, zorder=3, solid_capstyle="round")

        # Start / Finish Line
        ax.scatter([x_rot[0]], [y_rot[0]], color="#ffffff", s=60, zorder=6, edgecolors="#0d1117", linewidths=1.2)
        ax.annotate("S/F", (x_rot[0], y_rot[0]), color="#ffffff", fontsize=7.5, fontweight="bold", fontfamily="monospace", xytext=(8, 8), textcoords="offset points", bbox=dict(boxstyle="square,pad=0.2", fc="#161b22", ec="#ffffff", lw=0.8), zorder=7)

        # Annotate corners if circuit_info is present
        if circuit_info is not None and hasattr(circuit_info, "corners") and circuit_info.corners is not None and not circuit_info.corners.empty:
            try:
                c_df = circuit_info.corners.dropna(subset=["X", "Y"]).copy()
                if not c_df.empty:
                    c_xy_raw = c_df[["X", "Y"]].to_numpy()
                    cx_rot, cy_rot = _rotate_points(c_xy_raw, rot)
                    for idx, (_, c_row) in enumerate(c_df.iterrows()):
                        t_num = str(c_row.get("Number", idx + 1))
                        # Only label every corner if <= 16 corners, else every other
                        if len(c_df) <= 16 or int(t_num) % 2 == 1:
                            ax.scatter([cx_rot[idx]], [cy_rot[idx]], color="#262c36", s=32, zorder=4, edgecolors="#8b949e", linewidths=0.6)
                            ax.annotate(f"T{t_num}", (cx_rot[idx], cy_rot[idx]), color="#8b949e", fontsize=6.8, fontweight="bold", fontfamily="monospace", ha="center", va="center", bbox=dict(boxstyle="circle,pad=0.2", fc="#161b22", ec="#262c36", lw=0.6), zorder=5)
            except Exception:
                pass

        ax.set_aspect("equal", "datalim")
        ax.axis("off")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

        return {
            "driver_1": driver_1,
            "driver_2": driver_2,
            "color_1": color_d1,
            "color_2": color_d2,
            "count_1": count_1,
            "count_2": count_2,
            "pct_1": pct_1,
            "pct_2": pct_2,
            "total_turns": num_segments,
            "total_sectors": num_segments,
            "unit_label": unit_label,
            "d1_lap_time": str(laps_d1["LapTime"]).split()[-1][:8] if pd.notna(laps_d1.get("LapTime")) else "-",
            "d2_lap_time": str(laps_d2["LapTime"]).split()[-1][:8] if pd.notna(laps_d2.get("LapTime")) else "-",
        }
    except Exception:
        st.info("Track map dominance overlay unavailable for this session.")
        return None


_CORNER_MATRIX_CACHE = {}
_TYRE_MATRIX_CACHE = {}


def compute_corner_telemetry_matrix(session, p1_drv=None, p2_drv=None):
    """Computes corner-by-corner braking onset, apex minimum speed, gear selection,
    and throttle pick-up points comparing Driver 1 vs Driver 2.
    """
    laps = _safe_laps(session)
    if laps is None or laps.empty:
        return None

    if not p1_drv or not p2_drv:
        d1_cand, d2_cand = _get_top_2_drivers(session, laps)
        driver_1 = p1_drv or d1_cand
        driver_2 = p2_drv or d2_cand
    else:
        driver_1, driver_2 = p1_drv, p2_drv

    if not driver_1 or not driver_2:
        return None

    ev_name = str(getattr(getattr(session, "event", None), "EventName", ""))
    s_key = (str(getattr(session, "name", "")), ev_name, str(driver_1), str(driver_2))
    if s_key in _CORNER_MATRIX_CACHE:
        return _CORNER_MATRIX_CACHE[s_key]


    try:
        color_d1 = get_team_color(driver_1, default="#ff8000")
        color_d2 = get_team_color(driver_2, default="#1e41ff")
        if str(color_d1).lower() == str(color_d2).lower():
            color_d2 = "#ffffff" if color_d1 != "#ffffff" else "#f5a623"

        laps_d1 = _pick_fastest(_pick_driver_laps(laps, driver_1))
        laps_d2 = _pick_fastest(_pick_driver_laps(laps, driver_2))

        if laps_d1 is None or laps_d2 is None:
            return None

        _ensure_telemetry_loaded(session)
        tel_1 = laps_d1.get_telemetry()
        tel_2 = laps_d2.get_telemetry()

        if tel_1 is None or tel_2 is None or "Distance" not in tel_1.columns or "Speed" not in tel_1.columns:
            return None

        circuit_info = session.get_circuit_info()
        if circuit_info is None or not hasattr(circuit_info, "corners") or circuit_info.corners is None or circuit_info.corners.empty:
            return None

        corners = circuit_info.corners.dropna(subset=["Distance"]).sort_values("Distance").reset_index(drop=True)
        rows = []
        d1_wins = 0
        d2_wins = 0

        for _, c in corners.iterrows():
            t_num = int(c.get("Number", len(rows) + 1))
            apex_dist = float(c["Distance"])

            # Apex speed window: [apex - 70m, apex + 50m]
            w1 = tel_1[(tel_1["Distance"] >= apex_dist - 70) & (tel_1["Distance"] <= apex_dist + 50)]
            w2 = tel_2[(tel_2["Distance"] >= apex_dist - 70) & (tel_2["Distance"] <= apex_dist + 50)]
            if w1.empty or w2.empty:
                continue

            idx1 = w1["Speed"].idxmin()
            idx2 = w2["Speed"].idxmin()
            s1 = float(w1.loc[idx1, "Speed"])
            s2 = float(w2.loc[idx2, "Speed"])
            g1 = int(w1.loc[idx1, "nGear"]) if "nGear" in w1.columns and pd.notna(w1.loc[idx1, "nGear"]) else "-"
            g2 = int(w2.loc[idx2, "nGear"]) if "nGear" in w2.columns and pd.notna(w2.loc[idx2, "nGear"]) else "-"

            # Braking zone in [apex - 250m, apex]
            b_zone1 = tel_1[(tel_1["Distance"] >= apex_dist - 250) & (tel_1["Distance"] <= apex_dist)]
            b_zone2 = tel_2[(tel_2["Distance"] >= apex_dist - 250) & (tel_2["Distance"] <= apex_dist)]
            b_on1 = b_zone1[b_zone1["Brake"] > 0] if "Brake" in b_zone1.columns else pd.DataFrame()
            b_on2 = b_zone2[b_zone2["Brake"] > 0] if "Brake" in b_zone2.columns else pd.DataFrame()

            b1_dist = round(apex_dist - b_on1["Distance"].iloc[0], 1) if not b_on1.empty else None
            b2_dist = round(apex_dist - b_on2["Distance"].iloc[0], 1) if not b_on2.empty else None

            delta = round(s1 - s2, 1)
            if delta > 0:
                d1_wins += 1
                adv = driver_1
            elif delta < 0:
                d2_wins += 1
                adv = driver_2
            else:
                adv = "TIE"

            rows.append({
                "Turn": f"T{t_num}",
                "Apex (m)": int(round(apex_dist)),
                f"{driver_1} Spd": round(s1, 1),
                f"{driver_2} Spd": round(s2, 1),
                "Δ Spd (km/h)": f"{delta:+.1f}",
                f"{driver_1} Gear": f"G{g1}" if g1 != "-" else "-",
                f"{driver_2} Gear": f"G{g2}" if g2 != "-" else "-",
                f"{driver_1} Brake": f"{b1_dist}m" if b1_dist else "-",
                f"{driver_2} Brake": f"{b2_dist}m" if b2_dist else "-",
                "Advantage": adv,
                "_delta_val": delta,
                "_s1": s1,
                "_s2": s2,
            })

        if not rows:
            return None

        df = pd.DataFrame(rows)
        res = {
            "dataframe": df,
            "driver_1": driver_1,
            "driver_2": driver_2,
            "color_1": color_d1,
            "color_2": color_d2,
            "d1_wins": d1_wins,
            "d2_wins": d2_wins,
            "total_corners": len(rows),
        }
        _CORNER_MATRIX_CACHE[s_key] = res
        return res
    except Exception:
        return None


def plot_tyre_degradation_curves(session, compact=False):
    """Plots lap pace versus tyre age curves for each tyre compound in the race,
    fitting degradation trendlines on clean green-flag laps.
    """
    laps = _safe_laps(session)
    if laps is None or laps.empty or "Compound" not in laps.columns:
        st.info("Tyre compound data unavailable for degradation curves.")
        return None

    try:
        # Filter clean racing laps
        clean = laps[
            (laps["TrackStatus"] == "1")
            & (laps["PitInTime"].isna())
            & (laps["PitOutTime"].isna())
            & laps["LapTime"].notna()
        ].copy()

        if clean.empty or "TyreLife" not in clean.columns:
            st.info("Clean race lap sample insufficient to build degradation models.")
            return None

        clean["LapTimeSec"] = clean["LapTime"].dt.total_seconds()
        clean = clean.dropna(subset=["TyreLife", "LapTimeSec"])

        compound_colors = {
            "SOFT": "#e10600",
            "MEDIUM": "#f5a623",
            "HARD": "#f0f3f6",
            "INTERMEDIATE": "#39b54a",
            "WET": "#38bdf8",
        }

        fig_size = (7.6, 4.6) if compact else (9.5, 5.2)
        fig, ax = plt.subplots(figsize=fig_size)
        fig.patch.set_facecolor("#161b22")
        ax.set_facecolor("#161b22")

        has_curves = False
        stats = []

        for comp in ["SOFT", "MEDIUM", "HARD", "INTERMEDIATE", "WET"]:
            sub = clean[clean["Compound"] == comp]
            if len(sub) < 10:
                continue

            med = sub["LapTimeSec"].median()
            valid = sub[(sub["LapTimeSec"] >= med - 3.5) & (sub["LapTimeSec"] <= med + 3.5)].copy()
            if len(valid) < 8:
                continue

            c_color = compound_colors.get(comp, "#8b949e")
            x = valid["TyreLife"].values
            y = valid["LapTimeSec"].values
            poly = np.polyfit(x, y, 1)
            slope, intercept = poly[0], poly[1]

            # Scatter points
            ax.scatter(x, y, color=c_color, alpha=0.22, s=14, edgecolors="none")

            # Regression line
            x_range = np.linspace(x.min(), x.max(), 50)
            y_range = slope * x_range + intercept
            ax.plot(x_range, y_range, color=c_color, linewidth=2.4, label=f"{comp} ({slope:+.3f} s/lap)")
            has_curves = True

            stats.append({
                "Compound": comp,
                "BasePace": intercept,
                "DegRate": slope,
                "MaxLife": int(x.max()),
                "Laps": len(valid),
            })

        if not has_curves:
            st.info("Insufficient compound stint samples to compute degradation slopes.")
            plt.close(fig)
            return None

        ax.set_xlabel("Tyre Age (Laps)", color="#f0f3f6", fontsize=9)
        ax.set_ylabel("Lap Time (s)", color="#f0f3f6", fontsize=9)
        ax.tick_params(colors="#8b949e", labelsize=8.5)
        for spine in ax.spines.values():
            spine.set_color("#262c36")
        ax.grid(color="#262c36", alpha=0.55, linewidth=0.7)
        ax.legend(facecolor="#161b22", edgecolor="#262c36", labelcolor="#f0f3f6", fontsize="small", loc="upper left")

        event_name = session.event.EventName if session.event is not None else "Session"
        fig.suptitle(f"{event_name} - Race Tyre Degradation Curves", color="#f0f3f6", family="monospace", fontsize=10, weight="bold")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)
        return stats
    except Exception:
        st.info("Tyre degradation model could not be computed for this session.")
        return None


def get_tyre_strategy_matrix(session):
    """Computes tyre degradation wear rate, cliff lap threshold, and optimal stint window."""
    laps = _safe_laps(session)
    if laps is None or laps.empty or "Compound" not in laps.columns:
        return None

    ev_name = str(getattr(getattr(session, "event", None), "EventName", ""))
    s_key = (str(getattr(session, "name", "")), ev_name)
    if s_key in _TYRE_MATRIX_CACHE:
        return _TYRE_MATRIX_CACHE[s_key]

    try:
        clean = laps[
            (laps["TrackStatus"] == "1")
            & (laps["PitInTime"].isna())
            & (laps["PitOutTime"].isna())
            & laps["LapTime"].notna()
        ].copy()

        if clean.empty or "TyreLife" not in clean.columns:
            return None

        clean["LapTimeSec"] = clean["LapTime"].dt.total_seconds()
        clean = clean.dropna(subset=["TyreLife", "LapTimeSec"])

        matrix = []
        for comp in ["SOFT", "MEDIUM", "HARD", "INTERMEDIATE", "WET"]:
            sub = clean[clean["Compound"] == comp]
            if len(sub) < 10:
                continue

            med = sub["LapTimeSec"].median()
            valid = sub[(sub["LapTimeSec"] >= med - 3.5) & (sub["LapTimeSec"] <= med + 3.5)].copy()
            if len(valid) < 8:
                continue

            x = valid["TyreLife"].values
            y = valid["LapTimeSec"].values
            poly = np.polyfit(x, y, 1)
            slope, intercept = poly[0], poly[1]

            fuel_corr_deg = slope + 0.055
            max_life = int(x.max())

            # Cliff detection
            cliff_lap = max_life
            grouped = valid.groupby("TyreLife")["LapTimeSec"].median()
            for l_val in range(max(10, max_life - 6), max_life + 1):
                if l_val in grouped:
                    expected = intercept + slope * l_val
                    if grouped[l_val] - expected > 0.7:
                        cliff_lap = l_val
                        break

            pit_min = max(8, cliff_lap - 5)
            pit_max = min(max_life, cliff_lap + 1)

            def fmt_pace(s):
                m = int(s // 60)
                rem = s % 60
                return f"{m}:{rem:06.3f}"

            matrix.append({
                "Compound": comp,
                "Base Pace": fmt_pace(intercept),
                "Observed Deg": f"{slope:+.3f} s/lap",
                "Fuel-Adj Wear": f"{fuel_corr_deg:+.3f} s/lap",
                "Stint Window": f"Laps {pit_min} - {pit_max}",
                "Cliff Onset": f"Lap {cliff_lap}",
                "Laps Logged": len(valid),
            })

        if not matrix:
            return None

        res_df = pd.DataFrame(matrix)
        _TYRE_MATRIX_CACHE[s_key] = res_df
        return res_df
    except Exception:
        return None


