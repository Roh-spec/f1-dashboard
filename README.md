# F1 Retro Dashboard

A Streamlit dashboard for exploring Formula 1 lap data, telemetry, championship trends, and driver history with a bright retro CRT-style aesthetic. The app uses FastF1, Ergast-compatible endpoints, and Wikipedia APIs to pull historical race data, telemetry traces, circuit layouts, standings, and driver context.

## Features

- **Multi-page Architecture**: Separate pages for Race Select, the main Dashboard, and Driver Comparison & History.
- **Motorsport News Briefing**: A live summary section on the main page that aggregates recent headlines from multiple motorsport RSS feeds.
- **Session Telemetry**: Detailed matplotlib telemetry charts (Speed, Throttle, Brake) comparing the top drivers for qualifying and race sessions.
- **Lap-by-Lap Position Charts**: Visualization of track position, pit stops, and overtakes throughout the race.
- **Circuit Intelligence**: Track map displays, historical stats (first F1 race, length, laps, total distance), and Wikipedia excerpts for the selected Grand Prix. Handles layout changes across different years (e.g. Qatar).
- **Championship Standings**: World Driver and Constructor Championship standings updated dynamically for the selected race round.
- **Comprehensive Session Views**: Tailored data tables and visual representations for every session type in a weekend (Free Practice, Sprint Shootout, Sprint, Qualifying, Race).
- **Driver Dossier**: Career profile view for two selected drivers including races, wins, points, debut race, and season-level best/least points summaries.
- **Year-Scoped Driver Selection**: Driver comparison is filtered by selected season first, then drivers are selected from that season's participants.
- **Interactive Championship Progression Chart**: Round-by-round championship points comparison for two drivers in the selected season, with interactive tooltips and chart fallback behavior.
- **Retro Design System**: High-contrast, blocky layouts with a warm `#e5dccb` text on `#211d18` ink background to simulate a vintage paper or 8-bit timing screen.

## Project Structure

- `app.py`: Entry point for the Streamlit application. Configures the multi-page navigation.
- `pages/1_Race_Select.py`: User interface for selecting the historical year/specific Grand Prix and viewing motorsport news headlines.
- `pages/2_Dashboard.py`: Main dashboard view orchestrating the rendering of track info, standings, and sessions.
- `pages/3_Driver_Comparison.py`: Driver comparison and history page with season-first filtering and championship progression charting.
- `sessions.py`: Data layer for FastF1 loading, standings, motorsport RSS news, season driver lists, driver dossiers, and chart inputs.
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
- Streamlit `@st.cache_data` is used for selected API calls such as schedules, standings, and news feeds.
- Driver dossier calculations currently prioritize freshness for accuracy and are resolved on demand.

## Common Issues

### FastF1 takes time on first load

That is normal. It downloads and caches archive data the first time you select a session. Subsequent loads will be much faster.

### Missing Data

If some telemetry traces, speed traps, or tyre fields are empty:
- Not every historical FastF1 session has every field populated. The app is built to handle incomplete data gracefully.
- Standings data from the Ergast API might occasionally be delayed for recent races.
- Driver and season endpoints may occasionally be incomplete depending on upstream API availability. The app includes fallback strategies for season drivers and chart series.

### Driver Comparison Notes

- The comparison chart is season-specific. Select a year first, then select two drivers from that year.
- Championship progression is computed round-by-round; if one endpoint is unavailable, the app falls back to season results data.

## Good Next Improvements

- Add lap filtering by tyre compound or stint.
- Add team color styling to all data tables.
- Optimize loading times further with more aggressive caching.
