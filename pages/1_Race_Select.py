import re
from datetime import datetime
from html import escape

import streamlit as st

from sessions import get_motorsport_news, get_schedule


def _format_relative_time(pub_date) -> str:
    if not pub_date:
        return "Recent"
    try:
        now = datetime.now(pub_date.tzinfo) if pub_date.tzinfo else datetime.now()
        diff = now - pub_date
        secs = int(diff.total_seconds())
        if secs < 0:
            return "Just now"
        if secs < 60:
            return f"{secs}s ago"
        mins = secs // 60
        if mins < 60:
            return f"{mins}m ago"
        hrs = mins // 60
        if hrs < 24:
            return f"{hrs}h ago"
        days = hrs // 24
        if days < 7:
            return f"{days}d ago"
        return pub_date.strftime("%b %d")
    except Exception:
        return "Recent"


def _get_source_dot_color(source: str) -> str:
    source_lower = source.lower()
    if "racefans" in source_lower:
        return "#e10600"  # Red
    elif "motorsport" in source_lower:
        return "#f5a623"  # Amber
    elif "the-race" in source_lower:
        return "#38bdf8"  # Sky
    return "#e10600"


def _group_stories(stories: list[dict]) -> list[dict]:
    stop_words = {
        "the", "a", "an", "in", "to", "for", "of", "and", "at", "on", "is", "with",
        "from", "by", "after", "as", "over", "f1", "formula", "1", "grand", "prix",
        "gp", "team", "driver", "race", "says", "how", "why", "what", "new", "his",
    }

    def get_tokens(title: str) -> set[str]:
        words = re.findall(r"\b[a-zA-Z]{3,}\b", title.lower())
        return {w for w in words if w not in stop_words}

    grouped: list[dict] = []
    for story in stories:
        tokens = get_tokens(story.get("title", ""))
        matched = None
        if len(tokens) >= 2:
            for grp in grouped:
                overlap = tokens.intersection(grp["tokens"])
                if len(overlap) >= 3 or (len(overlap) >= 2 and len(overlap) / max(len(tokens), len(grp["tokens"])) >= 0.4):
                    matched = grp
                    break
        if matched:
            matched["more_sources"].append(story)
        else:
            grouped.append({"primary": story, "tokens": tokens, "more_sources": []})
    return grouped


