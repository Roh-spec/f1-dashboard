from __future__ import annotations

from contextlib import contextmanager
from html import escape

import streamlit as st
import streamlit.components.v1 as components


def inject_retro_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');

        :root {
            --paper: #fbf7ee;
            --paper-deep: #e5dccb;
            --ink: #211d18;
            --muted: #6f675b;
            --line: #211d18;
            --red: #9d2b22;
            --red-glow: rgba(157, 43, 34, 0.16);
            --black-glow: rgba(33, 29, 24, 0.16);
        }

        .stApp {
            background:
                radial-gradient(circle at 12% 14%, rgba(157, 43, 34, 0.08), transparent 18%),
                radial-gradient(circle at 84% 10%, rgba(33, 29, 24, 0.08), transparent 20%),
                linear-gradient(rgba(23, 23, 23, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(23, 23, 23, 0.03) 1px, transparent 1px),
                linear-gradient(180deg, #fffaf6 0%, #f6e6d8 100%);
            background-size: auto, auto, 24px 24px, 24px 24px, auto;
            color: var(--ink);
            font-family: 'VT323', monospace;
            font-size: 22px;
        }

        .stApp::before {
            content: "";
            pointer-events: none;
            position: fixed;
            inset: 0;
            z-index: 998;
            background: repeating-linear-gradient(
                to bottom,
                rgba(23, 23, 23, 0.04) 0,
                rgba(23, 23, 23, 0.04) 1px,
                transparent 1px,
                transparent 5px
            );
            mix-blend-mode: multiply;
        }

        .main .block-container {
            max-width: 1500px;
            padding-top: 1.6rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            font-family: 'Press Start 2P', cursive !important;
            color: var(--ink) !important;
            text-shadow: 3px 3px 0 var(--red-glow);
            text-transform: uppercase;
            margin-bottom: 1rem;
        }

        h1 {
            font-size: clamp(2.4rem, 5vw, 5.4rem) !important;
            line-height: 0.9;
            margin-top: 0;
        }

        h2 {
            font-size: clamp(1.3rem, 2vw, 2rem) !important;
        }

        h3 {
            font-size: clamp(1rem, 1.4vw, 1.4rem) !important;
        }

        p, li, label, .stMarkdown, .stText {
            font-family: 'VT323', monospace !important;
            color: var(--ink);
        }

        p, li {
            font-size: 24px !important;
        }

        a {
            color: var(--ink);
        }

        .hero {
            border: 3px solid var(--line);
            border-radius: 6px;
            background: linear-gradient(180deg, var(--paper) 0%, var(--paper-deep) 100%);
            box-shadow: 8px 8px 0 var(--line);
            padding: 24px 24px 22px;
            margin-bottom: 22px;
            position: relative;
            overflow: hidden;
        }

        .top-nav-shell {
            border: 3px solid var(--line);
            border-radius: 6px;
            background: linear-gradient(180deg, var(--paper) 0%, var(--paper-deep) 100%);
            box-shadow: 6px 6px 0 var(--line);
            margin-bottom: 18px;
            padding: 10px 14px;
        }

        .top-nav-title {
            font-family: 'Press Start 2P', cursive;
            font-size: 0.85rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin: 0;
            color: var(--ink);
        }

        div[data-testid="stPageLink"] a {
            border: 2px solid var(--line);
            border-radius: 4px;
            background: #fffaf2;
            box-shadow: 3px 3px 0 var(--line);
            color: var(--ink) !important;
            font-family: 'Press Start 2P', cursive;
            font-size: 0.62rem;
            letter-spacing: 0.04em;
            line-height: 1;
            min-height: 34px;
            padding: 8px 10px;
            text-transform: uppercase;
        }

        .hero::after {
            content: "";
            display: block;
            height: 6px;
            margin-top: 18px;
            background: linear-gradient(90deg, var(--red), var(--ink));
        }

        .eyebrow {
            margin: 0 0 10px;
            color: var(--muted);
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.18em;
            text-transform: uppercase;
        }

        .hero-title {
            font-family: 'Press Start 2P', cursive;
            font-size: clamp(2.7rem, 6.4vw, 6.2rem);
            line-height: 0.95;
            letter-spacing: 0.02em;
            margin: 0;
            text-shadow: 3px 3px 0 var(--red-glow);
        }

        .hero-subtitle {
            max-width: 980px;
            margin: 14px 0 0;
            font-size: 1.15rem;
        }

        .badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 16px;
        }

        .badge {
            border: 2px solid var(--line);
            border-radius: 4px;
            background: #ffffff;
            box-shadow: 4px 4px 0 var(--red);
            color: var(--ink);
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            padding: 8px 12px;
            text-transform: uppercase;
        }

        .section-kicker {
            color: var(--muted);
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.18em;
            margin: 0 0 8px;
            text-transform: uppercase;
        }

        .section-ribbon {
            border-top: 2px solid var(--line);
            border-bottom: 2px solid var(--line);
            background: linear-gradient(90deg, var(--red-glow), var(--black-glow));
            color: var(--ink);
            margin: 8px 0 20px;
            padding: 10px 14px;
            font-size: 0.84rem;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }

        .section-ribbon span {
            display: inline-block;
            margin-right: 12px;
        }

        .summary-strip,
        .panel-grid {
            display: grid;
            gap: 16px;
            margin-top: 18px;
        }

        .summary-strip {
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }

        .panel-grid {
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }

        .summary-card,
        .status-card,
        .practice-card,
        div[class*="st-key-track_archive_panel"],
        div[class*="st-key-circuit_map_panel"] {
            border: 3px solid var(--line);
            border-radius: 6px;
            background: linear-gradient(180deg, var(--paper) 0%, var(--paper-deep) 100%);
            box-shadow: 6px 6px 0 var(--line);
        }

        .summary-card {
            min-height: 116px;
            padding: 16px 18px 14px;
        }

        .summary-label {
            color: var(--muted);
            font-size: 0.74rem;
            font-weight: 700;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }

        .summary-value {
            font-family: 'Press Start 2P', cursive;
            font-size: 1.05rem;
            line-height: 1.35;
            margin: 14px 0 8px;
            text-shadow: 2px 2px 0 var(--red-glow);
        }

        .summary-note {
            color: var(--muted);
            margin: 0;
            font-size: 1rem;
            line-height: 1.25;
        }

        .panel-shell {
            border: 3px solid var(--line);
            border-radius: 6px;
            background: linear-gradient(180deg, var(--paper) 0%, var(--paper-deep) 100%);
            box-shadow: 6px 6px 0 var(--line);
            padding: 16px;
        }

        .panel-note {
            color: var(--muted);
            font-size: 0.84rem;
            margin-top: -4px;
        }

        div[data-testid="stVerticalBlockBorderWrapper"],
        div[class*="st-key-dialog_"] {
            border: 3px solid var(--line);
            border-radius: 6px;
            background: linear-gradient(180deg, var(--paper) 0%, var(--paper-deep) 100%);
            box-shadow: 8px 8px 0 var(--line);
            margin: 0 0 26px;
            padding: 18px;
            position: relative;
            overflow: hidden;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]::before,
        div[class*="st-key-dialog_"]::before {
            content: "";
            position: absolute;
            inset: 0 auto auto 0;
            width: 100%;
            height: 6px;
            background: linear-gradient(90deg, var(--red), var(--ink));
        }

        div[class*="st-key-dialog_header"] {
            padding: 26px 22px 18px;
        }

        div[class*="st-key-dialog_header"] h1 {
            margin-top: 0;
        }

        div[class*="st-key-dialog_stage_stats"] [data-testid="column"] {
            border: 2px solid var(--line);
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.42);
            box-shadow: 4px 4px 0 var(--line);
            padding: 10px 12px;
        }

        div[class*="st-key-track_archive_panel"],
        div[class*="st-key-circuit_map_panel"] {
            padding: 14px;
        }

        div[class*="st-key-circuit_map_panel"] [data-testid="stImage"],
        div[class*="st-key-circuit_map_panel"] [data-testid="stPyplot"] {
            border: 2px solid var(--line);
            border-radius: 4px;
            background: var(--paper);
            padding: 8px;
        }

        div[class*="st-key-dialog_track_details"] [data-testid="column"]:first-of-type {
            padding-right: 22px;
        }

        div[class*="st-key-dialog_track_details"] [data-testid="column"]:last-of-type {
            border-left: 3px dashed var(--line);
            padding-left: 22px;
        }

        div[class*="st-key-track_analysis_list"] {
            border-top: 3px dashed var(--line);
            margin-top: 22px;
            padding-top: 18px;
        }

        div[class*="st-key-track_analysis_list"] ul,
        div[class*="st-key-circuit_winners_list"] ul {
            border: 2px solid var(--line);
            border-radius: 4px;
            background: var(--paper);
            box-shadow: 4px 4px 0 var(--line);
            list-style-type: none;
            margin: 12px 0 0;
            padding: 12px 16px;
        }

        div[class*="st-key-track_analysis_list"] li,
        div[class*="st-key-circuit_winners_list"] li {
            border-bottom: 1px dashed rgba(23, 23, 23, 0.45);
            font-size: 22px !important;
            line-height: 1.28;
            padding: 8px 0;
        }

        div[class*="st-key-track_analysis_list"] li:last-child,
        div[class*="st-key-circuit_winners_list"] li:last-child {
            border-bottom: 0;
        }

        div[class*="st-key-circuit_winners_list"] {
            border-top: 3px dashed var(--line);
            margin-top: 18px;
            padding-top: 14px;
        }

        .session-kicker {
            color: var(--muted);
            font-size: 22px;
            margin-top: -6px;
        }

        .practice-card {
            min-height: 164px;
            padding: 16px;
            position: relative;
        }

        .practice-title {
            font-family: 'Press Start 2P', cursive;
            font-size: 1rem;
            margin: 0 0 12px;
            text-shadow: 2px 2px 0 var(--red-glow);
        }

        .practice-stat {
            margin: 7px 0;
            font-size: 22px;
            line-height: 1.05;
        }

        .practice-label {
            color: var(--muted);
            display: block;
            font-size: 18px;
            text-transform: uppercase;
        }

        .app-divider {
            border: 0;
            border-top: 2px dashed var(--line);
            margin: 18px 0 0;
        }

        [data-testid="stMetric"] {
            border: 2px solid var(--line);
            border-radius: 4px;
            padding: 18px;
            background: rgba(255, 250, 239, 0.95);
            box-shadow: 5px 5px 0 rgba(23, 23, 23, 0.08);
        }

        [data-testid="stMetricLabel"],
        [data-testid="stMetricDelta"] {
            color: var(--muted);
        }

        div[data-testid="stDataFrame"] {
            border: 2px solid var(--line);
            border-radius: 4px;
            overflow: hidden;
            box-shadow: 5px 5px 0 rgba(23, 23, 23, 0.08);
            background: rgba(255, 250, 239, 0.95);
        }

        .timing-card {
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 10px;
            background: linear-gradient(180deg, #14161d 0%, #0f1118 100%);
            box-shadow: 0 14px 40px rgba(0, 0, 0, 0.36);
            padding: 8px 10px 6px;
            margin: 8px 0 12px;
        }

        .timing-header {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            margin-bottom: 4px;
        }

        .timing-title {
            color: #d4dbea;
            font-family: 'Press Start 2P', cursive;
            font-size: 0.58rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .timing-row {
            display: grid;
            grid-template-columns: 34px 1fr auto;
            align-items: center;
            gap: 8px;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
            padding: 6px 0;
        }

        .timing-row:first-of-type {
            border-top: 0;
        }

        .timing-pos {
            font-family: 'Press Start 2P', cursive;
            font-size: 0.62rem;
            color: #f5f7fb;
            letter-spacing: 0.03em;
        }

        .timing-name {
            color: #f5f7fb;
            font-size: 0.95rem;
            line-height: 1.05;
        }

        .timing-team {
            color: #93a0b3;
            font-size: 0.78rem;
            line-height: 1.1;
            margin-top: 1px;
        }

        .timing-time {
            color: #b6bfd1;
            font-size: 0.8rem;
            white-space: nowrap;
            text-align: right;
            padding-left: 8px;
        }

        .timing-extra {
            color: #8f9cb0;
            font-size: 0.72rem;
            margin-top: 2px;
            letter-spacing: 0.01em;
        }

        .standings-card {
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            background: linear-gradient(180deg, #14161d 0%, #0f1118 100%);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.34);
            padding: 10px 12px 8px;
            margin: 8px 0 12px;
        }

        .standings-title {
            color: #8f9cb0;
            font-family: 'Press Start 2P', cursive;
            font-size: 0.52rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .standings-row {
            display: grid;
            grid-template-columns: 22px 1fr auto;
            align-items: center;
            gap: 8px;
            padding: 5px 0;
            border-top: 1px solid rgba(255, 255, 255, 0.06);
        }

        .standings-row:first-of-type {
            border-top: 0;
        }

        .standings-rank {
            color: #7f8898;
            font-size: 0.74rem;
            text-align: right;
        }

        .standings-main {
            min-width: 0;
        }

        .standings-name {
            color: #edf2fb;
            font-size: 0.92rem;
            line-height: 1.05;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .standings-bar-shell {
            margin-top: 4px;
            height: 4px;
            border-radius: 999px;
            background: #20283a;
            overflow: hidden;
        }

        .standings-bar {
            height: 100%;
            border-radius: 999px;
            background: #d81f2e;
        }

        .standings-points {
            color: #ff2f3f;
            font-family: 'Press Start 2P', cursive;
            font-size: 0.54rem;
            white-space: nowrap;
            padding-left: 6px;
        }

        [data-testid="stAlert"] {
            border-radius: 4px;
            border: 1px solid var(--line);
            box-shadow: 4px 4px 0 rgba(23, 23, 23, 0.08);
        }

        [data-testid="stSelectbox"] label,
        [data-testid="stMultiSelect"] label {
            color: var(--muted);
            font-family: 'Press Start 2P', cursive !important;
            font-size: 0.72rem;
            text-transform: uppercase;
        }

        div[data-baseweb="select"] > div {
            background-color: #ffffff;
            color: var(--ink);
            border: 2px solid var(--line);
            border-radius: 4px;
            box-shadow: 4px 4px 0 var(--line);
            font-family: 'VT323', monospace;
        }

        header {
            background: transparent !important;
        }

        @media (max-width: 1100px) {
            .summary-strip,
            .panel-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }

            div[class*="st-key-dialog_track_details"] [data-testid="column"]:last-of-type {
                border-left: 0;
                padding-left: 0;
            }
        }

        @media (max-width: 700px) {
            .summary-strip,
            .panel-grid {
                grid-template-columns: 1fr;
            }

            .hero {
                padding: 18px;
            }
        }
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #fbf7ee 0%, #e5dccb 100%);
            border-right: 2px solid var(--ink);
        }

        section[data-testid="stSidebar"] * {
            color: var(--ink);
        }

        .stButton button {
            background-color: var(--red) !important;
            color: #fbf7ee !important;
            border: 3px solid var(--ink) !important;
            font-family: 'Press Start 2P', cursive !important;
            font-size: 0.8rem !important;
            text-transform: uppercase;
            box-shadow: 4px 4px 0 var(--ink) !important;
            border-radius: 0 !important;
            transition: all 0.1s ease-in-out;
        }

        .stButton button:hover {
            transform: translate(2px, 2px);
            box-shadow: 2px 2px 0 var(--ink) !important;
            color: #ffffff !important;
            border-color: var(--ink) !important;
        }
        
        .stButton button:active {
            transform: translate(4px, 4px);
            box-shadow: 0 0 0 var(--ink) !important;
            color: #ffffff !important;
            border-color: var(--ink) !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@contextmanager
def anime_loading_box(message: str = "Loading API data..."):
        placeholder = st.empty()

        loader_html = f"""
        <div class=\"api-loader-shell\" role=\"status\" aria-live=\"polite\"> 
            <div class=\"api-loader-grid\"> 
                <div class=\"square\" style=\"--rotation: 0deg; --scale: 0.88;\"></div>
                <div class=\"square\" style=\"--rotation: 18deg; --scale: 1.03;\"></div>
                <div class=\"square\" style=\"--rotation: 32deg; --scale: 0.96;\"></div>
                <div class=\"square\" style=\"--rotation: -18deg; --scale: 1.06;\"></div>
                <div class=\"square\" style=\"--rotation: -32deg; --scale: 0.92;\"></div>
            </div>
            <p class=\"api-loader-text\">{escape(message)}</p>
        </div>

        <style>
            .api-loader-shell {{
                --hex-orange-1: #f79f45;
                --hex-red-1: #d04b33;
                width: min(560px, 100%);
                margin: 0 auto 12px;
                border: 3px solid #211d18;
                border-radius: 8px;
                background: linear-gradient(180deg, #fbf7ee 0%, #e5dccb 100%);
                box-shadow: 6px 6px 0 #211d18;
                padding: 14px 16px;
                box-sizing: border-box;
            }}

            .api-loader-grid {{
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 8px;
                align-items: center;
            }}

            .square {{
                aspect-ratio: 1 / 1;
                border: 3px solid var(--hex-orange-1);
                background: var(--hex-red-1);
                border-radius: 4px;
                transform-origin: center center;
                will-change: transform, border-color, background-color;
            }}

            .api-loader-text {{
                margin: 10px 0 0;
                font-family: 'Press Start 2P', cursive;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                font-size: 0.72rem;
                color: #211d18;
                text-align: center;
            }}
        </style>

        <script type=\"module\">
            import {{ waapi, animate, stagger }} from 'https://esm.sh/animejs';

            waapi.animate('.square',  {{
                borderColor: ['var(--hex-orange-1)', 'var(--hex-red-1)'],
                ease: 'inOutSine',
                duration: 1200,
                delay: stagger(110),
                loop: true,
                alternate: true,
            }});

            animate('.square',  {{
                rotate: ['0deg', 'var(--rotation)'],
                scale: [1, 'var(--scale)'],
                background: ['var(--hex-red-1)', 'var(--hex-orange-1)'],
                ease: 'inOutSine',
                duration: 1200,
                delay: stagger(110),
                loop: true,
                alternate: true,
            }});
        </script>
        """

        with placeholder.container():
                components.html(loader_html, height=126)

        try:
                yield
        finally:
                placeholder.empty()


def _pick_first_value(row, keys, empty="-"):
    for key in keys:
        value = row.get(key)
        text = str(value).strip() if value is not None else ""
        if text and text.lower() not in {"nan", "none", "nat"}:
            return text
    return empty


def render_timing_table_card(
    dataframe,
    title: str,
    badge: str | None = None,
    time_column: str | None = None,
    limit: int | None = 8,
    extra_columns: list[str] | None = None,
) -> None:
    if dataframe is None or getattr(dataframe, "empty", True):
        st.warning("No timing data available.")
        return

    rows_html = []
    data_slice = dataframe if limit is None else dataframe.head(limit)

    for _, row in data_slice.iterrows():
        position = _pick_first_value(row, ["POS", "position"], "-")
        driver = _pick_first_value(row, ["DRIVER", "TEAM"], "-")
        team = _pick_first_value(row, ["TEAM"], "")
        timing = _pick_first_value(
            row,
            [time_column] if time_column else ["TIME/GAP", "Q3", "Q2", "Q1", "PTS", "FASTEST LAP"],
            "-",
        )
        if time_column is None and timing == "-" and "PTS" in dataframe.columns:
            timing = f"{_pick_first_value(row, ['PTS'], '0')} pts"

        extra_text = ""
        if extra_columns:
            parts = []
            for column in extra_columns:
                if column in dataframe.columns:
                    value = _pick_first_value(row, [column], "-")
                    parts.append(f"{column}: {value}")
            if parts:
                extra_text = f"<div class='timing-extra'>{escape(' | '.join(parts))}</div>"

        rows_html.append(
            "<div class='timing-row'>"
            f"<div class='timing-pos'>P{escape(str(position))}</div>"
            "<div>"
            f"<div class='timing-name'>{escape(driver)}</div>"
            f"<div class='timing-team'>{escape(team)}</div>"
            f"{extra_text}"
            "</div>"
            f"<div class='timing-time'>{escape(timing)}</div>"
            "</div>"
        )

    badge_html = f"<div><span class='timing-label'>{escape(badge)}</span></div>" if badge else ""
    st.markdown(
        "<div class='timing-card'>"
        "<div class='timing-header'>"
        f"{badge_html}"
        f"<div class='timing-title'>{escape(title)}</div>"
        "</div>"
        f"{''.join(rows_html)}"
        "</div>",
        unsafe_allow_html=True,
    )


def render_standings_bar_card(
    dataframe,
    title: str,
    name_column: str,
    points_column: str = "PTS",
    limit: int = 10,
    highlight_top: bool = False,
) -> None:
    if dataframe is None or getattr(dataframe, "empty", True):
        st.warning("Standings unavailable.")
        return

    data_slice = dataframe.head(limit).copy()

    def _safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    max_points = max((_safe_float(v) for v in data_slice.get(points_column, [])), default=0.0) or 1.0

    rows_html = []
    for _, row in data_slice.iterrows():
        rank = _pick_first_value(row, ["POS", "position"], "-")
        name = _pick_first_value(row, [name_column], "-")
        points = _safe_float(row.get(points_column, 0))
        width_pct = max(0.0, min(100.0, (points / max_points) * 100.0))
        bar_color = "#f1f1f1" if highlight_top and str(rank) == "1" else "#d81f2e"

        rows_html.append(
            "<div class='standings-row'>"
            f"<div class='standings-rank'>{escape(str(rank))}</div>"
            "<div class='standings-main'>"
            f"<div class='standings-name'>{escape(name)}</div>"
            "<div class='standings-bar-shell'>"
            f"<div class='standings-bar' style='width:{width_pct:.2f}%; background:{bar_color};'></div>"
            "</div>"
            "</div>"
            f"<div class='standings-points'>{int(points) if points.is_integer() else f'{points:.1f}'} pts</div>"
            "</div>"
        )

    st.markdown(
        "<div class='standings-card'>"
        f"<div class='standings-title'>{escape(title)}</div>"
        f"{''.join(rows_html)}"
        "</div>",
        unsafe_allow_html=True,
    )


def render_top_podium_card(
    dataframe,
    title: str,
    subtitle: str = "",
    badge: str = "LAST RACE",
    time_column: str | None = None,
) -> None:
    if dataframe is None or getattr(dataframe, "empty", True):
        return

    top_three = dataframe.head(3)
    cells = []

    for _, row in top_three.iterrows():
        position = _pick_first_value(row, ["POS", "position"], "-")
        driver = _pick_first_value(row, ["DRIVER", "TEAM"], "-")
        team = _pick_first_value(row, ["TEAM"], "")
        timing = _pick_first_value(
            row,
            [time_column] if time_column else ["TIME/GAP", "Q3", "Q2", "Q1", "PTS", "FASTEST LAP"],
            "-",
        )
        if time_column is None and timing == "-" and "PTS" in dataframe.columns:
            timing = f"{_pick_first_value(row, ['PTS'], '0')} pts"

        pos_class = "podium-pos podium-pos-leader" if str(position) == "1" else "podium-pos"
        cells.append(
            "<div class='podium-cell'>"
            f"<div class='{pos_class}'>P{escape(str(position))}</div>"
            f"<div class='podium-name'>{escape(driver)}</div>"
            f"<div class='podium-team'>{escape(team)}</div>"
            f"<div class='podium-time'>{escape(timing)}</div>"
            "</div>"
        )

    subtitle_html = f"<div class='podium-subtitle'>{escape(subtitle)}</div>" if subtitle else ""
    html = (
        "<div class='podium-card'>"
        "<div class='podium-header'>"
        f"<span class='podium-badge'>{escape(badge)}</span>"
        f"<span class='podium-title'>{escape(title)}</span>"
        "</div>"
        f"{subtitle_html}"
        "<div class='podium-grid'>"
        f"{''.join(cells)}"
        "</div>"
        "</div>"
        "<style>"
        ".podium-card{border:1px solid rgba(255,255,255,.12);border-radius:10px;background:linear-gradient(180deg,#14161d 0%,#0f1118 100%);box-shadow:0 14px 40px rgba(0,0,0,.34);padding:12px 14px;margin:8px 0 12px;}"
        ".podium-header{display:flex;align-items:center;gap:10px;margin-bottom:4px;}"
        ".podium-badge{background:#ff2f21;color:#fff;border-radius:4px;padding:3px 8px;font-size:.62rem;font-weight:900;letter-spacing:.08em;line-height:1;}"
        ".podium-title{color:#f5f7fb;font-family:'Press Start 2P',cursive;font-size:.7rem;letter-spacing:.04em;}"
        ".podium-subtitle{color:#97a3b6;font-size:.78rem;margin-bottom:8px;}"
        ".podium-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;}"
        ".podium-cell{border:1px solid rgba(255,255,255,.07);border-radius:8px;background:rgba(255,255,255,.02);padding:8px 10px;}"
        ".podium-pos{font-family:'Press Start 2P',cursive;font-size:.85rem;color:#f5f7fb;margin-bottom:5px;}"
        ".podium-pos-leader{color:#ff2f21;}"
        ".podium-name{color:#f5f7fb;font-size:.98rem;line-height:1.12;}"
        ".podium-team{color:#93a0b3;font-size:.8rem;line-height:1.12;margin-top:2px;}"
        ".podium-time{color:#bcc5d6;font-size:.78rem;line-height:1.2;margin-top:6px;font-variant-numeric:tabular-nums;}"
        "@media(max-width:900px){.podium-grid{grid-template-columns:1fr;}}"
        "</style>"
    )
    st.markdown(html, unsafe_allow_html=True)
