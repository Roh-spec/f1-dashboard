# F1 Retro Dashboard

A Streamlit dashboard for exploring Formula 1 lap data, telemetry, and championship statistics with a bright retro CRT-style aesthetic. The app uses FastF1, Ergast, and Wikipedia APIs to pull real historical data, telemetry traces, circuit layouts, and track histories.

## Features

- **Multi-page Architecture**: Separate pages for "Race Select" and the main "Dashboard" to smoothly navigate between different weekends and seasons.
- **Session Telemetry**: Detailed matplotlib telemetry charts (Speed, Throttle, Brake) comparing the top drivers for qualifying and race sessions.
- **Lap-by-Lap Position Charts**: Visualization of track position, pit stops, and overtakes throughout the race.
- **Circuit Intelligence**: Track map displays, historical stats (first F1 race, length, laps, total distance), and Wikipedia excerpts for the selected Grand Prix. Handles layout changes across different years (e.g. Qatar).
- **Championship Standings**: World Driver and Constructor Championship standings updated dynamically for the selected race round.
- **Comprehensive Session Views**: Tailored data tables and visual representations for every session type in a weekend (Free Practice, Sprint Shootout, Sprint, Qualifying, Race).
- **Retro Design System**: High-contrast, blocky layouts with a warm `#e5dccb` text on `#211d18` ink background to simulate a vintage paper or 8-bit timing screen.

## Project Structure

- `app.py`: Entry point for the Streamlit application. Configures the multi-page navigation.
- `pages/1_Race_Select.py`: User interface for selecting the historical year and specific Grand Prix.
- `pages/2_Dashboard.py`: Main dashboard view orchestrating the rendering of track info, standings, and sessions.
- `sessions.py`: Handles caching and loading data from the FastF1 and Ergast APIs.
- `charts.py`: Encapsulates all matplotlib telemetry and track position charts.
- `circuit_map.py`: Logic for fuzzy-matching and displaying track layout images from the `circuits/` directory.
- `track_analysis.py`: Contains a database of track facts (length, laps, first race, most wins) and renders the track statistics UI.
- `design.py`: Custom CSS injection for the retro theme.
- `fps.py`, `qualifying.py`, `races.py`: Specific rendering logic, tables, and fallback UI for Free Practice, Qualifying, and Race sessions.

## How to Run

1. Make sure you have the required dependencies installed:
```powershell
pip install -r requirements.txt
```

2. Run the application using Streamlit:
```powershell
streamlit run app.py
```

3. The dashboard will open in your default browser at `http://localhost:8501`.

## Caching

The application caches API requests heavily to improve performance after the initial slow data download. 
- FastF1 telemetry and timing data is saved locally in the `f1_cache/` and `.fastf1_cache/` directories.
- Streamlit `@st.cache_data` is used in memory for faster circuit lookups, Wikipedia summaries, and API requests.

## Common Issues

### FastF1 takes time on first load

That is normal. It downloads and caches archive data the first time you select a session. Subsequent loads will be much faster.

### Missing Data

If some telemetry traces, speed traps, or tyre fields are empty:
- Not every historical FastF1 session has every field populated. The app is built to handle incomplete data gracefully.
- Standings data from the Ergast API might occasionally be delayed for recent races.

## Good Next Improvements

- Add specific driver-to-driver comparison modes.
- Add lap filtering by tyre compound or stint.
- Add team color styling to all data tables.
- Optimize loading times further with more aggressive caching.
