# 🏎️ F1 Race Control & Telemetry Archive

A broadcast-grade Formula 1 telemetry and race analysis workstation built with **Python**, **Streamlit**, and **FastF1**. Designed around an authentic pit-wall and FIA timing-tower visual language, the dashboard delivers high-fidelity circuit intelligence, lap-by-lap pace traces, corner-by-corner braking telemetry, tyre degradation modeling, incident window timelines, and dynamic official team styling.

---

## ⚡ Key Capabilities & Features

### 1. Broadcast-Grade Visual Design & Typography
- **Circuit Slate Theme**: High-contrast engineering palette (`#0d1117` / `#161b22`) with dynamic official F1 team livery color accents and safety car amber (`#f5a623`) highlights.
- **Technical Typography**: **Titillium Web** for broadcast headings and badges, **JetBrains Mono** for telemetry channels, sector tags, timing deltas, and timestamps, and **Inter** for readable narrative descriptions.
- **Square Motorsport Tabs**: Session and telemetry pill selectors are custom-styled with sharp 0px corners, high-contrast borders, and red active underlines matching professional telemetry software.
- **Sticky Timing-Tower Navigation**: Flush top navigation bar with sharp-angled branding and a sector-line active indicator.

---

### 2. Multi-Page Workstation Architecture

#### 🏁 Race Select (`pages/1_Race_Select.py`)
- **Championship Season Archive**: Fast selection across modern Formula 1 seasons (2000–present) with instant round and venue identification.
- **Live Paddock News Wire**: Real-time RSS aggregation from premier motorsport outlets (*Motorsport.com*, *RaceFans*, *The Race*) with source tags, relative publication timestamps, and direct article routing.
- **One-Click Session Preloading**: Loads FastF1 session data and telemetry into global session state for instant analysis across sub-pages.

#### 📊 Race Analysis & Telemetry (`pages/2_Dashboard.py`)
- **Race Briefing Ribbon**: Dynamic weekend session archive status ribbon:
  - *Standard Grand Prix*: `SESSION ARCHIVE : 3 PRACTICE 1 QUALIFYING 1 RACE`
  - *Sprint Weekend*: Dynamically formatted (e.g. `SESSION ARCHIVE : 1 PRACTICE 1 SPRINT QUALIFYING 1 SPRINT 1 QUALIFYING 1 RACE`).
- **Circuit Intelligence**:
  - High-precision GPS track outline with Start/Finish line and corner numbering markers (T1, T2, etc.).
  - Track records: Most wins, most pole positions, all-time race lap record, and circuit length.
  - Curated Wikipedia track history summaries.
- **Track Condition & Weather Overlay**:
  - OpenF1 environmental telemetry: Air temperature, track temperature, humidity, and wind speed.
  - Incident logs: Safety Car deployments, Virtual Safety Cars, Red Flags, and race control steward decisions.
- **Weekend Sessions in Square Motorsport Tabs**:
  - **Free Practice (FP1, FP2, FP3)**: Fastest lap leaderboards with tire compounds, gap to P1, and lap counts.
  - **Sprint Shootout / Sprint Race**: Full sprint session classification and podium cards for sprint events.
  - **Qualifying Results**: Q1, Q2, and Q3 elimination lap time tables with team-colored top-3 podium cards.
  - **Grand Prix Race Results**: Official race classification, finishing status, points earned, and gap to leader.
- **Qualifying Telemetry & Race Intelligence**:
  - **🗺️ Track Map Dominance**: Lap path segmented into 25 micro-sectors color-coded by the faster driver between P1 and P2 with seamless overlap, corner annotations, and a high-contrast sector dominance stat bar (`[N] SECTORS (X%)`).
  - **🎯 Corner Telemetry Inspector**: Turn-by-turn breakdown analyzing braking onset distance, apex minimum speed, gear selection, and throttle pickup points comparing Driver 1 vs Driver 2, supported by corner advantage metric cards.
  - **⚡ Waveform Telemetry**: Synchronized 10Hz comparative telemetry traces for Speed (km/h), Throttle (%), Brake (on/off), and Gear across the entire qualifying lap.
