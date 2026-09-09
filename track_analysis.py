import math
import os
import random
import re
import unicodedata
from difflib import SequenceMatcher
from html import escape
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", os.path.join(os.getcwd(), "f1_cache", "matplotlib"))
os.makedirs(os.environ["MPLCONFIGDIR"], exist_ok=True)

import fastf1
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from sessions import setup_fastf1_cache


SUPPORTED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

CIRCUIT_ALIASES = {
    "melbourne": "Albert Park Circuit",
    "australian grand prix": "Albert Park Circuit",
    "sakhir": "Bahrain International Circuit",
    "bahrain grand prix": "Bahrain International Circuit",
    "bahrain outer": "Bahrain International Circuit Outer Track",
    "shanghai": "Shanghai International Circuit",
    "chinese grand prix": "Shanghai International Circuit",
    "suzuka": "Suzuka International Racing Course",
    "japanese grand prix": "Suzuka International Racing Course",
    "miami": "Miami International Autodrome",
    "miami gardens": "Miami International Autodrome",
    "imola": "Autodromo Enzo e Dino Ferrari",
    "emilia romagna grand prix": "Autodromo Enzo e Dino Ferrari",
    "monaco": "Circuit de Monaco",
    "spanish grand prix": "Circuit de Barcelona-Catalunya",
    "barcelona": "Circuit de Barcelona-Catalunya",
    "montreal": "Circuit Gilles-Villeneuve",
    "canadian grand prix": "Circuit Gilles-Villeneuve",
    "spielberg": "Red Bull Ring",
    "austrian grand prix": "Red Bull Ring",
    "silverstone": "Silverstone Circuit",
    "british grand prix": "Silverstone Circuit",
    "spa francorchamps": "Circuit de Spa-Francorchamps",
    "spa-francorchamps": "Circuit de Spa-Francorchamps",
    "circuit de spa francorchamps": "Circuit de Spa-Francorchamps",
    "belgian grand prix": "Circuit de Spa-Francorchamps",
    "budapest": "Hungaroring",
    "hungarian grand prix": "Hungaroring",
    "zandvoort": "Circuit Zandvoort",
    "dutch grand prix": "Circuit Zandvoort",
    "monza": "Autodromo Nazionale Monza",
    "italian grand prix": "Autodromo Nazionale Monza",
    "baku": "Baku City Circuit",
    "azerbaijan grand prix": "Baku City Circuit",
    "marina bay": "Marina Bay Street Circuit",
    "singapore grand prix": "Marina Bay Street Circuit",
    "austin": "Circuit of the Americas",
    "united states grand prix": "Circuit of the Americas",
    "mexico city": "Autodromo Hermanos Rodriguez",
    "mexico city grand prix": "Autodromo Hermanos Rodriguez",
    "sao paulo": "Autodromo Jose Carlos Pace",
    "brazilian grand prix": "Autodromo Jose Carlos Pace",
    "interlagos": "Autodromo Jose Carlos Pace",
    "las vegas": "Las Vegas Strip Circuit",
    "las vegas grand prix": "Las Vegas Strip Circuit",
    "yas island": "Yas Marina Circuit",
    "abu dhabi grand prix": "Yas Marina Circuit",
    "istanbul": "Intercity Istanbul Park Circuit",
    "turkish grand prix": "Intercity Istanbul Park Circuit",
    "nurburgring": "Nurburgring",
    "eifel grand prix": "Nurburgring",
    "portimao": "Autodromo Internacional do Algarve",
    "portuguese grand prix": "Autodromo Internacional do Algarve",
    "losail": "Losail 2023",
    "lusail": "Losail 2023",
    "qatar grand prix": "Losail 2023",
    "jeddah": "Jeddah Street Circuit",
    "saudi arabian grand prix": "Jeddah Street Circuit",
    "sochi": "Sochi Autodrom",
    "russian grand prix": "Sochi Autodrom",
}

