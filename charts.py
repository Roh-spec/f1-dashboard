from __future__ import annotations

import pandas as pd
import streamlit as st


def make_lap_chart_data(data: pd.DataFrame) -> pd.DataFrame:
    return data.set_index("Lap")[["Lap Time"]]


def make_stint_chart_data(data: pd.DataFrame) -> pd.DataFrame:
    columns = [column for column in ["Speed", "Tyre Life"] if column in data.columns]
    return data.set_index("Lap")[columns]


def make_sector_chart_data(data: pd.DataFrame) -> pd.DataFrame:
    fastest = data.loc[data["Lap Time"].idxmin()]
    return pd.DataFrame(
        {
            "Sector": ["Sector 1", "Sector 2", "Sector 3"],
            "Seconds": [fastest["Sector 1"], fastest["Sector 2"], fastest["Sector 3"]],
        }
    ).set_index("Sector")


def render_chart_shell(title: str, caption: str = "") -> None:
    st.markdown(
        f"""
        <div class="status-label">{title}</div>
        <p style="color:#6f675b; margin-top: 4px;">{caption}</p>
        """,
        unsafe_allow_html=True,
    )


def render_lap_chart(data: pd.DataFrame) -> None:
    render_chart_shell(
        "Lap Time Trace",
        f"Average lap: {data['Lap Time'].mean():.3f}s",
    )
    st.line_chart(make_lap_chart_data(data), height=360, use_container_width=True)


def render_system_chart(data: pd.DataFrame) -> None:
    chart_data = make_stint_chart_data(data)
    render_chart_shell("Stint Register", "Speed-trap readings and tyre age where available.")
    if chart_data.empty:
        st.warning("No speed or tyre-life columns were available for this session.")
        return
    st.line_chart(chart_data, height=360, use_container_width=True)


def render_sector_chart(data: pd.DataFrame) -> None:
    fastest = data.loc[data["Lap Time"].idxmin()]
    render_chart_shell(
        f"Fastest Lap Split: Lap {int(fastest['Lap'])}",
        "Sector breakdown for the best lap.",
    )
    st.bar_chart(make_sector_chart_data(data), height=320, use_container_width=True)
