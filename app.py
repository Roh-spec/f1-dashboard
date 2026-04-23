import streamlit as st

from design import inject_retro_css
from sessions import setup_fastf1_cache

st.set_page_config(page_title="F1 RETRO DASH", layout="wide", initial_sidebar_state="collapsed")
inject_retro_css()
setup_fastf1_cache()

page_select = st.Page("pages/1_Race_Select.py", title="Race Select", icon="🏁", default=True)
page_dashboard = st.Page("pages/2_Dashboard.py", title="Dashboard", icon="📊")

pg = st.navigation([page_select, page_dashboard])
pg.run()
