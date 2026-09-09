# F1 Race Control & Telemetry Archive

A broadcast-grade Formula 1 telemetry and race analysis dashboard built with **Python**, **Streamlit**, and **FastF1**. Designed around an authentic pit-wall and timing-tower visual language, the dashboard delivers high-fidelity circuit intelligence, lap-by-lap pace traces, incident window timelines, telemetry comparisons, and dynamic official team styling.

---

## Key Features

### 1. Broadcast-Grade Visual Design & Typography
- **Circuit Slate Theme**: High-contrast engineering palette featuring cool dark slate (`#0d1117`), dark telemetry panels (`#161b22`), sharp borders (`#262c36`), and **F1 Racing Red (`#e10600`)** primary accents.
- **Dynamic Official F1 Team Colors**: Driver and constructor elements dynamically adapt to their official team branding:
  - **McLaren**: Papaya Orange (`#ff8000`)
  - **Red Bull Racing**: Dark Blue (`#1e41ff`)
  - **Mercedes**: Mercedes Blue (`#00a0dd`)
  - **Ferrari**: Racing Red (`#e80020`)
  - **Aston Martin**: British Racing Green (`#229971`)
  - **Sauber / Kick Sauber**: Neon Green (`#52e252`)
  - **RB / Racing Bulls**: Electric Blue (`#6692ff`)
  - **Williams**: Williams Blue (`#64c4ff`)
  - **Alpine**: Alpine Blue (`#0093cc`)
  - **Haas**: Haas Red (`#e6002b`)
- **Technical Typography**: **Titillium Web** for broadcast headings, **JetBrains Mono** for telemetry channels, sector tags, and timestamps, and **Inter** for readable narrative descriptions.
- **Sticky Timing-Tower Navigation**: Flush top navigation bar with sharp-angled branding and a sector-line active indicator.

### 2. Multi-Page Architecture
- **Race Select (`pages/1_Race_Select.py`)**:
  - Championship season selector (2000–present) and Grand Prix round navigation.
  - Live paddock RSS wire aggregating breaking headlines with source badges (Motorsport.com, RaceFans, The Race).
  - Quick-action routing to telemetry, comparisons, and dossiers.
- **Race Analysis (`pages/2_Dashboard.py`)**:
  - **Race Briefing**: Event dates, venue specs, format indicators, and session archive breakdown.
  - **Circuit Intelligence**: Track layout map with start/finish sectors, track milestones, historical records (most wins, most poles, lap record), and Wikipedia track history.
  - **Session Breakdown**: Individual cards for Free Practice (FP1, FP2, FP3), Sprint Shootout, Sprint, Qualifying, and Grand Prix Race results.
  - **Qualifying & Race Podiums**: P1/P2/P3 podium cards themed in the winning drivers' team colors with official lap times and gaps.
  - **Lap Pace vs. Incident Windows**: High-density pace chart with shaded incident intervals (Safety Car, VSC, Red Flag, Penalty, Investigation) and a dedicated Telemetry Key.
  - **Qualifying vs. Race Pace Overlays**: Top 3 qualifiers compared across Qualifying vs. Race pace using multi-channel telemetry overlays (Speed, Throttle, Brake, Gear, Delta).
  - **Championship Standings**: World Drivers' and Constructors' championship standings updated for the selected round, styled with team-colored progress bars.
- **Driver Comparison (`pages/3_Driver_Compare.py`)**:
  - Season-filtered driver selection for head-to-head analysis.
  - Career dossiers: Grand Prix starts, podiums, wins, career points, and best/worst season milestones.
  - Round-by-round championship points progression chart with dual driver-colored traces.
- **Team Wiki (`pages/4_Team_Wiki.py`)**:
  - Season-scoped constructor dossiers with team color indicators.
  - Technical overview: debut season, team principal, total races, WDC/WCC title history, and constructor lineage.

---

## Project Structure

```
F1-dashboard/
├── app.py                      # Application entrypoint and multi-page routing
├── ui.py                       # Global design system, CSS variables, nav bar, and cards
├── sessions.py                 # FastF1 data loader, Ergast API client, Wikipedia & RSS layer
├── charts.py                   # Matplotlib telemetry overlays, pace charts, tyre strategy
├── track_analysis.py           # Circuit map generation, historical track milestones, and stats
├── fps.py                      # Practice session parsing and team-colored card rendering
├── qualifying.py               # Qualifying tables, session intelligence, and podium cards
├── races.py                    # Race results, tyre compound strategy, and podium rendering
├── pages/
│   ├── 1_Race_Select.py        # Archive selector and live news wire
│   ├── 2_Dashboard.py          # Full race weekend analysis and telemetry breakdown
│   ├── 3_Driver_Compare.py     # Head-to-head driver dossier and points progression
│   └── 4_Team_Wiki.py          # Constructor dossiers, lineage, and title records
├── .streamlit/
│   └── config.toml             # Streamlit server and theme configuration
├── circuits/                   # Local circuit track layout maps
├── requirements.txt            # Python package dependencies
└── README.md                   # Project documentation
```

---

## Installation & Setup

### 1. Prerequisites
- **Python 3.10+**
- `pip` package manager

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/F1-dashboard.git
cd F1-dashboard
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Dashboard
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## Data Caching & Performance

The dashboard implements multi-tiered caching to minimize API latency:
- **FastF1 Telemetry Cache**: Raw session data and telemetry streams are persisted locally in `.fastf1_cache/` and `f1_cache/`. Initial load of a session downloads archive data; subsequent loads are instantaneous.
- **Ergast Championship Data**: Season schedules, standings, and driver lists are cached via Streamlit `@st.cache_data(ttl=3600)`.
- **Wikipedia Summaries**: Track and constructor encyclopedic entries are cached for 24 hours (`ttl=86400`).
- **Motorsport News Wire**: RSS paddock headlines refresh every 30 minutes (`ttl=1800`).

---

## Tech Stack

- **Framework**: Streamlit
- **Telemetry Engine**: FastF1
- **Data Manipulation**: Pandas, NumPy
- **Visualizations**: Matplotlib, Altair
- **Styling**: Vanilla CSS, Google Fonts (Titillium Web, JetBrains Mono, Inter)
- **External Data**: Ergast / Jolpica F1 API, Wikipedia API, Motorsport RSS feeds
