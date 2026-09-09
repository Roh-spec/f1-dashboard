from __future__ import annotations

from contextlib import contextmanager
from html import escape

import streamlit as st


def inject_retro_css() -> None:
    """Injects sleek modern Formula 1 telemetry styling (Circuit Slate aesthetic)."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Titillium+Web:ital,wght@0,400;0,600;0,700;0,900;1,700&family=JetBrains+Mono:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=Inter:wght@400;500;600;700&display=swap');

        :root {
            --bg-page: #0d1117;
            --bg-card: #161b22;
            --bg-card-hover: #1c212a;
            --bg-card-elevated: #1c212a;
            --border-card: #262c36;
            --border-card-hover: #374151;
            --border-subtle: rgba(255, 255, 255, 0.06);

            --accent-red: #e10600;
            --accent-red-hover: #ff1e16;
            --accent-red-tint: rgba(225, 6, 0, 0.18);
            --accent-red-border: rgba(225, 6, 0, 0.45);

            --accent-amber: #f5a623;
            --accent-amber-tint: rgba(245, 166, 35, 0.15);

            --accent-teal: #e10600;
            --accent-teal-hover: #ff1e16;
            --accent-teal-tint: rgba(225, 6, 0, 0.18);
            --accent-teal-border: rgba(225, 6, 0, 0.45);

            --text-heading: #f0f3f6;
            --text-body: #c9d1d9;
            --text-muted: #8b949e;

            --radius-card: 0px;
            --radius-pill: 9999px;
            --radius-button: 0px;
            --left-bar-width: 3px;
        }

        html, body {
            scroll-behavior: smooth !important;
        }

        /* CRITICAL: Eliminate Streamlit top padding and header completely */
        header[data-testid="stHeader"],
        header {
            display: none !important;
            height: 0px !important;
            min-height: 0px !important;
            padding: 0px !important;
            margin: 0px !important;
            visibility: hidden !important;
        }

        [data-testid="stToolbar"] {
            display: none !important;
        }

        [data-testid="stAppViewContainer"] {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }

        [data-testid="stMainBlockContainer"],
        .main .block-container,
        .stMain .block-container,
        div[data-testid="stMainBlockContainer"],
        section[data-testid="stMain"] > div {
            padding-top: 0px !important;
            padding-left: 24px !important;
            padding-right: 24px !important;
            padding-bottom: 3.5rem !important;
            margin-top: 0px !important;
            max-width: 1560px !important;
        }

        /* Global application background: Circuit Slate (#0d1117) */
        .stApp {
            background-color: var(--bg-page) !important;
            background: var(--bg-page) !important;
            color: var(--text-body);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 14.5px;
        }

        /* F1 Broadcast Timing-Tower Typography */
        h1, h2, h3, h4 {
            font-family: 'Titillium Web', -apple-system, BlinkMacSystemFont, sans-serif !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.04em !important;
            color: var(--text-heading) !important;
            margin: 0 0 0.5rem 0 !important;
        }

        h1 {
            font-size: clamp(1.8rem, 3.2vw, 2.6rem) !important;
            font-weight: 900 !important;
            letter-spacing: 0.01em !important;
            line-height: 1.1;
        }

        h2 {
            font-size: clamp(1.2rem, 2vw, 1.6rem) !important;
            font-weight: 700 !important;
            color: var(--text-heading) !important;
        }

        h3 {
            font-size: clamp(1rem, 1.4vw, 1.3rem) !important;
            color: var(--text-heading) !important;
        }

        /* Tabular Monospace for Numbers, Timestamps, and Metrics */
        .mono-num,
        .stat-mono,
        .timing-mono,
        code {
            font-family: 'JetBrains Mono', monospace !important;
            font-variant-numeric: tabular-nums !important;
        }

        p, li, label, .stMarkdown {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            font-size: 14.5px !important;
            line-height: 1.55;
            color: var(--text-body);
        }

        a {
            color: var(--accent-teal) !important;
            text-decoration: none;
            transition: color 0.15s ease;
        }
        a:hover {
            color: var(--accent-teal-hover) !important;
        }

        /* Top Navigation Bar: Sticky, Flush, Timing-Tower Base Strip, Sharp Edges */
        div[data-testid="stHorizontalBlock"]:has(.topbar-brand) {
            position: sticky !important;
            top: 0px !important;
            z-index: 999999 !important;
            background: #10141a !important;
            background-color: #10141a !important;
            border-bottom: 2px solid #21262d !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6) !important;
            border-radius: 0px !important;
            padding: 8px 24px !important;
            margin-top: 0px !important;
            margin-bottom: 24px !important;
            align-items: center !important;
        }

        .topbar-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 2px 0;
            user-select: none;
        }

        .f1-badge {
            background: var(--accent-red);
            color: #ffffff !important;
            font-family: 'Titillium Web', sans-serif !important;
            font-weight: 900 !important;
            font-style: italic;
            font-size: 1.15rem !important;
            letter-spacing: -0.02em;
            padding: 3px 9px 3px 8px;
            border-radius: 0px;
            clip-path: polygon(0 0, 100% 0, 86% 100%, 0% 100%);
            display: inline-block;
            line-height: 1;
        }

        .brand-text {
            display: flex;
            flex-direction: column;
            line-height: 1.1;
        }

        .brand-title {
            font-family: 'Titillium Web', sans-serif !important;
            font-weight: 900 !important;
            font-size: 1.05rem !important;
            color: var(--text-heading) !important;
            letter-spacing: 0.10em;
            text-transform: uppercase;
        }

        .brand-sub {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.65rem !important;
            color: var(--text-muted) !important;
            letter-spacing: 0.14em;
        }

        /* Sector-line active underline & hover for nav */
        div[data-testid="stHorizontalBlock"]:has(.topbar-brand) ul.nav {
            justify-content: flex-end !important;
            gap: 6px !important;
            align-items: stretch !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.topbar-brand) ul.nav li.nav-item {
            flex: 0 0 auto !important;
            margin: 0px !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.topbar-brand) ul.nav li.nav-item a.nav-link {
            font-family: 'Titillium Web', sans-serif !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
            border-radius: 0px !important;
            border: none !important;
            border-bottom: 3px solid transparent !important;
            background: transparent !important;
            padding: 10px 16px 8px 16px !important;
            transition: all 0.15s ease !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.topbar-brand) ul.nav li.nav-item a.nav-link:hover {
            color: #f0f3f6 !important;
            border-bottom: 3px solid rgba(225, 6, 0, 0.45) !important;
            background: rgba(255, 255, 255, 0.02) !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.topbar-brand) ul.nav li.nav-item a.nav-link.active,
        div[data-testid="stHorizontalBlock"]:has(.topbar-brand) ul.nav li.nav-item a.nav-link-selected {
            color: #ffffff !important;
            font-weight: 700 !important;
            border-radius: 0px !important;
            border: none !important;
            border-bottom: 3px solid var(--accent-red) !important;
            background: rgba(225, 6, 0, 0.06) !important;
            box-shadow: none !important;
        }

        /* Section Headings: Standardized left accent bars */
        .section-header-red {
            border-left: var(--left-bar-width) solid var(--accent-red);
            padding-left: 14px;
            margin-bottom: 14px;
        }

        .section-header-teal {
            border-left: var(--left-bar-width) solid var(--accent-red);
            padding-left: 14px;
            margin-bottom: 14px;
        }

        .section-header {
            border-left: var(--left-bar-width) solid var(--accent-red);
            padding-left: 14px;
            margin-bottom: 14px;
        }

        .section-eyebrow,
        .hero-eyebrow {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.70rem !important;
            font-weight: 700 !important;
            color: var(--text-muted) !important;
            letter-spacing: 0.14em !important;
            text-transform: uppercase !important;
            margin: 0 0 4px 0 !important;
            line-height: 1 !important;
            display: flex;
            align-items: center;
        }

        .section-title {
            font-family: 'Titillium Web', sans-serif !important;
            font-size: 1.5rem !important;
            font-weight: 800 !important;
            color: var(--text-heading) !important;
            letter-spacing: 0.04em !important;
            text-transform: uppercase !important;
            margin: 0 !important;
            line-height: 1.2 !important;
        }

        .section-description {
            color: var(--text-muted) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 14px !important;
            line-height: 1.6 !important;
            margin: 0 0 20px 0 !important;
        }

        /* Live Pulsing Dot (strictly used for live signals like Paddock Feed) */
        .live-dot-pulse {
            width: 7px;
            height: 7px;
            background-color: var(--accent-red);
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
            box-shadow: 0 0 8px var(--accent-red);
            animation: live-pulse 2s infinite ease-in-out;
            vertical-align: middle;
        }

        @keyframes live-pulse {
            0% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.35; transform: scale(0.85); }
            100% { opacity: 1; transform: scale(1); }
        }

        /* Hero Section: Full-bleed broadcast presentation, NO card border or background box */
        .hero-bleed {
            position: relative;
            padding: 8px 0 26px 0;
            margin-bottom: 28px;
            border-bottom: 1px solid #21262d;
            background: radial-gradient(circle at 85% 20%, rgba(225, 6, 0, 0.04) 0%, transparent 60%);
        }

        .hero-kicker {
            display: flex;
            align-items: center;
            gap: 8px;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.70rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.16em !important;
            text-transform: uppercase !important;
            color: var(--text-muted);
            margin-bottom: 8px;
        }

        .kicker-lead {
            color: var(--accent-red);
            font-weight: 700;
        }

        .kicker-sep {
            color: #374151;
        }

        .kicker-sub {
            color: var(--text-muted);
        }

        .hero-display-title {
            font-family: 'Titillium Web', sans-serif !important;
            font-weight: 900 !important;
            font-size: clamp(2.2rem, 3.6vw, 3.1rem) !important;
            letter-spacing: 0.01em !important;
            line-height: 1.05 !important;
            color: var(--text-heading) !important;
            text-transform: uppercase !important;
            margin: 0 0 12px 0 !important;
        }

        .hero-title-dim {
            color: #4b5563;
            font-weight: 400;
            margin: 0 4px;
        }

        .hero-dek {
            color: var(--text-muted) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 14.5px !important;
            line-height: 1.6 !important;
            max-width: 66ch !important;
            margin: 0 0 22px 0 !important;
        }

        /* Timing-Tower Category Tags (replacing dot+pill badges) */
        .timing-tags-strip {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
        }

        .timing-tag {
            display: inline-flex;
            align-items: stretch;
            border-radius: 0px !important;
            border: 1px solid var(--border-card);
            border-left: 2px solid var(--accent-red);
            background: #14181f;
            transition: all 0.16s ease;
            cursor: default;
        }

        .timing-tag:hover {
            border-left-color: var(--accent-red-hover);
            border-color: #374151;
            background: #1a202a;
            transform: translateY(-1px);
        }

        .tag-code {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            font-weight: 700;
            color: var(--accent-red);
            background: rgba(225, 6, 0, 0.12);
            padding: 4px 7px;
            border-right: 1px solid var(--border-card);
            letter-spacing: 0.06em;
            display: flex;
            align-items: center;
        }

        .tag-label {
            font-family: 'Titillium Web', sans-serif;
            font-size: 0.74rem;
            font-weight: 700;
            color: var(--text-body);
            padding: 4px 12px;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            display: flex;
            align-items: center;
        }

        .section-kicker {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            font-weight: 800;
            color: var(--accent-red) !important;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            margin-bottom: 3px;
        }

        .section-ribbon {
            display: flex;
            flex-wrap: wrap;
            gap: 14px;
            padding: 7px 14px;
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-left: 3px solid var(--accent-red) !important;
            border-radius: 0px;
            margin: 10px 0 16px;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 600;
            font-size: 0.82rem;
            color: var(--text-body);
            letter-spacing: 0.06em;
        }

        /* Summary Cards */
        .summary-strip {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
            margin: 12px 0 16px;
        }

        .summary-card {
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-top: 2px solid var(--accent-red) !important;
            border-radius: 0px;
            padding: 14px 16px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
            transition: transform 0.15s ease, border-color 0.15s ease;
        }

        .summary-card:hover {
            transform: translateY(-2px);
            border-color: var(--border-card-hover);
        }

        .summary-label {
            font-family: 'Titillium Web', sans-serif;
            font-size: 0.76rem;
            font-weight: 700;
            color: var(--accent-red) !important;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 4px;
        }

        .summary-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--text-heading);
            margin-bottom: 3px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .summary-note {
            font-family: 'Inter', sans-serif;
            font-size: 13px !important;
            color: var(--text-muted) !important;
            margin: 0;
        }

        /* Circuit Records 3-card Grid */
        .circuit-records-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
            margin-top: 10px;
            margin-bottom: 8px;
        }

        .record-card {
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-top: 2px solid var(--accent-red) !important;
            border-radius: 0px;
            padding: 12px 14px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
        }

        .record-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 6px;
            margin-bottom: 6px;
        }

        .record-label {
            font-family: 'Titillium Web', sans-serif;
            font-weight: 700;
            font-size: 0.74rem;
            color: var(--accent-red) !important;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .record-subtag {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.64rem;
            font-weight: 700;
            color: var(--accent-amber);
            background: rgba(245, 166, 35, 0.1);
            border: 1px solid rgba(245, 166, 35, 0.3);
            border-radius: 0px;
            padding: 1px 5px;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            white-space: nowrap;
        }

        .record-value {
            font-family: 'Titillium Web', sans-serif;
            font-weight: 700;
            font-size: 1.05rem;
            color: var(--text-heading);
            line-height: 1.25;
        }

        .record-timing {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.92rem;
            color: #f0f3f6;
        }

        /* Practice Cards */
        .practice-card {
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-top: 2px solid var(--accent-red);
            border-radius: 0px;
            padding: 14px 16px;
            margin-bottom: 12px;
        }

        .practice-title {
            font-family: 'Titillium Web', sans-serif;
            font-weight: 700;
            font-size: 1rem;
            color: var(--text-heading);
            letter-spacing: 0.04em;
            margin-bottom: 6px;
        }

        .practice-stat {
            font-family: 'Inter', sans-serif;
            font-size: 14px !important;
            color: var(--text-body);
            margin: 4px 0;
        }

        .practice-label {
            color: var(--accent-red);
            font-weight: 600;
            margin-right: 6px;
        }

        /* Metric readouts */
        div[data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace !important;
            color: var(--text-heading) !important;
            font-size: 1.45rem !important;
            font-weight: 700 !important;
        }
        div[data-testid="stMetricLabel"] {
            font-family: 'Titillium Web', sans-serif !important;
            color: var(--text-muted) !important;
            font-size: 0.82rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
        }

        /* BaseWeb Selectbox Overrides: sleek motorsport telemetry style */
        div[data-baseweb="select"] {
            margin-top: 4px !important;
        }

        div[data-baseweb="select"] > div {
            background-color: #12161e !important;
            border: 1px solid var(--border-card) !important;
            border-radius: 0px !important;
            color: var(--text-heading) !important;
            padding: 4px 8px !important;
            min-height: 44px !important;
            transition: all 0.15s ease !important;
        }

        div[data-baseweb="select"] > div:hover {
            border-color: var(--border-card-hover) !important;
        }

        div[data-baseweb="select"] > div:focus-within {
            border-color: var(--accent-red) !important;
            box-shadow: 0 0 0 2px var(--accent-red-tint) !important;
        }

        div[data-baseweb="select"] span {
            color: var(--text-heading) !important;
            font-family: 'Titillium Web', sans-serif !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.03em !important;
        }

        div[data-baseweb="popover"],
        div[data-baseweb="menu"],
        ul[role="listbox"] {
            background-color: var(--bg-card) !important;
            border: 1px solid var(--border-card) !important;
            border-radius: 6px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.7) !important;
        }

        li[role="option"] {
            color: var(--text-body) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 14px !important;
            padding: 8px 14px !important;
            transition: background 0.15s ease !important;
        }

        li[role="option"]:hover,
        li[aria-selected="true"] {
            background-color: var(--accent-red-tint) !important;
            color: #ffffff !important;
        }

        div[data-testid="stWidgetLabel"] label,
        div[data-testid="stWidgetLabel"] p {
            font-family: 'Titillium Web', sans-serif !important;
            font-size: 0.80rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.12em !important;
            text-transform: uppercase !important;
            color: var(--text-muted) !important;
            margin-bottom: 6px !important;
        }

        /* PRIMARY CTA BUTTON: Angular-clipped telemetry button, bold Titillium Web, racing red gradient */
        button[data-testid="baseButton-primary"],
        .stButton > button[kind="primary"],
        .stButton > button[data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, var(--accent-red) 0%, #b30500 100%) !important;
            color: #ffffff !important;
            border: 1px solid #ff3b30 !important;
            border-radius: 0px !important;
            clip-path: polygon(0 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%) !important;
            font-family: 'Titillium Web', sans-serif !important;
            font-size: 0.96rem !important;
            font-weight: 800 !important;
            letter-spacing: 0.10em !important;
            text-transform: uppercase !important;
            padding: 13px 26px !important;
            min-height: 48px !important;
            height: 48px !important;
            line-height: 1 !important;
            box-shadow: 0 4px 20px rgba(225, 6, 0, 0.45) !important;
            transition: all 0.16s ease !important;
            cursor: pointer !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 8px !important;
            width: 100% !important;
        }

        button[data-testid="baseButton-primary"]:hover,
        .stButton > button[kind="primary"]:hover,
        .stButton > button[data-testid="baseButton-primary"]:hover {
            background: linear-gradient(135deg, var(--accent-red-hover) 0%, #c40600 100%) !important;
            border-color: #ff7870 !important;
            box-shadow: 0 6px 28px rgba(225, 6, 0, 0.65) !important;
            transform: translateY(-2px) !important;
            filter: brightness(1.08) !important;
        }

        /* SECONDARY BUTTONS: Angular-clipped telemetry outline buttons */
        button[data-testid="baseButton-secondary"],
        .stButton > button[kind="secondary"],
        .stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]) {
            background: #181d27 !important;
            color: var(--text-muted) !important;
            border: 1px solid #2e3646 !important;
            border-radius: 0px !important;
            clip-path: polygon(0 0, 100% 0, 100% calc(100% - 10px), calc(100% - 10px) 100%, 0 100%) !important;
            font-family: 'Titillium Web', sans-serif !important;
            font-size: 0.88rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
            padding: 13px 20px !important;
            min-height: 48px !important;
            height: 48px !important;
            line-height: 1 !important;
            box-shadow: none !important;
            transition: all 0.16s ease !important;
            cursor: pointer !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
        }

        button[data-testid="baseButton-secondary"]:hover,
        .stButton > button[kind="secondary"]:hover,
        .stButton > button:not([kind="primary"]):not([data-testid="baseButton-primary"]):hover {
            background: #222938 !important;
            color: #ffffff !important;
            border-color: var(--accent-teal) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4) !important;
        }

        /* Streamlit Tabs */
        button[data-baseweb="tab"] {
            font-family: 'Titillium Web', sans-serif !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            letter-spacing: 0.06em !important;
            text-transform: uppercase !important;
            color: var(--text-muted) !important;
            padding: 8px 16px !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: var(--text-heading) !important;
            border-bottom: 2px solid var(--accent-red) !important;
        }

        /* General Card Containers */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--bg-card) !important;
            border: 1px solid var(--border-card) !important;
            border-radius: 0px !important;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.4) !important;
            margin-bottom: 30px !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] > div {
            padding: 24px 28px !important;
        }

        /* ARCHIVE SELECTOR: Control Panel Treatment (distinct contrast, sharp chamfered panel) */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.st-key-cell_select_year),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.ctrl-panel-header) {
            background: #12161f !important;
            border: 1px solid #2c3444 !important;
            border-radius: 0px !important;
            clip-path: polygon(0 0, 100% 0, 100% calc(100% - 14px), calc(100% - 14px) 100%, 0 100%) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6) !important;
        }

        .ctrl-panel-header {
            margin-bottom: 18px;
        }

        .ctrl-panel-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 6px;
        }

        .ctrl-code {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            font-weight: 700;
            color: var(--accent-red);
            background: rgba(225, 6, 0, 0.12);
            padding: 2px 7px;
            border: 1px solid rgba(225, 6, 0, 0.35);
            letter-spacing: 0.1em;
        }

        .ctrl-type {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            font-weight: 600;
            color: var(--text-muted);
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }

        .ctrl-panel-title {
            font-family: 'Titillium Web', sans-serif !important;
            font-size: 1.45rem !important;
            font-weight: 900 !important;
            color: var(--text-heading) !important;
            letter-spacing: 0.05em !important;
            text-transform: uppercase !important;
            margin: 4px 0 6px 0 !important;
            line-height: 1.15 !important;
        }

        .ctrl-panel-desc {
            font-family: 'Inter', sans-serif !important;
            font-size: 14px !important;
            color: var(--text-muted) !important;
            margin: 0 0 18px 0 !important;
            line-height: 1.55 !important;
        }

        /* Distinct elevated card cells for Archive Select inputs */
        .st-key-cell_select_year,
        .st-key-cell_select_round,
        div[class*="st-key-cell_select"] {
            background: #171c26 !important;
            border: 1px solid #2b3342 !important;
            border-radius: 0px !important;
            padding: 14px 18px !important;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
        }

        /* MOTORSPORT HEADLINES SECTION: Timing-Tower Results Strip & Table Rows */
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.feed-header-strip),
        div[data-testid="stVerticalBlockBorderWrapper"]:has(.feed-row) {
            background: #10141a !important;
            border: 1px solid #232a36 !important;
            border-radius: 0px !important;
            padding: 0px !important;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.5) !important;
            overflow: hidden !important;
        }

        div[data-testid="stVerticalBlockBorderWrapper"]:has(.feed-header-strip) > div {
            padding: 0px !important;
        }

        .feed-header-strip {
            background: linear-gradient(90deg, #181d26 0%, #10141a 100%);
            border-top: 2px solid var(--accent-red);
            border-bottom: 1px solid #232a36;
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .feed-strip-left {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .feed-strip-kicker {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.70rem;
            font-weight: 700;
            color: var(--accent-red);
            letter-spacing: 0.12em;
            text-transform: uppercase;
        }

        .feed-strip-divider {
            color: #374151;
            font-family: 'JetBrains Mono', monospace;
        }

        .feed-strip-title {
            font-family: 'Titillium Web', sans-serif !important;
            font-size: 1.05rem !important;
            font-weight: 800 !important;
            color: var(--text-heading) !important;
            letter-spacing: 0.08em !important;
            text-transform: uppercase !important;
            margin: 0 !important;
        }

        .feed-strip-right {
            display: flex;
            align-items: center;
        }

        .feed-strip-status {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.65rem;
            color: var(--accent-teal);
            letter-spacing: 0.14em;
        }

        /* Headline table rows (replacing card-in-card boxes) */
        .feed-row-group {
            border-bottom: 1px solid #1c222e;
        }

        .feed-row-group:last-child {
            border-bottom: none;
        }

        .feed-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 16px;
            padding: 13px 20px;
            text-decoration: none !important;
            border-left-width: 3px;
            border-left-style: solid;
            background: transparent;
            transition: all 0.14s ease;
        }

        .feed-row:hover {
            background: #161b24 !important;
            border-left-color: var(--accent-teal) !important;
        }

        .feed-row-main {
            display: flex;
            align-items: center;
            flex: 1;
            padding-right: 14px;
        }

        .feed-row-title {
            color: var(--text-heading) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            line-height: 1.45 !important;
            text-decoration: none !important;
            transition: color 0.14s ease;
        }

        .feed-row:hover .feed-row-title {
            color: #ffffff !important;
            text-decoration: none !important;
        }

        .feed-row-meta {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-shrink: 0;
        }

        .feed-meta-source {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.70rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .feed-meta-sep {
            color: #374151;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
        }

        .feed-meta-time {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.70rem;
            color: var(--text-muted);
            letter-spacing: 0.04em;
        }

        /* Expandable "+N MORE SOURCES" */
        .feed-sources-details {
            padding: 0 20px 10px 20px;
            background: rgba(16, 20, 26, 0.5);
        }

        .feed-sources-summary {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.70rem;
            font-weight: 700;
            color: var(--accent-teal);
            cursor: pointer;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            user-select: none;
            padding: 4px 8px;
            border-radius: 0px;
            display: inline-block;
            transition: all 0.14s ease;
        }

        .feed-sources-summary:hover {
            color: #ffffff;
            background: rgba(225, 6, 0, 0.15);
        }

        .feed-sources-list {
            margin-top: 6px;
            display: flex;
            flex-direction: column;
            gap: 4px;
            padding-left: 10px;
            border-left: 2px solid #232a36;
        }

        .feed-sub-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            padding: 8px 12px;
            text-decoration: none !important;
            background: #141822;
            border-left-width: 2px;
            border-left-style: solid;
            transition: all 0.14s ease;
        }

        .feed-sub-row:hover {
            background: #1b212f !important;
            border-left-color: var(--accent-teal) !important;
        }

        .feed-sub-title {
            color: var(--text-body) !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 13px !important;
            font-weight: 400 !important;
            text-decoration: none !important;
        }

        /* Dataframes */
        div[data-testid="stDataFrame"] {
            border: 1px solid var(--border-card);
            border-radius: 0px;
            background: var(--bg-card);
        }

        /* Standings Bar Cards */
        .standings-card {
            background: #161b22;
            border: 1px solid var(--border-card);
            border-top: 3px solid var(--accent-red);
            border-radius: 0px;
            padding: 16px 18px;
            margin: 12px 0;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
        }

        .standings-title {
            font-family: 'Titillium Web', sans-serif !important;
            font-weight: 800;
            font-size: 1.05rem;
            color: var(--text-heading);
            margin-bottom: 12px;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }

        .standings-row {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 6px;
            padding: 3px 0;
        }

        .standings-rank {
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            font-size: 0.82rem;
            color: var(--accent-amber);
            width: 28px;
            text-align: center;
        }

        .standings-main {
            flex: 1;
        }

        .standings-name {
            font-family: 'Titillium Web', sans-serif;
            font-size: 13.5px;
            font-weight: 700;
            color: #f0f3f6;
            line-height: 1.1;
            margin-bottom: 3px;
        }

        .standings-bar-shell {
            height: 6px;
            background: #262c36;
            border-radius: 0px;
            overflow: hidden;
        }

        .standings-bar {
            height: 100%;
            border-radius: 0px;
            transition: width 0.3s ease;
        }

        .standings-points {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            color: var(--text-muted);
            width: 75px;
            text-align: right;
        }

        /* Top Podium Card */
        .podium-card {
            border: 1px solid var(--border-card);
            border-top: 3px solid var(--accent-red);
            border-radius: 0px;
            background: #161b22;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.45);
            padding: 16px 18px;
            margin: 12px 0 16px;
        }

        .podium-header {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
        }

        .podium-badge {
            background: var(--accent-red);
            color: #ffffff;
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            border-radius: 0px;
            padding: 3px 8px;
            font-size: 0.70rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .podium-title {
            color: var(--text-heading);
            font-family: 'Titillium Web', sans-serif !important;
            font-weight: 800;
            font-weight: 700;
            font-size: 1.05rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
        }

        .podium-subtitle {
            color: var(--text-muted);
            font-family: 'Inter', sans-serif;
            font-size: 13.5px;
            margin-bottom: 12px;
        }

        .podium-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 10px;
        }

        .podium-cell {
            border: 1px solid var(--border-card);
            border-radius: 0px;
            background: #12161f;
            padding: 12px 14px;
        }

        .podium-pos {
            font-family: 'Titillium Web', sans-serif;
            font-weight: 800;
            font-size: 1.15rem;
            color: var(--text-heading);
            margin-bottom: 4px;
        }

        .podium-pos-leader {
            color: var(--accent-amber);
        }

        .podium-name {
            color: var(--text-heading);
            font-family: 'Titillium Web', sans-serif;
            font-size: 1.1rem;
            line-height: 1.2;
            font-weight: 700;
        }

        .podium-team {
            color: var(--text-muted);
            font-family: 'Inter', sans-serif;
            font-size: 13px;
            margin-top: 2px;
        }

        .podium-time {
            color: var(--accent-red);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            margin-top: 8px;
            font-weight: 600;
        }

        /* Loading Box */
        .loading-box {
            border: 1px solid var(--accent-red);
            border-radius: 0px;
            background: var(--bg-card);
            padding: 10px 14px;
            margin: 8px 0;
            color: var(--text-heading);
            font-family: 'JetBrains Mono', monospace;
            font-weight: 700;
            font-size: 0.92rem;
            letter-spacing: 0.05em;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        @media (max-width: 900px) {
            .circuit-records-grid {
                grid-template-columns: 1fr;
            }
            .podium-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_topbar(current_index: int = 0, route_map: dict | None = None, **kwargs) -> None:
    """Renders a sleek, single-row F1 race control top navigation bar using streamlit-option-menu."""
    if st.session_state.get("_topbar_rendered_in_run", False):
        return
    st.session_state["_topbar_rendered_in_run"] = True

    try:
        from streamlit_option_menu import option_menu
    except ImportError:
        option_menu = None

    col_brand, col_nav = st.columns([1.2, 2.8], vertical_alignment="center")

    with col_brand:
        st.markdown(
            """
            <div class="topbar-brand">
                <span class="f1-badge">F1</span>
                <div class="brand-text">
                    <span class="brand-title">RACE CONTROL</span>
                    <span class="brand-sub">TELEMETRY ARCHIVE</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    options = ["Race Select", "Race Analysis", "Driver Compare", "Team Wiki"]
    icons = ["flag", "bar-chart-line", "people", "trophy"]

    if option_menu is not None:
        with col_nav:
            selected = option_menu(
                menu_title=None,
                options=options,
                icons=icons,
                default_index=current_index,
                orientation="horizontal",
                styles={
                    "container": {
                        "padding": "0px !important",
                        "margin": "0px !important",
                        "background-color": "transparent",
                        "border": "none",
                    },
                    "nav": {
                        "justify-content": "flex-end !important",
                        "gap": "6px !important",
                        "align-items": "stretch !important",
                    },
                    "nav-item": {
                        "flex": "none !important",
                        "margin": "0px !important",
                    },
                    "icon": {
                        "color": "inherit",
                        "font-size": "12px",
                        "vertical-align": "-1px",
                        "margin-right": "6px",
                    },
                    "nav-link": {
                        "font-family": "'Titillium Web', sans-serif",
                        "font-size": "13px",
                        "font-weight": "600",
                        "text-transform": "uppercase",
                        "letter-spacing": "0.08em",
                        "color": "#8b949e",
                        "background-color": "transparent",
                        "padding": "10px 16px 8px 16px",
                        "margin": "0px",
                        "border-radius": "0px",
                        "border": "none",
                        "border-bottom": "3px solid transparent",
                        "transition": "all 0.14s ease",
                    },
                    "nav-link-selected": {
                        "background-color": "rgba(225, 6, 0, 0.06) !important",
                        "color": "#ffffff !important",
                        "font-weight": "700 !important",
                        "border": "none !important",
                        "border-bottom": "3px solid #e10600 !important",
                        "border-radius": "0px !important",
                        "box-shadow": "none !important",
                    },
                },
                key=f"f1_top_nav_{current_index}",
            )
    else:
        with col_nav:
            cols = st.columns(len(options))
            selected = options[current_index]
            for i, opt in enumerate(options):
                with cols[i]:
                    btn_type = "primary" if i == current_index else "secondary"
                    if st.button(opt, key=f"f1_top_fallback_{i}", type=btn_type, use_container_width=True):
                        selected = opt

    if route_map and selected in route_map:
        target = route_map[selected]
        selected_index = options.index(selected)
        if selected_index != current_index:
            st.switch_page(target)