- **Grand Prix Tyre Intelligence & Pit Windows**:
  - **Tyre Strategy Timeline**: Driver-by-driver stint progression with compound badges (Soft, Medium, Hard, Intermediate, Wet).
  - **Tyre Degradation Curves**: Polynomial degradation modeling with fuel-burnoff compensation (~0.055 s/lap car weight reduction).
  - **Pit Window Strategy Matrix**: Observed degradation rates, fuel-adjusted wear rates, and thermal cliff onset lap indicators derived from clean green-flag racing laps.
- **Qualifying vs. Race Pace Overlays**: Top 3 qualifiers compared across single-lap qualifying attack pace vs. race pace stint medians.
- **World Championship Standings**: Live updated World Drivers' Championship (WDC) and World Constructors' Championship (WCC) standings for the selected round with team-colored progress bars.

#### ⚔️ Driver Comparison (`pages/3_Driver_Compare.py`)
- **Head-to-Head Driver Analysis**: Compare any two drivers active in the selected season.
- **Career Dossiers**: Grand Prix starts, podium finishes, race wins, career points, and best/worst season milestones.
- **Championship Points Progression**: Round-by-round cumulative points chart with dual driver-colored traces.

#### 🏎️ Team Wiki (`pages/4_Team_Wiki.py`)
- **Constructor Dossiers**: Season-scoped team profiles with official team livery accents.
- **Technical & Historical Milestones**: Team principal, base location, debut Grand Prix, total race starts, WDC and WCC title totals, and constructor lineage.
- **Driver Lineup**: Active driver pairings styled with team color indicators.

#### 🏆 Racers' Wiki (`pages/5_Racers_Wiki.py`)
- **Championship Tiers**: Complete historical database categorized by World Drivers' Championship titles won (7x down to 1x, featuring Lando Norris as 2025 WDC).
- **Active Grid Prioritization**: Current on-grid paddock drivers are highlighted at the top of the non-champions catalog, followed by all-time race winners and historical legends.
- **Comprehensive Driver Metrics**: Grand Prix starts, wins, poles, podiums, career points, win/podium percentages, debut race, first win, honors, and Wikipedia biographical dossiers.

---

## 🔬 Data Pipeline & Analytical Modeling

The application implements an end-to-end data processing pipeline combining raw telemetry, official timing, and statistical derivation:

```
 Selection (Season, Round, Event)
        │
        ▼
 Acquire   FastF1 · Jolpica/Ergast · OpenF1 · Wikipedia · RSS        (sessions.py)
        │
        ▼
 Clean     pick_quicklaps · pick_fastest · clean-lap masks · outlier trim
        │
        ▼
 Derive    Distance-aligned delta time · micro-sector winners · corner metrics ·
           median race pace · tyre degradation slope · thermal cliff lap
        │
        ▼
 Encode    Position, livery colors, incident shading, telemetry traces → Matplotlib / Streamlit
```

### 1. Distance-Aligned Telemetry Engine
- **Spatial Alignment**: Rather than comparing telemetry over raw time (which drifts after the first braking point), telemetry channels (Speed, Throttle, Brake, Gear) are aligned over **track distance in meters** using `fastf1.utils.delta_time`.
- **Micro-Sector Dominance**: The circuit is sliced into 25 equidistant segments. Driver split times are calculated via linear interpolation along distance arrays, color-coding each zone with the faster driver's team livery.
- **Corner Metrics Extraction**: Corner apexes are detected via track distance offsets (`circuit_info.corners`), isolating braking onset thresholds, minimum cornering speeds, and throttle application points.

