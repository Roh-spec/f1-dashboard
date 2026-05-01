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
- **Team Wiki (INCOMPLETE)**: Alphabetical constructor encyclopedia with debut, leader, drivers, races, previous names, and WDC/WCC title-year breakdowns.
- **Retro Design System**: High-contrast, blocky layouts with a warm `#e5dccb` text on `#211d18` ink background to simulate a vintage paper or 8-bit timing screen.

## Project Structure

- `app.py`: Entry point for the Streamlit application. Configures the multi-page navigation.
- `pages/1_Race_Select.py`: User interface for selecting the historical year/specific Grand Prix and viewing motorsport news headlines.
- `pages/2_Dashboard.py`: Main dashboard view orchestrating the rendering of track info, standings, and sessions.
- `pages/3_Driver_Compare.py`: Driver comparison and history page with season-first filtering and championship progression charting.
- `pages/4_Team_Wiki.py`: Team encyclopedia page with season filter, compact team cards, and title history tables.
- `sessions.py`: Data layer for FastF1 loading, Ergast-compatible endpoints, Wikipedia summaries, motorsport RSS news, season driver lists, driver dossiers, and chart inputs.
- `charts.py`: Shared FastF1 chart rendering helpers for telemetry overlays, lap-time traces, position plots, and tyre strategy timelines.
- `track_analysis.py`: Contains circuit image lookup, circuit map rendering, track facts (length, laps, first race, most wins), and track statistics UI.
- `ui.py`: Shared Streamlit UI helpers for custom retro cards, loading states, and compact table/card rendering.
- `.streamlit/config.toml`: Streamlit theme configuration for the app color scheme, monospace font, and minimal toolbar mode.
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
- Streamlit `@st.cache_data` is used for selected API calls such as schedules, standings, news feeds, Ergast-compatible data, and Wikipedia summaries.
- Ergast-compatible data is cached for 1 hour.
- Wikipedia summaries are cached for 24 hours.
- Motorsport RSS headlines are cached for 30 minutes.

## v2.0 Updates

- Replaced `design.py` with a proper Streamlit theme config in `.streamlit/config.toml`; shared custom UI helpers now live in `ui.py`.
- Merged circuit map lookup and rendering into `track_analysis.py`, removing the separate `circuit_map.py` module.
- Added a unified cache layer for Ergast-compatible API calls and Wikipedia summaries with clearer TTLs.
- Kept `charts.py` as a documented shared chart module because it owns reusable FastF1/Matplotlib styling and chart transformations.
- Audited RSS usage: the motorsport news feed is consumed by Race Select and remains cached at 30 minutes.
- Renamed and wired the Driver Compare page as `pages/3_Driver_Compare.py`.
- Confirmed the local import graph has no circular imports.

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

### Team Wiki Notes (INCOMPLETE)

- Team Wiki cards are shown in alphabetical order.
- Some historical constructor lineage mappings and title-era attribution can be incomplete depending on upstream data availability and naming continuity.
- The page displays an explicit INCOMPLETE notice as a reminder that team history stats may require manual verification.

## Good Next Improvements

- Add lap filtering by tyre compound or stint.
- Add team color styling to all data tables.
- Optimize loading times further with more aggressive caching.