TRACK_FACTS = {
    "albert park circuit": {
        "first_f1": "1996",
        "races": "28 Australian GPs through 2025",
        "most_wins": "Michael Schumacher (4 wins)",
        "most_poles": "Lewis Hamilton (8 poles)",
        "lap_record": "Charles Leclerc - 1:19.813 (2024)",
        "length": "5.278 km",
        "laps": "58",
    },
    "bahrain international circuit": {
        "first_f1": "2004",
        "races": "21 Bahrain GPs through 2025",
        "most_wins": "Lewis Hamilton (5 wins)",
        "most_poles": "Lewis Hamilton (3 poles)",
        "lap_record": "Pedro de la Rosa - 1:31.447 (2005)",
        "length": "5.412 km",
        "laps": "57",
    },
    "shanghai international circuit": {
        "first_f1": "2004",
        "races": "18 Chinese GPs through 2025",
        "most_wins": "Lewis Hamilton (6 wins)",
        "most_poles": "Lewis Hamilton (6 poles)",
        "lap_record": "Michael Schumacher - 1:32.238 (2004)",
        "length": "5.451 km",
        "laps": "56",
    },
    "suzuka international racing course": {
        "first_f1": "1987",
        "races": "34 Japanese GPs through 2025",
        "most_wins": "Michael Schumacher (6 wins)",
        "most_poles": "Michael Schumacher (8 poles)",
        "lap_record": "Lewis Hamilton - 1:30.983 (2019)",
        "length": "5.807 km",
        "laps": "53",
    },
    "miami international autodrome": {
        "first_f1": "2022",
        "races": "4 Miami GPs through 2025",
        "most_wins": "Max Verstappen (2 wins)",
        "most_poles": "Max Verstappen & Charles Leclerc (1 pole each)",
        "lap_record": "Max Verstappen - 1:29.708 (2023)",
        "length": "5.412 km",
        "laps": "57",
    },
    "autodromo enzo e dino ferrari": {
        "first_f1": "1980",
        "races": "31 GPs (Imola / San Marino / Emilia Romagna)",
        "most_wins": "Michael Schumacher (7 wins)",
        "most_poles": "Ayrton Senna (8 poles)",
        "lap_record": "Lewis Hamilton - 1:15.484 (2020)",
        "length": "4.909 km",
        "laps": "63",
    },
    "circuit de monaco": {
        "first_f1": "1950",
        "races": "70+ Monaco GPs",
        "most_wins": "Ayrton Senna (6 wins)",
        "most_poles": "Ayrton Senna (5 poles)",
        "lap_record": "Lewis Hamilton - 1:12.909 (2021)",
        "length": "3.337 km",
        "laps": "78",
    },
    "circuit de barcelona catalunya": {
        "first_f1": "1991",
        "races": "34 Spanish GPs since 1991",
        "most_wins": "Michael Schumacher & Lewis Hamilton (6 wins each)",
        "most_poles": "Michael Schumacher (7 poles)",
        "lap_record": "Max Verstappen - 1:16.330 (2023)",
        "length": "4.657 km",
        "laps": "66",
    },
    "circuit gilles villeneuve": {
        "first_f1": "1978",
        "races": "43 Canadian GPs since 1978",
        "most_wins": "Michael Schumacher & Lewis Hamilton (7 wins each)",
        "most_poles": "Michael Schumacher & Lewis Hamilton (6 poles each)",
        "lap_record": "Valtteri Bottas - 1:13.078 (2019)",
        "length": "4.361 km",
        "laps": "70",
    },
    "red bull ring": {
        "first_f1": "1970",
        "races": "38 Austrian GPs",
        "most_wins": "Max Verstappen (5 wins)",
        "most_poles": "Max Verstappen (4 poles)",
        "lap_record": "Carlos Sainz - 1:05.619 (2020)",
        "length": "4.318 km",
        "laps": "71",
    },
    "silverstone circuit": {
        "first_f1": "1950",
        "races": "58 British GPs at Silverstone",
        "most_wins": "Lewis Hamilton (9 wins)",
        "most_poles": "Lewis Hamilton (8 poles)",
        "lap_record": "Max Verstappen - 1:27.097 (2020)",
        "length": "5.891 km",
        "laps": "52",
    },
    "hungaroring": {
        "first_f1": "1986",
        "races": "39 Hungarian GPs since 1986",
        "most_wins": "Lewis Hamilton (8 wins)",
        "most_poles": "Lewis Hamilton (9 poles)",
        "lap_record": "Lewis Hamilton - 1:16.627 (2020)",
        "length": "4.381 km",
        "laps": "70",
    },
    "circuit de spa francorchamps": {
        "first_f1": "1950",
        "races": "57 Belgian GPs at Spa",
        "most_wins": "Michael Schumacher (6 wins)",
        "most_poles": "Lewis Hamilton (6 poles)",
        "lap_record": "Sergio Perez - 1:44.701 (2024)",
        "length": "7.004 km",
        "laps": "44",
    },
    "circuit zandvoort": {
        "first_f1": "1952",
        "races": "34 Dutch GPs",
        "most_wins": "Jim Clark (4 wins)",
        "most_poles": "René Arnoux (3 poles)",
        "lap_record": "Lewis Hamilton - 1:11.097 (2021)",
        "length": "4.259 km",
        "laps": "72",
    },
    "autodromo nazionale monza": {
        "first_f1": "1950",
        "races": "74 Italian GPs at Monza",
        "most_wins": "Michael Schumacher & Lewis Hamilton (5 wins each)",
        "most_poles": "Lewis Hamilton (7 poles)",
        "lap_record": "Rubens Barrichello - 1:21.046 (2004)",
        "length": "5.793 km",
        "laps": "53",
    },
    "baku city circuit": {
        "first_f1": "2016",
        "races": "8 Azerbaijan GPs",
        "most_wins": "Sergio Perez (2 wins)",
        "most_poles": "Charles Leclerc (4 poles)",
        "lap_record": "Charles Leclerc - 1:43.009 (2019)",
        "length": "6.003 km",
        "laps": "51",
    },
    "marina bay street circuit": {
        "first_f1": "2008",
        "races": "15 Singapore GPs",
        "most_wins": "Sebastian Vettel (5 wins)",
        "most_poles": "Lewis Hamilton & Sebastian Vettel (4 poles each)",
        "lap_record": "Daniel Ricciardo - 1:34.486 (2024)",
        "length": "4.940 km",
        "laps": "62",
    },
    "circuit of the americas": {
        "first_f1": "2012",
        "races": "12 US GPs in Austin",
        "most_wins": "Lewis Hamilton (5 wins)",
        "most_poles": "Lewis Hamilton (3 poles)",
        "lap_record": "Charles Leclerc - 1:36.169 (2019)",
        "length": "5.513 km",
        "laps": "56",
    },
    "autodromo hermanos rodriguez": {
        "first_f1": "1963",
        "races": "24 Mexico City GPs",
        "most_wins": "Max Verstappen (5 wins)",
        "most_poles": "Jim Clark (4 poles)",
        "lap_record": "Valtteri Bottas - 1:17.774 (2021)",
        "length": "4.304 km",
        "laps": "71",
    },
    "autodromo jose carlos pace": {
        "first_f1": "1973",
        "races": "41 Brazilian GPs at Interlagos",
        "most_wins": "Michael Schumacher (4 wins)",
        "most_poles": "Ayrton Senna (6 poles)",
        "lap_record": "Valtteri Bottas - 1:10.540 (2018)",
        "length": "4.309 km",
        "laps": "71",
    },
    "las vegas strip circuit": {
        "first_f1": "2023",
        "races": "2 Las Vegas GPs",
        "most_wins": "Max Verstappen & George Russell (1 win each)",
        "most_poles": "Charles Leclerc & George Russell (1 pole each)",
        "lap_record": "Lando Norris - 1:34.876 (2024)",
        "length": "6.201 km",
        "laps": "50",
    },
    "yas marina circuit": {
        "first_f1": "2009",
        "races": "16 Abu Dhabi GPs",
        "most_wins": "Lewis Hamilton (5 wins)",
        "most_poles": "Lewis Hamilton (5 poles)",
        "lap_record": "Kevin Magnussen - 1:25.637 (2024)",
        "length": "5.281 km",
        "laps": "58",
    },
    "losail 2023": {
        "first_f1": "2021",
        "races": "3 Qatar GPs",
        "most_wins": "Max Verstappen (2 wins)",
        "most_poles": "Lewis Hamilton, Max Verstappen, George Russell (1 pole each)",
        "lap_record": "Max Verstappen - 1:24.319 (2023)",
        "length": "5.419 km",
        "laps": "57",
    },
    "losail until 2023": {
        "first_f1": "2021",
        "races": "Qatar GP host (original)",
        "most_wins": "Lewis Hamilton (1 win)",
        "most_poles": "Lewis Hamilton (1 pole)",
        "lap_record": "Max Verstappen - 1:23.196 (2021)",
        "length": "5.380 km",
        "laps": "57",
    },
    "jeddah street circuit": {
        "first_f1": "2021",
        "races": "4 Saudi Arabian GPs",
        "most_wins": "Max Verstappen (2 wins)",
        "most_poles": "Sergio Perez (2 poles)",
        "lap_record": "Lewis Hamilton - 1:30.734 (2021)",
        "length": "6.174 km",
        "laps": "50",
    },
    "autodromo internacional do algarve": {
        "first_f1": "2020",
        "races": "2 Portuguese GPs (2020-2021)",
        "most_wins": "Lewis Hamilton (2 wins)",
        "most_poles": "Valtteri Bottas & Lewis Hamilton (1 pole each)",
        "lap_record": "Lewis Hamilton - 1:18.750 (2020)",
        "length": "4.653 km",
        "laps": "66",
    },
    "intercity istanbul park circuit": {
        "first_f1": "2005",
        "races": "9 Turkish GPs",
        "most_wins": "Felipe Massa (3 wins)",
        "most_poles": "Felipe Massa (3 poles)",
        "lap_record": "Juan Pablo Montoya - 1:24.770 (2005)",
        "length": "5.338 km",
        "laps": "58",
    },
    "sochi autodrom": {
        "first_f1": "2014",
        "races": "8 Russian GPs (2014-2021)",
        "most_wins": "Lewis Hamilton (5 wins)",
        "most_poles": "Lewis Hamilton & Nico Rosberg (2 poles each)",
        "lap_record": "Lewis Hamilton - 1:35.761 (2019)",
        "length": "5.848 km",
        "laps": "53",
    },
    "bahrain international circuit outer track": {
        "first_f1": "2020",
        "races": "1 Sakhir GP (2020)",
        "most_wins": "Sergio Perez (1 win)",
        "most_poles": "Valtteri Bottas (1 pole)",
        "lap_record": "George Russell - 0:55.404 (2020)",
        "length": "3.543 km",
        "laps": "87",
    },
    "nurburgring": {
        "first_f1": "1951",
        "races": "German, European, and Eifel GPs",
        "most_wins": "Michael Schumacher (5 wins)",
        "most_poles": "Michael Schumacher (3 poles)",
        "lap_record": "Max Verstappen - 1:28.139 (2020)",
        "length": "5.148 km",
        "laps": "60",
    },
}