### 2. Tyre Degradation & Pit Window Modeling
- **Outlier Filtering**: In-laps, out-laps, Safety Car periods, and anomalous laps are pruned using `pick_quicklaps` and a $1.15 \times \text{median}$ threshold.
- **Fuel-Burnoff Compensation**: Linear regression models compound wear ($s / \text{lap}$) while compensating for car lightening (~$0.055 \text{ s/lap}$ fuel burn adjustment).
- **Thermal Cliff Detection**: Evaluates consecutive lap times against predicted pace to detect the strategic tyre cliff (lap where performance drops $> 0.7\text{s}$ beyond expected degradation), establishing target pit windows.

---

## 📁 Project Structure

```
F1-dashboard/
├── app.py                      # Application entrypoint, page routing, and top navigation
├── ui.py                       # Circuit Slate design system, CSS styling, components & cards
├── sessions.py                 # FastF1 data loader, Ergast/Jolpica client, Wikipedia & RSS layer
├── charts.py                   # Matplotlib telemetry overlays, micro-sectors, tyre degradation
├── track_analysis.py           # Circuit map generation, historical track milestones, and stats
├── fps.py                      # Free practice session parsing and team-colored card rendering
├── qualifying.py               # Qualifying tables, micro-sector dominance, corner telemetry inspector
├── races.py                    # Race results, tyre compound strategy, degradation & pit matrix
├── pages/
│   ├── 1_Race_Select.py        # Season/round archive selector and live paddock RSS news wire
│   ├── 2_Dashboard.py          # Full weekend analysis, telemetry breakdown, and standings
│   ├── 3_Driver_Compare.py     # Head-to-head driver dossier and championship progression
│   ├── 4_Team_Wiki.py          # Constructor dossiers, technical leadership, and lineage
│   └── 5_Racers_Wiki.py        # Driver encyclopedia with championship tiers & active grid
├── .streamlit/
│   └── config.toml             # Streamlit server and theme configuration
├── circuits/                   # Circuit track layout reference maps
├── requirements.txt            # Python package dependencies
└── README.md                   # Project documentation & engineering roadmap
```

---

## 🚀 Installation & Quick Start

### 1. Prerequisites
- **Python 3.10+** (Tested on Python 3.10, 3.11, 3.12, 3.14)
- `pip` package manager

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/F1-dashboard.git
cd F1-dashboard
```

### 3. Set Up a Virtual Environment (Recommended)
```bash
python -m venv .venv

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Linux / macOS:
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Launch the Dashboard
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

---

## 💾 Data Caching & Performance Architecture

To maintain broadcast-grade performance and avoid API rate limits, the application implements a multi-tiered caching architecture:

- **FastF1 Telemetry Cache (`f1_cache/` / `.fastf1_cache/`)**: Raw telemetry streams (GPS coordinates, speed, throttle, brake, gear, RPM) are cached locally. The first load of an event downloads the session; subsequent accesses are instantaneous.
- **Ergast / Jolpica Championship Cache**: Season schedules, driver standings, and constructor points are cached in-memory with `@st.cache_data(ttl=3600)`.
- **Wikipedia Encyclopedic Cache**: Track dossiers and driver biographical summaries are cached for 24 hours (`ttl=86400`).
- **Paddock RSS Feed Cache**: Live headlines from motorsport news feeds refresh every 30 minutes (`ttl=1800`).

---

## ⚠️ Current Limitations & Known Considerations

- **First-Load Latency**: Loading an un-cached historical session requires downloading multi-megabyte telemetry files from FastF1/FIA data servers. Once cached locally, subsequent loads are instantaneous.
- **Historical Telemetry Gaps**: Sessions prior to 2018 may have incomplete high-frequency GPS or channel telemetry (e.g. brake pedal traces, gear sensor streams, or tyre compound tags) depending on FIA timing feed availability for that era.
- **OpenF1 Weather Availability**: Environmental weather sensors (track temp, air temp, wind speed) and granular race control incident timestamps are sourced from OpenF1 and are primarily available for 2023+ events.
- **Upstream Ergast / Jolpica Delays**: Official championship standings may experience a short latency window immediately following the conclusion of a live Grand Prix until upstream databases finalize classifications.
- **Historical Constructor Lineage**: Historical team rebrands and mergers (e.g., Jordan → Midland → Spyker → Force India → Racing Point → Aston Martin) are mapped based on primary lineage; older title attributions reflect official constructor designations of each era.

