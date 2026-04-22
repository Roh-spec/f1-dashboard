import streamlit as st
import fastf1
import pandas as pd
import wikipedia
import os

# --- PAGE SETUP ---
st.set_page_config(page_title="F1 RETRO DASH", layout="wide")

# --- RETRO CSS STYLING (Synthwave / 8-Bit Arcade Style) ---
retro_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');

/* Main Background and Text */
.stApp {
    background-color: #0d0221; /* Deep dark purple/black */
    color: #00f0ff; /* Neon Cyan */
    font-family: 'VT323', monospace;
    font-size: 22px;
}

/* Headers */
h1, h2, h3 {
    font-family: 'Press Start 2P', cursive !important;
    color: #ff007f !important; /* Neon Pink */
    text-shadow: 4px 4px #00f0ff;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* Override Markdown Text */
p, li {
    font-family: 'VT323', monospace !important;
    font-size: 24px !important;
    color: #a67cff; 
}

/* DataFrames / Tables */[data-testid="stDataFrame"] {
    border: 2px solid #ff007f;
    box-shadow: 5px 5px 0px #00f0ff;
    background-color: #000000;
}

/* Select boxes */
div[data-baseweb="select"] > div {
    background-color: #1f0b40;
    color: #00f0ff;
    border: 2px solid #ff007f;
    font-family: 'VT323', monospace;
}

/* Streamlit Top Bar styling */
header {
    background: transparent !important;
}
</style>
"""
st.markdown(retro_css, unsafe_allow_html=True)

# --- FASTF1 CACHE SETUP ---
# FastF1 needs a cache directory to store downloaded data
if not os.path.exists("f1_cache"):
    os.makedirs("f1_cache")
fastf1.Cache.enable_cache("f1_cache")

# --- APP HEADER ---
st.markdown("<h1>🏎️ F1 RETRO DASH</h1>", unsafe_allow_html=True)
st.markdown("<p>INSERT COIN TO START...</p>", unsafe_allow_html=True)
st.divider()

# --- SIDEBAR & USER INPUTS ---
col1, col2 = st.columns(2)
with col1:
    # Let user select a year (FastF1 has good data from 2018 onwards)
    selected_year = st.selectbox("SELECT YEAR:", list(range(2025, 2017, -1)))

# Fetch the schedule for the selected year
@st.cache_data
def get_schedule(year):
    return fastf1.get_event_schedule(year)

schedule = get_schedule(selected_year)
# Filter out testing sessions, keep only actual race rounds
races = schedule[schedule['EventFormat'] != 'testing']

with col2:
    # Select the race
    selected_race = st.selectbox("SELECT STAGE (RACE):", races['EventName'].tolist())

# --- DATA FETCHING ---
event = races[races['EventName'] == selected_race].iloc[0]

@st.cache_data
def load_session_results(year, race_name, session_type):
    try:
        session = fastf1.get_session(year, race_name, session_type)
        session.load(telemetry=False, weather=False) # Keep it light and fast
        return session.results
    except Exception as e:
        return None

# --- TRACK DETAILS & HISTORY ---
st.markdown(f"<h2>🏁 STAGE: {event['Location']}</h2>", unsafe_allow_html=True)

col_track1, col_track2 = st.columns([2, 1])

with col_track1:
    st.markdown("<h3>TRACK ARCHIVES (WIKI)</h3>", unsafe_allow_html=True)
    # Fetch historical details using Wikipedia API based on the Circuit Name
    circuit_name = event['Location'] + " Grand Prix"
    try:
        wiki_summary = wikipedia.summary(circuit_name, sentences=4)
        st.write(f"> {wiki_summary}")
    except:
        try:
            # Fallback to general circuit name if GP page fails
            wiki_summary = wikipedia.summary(event['EventName'], sentences=4)
            st.write(f"> {wiki_summary}")
        except:
            st.write("> DATA CORRUPTED. UNABLE TO LOAD TRACK HISTORY.")

with col_track2:
    st.markdown("<h3>STAGE STATS</h3>", unsafe_allow_html=True)
    st.write(f"**ROUND:** {event['RoundNumber']}")
    st.write(f"**CIRCUIT:** {event['EventName']}")
    st.write(f"**LOCATION:** {event['Location']}, {event['Country']}")
    st.write(f"**DATE:** {event['EventDate'].date()}")

st.divider()

# --- RACE RESULTS ---
st.markdown("<h2>🏆 RACE RESULTS</h2>", unsafe_allow_html=True)
with st.spinner('LOADING RACE DATA...'):
    race_results = load_session_results(selected_year, selected_race, 'R')
    
    if race_results is not None and not race_results.empty:
        # Format the DataFrame for better display
        df_race = race_results[['Position', 'BroadcastName', 'TeamName', 'GridPosition', 'Time', 'Status', 'Points']].copy()
        df_race.columns =['POS', 'DRIVER', 'TEAM', 'GRID', 'TIME/GAP', 'STATUS', 'PTS']
        
        # Convert TimeDelta to string format
        df_race['TIME/GAP'] = df_race['TIME/GAP'].astype(str).str.split('.').str[0]
        df_race['TIME/GAP'] = df_race['TIME/GAP'].replace('NaT', 'N/A')
        
        st.dataframe(df_race.set_index('POS'), use_container_width=True)
        
        winner = df_race.iloc[0]['DRIVER']
        st.success(f"🎉 WINNER: {winner} 🎉")
    else:
        st.warning("⚠️ STAGE NOT COMPLETED YET OR DATA UNAVAILABLE.")

st.divider()

# --- QUALIFYING RESULTS ---
st.markdown("<h2>⏱️ QUALIFYING RESULTS</h2>", unsafe_allow_html=True)
with st.spinner('LOADING QUALI DATA...'):
    quali_results = load_session_results(selected_year, selected_race, 'Q')
    
    if quali_results is not None and not quali_results.empty:
        df_quali = quali_results[['Position', 'BroadcastName', 'TeamName', 'Q1', 'Q2', 'Q3']].copy()
        df_quali.columns =['POS', 'DRIVER', 'TEAM', 'Q1', 'Q2', 'Q3']
        
        # Format times
        for col in ['Q1', 'Q2', 'Q3']:
            df_quali[col] = df_quali[col].astype(str).str.split('.').str[0].str.replace('NaT', '-')
            df_quali[col] = df_quali[col].str.replace('0 days 00:', '')

        st.dataframe(df_quali.set_index('POS'), use_container_width=True)
        
        pole = df_quali.iloc[0]['DRIVER']
        st.info(f"⚡ POLE POSITION: {pole} ⚡")
    else:
        st.warning("⚠️ QUALIFYING DATA UNAVAILABLE.")