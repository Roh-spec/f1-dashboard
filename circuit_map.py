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
    "montréal": "Circuit Gilles-Villeneuve",
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
    "mexico city": "Autódromo Hermanos Rodríguez",
    "mexico city grand prix": "Autódromo Hermanos Rodríguez",
    "sao paulo": "Autódromo José Carlos Pace",
    "são paulo": "Autódromo José Carlos Pace",
    "brazilian grand prix": "Autódromo José Carlos Pace",
    "las vegas": "Las Vegas Strip Circuit",
    "las vegas grand prix": "Las Vegas Strip Circuit",
    "yas island": "Yas Marina Circuit",
    "abu dhabi grand prix": "Yas Marina Circuit",
    "istanbul": "Intercity Istanbul Park Circuit",
    "turkish grand prix": "Intercity Istanbul Park Circuit",
    "nurburgring": "Nurburgring",
    "nürburgring": "Nurburgring",
    "eifel grand prix": "Nurburgring",
    "portimao": "Autódromo Internacional do Algarve",
    "portimão": "Autódromo Internacional do Algarve",
    "portuguese grand prix": "Autódromo Internacional do Algarve",
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


def _normalize(value) -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return ""

    text = unicodedata.normalize("NFKD", str(value))
    text = "".join(character for character in text if not unicodedata.combining(character))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


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
