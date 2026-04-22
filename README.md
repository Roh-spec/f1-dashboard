# Retro F1 Timing Room

A Streamlit dashboard for exploring Formula 1 lap data with a bright retro timing-room style. The app uses FastF1 as its main data source and falls back to deterministic demo data if FastF1 is unavailable, disabled, or cannot load the selected session.

## What It Shows

- Real F1 lap timing from FastF1
- Fastest lap and lap-by-lap trend
- Sector 1, 2, and 3 split for the fastest lap
- Speed-trap data where available
- Tyre compound and tyre age
- Stint count
- Track status and lap accuracy flags
- A warm off-white retro interface inspired by paper timing sheets and old CRT monitors

## How To Run

From this folder:

```powershell
cd c:\Users\hudge\WB\F1-dashboard
python -m pip install -r requirements.txt
python -m streamlit run retro_f1_app.py
```

Streamlit will print a local URL, usually:

```text
http://localhost:8501
```

Open that URL in your browser.

## FastF1 Notes

FastF1 needs internet the first time it loads a session. After that, it stores data in:

```text
.fastf1_cache
```

If FastF1 cannot load data, the dashboard does not crash. It switches to demo data and shows a note at the top of the page explaining what happened.

You can also turn off FastF1 manually from the sidebar with:

```text
Use FastF1 data
```

## Project Files

### `retro_f1_app.py`

This is the main Streamlit app file. Think of it as the dashboard page controller.

It does four jobs:

1. Configures the Streamlit page.
2. Loads the retro CSS.
3. Reads user choices from the sidebar.
4. Arranges all dashboard sections on the page.

Important functions:

- `configure_page()`: Sets the Streamlit page title, layout, and sidebar behavior.
- `render_dashboard_page()`: Builds the whole dashboard layout.
- `main()`: Starts the app.

This file intentionally stays small. Most features live in separate files so the project is easier to understand and extend.

### `controls.py`

This file owns the sidebar controls.

It lets the user choose:

- Whether to use FastF1
- Season year
- Grand Prix
- Session type
- Driver

Important function:

- `render_race_controls()`: Draws the sidebar and returns a `SessionConfig` object.

The returned config is passed into the data layer so the app knows which session to load.

### `models.py`

This file contains shared data structures.

It currently defines two dataclasses:

- `SessionConfig`: Stores the user selections from the sidebar.
- `SessionMeta`: Stores information about the loaded session, such as source, event name, driver, team, circuit, status, and notes.

These classes keep the app clean because different modules can pass structured data around instead of loose dictionaries.

### `constants.py`

This file stores app-wide fixed data.

It includes:

- `CURRENT_DRIVERS`: Driver code to driver name mapping.
- `EVENT_PRESETS`: Grand Prix names shown in the sidebar.
- `SESSION_TYPES`: Friendly session names mapped to FastF1 session codes.
- `DEMO_DRIVER_BASE_PACE`: Base lap-time values for fallback demo data.

If you want to add more drivers, events, or adjust demo behavior, this is the first place to look.

### `telemetry.py`

This is the data layer. It decides whether the dashboard gets real FastF1 data or fallback demo data.

Main function:

- `load_session_data(config)`: The public entry point used by the app.

FastF1 path:

- `_try_load_fastf1_data(config)`: Tries to import FastF1, enable cache, load the selected session, filter by driver, and normalize the lap data.
- `_load_fastf1_session(year, grand_prix, session_type)`: Calls FastF1 with `fastf1.get_session(...)` and `session.load(...)`.
- `_normalize_fastf1_laps(laps)`: Converts FastF1 lap columns into the simpler column names used by the dashboard.

Fallback path:

- `_build_demo_session_data(config)`: Creates deterministic fake lap data if FastF1 is unavailable or disabled.
- `_fallback_meta(config, note)`: Creates matching metadata for the fallback mode.

The dashboard expects the data frame to contain columns like:

```text
Lap
Lap Time
Sector 1
Sector 2
Sector 3
Speed
Tyre Life
Compound
Position
Stint
Track Status
Is Accurate
```

### `charts.py`

This file owns chart-specific transformations and chart rendering.

It uses Streamlit native charts:

- `st.line_chart`
- `st.bar_chart`

Important functions:

- `render_lap_chart(data)`: Shows lap time over the session.
- `render_system_chart(data)`: Shows speed and tyre age over laps.
- `render_sector_chart(data)`: Shows sector splits for the fastest lap.

Helper functions:

- `make_lap_chart_data(data)`
- `make_stint_chart_data(data)`
- `make_sector_chart_data(data)`
- `render_chart_shell(title, caption)`

The helper functions keep formatting and data shaping separate from page layout.

### `panels.py`

This file owns the non-chart dashboard sections.

It renders:

- Hero/header section
- Top metric cards
- Strategy/readout cards
- Lap log table

Important functions:

- `render_hero(config, meta)`: Shows the dashboard title and current session badges.
- `render_status_cards(data, meta)`: Shows fastest lap, top speed, tyre age, and consistency.
- `render_strategy_panel(data, meta)`: Shows session status, fastest reference, and tyre notebook cards.
- `render_lap_log(data)`: Shows the detailed lap table.

Small formatting helpers:

- `_format_speed(value)`
- `_format_tyre_age(row)`

### `styles.py`

This file contains the custom CSS for the visual design.

Important function:

- `inject_retro_css()`: Injects the app's CSS into Streamlit.

The current visual direction is:

- Off-white paper background
- Subtle grid texture
- CRT-style scanlines
- Dark ink borders
- Muted red and green accents
- Vintage square cards

If you want to change the look of the dashboard, edit this file first.

### `requirements.txt`

Lists the Python packages needed to run the app:

```text
streamlit
pandas
numpy
fastf1
```

Install them with:

```powershell
python -m pip install -r requirements.txt
```

## Data Flow

The app runs in this order:

1. `retro_f1_app.py` configures the Streamlit page.
2. `styles.py` injects the retro CSS.
3. `controls.py` reads sidebar inputs.
4. `telemetry.py` loads FastF1 data or fallback demo data.
5. `panels.py` renders headings, cards, and the lap log.
6. `charts.py` renders lap, speed/tyre, and sector charts.

In short:

```text
Sidebar controls -> SessionConfig -> FastF1/demo data -> dashboard panels and charts
```

## Common Issues

### FastF1 takes time on first load

That is normal. It downloads and caches archive data the first time you select a session.

### The app shows demo fallback data

This usually means one of these happened:

- FastF1 is not installed.
- The machine has no internet access.
- The selected session is not available.
- FastF1 could not load the selected event/driver combination.
- The `Use FastF1 data` toggle is off.

### Some speed or tyre fields are empty

Not every FastF1 session has every field populated for every lap. The app keeps running and shows `N/A` where needed.

## Good Next Improvements

- Add driver comparison mode.
- Add qualifying session-specific views.
- Add fastest lap telemetry traces with throttle/brake/speed.
- Add lap filtering by compound or stint.
- Add team color styling.
- Add circuit map support from FastF1.
