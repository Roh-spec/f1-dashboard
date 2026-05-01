import math
import os
import random
import re
import unicodedata
from difflib import SequenceMatcher
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
    "spa francorchamps": "Belgium-1-scaled",
    "spa-francorchamps": "Belgium-1-scaled",
    "belgian grand prix": "Belgium-1-scaled",
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
}

TRACK_FACTS = {
    "albert park circuit": {
        "first_f1": "1996",
        "races": "28 Australian GPs through 2025",
        "winners": "Michael Schumacher 4, Jenson Button 3, Sebastian Vettel 3",
        "length": "5.278 km",
        "laps": "58",
    },
    "bahrain international circuit": {
        "first_f1": "2004",
        "races": "21 Bahrain GPs through 2025",
        "winners": "Lewis Hamilton 5, Sebastian Vettel 4, Fernando Alonso 3",
        "length": "5.412 km",
        "laps": "57",
    },
    "shanghai international circuit": {
        "first_f1": "2004",
        "races": "18 Chinese GPs through 2025",
        "winners": "Lewis Hamilton 6, Fernando Alonso 2, Nico Rosberg 1",
        "length": "5.451 km",
        "laps": "56",
    },
    "suzuka international racing course": {
        "first_f1": "1987",
        "races": "Japanese GP regular host",
        "winners": "Michael Schumacher 6, Lewis Hamilton 5, Sebastian Vettel 4",
        "length": "5.807 km",
        "laps": "53",
    },
    "miami international autodrome": {
        "first_f1": "2022",
        "races": "4 Miami GPs through 2025",
        "winners": "Max Verstappen 2, Lando Norris 1, Oscar Piastri 1",
        "length": "5.412 km",
        "laps": "57",
    },
    "autodromo enzo e dino ferrari": {
        "first_f1": "1980",
        "races": "Italian, San Marino, and Emilia Romagna GPs",
        "winners": "Michael Schumacher 7, Max Verstappen 3, Ayrton Senna 3",
        "length": "4.909 km",
        "laps": "63",
    },
    "circuit de monaco": {
        "first_f1": "1950",
        "races": "70+ Monaco GPs",
        "winners": "Ayrton Senna 6, Graham Hill 5, Michael Schumacher 5",
        "length": "3.337 km",
        "laps": "78",
    },
    "circuit de barcelona catalunya": {
        "first_f1": "1991",
        "races": "Spanish GP host since 1991",
        "winners": "Lewis Hamilton 6, Michael Schumacher 6, Max Verstappen 4",
        "length": "4.657 km",
        "laps": "66",
    },
    "circuit gilles villeneuve": {
        "first_f1": "1978",
        "races": "Canadian GP host since 1978",
        "winners": "Michael Schumacher 7, Lewis Hamilton 7, Nelson Piquet 3",
        "length": "4.361 km",
        "laps": "70",
    },
    "red bull ring": {
        "first_f1": "1970",
        "races": "Austrian GP eras at Osterreichring/A1 Ring/Red Bull Ring",
        "winners": "Max Verstappen 5, Alain Prost 3, Ronnie Peterson 2",
        "length": "4.318 km",
        "laps": "71",
    },
    "silverstone circuit": {
        "first_f1": "1950",
        "races": "British GP cornerstone venue",
        "winners": "Lewis Hamilton 9, Jim Clark 5, Alain Prost 5",
        "length": "5.891 km",
        "laps": "52",
    },
    "belgium 1 scaled": {
        "first_f1": "1950",
        "races": "Belgian GP classic venue",
        "winners": "Michael Schumacher 6, Ayrton Senna 5, Jim Clark 4",
        "length": "7.004 km",
        "laps": "44",
    },
    "hungaroring": {
        "first_f1": "1986",
        "races": "Hungarian GP host since 1986",
        "winners": "Lewis Hamilton 8, Michael Schumacher 4, Ayrton Senna 3",
        "length": "4.381 km",
        "laps": "70",
    },
    "circuit zandvoort": {
        "first_f1": "1952",
        "races": "Dutch GP historic and modern host",
        "winners": "Jim Clark 4, Max Verstappen 3, Jackie Stewart 3",
        "length": "4.259 km",
        "laps": "72",
    },
    "autodromo nazionale monza": {
        "first_f1": "1950",
        "races": "Italian GP's long-time home",
        "winners": "Michael Schumacher 5, Lewis Hamilton 5, Nelson Piquet 4",
        "length": "5.793 km",
        "laps": "53",
    },
    "baku city circuit": {
        "first_f1": "2016",
        "races": "Azerbaijan/European GPs",
        "winners": "Sergio Perez 2, Nico Rosberg 1, Daniel Ricciardo 1",
        "length": "6.003 km",
        "laps": "51",
    },
    "marina bay street circuit": {
        "first_f1": "2008",
        "races": "Singapore GP night-race host",
        "winners": "Sebastian Vettel 5, Lewis Hamilton 4, Fernando Alonso 2",
        "length": "4.940 km",
        "laps": "62",
    },
    "circuit of the americas": {
        "first_f1": "2012",
        "races": "United States GP host since 2012",
        "winners": "Lewis Hamilton 5, Max Verstappen 3, Charles Leclerc 1",
        "length": "5.513 km",
        "laps": "56",
    },
    "autodromo hermanos rodriguez": {
        "first_f1": "1963",
        "races": "Mexican/Mexico City GP venue",
        "winners": "Max Verstappen 5, Jim Clark 3, Alain Prost 2",
        "length": "4.304 km",
        "laps": "71",
    },
    "autodromo jose carlos pace": {
        "first_f1": "1973",
        "races": "Brazilian/Sao Paulo GP host",
        "winners": "Michael Schumacher 4, Sebastian Vettel 3, Carlos Reutemann 3",
        "length": "4.309 km",
        "laps": "71",
    },
    "las vegas strip circuit": {
        "first_f1": "2023",
        "races": "Las Vegas GP host since 2023",
        "winners": "Max Verstappen 1, George Russell 1",
        "length": "6.201 km",
        "laps": "50",
    },
    "yas marina circuit": {
        "first_f1": "2009",
        "races": "Abu Dhabi GP host since 2009",
        "winners": "Lewis Hamilton 5, Max Verstappen 4, Sebastian Vettel 3",
        "length": "5.281 km",
        "laps": "58",
    },
    "qatar grand prix": {
        "first_f1": "2021",
        "races": "Qatar GP host",
        "winners": "Max Verstappen 1, Lewis Hamilton 1",
        "length": "5.419 km",
        "laps": "57",
    },
    "jeddah street circuit": {
        "first_f1": "2021",
        "races": "Saudi Arabian GP host since 2021",
        "winners": "Max Verstappen 2, Lewis Hamilton 1, Sergio Perez 1",
        "length": "6.174 km",
        "laps": "50",
    },
    "autodromo internacional do algarve": {
        "first_f1": "2020",
        "races": "Portuguese GP host (2020-2021)",
        "winners": "Lewis Hamilton 2",
        "length": "4.653 km",
        "laps": "66",
    },
    "intercity istanbul park circuit": {
        "first_f1": "2005",
        "races": "Turkish GP host",
        "winners": "Felipe Massa 3, Lewis Hamilton 2, Kimi Raikkonen 1",
        "length": "5.338 km",
        "laps": "58",
    },
    "sochi autodrom": {
        "first_f1": "2014",
        "races": "Russian GP host (2014-2021)",
        "winners": "Lewis Hamilton 5, Valtteri Bottas 2, Nico Rosberg 1",
        "length": "5.848 km",
        "laps": "53",
    },
    "bahrain international circuit outer track": {
        "first_f1": "2020",
        "races": "Sakhir GP host (2020)",
        "winners": "Sergio Perez 1",
        "length": "3.543 km",
        "laps": "87",
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
    fig.patch.set_facecolor("#fff0e7")
    ax.set_facecolor("#fff0e7")

    ax.plot(points["X"], points["Y"], color="#171717", linewidth=4.0, solid_capstyle="round")
    ax.plot(points["X"], points["Y"], color="#37b4c8", linewidth=1.6, solid_capstyle="round")
    ax.scatter(points["X"], points["Y"], s=26, color="#f06a8a", edgecolors="#171717", linewidths=0.8, zorder=3)

    start = points.iloc[0]
    ax.scatter([start["X"]], [start["Y"]], s=58, marker="s", color="#ffffff", edgecolors="#171717", linewidths=1.2, zorder=4)
    ax.text(start["X"], start["Y"], "S", ha="center", va="center", fontsize=8, weight="bold", color="#171717", zorder=5)

    ax.set_title(str(event["EventName"]).upper(), fontsize=9, color="#171717", pad=10, fontweight="bold")
    ax.text(
        0.02,
        0.03,
        source_label,
        transform=ax.transAxes,
        fontsize=7,
        color="#6b4b3b",
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
    candidates = [
        event.get("CircuitName"),
        event.get("Location"),
        event.get("EventName"),
        event.get("OfficialEventName"),
    ]

    try:
        year = event["EventDate"].year
    except Exception:
        year = 2024

    is_qatar = any(
        candidate and any(term in str(candidate).lower() for term in ("qatar", "lusail", "losail"))
        for candidate in candidates
    )

    if is_qatar:
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

    return best_path if best_score >= 0.58 else None


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
                    f"- **F1 debut:** {facts['first_f1']}",
                    f"- **Number of races:** {facts['races']}",
                    f"- **Track length:** {facts['length']}",
                    f"- **Race laps:** {facts['laps']}",
                    f"- **Total distance:** {_total_distance(facts)}",
                ]
            )
        )


