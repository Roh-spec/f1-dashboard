import streamlit as st

from ui import inject_retro_css
from sessions import setup_fastf1_cache

st.set_page_config(page_title="F1 RETRO DASH", layout="wide", initial_sidebar_state="collapsed")
inject_retro_css()
setup_fastf1_cache()


def render_top_header() -> None:
    with st.container(border=False):
        st.markdown("<div class='top-nav-shell'>", unsafe_allow_html=True)
        left_col, right_col = st.columns([1.2, 3.8], vertical_alignment="center")

        with left_col:
            st.markdown("<p class='top-nav-title'>F1 Retro Dash</p>", unsafe_allow_html=True)

        with right_col:
            nav_1, nav_2, nav_3, nav_4 = st.columns(4)
            with nav_1:
                if st.button("🏁 Race Select", key="header_nav_race_select"):
                    st.switch_page("pages/1_Race_Select.py")
            with nav_2:
                if st.button("📊 Race Analysis", key="header_nav_race_analysis"):
                    st.switch_page("pages/2_Dashboard.py")
            with nav_3:
                if st.button("👥 Driver Compare", key="header_nav_driver_compare"):
                    st.switch_page("pages/3_Driver_Compare.py")
            with nav_4:
                if st.button("🏎️ Team Wiki", key="header_nav_team_wiki"):
                    st.switch_page("pages/4_Team_Wiki.py")

        st.markdown("</div>", unsafe_allow_html=True)


render_top_header()
page_select = st.Page("pages/1_Race_Select.py", title="Race Select", icon="🏁", default=True)
page_dashboard = st.Page("pages/2_Dashboard.py", title="Race Analysis", icon="📊")
page_driver_compare = st.Page("pages/3_Driver_Compare.py", title="Driver Comparison", icon="👥")
page_team_wiki = st.Page("pages/4_Team_Wiki.py", title="Team Wiki", icon="🏎️")

pg = st.navigation([page_select, page_dashboard, page_driver_compare, page_team_wiki])
pg.run()

