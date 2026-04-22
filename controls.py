from __future__ import annotations

import streamlit as st

from constants import CURRENT_DRIVERS, EVENT_PRESETS, SESSION_TYPES
from models import SessionConfig


def render_race_controls() -> SessionConfig:
    with st.sidebar:
        st.title("Archive Controls")
        use_fastf1 = st.toggle("Use FastF1 data", value=True)
        year = st.number_input("Season", min_value=2018, max_value=2025, value=2024, step=1)
        grand_prix = st.selectbox("Grand Prix", EVENT_PRESETS, index=15)
        session_label = st.selectbox("Session", list(SESSION_TYPES.keys()), index=0)
        driver_label = st.selectbox(
            "Driver",
            [f"{code} - {name}" for code, name in CURRENT_DRIVERS.items()],
            index=0,
        )
        st.caption("FastF1 loads real lap timing, sectors, compounds, tyre life, and speed-trap data.")

    return SessionConfig(
        year=int(year),
        grand_prix=grand_prix,
        session_type=SESSION_TYPES[session_label],
        driver=driver_label.split(" - ", maxsplit=1)[0],
        use_fastf1=use_fastf1,
    )