def render_circuit_map(year: int, race_name: str, event) -> None:
    local_map = find_circuit_image(event)

    st.markdown("<h3>Circuit Map</h3>", unsafe_allow_html=True)
    if local_map is not None:
        st.image(str(local_map), caption=local_map.stem, use_container_width=True)
        return

    points, source_label = _get_circuit_points(year, race_name, event["EventName"])

    fig, ax = plt.subplots(figsize=(5.8, 3.8), dpi=140)
    fig.patch.set_facecolor("#161b22")
    ax.set_facecolor("#161b22")

    ax.plot(points["X"], points["Y"], color="#262c36", linewidth=5.0, solid_capstyle="round")
    ax.plot(points["X"], points["Y"], color="#e10600", linewidth=2.0, solid_capstyle="round")
    ax.scatter(points["X"], points["Y"], s=26, color="#f0f3f6", edgecolors="#e10600", linewidths=1.0, zorder=3)

    start = points.iloc[0]
    ax.scatter([start["X"]], [start["Y"]], s=64, marker="s", color="#e10600", edgecolors="#f0f3f6", linewidths=1.4, zorder=4)
    ax.text(start["X"], start["Y"], "S", ha="center", va="center", fontsize=8, weight="bold", color="#ffffff", zorder=5)

    ax.set_title(str(event["EventName"]).upper(), fontsize=9, color="#f0f3f6", pad=10, fontweight="bold", fontfamily="monospace")
    ax.text(
        0.02,
        0.03,
        source_label,
        transform=ax.transAxes,
        fontsize=7,
        color="#8b949e",
        fontweight="bold",
    )
    ax.set_aspect("equal", adjustable="datalim")
    ax.axis("off")
    fig.tight_layout(pad=0.5)
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def find_circuit_image(event) -> Path | None:
    circuit_dir = Path("circuits")
    if not circuit_dir.exists():
        return None

    images = [
        path
        for path in circuit_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
    ]
    if not images:
        return None

    lookup = {_normalize(path.stem): path for path in images}
    alias_lookup = {_normalize(key): value for key, value in CIRCUIT_ALIASES.items()}

    # Core identification terms (exclude OfficialEventName which often contains title sponsors like Qatar Airways)
    candidates = [
        event.get("CircuitName"),
        event.get("Location"),
        event.get("EventName"),
    ]

    try:
        year = event["EventDate"].year
    except Exception:
        year = 2024

    # True Qatar GP detection (based on location/event name, not sponsor names)
    is_true_qatar = any(
        c and any(term in str(c).lower() for term in ("lusail", "losail")) or str(c).lower() == "qatar grand prix"
        for c in candidates
    )

    if is_true_qatar:
        target = "losail 2023" if year >= 2023 else "losail until 2023"
        if target in lookup:
            return lookup[target]

    for candidate in candidates:
        candidate_key = _normalize(candidate)
        if not candidate_key:
            continue

        alias = alias_lookup.get(candidate_key)
        if alias and _normalize(alias) in lookup:
            return lookup[_normalize(alias)]

        if candidate_key in lookup:
            return lookup[candidate_key]

        for image_key, path in lookup.items():
            if candidate_key in image_key or image_key in candidate_key:
                return path

    best_path = None
    best_score = 0.0
    normalized_candidates = [_normalize(candidate) for candidate in candidates if _normalize(candidate)]
    for candidate_key in normalized_candidates:
        for image_key, path in lookup.items():
            score = SequenceMatcher(None, candidate_key, image_key).ratio()
            if score > best_score:
                best_score = score
                best_path = path

    return best_path if best_score >= 0.52 else None