def render_header() -> None:
    st.markdown(
        """
        <div class="hero-bleed">
            <div class="hero-kicker">
                <span class="kicker-lead">FIA FORMULA 1</span>
                <span class="kicker-sep">//</span>
                <span class="kicker-sub">OFFICIAL TELEMETRY &amp; ARCHIVE CONTROL</span>
            </div>
            <h1 class="hero-display-title">
                RACE CONTROL <span class="hero-title-dim">&amp;</span> TELEMETRY ARCHIVE
            </h1>
            <p class="hero-dek">
                High-fidelity motorsport telemetry, circuit intelligence, lap-by-lap pace traces, and team championship dossiers.
            </p>
            <div class="timing-tags-strip">
                <div class="timing-tag">
                    <span class="tag-code">SYS.01</span>
                    <span class="tag-label">FASTF1 TELEMETRY</span>
                </div>
                <div class="timing-tag">
                    <span class="tag-code">SYS.02</span>
                    <span class="tag-label">LAP PACE ANALYSIS</span>
                </div>
                <div class="timing-tag">
                    <span class="tag-code">SYS.03</span>
                    <span class="tag-label">CIRCUIT RECORDS</span>
                </div>
                <div class="timing-tag">
                    <span class="tag-code">SYS.04</span>
                    <span class="tag-label">QUALIFYING &amp; RACE ARCHIVE</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_controls():
    with st.container(border=True, key="dialog_race_select"):
        st.markdown(
            """
            <div class="ctrl-panel-header">
                <div class="ctrl-panel-badge">
                    <span class="ctrl-code">CTRL // 01</span>
                    <span class="ctrl-type">SESSION CONFIGURATION</span>
                </div>
                <h2 class="ctrl-panel-title">ARCHIVE SELECTOR</h2>
                <p class="ctrl-panel-desc">
                    Select a championship season and grand prix round to load high-fidelity circuit intelligence, telemetry traces, and historical results.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        with col1:
            with st.container(key="cell_select_year"):
                selected_year = st.selectbox("SELECT YEAR", list(range(2025, 1999, -1)))

        schedule = get_schedule(selected_year)
        races = schedule[schedule["EventFormat"] != "testing"]

        with col2:
            with st.container(key="cell_select_round"):
                selected_race = st.selectbox("SELECT ROUND", races["EventName"].tolist())

        event = schedule[schedule["EventName"] == selected_race].iloc[0]

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

        col_primary, col_secondary, col_tertiary = st.columns([1.6, 1.2, 1.2])

        with col_primary:
            if st.button("⚡ LOAD ARCHIVE DATA", type="primary", use_container_width=True, key="btn_load_archive"):
                st.session_state.selected_year = selected_year
                st.session_state.selected_race = selected_race
                st.session_state.selected_event = event
                st.switch_page("pages/2_Dashboard.py")

        with col_secondary:
            if st.button("DRIVER COMPARISON", use_container_width=True, key="btn_driver_compare"):
                st.switch_page("pages/3_Driver_Compare.py")

        with col_tertiary:
            if st.button("TEAM WIKI", use_container_width=True, key="btn_team_wiki"):
                st.switch_page("pages/4_Team_Wiki.py")

        return selected_year, selected_race, event


def render_news_briefing() -> None:
    with st.container(border=True, key="dialog_news_briefing"):
        st.markdown(
            """
            <div class="feed-header-strip">
                <div class="feed-strip-left">
                    <span class="live-dot-pulse"></span>
                    <span class="feed-strip-kicker">GLOBAL PADDOCK FEED</span>
                    <span class="feed-strip-divider">|</span>
                    <h2 class="feed-strip-title">MOTORSPORT HEADLINES</h2>
                </div>
                <div class="feed-strip-right">
                    <span class="feed-strip-status">LIVE WIRE // RSS</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        stories = get_motorsport_news()
        if not stories:
            st.info("News feed unavailable right now. Try reloading in a moment.")
            return

        grouped_stories = _group_stories(stories)
        rows_html = []

        for grp in grouped_stories:
            primary = grp["primary"]
            more_sources = grp["more_sources"]
            p_title = escape(primary.get("title", ""))
            p_link = escape(primary.get("link", "#"))
            p_source = escape(primary.get("source", "Paddock News").upper())
            p_time = escape(_format_relative_time(primary.get("published")).upper())
            p_dot = _get_source_dot_color(primary.get("source", ""))

            sub_html = ""
            if more_sources:
                sub_items = []
                for sub in more_sources:
                    s_title = escape(sub.get("title", ""))
                    s_link = escape(sub.get("link", "#"))
                    s_source = escape(sub.get("source", "").upper())
                    s_time = escape(_format_relative_time(sub.get("published")).upper())
                    s_dot = _get_source_dot_color(sub.get("source", ""))
                    sub_items.append(
                        f"<a href='{s_link}' target='_blank' rel='noopener noreferrer' class='feed-sub-row' style='border-left-color: {s_dot};'>"
                        f"<span class='feed-sub-title'>{s_title}</span>"
                        f"<div class='feed-row-meta'>"
                        f"<span class='feed-meta-source' style='color: {s_dot};'>{s_source}</span>"
                        f"<span class='feed-meta-sep'>//</span>"
                        f"<span class='feed-meta-time'>{s_time}</span>"
                        f"</div>"
                        f"</a>"
                    )
                count = len(more_sources)
                plural = "SOURCES" if count > 1 else "SOURCE"
                sub_html = (
                    f"<details class='feed-sources-details'>"
                    f"<summary class='feed-sources-summary'>+{count} MORE {plural}</summary>"
                    f"<div class='feed-sources-list'>{''.join(sub_items)}</div>"
                    f"</details>"
                )

            rows_html.append(
                f"<div class='feed-row-group'>"
                f"<a href='{p_link}' target='_blank' rel='noopener noreferrer' class='feed-row' style='border-left-color: {p_dot};'>"
                f"<div class='feed-row-main'><span class='feed-row-title'>{p_title}</span></div>"
                f"<div class='feed-row-meta'>"
                f"<span class='feed-meta-source' style='color: {p_dot};'>{p_source}</span>"
                f"<span class='feed-meta-sep'>//</span>"
                f"<span class='feed-meta-time'>{p_time}</span>"
                f"</div>"
                f"</a>"
                f"{sub_html}"
                f"</div>"
            )

        st.markdown("".join(rows_html), unsafe_allow_html=True)


render_header()
render_controls()
render_news_briefing()
