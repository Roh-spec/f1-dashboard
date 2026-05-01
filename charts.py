"""Shared FastF1 chart rendering helpers.

This module owns the app-wide Matplotlib/FastF1 chart style plus the reusable
data transformations for telemetry overlays, lap-time traces, position plots,
and tyre-stint timelines. Rendering pages should call these helpers when they
need those shared transformations instead of duplicating plotting setup.
"""

import matplotlib.pyplot as plt
import fastf1.plotting
import streamlit as st
import pandas as pd
from matplotlib.patches import Patch

# Use fastf1 setup
fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')

def _set_retro_style(fig, ax_list):
    fig.patch.set_facecolor('#211d18') # --ink
    for ax in ax_list:
        ax.set_facecolor('#211d18')
        ax.tick_params(colors='#e5dccb') # --paper-deep
        for spine in ax.spines.values():
            spine.set_color('#6f675b') # --muted

def plot_top_2_telemetry(session, compact=False):
    if session is None or session.laps is None or session.laps.empty:
        st.warning("No lap data available for telemetry.")
        return

    try:
        results = session.results
        top_2_drivers = results.iloc[:2]['Abbreviation'].tolist()
    except Exception:
        top_laps = session.laps.pick_quicklaps().sort_values(by='LapTime').dropna(subset=['LapTime'])
        if top_laps.empty:
            st.warning("No quick laps available.")
            return
        top_2_drivers = top_laps['Driver'].unique()[:2].tolist()

    if len(top_2_drivers) < 2:
        st.warning("Not enough drivers with data to compare.")
        return
        
    driver_1, driver_2 = top_2_drivers[0], top_2_drivers[1]

    try:
        laps_d1 = session.laps.pick_driver(driver_1).pick_fastest()
        laps_d2 = session.laps.pick_driver(driver_2).pick_fastest()
        
        if pd.isna(laps_d1['LapTime']) or pd.isna(laps_d2['LapTime']):
            st.warning("Could not find valid fastest lap for top drivers.")
            return

        tel_d1 = laps_d1.get_telemetry()
        tel_d2 = laps_d2.get_telemetry()
    except Exception as e:
        st.warning(f"Telemetry data unavailable: {e}")
        return

    color_d1 = fastf1.plotting.get_driver_color(driver_1, session)
    color_d2 = fastf1.plotting.get_driver_color(driver_2, session)

    fig_size = (7.6, 5.6) if compact else (10, 8)
    fig, ax = plt.subplots(3, 1, figsize=fig_size, sharex=True)
    _set_retro_style(fig, ax)

    ax[0].plot(tel_d1['Distance'], tel_d1['Speed'], color=color_d1, label=driver_1)
    ax[0].plot(tel_d2['Distance'], tel_d2['Speed'], color=color_d2, label=driver_2)
    ax[0].set_ylabel("Speed (km/h)", color='#e5dccb')
    ax[0].legend(facecolor='#211d18', edgecolor='#6f675b', labelcolor='#e5dccb')

    ax[1].plot(tel_d1['Distance'], tel_d1['Throttle'], color=color_d1)
    ax[1].plot(tel_d2['Distance'], tel_d2['Throttle'], color=color_d2)
    ax[1].set_ylabel("Throttle %", color='#e5dccb')

    ax[2].plot(tel_d1['Distance'], tel_d1['Brake'], color=color_d1)
    ax[2].plot(tel_d2['Distance'], tel_d2['Brake'], color=color_d2)
    ax[2].set_ylabel("Brake", color='#e5dccb')
    ax[2].set_xlabel("Distance (m)", color='#e5dccb')

    event_name = session.event.EventName if session.event is not None else "Session"
    fig.suptitle(f"{event_name} - {session.name}\n{driver_1} vs {driver_2} Fastest Lap Telemetry", color='#fbf7ee', family='monospace')
    fig.tight_layout()
    st.pyplot(fig)

def plot_lap_times(session, compact=False):
    if session is None or session.laps is None or session.laps.empty:
        return
        
    try:
        drivers = session.results['Abbreviation'].tolist()
    except Exception:
        drivers = session.laps['Driver'].unique().tolist()
        
    fig_size = (7.6, 4.6) if compact else (10, 6)
    fig, ax = plt.subplots(figsize=fig_size)
    _set_retro_style(fig, [ax])

    for drv in drivers:
        drv_laps = session.laps.pick_driver(drv).pick_quicklaps()
        if not drv_laps.empty:
            try:
                color = fastf1.plotting.get_driver_color(drv, session)
            except Exception:
                color = '#e5dccb' # fallback color
            ax.plot(drv_laps['LapNumber'], drv_laps['LapTime'].dt.total_seconds(), color=color, label=drv, alpha=0.8, linewidth=1.5)

    ax.set_xlabel("Lap Number", color='#e5dccb')
    ax.set_ylabel("Lap Time (s)", color='#e5dccb')
    
    event_name = session.event.EventName if session.event is not None else "Session"
    fig.suptitle(f"{event_name} - {session.name} Lap Times", color='#fbf7ee', family='monospace')
    
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', facecolor='#211d18', edgecolor='#6f675b', labelcolor='#e5dccb', fontsize='small')
    fig.tight_layout()
    st.pyplot(fig)

