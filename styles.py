from __future__ import annotations

import streamlit as st


def inject_retro_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;500;700&display=swap');

        :root {
            --paper: #f4efe4;
            --paper-deep: #e5dccb;
            --ink: #211d18;
            --muted: #6f675b;
            --line: #c8bca9;
            --panel: rgba(255, 250, 239, 0.86);
            --red: #9d2b22;
            --green: #2f5f4a;
            --ochre: #a87424;
        }

        .stApp {
            color: var(--ink);
            background:
                linear-gradient(rgba(33, 29, 24, 0.025) 1px, transparent 1px),
                linear-gradient(90deg, rgba(33, 29, 24, 0.025) 1px, transparent 1px),
                radial-gradient(circle at 18% 8%, rgba(157, 43, 34, 0.10), transparent 28%),
                radial-gradient(circle at 82% 12%, rgba(47, 95, 74, 0.10), transparent 24%),
                linear-gradient(135deg, #fbf7ee 0%, #efe6d5 52%, #f7f1e7 100%);
            background-size: 22px 22px, 22px 22px, auto, auto, auto;
            font-family: "IBM Plex Mono", monospace;
        }

        .stApp::before {
            content: "";
            pointer-events: none;
            position: fixed;
            inset: 0;
            z-index: 1000;
            background:
                repeating-linear-gradient(
                    to bottom,
                    rgba(48, 39, 28, 0.035) 0,
                    rgba(48, 39, 28, 0.035) 1px,
                    transparent 1px,
                    transparent 5px
                );
            mix-blend-mode: multiply;
        }

        h1, h2, h3, [data-testid="stMetricValue"] {
            color: var(--ink);
            font-family: "Bebas Neue", sans-serif;
            letter-spacing: 0.07em;
        }

        .hero {
            border: 2px solid var(--ink);
            border-radius: 4px;
            padding: 28px;
            margin-bottom: 20px;
            background:
                linear-gradient(135deg, rgba(255,255,255,0.36), rgba(228,216,195,0.32)),
                var(--panel);
            box-shadow: 8px 8px 0 rgba(33, 29, 24, 0.12);
        }

        .eyebrow {
            margin: 0 0 8px;
            color: var(--red);
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.22em;
        }

        .hero-title {
            color: var(--ink);
            font-family: "Bebas Neue", sans-serif;
            font-size: clamp(2.8rem, 7vw, 6.6rem);
            line-height: 0.86;
            margin: 0;
            text-shadow: 3px 3px 0 rgba(157, 43, 34, 0.18);
        }

        .hero-subtitle {
            color: var(--muted);
            margin-top: 12px;
            max-width: 900px;
        }

        .badge-row {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-top: 18px;
        }

        .badge {
            border: 1px solid var(--ink);
            border-radius: 3px;
            padding: 8px 12px;
            background: #fffaf0;
            color: var(--ink);
            font-size: 0.82rem;
            box-shadow: 3px 3px 0 rgba(33, 29, 24, 0.10);
        }

        [data-testid="stMetric"] {
            border: 1px solid var(--line);
            border-radius: 4px;
            padding: 18px;
            background: rgba(255, 250, 239, 0.86);
            box-shadow: 5px 5px 0 rgba(33, 29, 24, 0.08);
        }

        [data-testid="stMetricLabel"],
        [data-testid="stMetricDelta"] {
            color: var(--muted);
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f6efe2 0%, #e6dccb 100%);
            border-right: 2px solid var(--ink);
        }

        section[data-testid="stSidebar"] * {
            color: var(--ink);
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 4px;
            overflow: hidden;
            box-shadow: 5px 5px 0 rgba(33, 29, 24, 0.08);
        }

        .status-card {
            border: 1px solid var(--line);
            border-radius: 4px;
            padding: 18px;
            background: rgba(255, 250, 239, 0.86);
            min-height: 152px;
            box-shadow: 5px 5px 0 rgba(33, 29, 24, 0.08);
        }

        .status-label {
            color: var(--red);
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.14em;
        }

        .status-value {
            color: var(--green);
            font-family: "Bebas Neue", sans-serif;
            font-size: 2rem;
            letter-spacing: 0.05em;
            margin-top: 6px;
        }

        .dashboard-section {
            margin-top: 22px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
