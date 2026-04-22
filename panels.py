from __future__ import annotations

import pandas as pd
import streamlit as st

from models import SessionConfig, SessionMeta


def render_hero(config: SessionConfig, meta: SessionMeta) -> None:
    st.markdown(
        f"""
        <div class="hero">
            <p class="eyebrow">FASTF1 ARCHIVE DASHBOARD</p>
            <p class="hero-title">RETRO F1<br/>TIMING ROOM</p>
            <p class="hero-subtitle">
                A warm paper-and-CRT inspired timing board for real Formula 1 lap data:
                sectors, compounds, tyre life, speed traps, and lap accuracy flags.
            </p>
            <div class="badge-row">
                <span class="badge">SOURCE: {meta.source}</span>
                <span class="badge">EVENT: {meta.event_name}</span>
                <span class="badge">SESSION: {meta.session_name}</span>
                <span class="badge">DRIVER: {meta.driver}</span>
                <span class="badge">TEAM: {meta.team}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if meta.note:
        st.info(meta.note)


def render_status_cards(data: pd.DataFrame, meta: SessionMeta) -> None:
    fastest = data.loc[data["Lap Time"].idxmin()]
    latest = data.iloc[-1]
    consistency = data["Lap Time"].std()
    accurate_laps = int(data["Is Accurate"].fillna(False).sum()) if "Is Accurate" in data else 0
    best_speed = data["Speed"].max(skipna=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Fastest Lap", f"{fastest['Lap Time']:.3f}s", f"Lap {int(fastest['Lap'])}")
    col2.metric("Top Speed Trap", _format_speed(best_speed), meta.source)
    col3.metric("Tyre Age", _format_tyre_age(latest), f"{latest.get('Compound', 'Unknown')}")
    col4.metric("Consistency", f"{consistency:.3f}s", f"{accurate_laps} accurate laps")


def render_strategy_panel(data: pd.DataFrame, meta: SessionMeta) -> None:
    latest = data.iloc[-1]
    fastest = data.loc[data["Lap Time"].idxmin()]
    compounds = ", ".join(str(value) for value in data["Compound"].dropna().unique()) or "Unknown"
    stint_count = int(data["Stint"].dropna().nunique()) if "Stint" in data else 0

    col1, col2, col3 = st.columns(3)
    col1.markdown(
        f"""
        <div class="status-card">
            <div class="status-label">Race Desk Readout</div>
            <div class="status-value">{meta.status}</div>
            <p>{meta.circuit}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col2.markdown(
        f"""
        <div class="status-card">
            <div class="status-label">Fastest Reference</div>
            <div class="status-value">Lap {int(fastest["Lap"])}</div>
            <p>{fastest["Lap Time"]:.3f}s with track status {fastest.get("Track Status", "unknown")}.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    col3.markdown(
        f"""
        <div class="status-card">
            <div class="status-label">Tyre Notebook</div>
            <div class="status-value">{stint_count} Stints</div>
            <p>Compounds: {compounds}. Latest lap tyre age: {_format_tyre_age(latest)}.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_lap_log(data: pd.DataFrame) -> None:
    st.subheader("Lap Log")
    display_columns = [
        "Lap",
        "Lap Time",
        "Sector 1",
        "Sector 2",
        "Sector 3",
        "Speed",
        "Compound",
        "Tyre Life",
        "Track Status",
        "Is Accurate",
    ]
    available_columns = [column for column in display_columns if column in data.columns]
    st.dataframe(
        data[available_columns].sort_values("Lap", ascending=False),
        use_container_width=True,
        hide_index=True,
    )


def _format_speed(value: float) -> str:
    if pd.isna(value):
        return "N/A"
    return f"{value:.1f} km/h"


def _format_tyre_age(row: pd.Series) -> str:
    tyre_life = row.get("Tyre Life")
    if pd.isna(tyre_life):
        return "N/A"
    return f"{tyre_life:.0f} laps"