def plot_driver_positions(session, compact=False):
    if session is None or session.laps is None or session.laps.empty:
        return
        
    try:
        drivers = session.results['Abbreviation'].tolist()
    except Exception:
        drivers = session.laps['Driver'].unique().tolist()
        
    fig_size = (7.6, 5.4) if compact else (10, 8)
    fig, ax = plt.subplots(figsize=fig_size)
    _set_retro_style(fig, [ax])

    for drv in drivers:
        drv_laps = session.laps.pick_driver(drv)
        # Drop laps without position data
        drv_laps = drv_laps.dropna(subset=['Position'])
        if not drv_laps.empty:
            try:
                color = fastf1.plotting.get_driver_color(drv, session)
            except Exception:
                color = '#e5dccb' # fallback color
            ax.plot(drv_laps['LapNumber'], drv_laps['Position'], color=color, label=drv, alpha=0.8, linewidth=2.0)

    ax.set_ylim(20.5, 0.5)
    ax.set_yticks(range(1, 21))
    
    ax.set_xlabel("Lap Number", color='#e5dccb')
    ax.set_ylabel("Position", color='#e5dccb')
    
    event_name = session.event.EventName if session.event is not None else "Session"
    fig.suptitle(f"{event_name} - {session.name} Track Positions", color='#fbf7ee', family='monospace')
    
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', facecolor='#211d18', edgecolor='#6f675b', labelcolor='#e5dccb', fontsize='small')
    fig.tight_layout()
    st.pyplot(fig)


def plot_tyre_strategy_timeline(session, max_drivers=20, compact=False):
    if session is None or session.laps is None or session.laps.empty:
        st.warning("No lap data available for tyre strategy.")
        return

    laps = session.laps.copy()
    required = {"Driver", "Stint", "Compound", "LapNumber"}
    if not required.issubset(set(laps.columns)):
        st.warning("Tyre strategy data unavailable for this session.")
        return

    laps = laps.dropna(subset=["Driver", "Stint", "LapNumber"]).copy()
    if laps.empty:
        st.warning("Tyre strategy data unavailable for this session.")
        return

    compound_colors = {
        "SOFT": "#d81f2e",
        "MEDIUM": "#f4d03f",
        "HARD": "#f5f6fa",
        "INTERMEDIATE": "#32c36c",
        "WET": "#2a7fff",
        "UNKNOWN": "#8f9cb0",
    }

    try:
        driver_order = session.results["Abbreviation"].dropna().astype(str).tolist()
    except Exception:
        driver_order = laps["Driver"].dropna().astype(str).unique().tolist()

    if not driver_order:
        driver_order = laps["Driver"].dropna().astype(str).unique().tolist()
    if compact:
        max_drivers = min(max_drivers, 12)
    driver_order = driver_order[:max_drivers]

    if compact:
        fig_height = max(3.8, min(6.2, 0.28 * len(driver_order) + 1.8))
        fig_width = 8.4
    else:
        fig_height = max(4.8, min(10.5, 0.42 * len(driver_order) + 2.0))
        fig_width = 11

    fig, ax = plt.subplots(figsize=(fig_width, fig_height))
    _set_retro_style(fig, [ax])

    y_positions = list(range(len(driver_order)))
    y_map = {drv: idx for idx, drv in enumerate(driver_order)}
    bar_height = 0.62

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
                edgecolors="#0e1220",
                linewidth=0.8,
            )

        # Mark pit-stop points at stint boundaries
        pit_laps = stint_groups["lap_start"].tolist()[1:]
        if pit_laps:
            ax.scatter(
                [float(l) - 0.5 for l in pit_laps],
                [y] * len(pit_laps),
                s=16,
                color="#ff2f3f",
                edgecolors="#0e1220",
                linewidths=0.6,
                zorder=4,
            )

    max_lap = int(laps["LapNumber"].max()) if not laps["LapNumber"].dropna().empty else 0
    ax.set_xlim(0.5, max(5.5, max_lap + 1))
    ax.set_ylim(-0.8, len(driver_order) - 0.2)
    ax.set_yticks(y_positions)
    ax.set_yticklabels(driver_order, color="#e5dccb")
    ax.invert_yaxis()
    ax.set_xlabel("Lap Number", color="#e5dccb")
    ax.set_ylabel("Driver", color="#e5dccb")
    ax.grid(axis="x", color="#2a3146", linestyle="-", linewidth=0.5, alpha=0.45)

    legend_items = [
        Patch(facecolor=compound_colors["SOFT"], edgecolor="none", label="Soft"),
        Patch(facecolor=compound_colors["MEDIUM"], edgecolor="none", label="Medium"),
        Patch(facecolor=compound_colors["HARD"], edgecolor="none", label="Hard"),
        Patch(facecolor=compound_colors["INTERMEDIATE"], edgecolor="none", label="Intermediate"),
        Patch(facecolor=compound_colors["WET"], edgecolor="none", label="Wet"),
    ]
    ax.legend(
        handles=legend_items,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.06),
        ncol=5 if not compact else 3,
        frameon=True,
        facecolor="#211d18",
        edgecolor="#6f675b",
        labelcolor="#e5dccb",
        fontsize="small" if not compact else "x-small",
    )

    event_name = session.event.EventName if session.event is not None else "Session"
    fig.suptitle(f"{event_name} - {session.name} Tyre Strategy Timeline", color="#fbf7ee", family="monospace")
    fig.tight_layout()
    st.pyplot(fig)