def _pick_first_value(row, keys: list[str], default: str = "-") -> str:
    for key in keys:
        if key in row and str(row[key]).strip() and str(row[key]).lower() != "nan":
            return str(row[key]).strip()
    return default


def get_team_color(identifier: str | None, default: str = "#e10600") -> str:
    """Returns the official F1 team color for a team name, driver name, or driver abbreviation.
    Accurate F1 team color mapping:
    - McLaren -> Orange (#ff8000)
    - Red Bull -> Dark Blue (#1e41ff / #3671c6)
    - Mercedes -> Blue (#00a0dd)
    - Ferrari -> Red (#e80020)
    - Aston Martin -> Racing Green (#229971)
    - Alpine -> Alpine Blue (#0093cc)
    - Williams -> Williams Blue (#64c4ff)
    - RB / Racing Bulls -> Electric Blue (#6692ff)
    - Sauber / Kick Sauber -> Neon Green (#52e252)
    - Haas -> Haas Red (#e6002b)
    Default fallback is F1 Red (#e10600).
    """
    if not identifier:
        return default
    text = str(identifier).lower().strip()

    # McLaren - Orange
    if any(k in text for k in ["mclaren", "norris", "piastri"]) or text in ["mcl", "nor", "pia"]:
        return "#ff8000"

    # Red Bull - Dark Blue
    if any(k in text for k in ["red bull", "verstappen", "perez"]) or text in ["rbr", "ver", "per"]:
        return "#1e41ff"

    # Ferrari - Racing Red
    if any(k in text for k in ["ferrari", "leclerc", "sainz"]) or text in ["fer", "lec", "sai"]:
        return "#e80020"

    # Mercedes - Mercedes Blue
    if any(k in text for k in ["mercedes", "russell", "antonelli"]) or text in ["mer", "rus", "ant"]:
        return "#00a0dd"
    if "hamilton" in text or text == "ham":
        if "ferrari" in text:
            return "#e80020"
        return "#00a0dd"

    # Aston Martin - British Racing Green
    if any(k in text for k in ["aston martin", "alonso", "stroll"]) or text in ["amr", "alo", "str"]:
        return "#229971"

    # Alpine - Alpine Blue
    if any(k in text for k in ["alpine", "gasly", "ocon", "doohan"]) or text in ["alp", "gas", "oco", "doo"]:
        return "#0093cc"

    # Williams - Williams Blue
    if any(k in text for k in ["williams", "albon", "sargeant", "colapinto"]) or text in ["wil", "alb", "sar", "col"]:
        return "#64c4ff"

    # Racing Bulls / RB / AlphaTauri / Toro Rosso - Electric Blue
    if any(k in text for k in ["racing bulls", "alphatauri", "toro rosso", "vcarb", "ricciardo", "tsunoda", "lawson", "hadjar"]) or text in ["rb", "vcarb", "ric", "tsu", "law", "had"] or text.startswith("rb ") or " rb" in text:
        return "#6692ff"

    # Sauber / Kick Sauber / Alfa Romeo - Neon Green
    if any(k in text for k in ["sauber", "kick sauber", "alfa romeo", "bottas", "zhou", "bortoleto"]) or text in ["sau", "bot", "zho", "bor"]:
        return "#52e252"

    # Haas - Haas Red
    if any(k in text for k in ["haas", "magnussen", "bearman", "hulkenberg"]) or text in ["haa", "mag", "bea", "hul"]:
        return "#e6002b"

    return default


