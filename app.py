import importlib
import streamlit as st

import ui
importlib.reload(ui)
import sessions
importlib.reload(sessions)
from ui import inject_retro_css, render_topbar
from sessions import setup_fastf1_cache

st.set_page_config(
    page_title="F1 RACE CONTROL",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

setup_fastf1_cache()

page_select = st.Page("pages/1_Race_Select.py", title="Race Select", url_path="Race_Select", default=True)
page_dashboard = st.Page("pages/2_Dashboard.py", title="Race Analysis", url_path="Dashboard")
page_driver_compare = st.Page("pages/3_Driver_Compare.py", title="Driver Comparison", url_path="Driver_Compare")
page_team_wiki = st.Page("pages/4_Team_Wiki.py", title="Team Wiki", url_path="Team_Wiki")

pg = st.navigation([page_select, page_dashboard, page_driver_compare, page_team_wiki], position="hidden")

# Reset guard so topbar renders exactly once per rerun from app.py
st.session_state["_topbar_rendered_in_run"] = False

route_map = {
    "Race Select": page_select,
    "Race Analysis": page_dashboard,
    "Driver Compare": page_driver_compare,
    "Team Wiki": page_team_wiki,
}
url_to_index = {
    "Race_Select": 0,
    "Dashboard": 1,
    "Driver_Compare": 2,
    "Team_Wiki": 3,
}
current_index = url_to_index.get(getattr(pg, "url_path", "Race_Select"), 0)

inject_retro_css()
render_topbar(current_index=current_index, route_map=route_map)

pg.run()