@st.cache_data(show_spinner=False)
def _get_circuit_points(year: int, race_name: str, event_name: str) -> tuple[pd.DataFrame, str]:
    setup_fastf1_cache()
    try:
        session = fastf1.get_session(year, race_name, "R")
        session.load(laps=False, telemetry=False, weather=False, messages=False)

        circuit_info = session.get_circuit_info()
        corners = circuit_info.corners[["X", "Y"]].dropna().copy()
        if len(corners) >= 4:
            corners = pd.concat([corners, corners.iloc[[0]]], ignore_index=True)
            return corners, "FASTF1 CIRCUIT MARKERS"
    except Exception:
        pass

    return _build_fallback_outline(event_name), "ARCHIVE MAP FALLBACK"


def _build_fallback_outline(event_name: str) -> pd.DataFrame:
    rng = random.Random(event_name)
    point_count = rng.randint(11, 15)
    base_rotation = rng.uniform(0, math.tau)
    points = []

    for index in range(point_count):
        angle = base_rotation + (math.tau * index / point_count)
        radius = 1.0 + rng.uniform(-0.28, 0.32)
        x_scale = rng.uniform(1.15, 1.65)
        y_scale = rng.uniform(0.72, 1.08)
        x = math.cos(angle) * radius * x_scale
        y = math.sin(angle) * radius * y_scale
        points.append((x, y))

    points.append(points[0])
    return pd.DataFrame(points, columns=["X", "Y"])