def render_standings_bar_card(
    dataframe,
    title: str,
    name_column: str,
    points_column: str = "PTS",
    limit: int = 20,
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
        
        # Color driver or constructor bar in their exact team color
        bar_color = get_team_color(name)

        rows_html.append(
            "<div class='standings-row'>"
            f"<div class='standings-rank' style='color:{bar_color};'>{escape(str(rank))}</div>"
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
    p1_color = "#e10600"

    for _, row in top_three.iterrows():
        position = _pick_first_value(row, ["POS", "position"], "-")
        driver = _pick_first_value(row, ["DRIVER", "BroadcastName", "FullName"], "-")
        team = _pick_first_value(row, ["TEAM", "TeamName"], "")
        timing = _pick_first_value(
            row,
            [time_column] if time_column else ["TIME/GAP", "Q3", "Q2", "Q1", "PTS", "FASTEST LAP"],
            "-",
        )
        if time_column is None and timing == "-" and "PTS" in dataframe.columns:
            timing = f"{_pick_first_value(row, ['PTS'], '0')} pts"

        team_color = get_team_color(team or driver)
        if str(position) in ["1", "1.0", "P1"]:
            p1_color = team_color

        cells.append(
            f"<div class='podium-cell' style='border-top: 3px solid {team_color}; box-shadow: 0 4px 16px rgba(0,0,0,0.4);'>"
            f"<div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;'>"
            f"<span class='podium-pos' style='color: {team_color}; font-size: 1.25rem;'>P{escape(str(position))}</span>"
            f"<span style='font-family: \"JetBrains Mono\", monospace; font-size: 0.65rem; font-weight: 700; color: {team_color}; background: rgba(255,255,255,0.04); border: 1px solid {team_color}; padding: 1px 6px; text-transform: uppercase;'>{escape(str(team))}</span>"
            f"</div>"
            f"<div class='podium-name' style='font-size: 1.12rem;'>{escape(driver)}</div>"
            f"<div class='podium-time' style='color: {team_color}; font-size: 0.95rem; font-weight: 700;'>{escape(timing)}</div>"
            "</div>"
        )

    subtitle_html = f"<div class='podium-subtitle'>{escape(subtitle)}</div>" if subtitle else ""
    st.markdown(
        f"<div class='podium-card' style='border-top: 3px solid {p1_color};'>"
        "<div class='podium-header'>"
        f"<span class='podium-badge' style='background: {p1_color}; color: #ffffff;'>{escape(badge)}</span>"
        f"<span class='podium-title'>{escape(title)}</span>"
        "</div>"
        f"{subtitle_html}"
        "<div class='podium-grid'>"
        f"{''.join(cells)}"
        "</div>"
        "</div>",
        unsafe_allow_html=True,
    )


@contextmanager
def anime_loading_box(message: str = "Loading..."):
    placeholder = st.empty()
    placeholder.markdown(
        f"<div class='loading-box'><span>⚡</span><span>{escape(message)}</span></div>",
        unsafe_allow_html=True,
    )
    try:
        yield
    finally:
        placeholder.empty()