def render_circuit_winners(event) -> None:
    winners = get_track_facts(event)["winners"]
    with st.container(key="circuit_winners_list"):
        st.markdown("<h3>Most wins</h3>", unsafe_allow_html=True)
        for winner in _split_winners(winners):
            if winner != "Archive pending" and winner[-1].isdigit():
                parts = winner.rsplit(" ", 1)
                count = parts[1]
                word = "win" if count == "1" else "wins"
                winner = f"{parts[0]}: {count} {word}"
            st.markdown(f"- {winner}")


def get_track_facts(event) -> dict[str, str]:
    local_map = find_circuit_image(event)
    keys = []
    if local_map is not None:
        keys.append(_normalize(local_map.stem))

    keys.extend(
        _normalize(event.get(field))
        for field in ("CircuitName", "Location", "EventName", "OfficialEventName")
    )

    for key in keys:
        if key in TRACK_FACTS:
            return TRACK_FACTS[key]

    return {
        "first_f1": "Archive pending",
        "races": "Archive pending",
        "winners": "Archive pending",
        "length": "Archive pending",
        "laps": "Archive pending",
    }

def _split_winners(winners: str) -> list[str]:
    if winners == "Archive pending":
        return [winners]
    return [winner.strip() for winner in winners.split(",") if winner.strip()]


def _total_distance(facts: dict[str, str]) -> str:
    try:
        length = float(facts["length"].replace("km", "").strip())
        laps = int(facts["laps"])
    except ValueError:
        return "Archive pending"

    return f"{length * laps:.3f} km"


def _normalize(value) -> str:
    if value is None:
        return ""

    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(character for character in text if not unicodedata.combining(character))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())
