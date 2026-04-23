from __future__ import annotations

import streamlit as st


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
