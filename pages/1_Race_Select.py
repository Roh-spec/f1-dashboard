import streamlit as st
from sessions import get_schedule

def render_header() -> None:
    with st.container(border=True, key="dialog_header"):
        st.markdown(
            """
            <div class="hero">
                <h1 class="hero-title">PERSONAL F1-DASHBOARD</h1>
                <p class="hero-subtitle">
                    A CRT-style race control board for archived Formula 1 data, with track history,
                    lap timing, qualifying results, and race summaries in one place.
                </p>
                <div class="badge-row">
                    <span class="badge">TIMING ARCHIVE</span>
                    <span class="badge">TRACK HISTORY</span>
                    <span class="badge">QUALIFYING</span>
                    <span class="badge">RACE CONTROL</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_controls():
    with st.container(border=True, key="dialog_race_select"):
        st.markdown("<p class='section-kicker'>Select Archive</p>", unsafe_allow_html=True)
        st.markdown("<h2>Race Select</h2>", unsafe_allow_html=True)
        st.markdown("<p class='panel-note'>Choose a season and round to load the relevant circuit, session, and results panels.</p>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            selected_year = st.selectbox("SELECT YEAR:", list(range(2025, 1999, -1)))

        schedule = get_schedule(selected_year)
        races = schedule[schedule["EventFormat"] != "testing"]

        with col2:
            selected_race = st.selectbox("SELECT STAGE (RACE):", races["EventName"].tolist())

    event = races[races["EventName"] == selected_race].iloc[0]
    return selected_year, selected_race, event


render_header()
selected_year, selected_race, event = render_controls()

if st.button("LOAD ARCHIVE DATA", use_container_width=True):
    st.session_state.selected_year = selected_year
    st.session_state.selected_race = selected_race
    st.session_state.selected_event = event
    st.switch_page("pages/2_Dashboard.py")
