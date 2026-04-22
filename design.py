import streamlit as st


def inject_retro_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');

        :root {
            --paper: #ffffff;
            --ink: #171717;
            --muted: #6b4b3b;
            --line: #171717;
            --pink: #f06a8a;
            --cyan: #37b4c8;
            --peach: #ffd8c2;
            --peach-light: #fff0e7;
            --peach-deep: #f4a77d;
        }

        .stApp {
            background: var(--paper);
            color: var(--ink);
            font-family: 'VT323', monospace;
            font-size: 22px;
        }

        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            font-family: 'Press Start 2P', cursive !important;
            color: var(--ink) !important;
            text-shadow: 3px 3px 0 var(--cyan);
            text-transform: uppercase;
            margin-bottom: 1rem;
        }

        p, li, label, .stMarkdown, .stText {
            font-family: 'VT323', monospace !important;
            color: var(--ink);
        }

        p, li {
            font-size: 24px !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"],
        div[class*="st-key-dialog_"] {
            border: 3px solid var(--line);
            border-radius: 6px;
            background: linear-gradient(180deg, var(--peach-light) 0%, var(--peach) 100%);
            box-shadow: 8px 8px 0 var(--peach-deep);
            margin: 0 0 34px;
            padding: 18px;
            position: relative;
        }

        div[class*="st-key-dialog_header"] {
            padding: 28px 24px 22px;
        }

        div[class*="st-key-dialog_header"] h1 {
            margin-top: 0;
        }

        div[data-testid="stDataFrame"] {
            border: 2px solid var(--line);
            border-radius: 4px;
            box-shadow: 5px 5px 0 var(--pink);
            background-color: #ffffff;
        }

        div[data-baseweb="select"] > div {
            background-color: #ffffff;
            color: var(--ink);
            border: 2px solid var(--line);
            border-radius: 4px;
            box-shadow: 4px 4px 0 var(--cyan);
            font-family: 'VT323', monospace;
        }

        div[data-testid="stSelectbox"] label {
            color: var(--muted);
            font-family: 'Press Start 2P', cursive !important;
            font-size: 0.72rem;
            text-transform: uppercase;
        }

        div[class*="st-key-dialog_stage_stats"] [data-testid="column"] {
            border: 2px solid var(--line);
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.42);
            box-shadow: 4px 4px 0 var(--cyan);
            padding: 10px 12px;
        }

        div[class*="st-key-track_archive_panel"],
        div[class*="st-key-circuit_map_panel"] {
            border: 2px solid var(--line);
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.36);
            box-shadow: 5px 5px 0 var(--cyan);
            padding: 14px;
        }

        div[class*="st-key-circuit_map_panel"] [data-testid="stImage"],
        div[class*="st-key-circuit_map_panel"] [data-testid="stPyplot"] {
            border: 2px solid var(--line);
            border-radius: 4px;
            background: var(--peach-light);
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
            background: var(--peach-light);
            box-shadow: 4px 4px 0 var(--pink);
            list-style-position: inside;
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
            border: 3px solid var(--line);
            border-radius: 6px;
            background: linear-gradient(180deg, var(--peach-light) 0%, var(--peach) 100%);
            box-shadow: 6px 6px 0 var(--cyan);
            min-height: 164px;
            padding: 16px;
            position: relative;
        }

        .practice-title {
            font-family: 'Press Start 2P', cursive;
            font-size: 1rem;
            margin: 0 0 12px;
            text-shadow: 2px 2px 0 var(--cyan);
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

        header {
            background: transparent !important;
        }

        @media (max-width: 1100px) {
            div[class*="st-key-dialog_track_details"] [data-testid="column"]:last-of-type {
                border-left: 0;
                padding-left: 0;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