---

## 🗺️ Engineering Roadmap & Planned Follow-Ups

The following milestones and architectural improvements are actively planned for upcoming releases:

### 🎮 Telemetry & Interactive Visualizations
- [ ] **Part 2: Cockpit HUD & Steering Wheel Telemetry Playback**
  - Interactive virtual steering wheel display replicating modern F1 digital LCD screens (McLaren/Ferrari/Mercedes layouts).
  - Synchronized lap scrubber with dynamic RPM LED shift lights, gear shifts, speed, and real-time throttle/brake input bars.
  - DRS flap deployment indicator and ERS deployment mode status.
- [ ] **Part 3: Radar Telemetry & Head-to-Head Delta Analyzer**
  - Multi-attribute polar radar plots comparing driving characteristics (high-speed cornering load, mechanical grip, braking threshold, exit traction, and top speed).
  - Continuous micro-second delta time traces along track distance showing exact corner gains and straight-line losses.
- [ ] **Part 4: Global Command Palette & Keyboard Shortcuts**
  - Keyboard-first command palette (`Ctrl+K` / `Cmd+K`) for instantaneous jumping to any season, Grand Prix, driver dossier, or telemetry view.
  - Fuzzy-search for drivers and constructors with direct deep-linking.
- [ ] **Tyre Stint Wear Circuit Map Overlay**
  - Interactive compound wear simulation directly overlaid onto the circuit map showing predicted thermal degradation zones and pit window crossover deltas.

### ☁️ Cloud Infrastructure & Backend Scaling (From Architecture Plan)
- [ ] **Hugging Face Cloud Storage Cache Bootstrap**:
  - Integrate remote cache archive storage using Hugging Face Storage Buckets / Datasets to preload yearly FastF1 cache bundles (`2021.tar.zst`, `2022.tar.zst`, etc.).
  - Reduce Streamlit Cloud cold start latency by bootstrapping only selected season archives into `/tmp/fastf1_cache`.
- [ ] **Offline Cache Warmer (`scripts/warm_cache.py`)**:
  - Independent background script to pre-fetch, compress, and sync newly completed Grand Prix telemetry to cloud storage outside user-facing Streamlit runs.
- [ ] **Data Layer Modularization**:
  - Decouple `sessions.py` into dedicated API client modules (`fastf1_loader.py`, `ergast_client.py`, `openf1_client.py`, `wikipedia_client.py`, `news_client.py`).
  - Move global CSS out of `ui.py` into `assets/styles.css` for enhanced maintainability.
- [ ] **Dynamic Calendar Handling**:
  - Add calendar status awareness for in-progress seasons: automatically detect completed vs. upcoming Grand Prix rounds and set intelligent default selections to the most recently completed race.

---

## 🛠️ Tech Stack

- **Frontend & App Framework**: [Streamlit](https://streamlit.io/)
- **Telemetry Engine**: [FastF1](https://docs.fastf1.dev/)
- **Data Engineering**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Visualization Engine**: [Matplotlib](https://matplotlib.org/), [Altair](https://altair-viz.github.io/)
- **Design & Styling**: Custom Vanilla CSS (Circuit Slate Design System), Google Fonts (*Titillium Web*, *JetBrains Mono*, *Inter*)
- **Data Sources**: FastF1 Live Timing, Ergast / Jolpica API, OpenF1, Wikipedia API, RSS Paddock Feeds
