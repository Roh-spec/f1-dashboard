import streamlit as st

from design import inject_retro_css
from sessions import setup_fastf1_cache

st.set_page_config(page_title="F1 RETRO DASH", layout="wide", initial_sidebar_state="collapsed")
inject_retro_css()
st.markdown(
    """
    <div id="topbar">
      <span class="topbar-brand">F1 RETRO DASH</span>
      <div class="topbar-links">
        <a href="/" target="_self">Race Select</a>
        <a href="/Dashboard" target="_self">Race Analysis</a>
        <a href="/Driver_Compare" target="_self">Driver Compare</a>
        <a href="/Team_Wiki" target="_self">Team Wiki</a>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
setup_fastf1_cache()
page_select = st.Page("pages/1_Race_Select.py", title="Race Select", icon="🏁", url_path="Race_Select", default=True)
page_dashboard = st.Page("pages/2_Dashboard.py", title="Race Analysis", icon="📊", url_path="Dashboard")
page_driver_compare = st.Page("pages/3_Driver_Compare.py", title="Driver Comparison", icon="👥", url_path="Driver_Compare")
page_team_wiki = st.Page("pages/4_Team_Wiki.py", title="Team Wiki", icon="🏎️", url_path="Team_Wiki")

pg = st.navigation([page_select, page_dashboard, page_driver_compare, page_team_wiki], position="hidden")
pg.run()

