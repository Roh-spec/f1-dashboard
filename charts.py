import matplotlib.pyplot as plt
import fastf1.plotting
import streamlit as st
import pandas as pd

# Use fastf1 setup
fastf1.plotting.setup_mpl(mpl_timedelta_support=False, misc_mpl_mods=False, color_scheme='fastf1')

def _set_retro_style(fig, ax_list):
    fig.patch.set_facecolor('#211d18') # --ink
    for ax in ax_list:
        ax.set_facecolor('#211d18')
        ax.tick_params(colors='#e5dccb') # --paper-deep
        for spine in ax.spines.values():
            spine.set_color('#6f675b') # --muted

def plot_top_2_telemetry(session):
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

    fig, ax = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
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

def plot_lap_times(session):
    if session is None or session.laps is None or session.laps.empty:
        return
        
    try:
        drivers = session.results['Abbreviation'].tolist()
    except Exception:
        drivers = session.laps['Driver'].unique().tolist()
        
    fig, ax = plt.subplots(figsize=(10, 6))
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
