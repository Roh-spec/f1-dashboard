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

        div[data-testid="stVerticalBlockBorderWrapper"] {
            border: 3px solid var(--line);
            border-radius: 6px;
            background: linear-gradient(180deg, var(--peach-light) 0%, var(--peach) 100%);
            box-shadow: 8px 8px 0 var(--peach-deep);
            margin-bottom: 26px;
            padding: 18px;
            position: relative;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]::after {
            content: "";
            position: absolute;
            left: 28px;
            bottom: -15px;
            width: 22px;
            height: 22px;
            background: var(--peach);
            border-right: 3px solid var(--line);
            border-bottom: 3px solid var(--line);
            transform: rotate(45deg);
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
            font-family: 'VT323', monospace;
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

        .practice-card::after {
            content: "";
            position: absolute;
            left: 20px;
            bottom: -12px;
            width: 16px;
            height: 16px;
            background: var(--peach);
            border-right: 3px solid var(--line);
            border-bottom: 3px solid var(--line);
            transform: rotate(45deg);
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
        </style>
        """,
        unsafe_allow_html=True,
    )