def render_track_analysis(event) -> None:
    facts = get_track_facts(event)
    with st.container(key="track_analysis_list"):
        st.markdown("<h3>Track Analysis</h3>", unsafe_allow_html=True)
        st.markdown(
            "\n".join(
                [
                    f"- **F1 debut:** {facts.get('first_f1', 'Archive pending')}",
                    f"- **Number of races:** {facts.get('races', 'Archive pending')}",
                    f"- **Track length:** {facts.get('length', 'Archive pending')}",
                    f"- **Race laps:** {facts.get('laps', 'Archive pending')}",
                    f"- **Total distance:** {_total_distance(facts)}",
                ]
            )
        )


def render_circuit_records(event) -> None:
    """Renders the top historical circuit milestones: Most Wins, Most Poles, and Fastest Lap (Lap Record)."""
    facts = get_track_facts(event)
    most_wins = facts.get("most_wins", "Archive pending")
    most_poles = facts.get("most_poles", "Archive pending")
    lap_record = facts.get("lap_record", "Archive pending")

    with st.container(key="circuit_records_box"):
        st.markdown("<p class='section-kicker'>Circuit Milestones</p>", unsafe_allow_html=True)
        st.markdown("<h3>Track Records</h3>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div class="circuit-records-grid">
                <div class="record-card">
                    <div class="record-header">
                        <span class="record-label">MOST WINS</span>
                    </div>
                    <div class="record-value">{escape(most_wins)}</div>
                </div>
                <div class="record-card">
                    <div class="record-header">
                        <span class="record-label">MOST POLES</span>
                    </div>
                    <div class="record-value">{escape(most_poles)}</div>
                </div>
                <div class="record-card">
                    <div class="record-header">
                        <span class="record-label">FASTEST LAP</span>
                    </div>
                    <div class="record-value record-timing">{escape(lap_record)}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# Backward compatibility alias
render_circuit_winners = render_circuit_records


def get_track_facts(event) -> dict[str, str]:
    local_map = find_circuit_image(event)
    keys = []
    if local_map is not None:
        keys.append(_normalize(local_map.stem))

    keys.extend(
        _normalize(event.get(field))
        for field in ("CircuitName", "Location", "EventName")
    )

    for key in keys:
        if key in TRACK_FACTS:
            return TRACK_FACTS[key]

        # Check alias
        alias = CIRCUIT_ALIASES.get(key)
        if alias and _normalize(alias) in TRACK_FACTS:
            return TRACK_FACTS[_normalize(alias)]

    return {
        "first_f1": "Archive pending",
        "races": "Archive pending",
        "most_wins": "Archive pending",
        "most_poles": "Archive pending",
        "lap_record": "Archive pending",
        "length": "Archive pending",
        "laps": "Archive pending",
    }


def _total_distance(facts: dict[str, str]) -> str:
    try:
        length = float(facts.get("length", "").replace("km", "").strip())
        laps = int(facts.get("laps", 0))
        return f"{length * laps:.3f} km"
    except (ValueError, TypeError):
        return "Archive pending"


def _normalize(value) -> str:
    if value is None:
        return ""

    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(character for character in text if not unicodedata.combining(character))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())
