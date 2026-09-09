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
        return session.laps
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


def plot_top_2_telemetry(session, compact=False):
    laps = _safe_laps(session)
    if laps is None or laps.empty:
        st.warning("No lap data available for telemetry.")
        return

    results = _safe_results(session)
    if results is not None and not results.empty and "Abbreviation" in results:
        top_2_drivers = results.iloc[:2]['Abbreviation'].dropna().tolist()
    else:
        top_laps = laps.pick_quicklaps().sort_values(by='LapTime').dropna(subset=['LapTime'])
        if top_laps.empty:
            st.warning("No quick laps available.")
            return
        top_2_drivers = top_laps['Driver'].unique()[:2].tolist()

    if len(top_2_drivers) < 2:
        st.warning("Not enough drivers with data to compare telemetry.")
        return

    driver_1, driver_2 = top_2_drivers[0], top_2_drivers[1]

    try:
        laps_d1 = laps.pick_driver(driver_1).pick_fastest()
        laps_d2 = laps.pick_driver(driver_2).pick_fastest()

        if pd.isna(laps_d1['LapTime']) or pd.isna(laps_d2['LapTime']):
            st.warning("Could not find valid fastest lap for top drivers.")
            return

        _ensure_telemetry_loaded(session)
        import fastf1.utils
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            delta_time, tel_d1, tel_d2 = fastf1.utils.delta_time(laps_d1, laps_d2)
    except Exception as e:
        st.info(f"Detailed 10Hz telemetry overlay unavailable ({e}). Lap pace and race traces are displayed below.")
        return

    try:
        color_d1 = fastf1.plotting.get_driver_color(driver_1, session)
    except Exception:
        color_d1 = None
    if not color_d1:
        color_d1 = get_team_color(driver_1, default="#ff8000")

    try:
        color_d2 = fastf1.plotting.get_driver_color(driver_2, session)
    except Exception:
        color_d2 = None
    if not color_d2:
        color_d2 = get_team_color(driver_2, default="#1e41ff")

    if str(color_d1).lower() == str(color_d2).lower():
        color_d2 = "#ffffff" if color_d1 != "#ffffff" else "#f5a623"

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
        drv_laps = laps.pick_driver(drv).pick_quicklaps()
        if not drv_laps.empty:
            try:
                color = fastf1.plotting.get_driver_color(drv, session)
            except Exception:
                color = '#e10600'
            ax.plot(drv_laps['LapNumber'], drv_laps['LapTime'].dt.total_seconds(), color=color, label=drv, alpha=0.85, linewidth=1.4)

    ax.set_xlabel("Lap Number", color='#f0f3f6', fontsize=9)
    ax.set_ylabel("Lap Time (s)", color='#f0f3f6', fontsize=9)

    event_name = session.event.EventName if session.event is not None else "Session"
    fig.suptitle(f"{event_name} - {session.name} Lap Times", color='#f0f3f6', family='monospace', fontsize=10, weight='bold')

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
        drv_laps = laps.pick_driver(drv)
        drv_laps = drv_laps.dropna(subset=['Position'])
        if not drv_laps.empty:
            try:
                from ui import get_team_color
                color = get_team_color(drv)
            except Exception:
                try:
                    color = fastf1.plotting.get_driver_color(drv, session)
                except Exception:
                    color = '#e10600'
            ax.plot(drv_laps['LapNumber'], drv_laps['Position'], color=color, label=drv, alpha=0.85, linewidth=1.8)

    max_pos = min(22, max(20, len(drivers)))
    ax.set_ylim(max_pos + 0.5, 0.5)
    ax.set_yticks(range(1, max_pos + 1))

    ax.set_xlabel("Lap Number", color='#f0f3f6', fontsize=9)
    ax.set_ylabel("Position", color='#f0f3f6', fontsize=9)

    event_name = session.event.EventName if session.event is not None else "Session"
    fig.suptitle(f"{event_name} - {session.name} Track Positions", color='#f0f3f6', family='monospace', fontsize=10, weight='bold')

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
    if not required.issubset(set(laps.columns)):
        st.warning("Tyre strategy data unavailable for this session.")
        return

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
        lap1 = laps1.pick_driver(driver).pick_fastest()
        lap2 = laps2.pick_driver(driver).pick_fastest()

        if pd.isna(lap1['LapTime']) or pd.isna(lap2['LapTime']):
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
