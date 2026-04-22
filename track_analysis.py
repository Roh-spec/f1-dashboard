import re
import unicodedata

import streamlit as st

from circuit_map import find_circuit_image


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
}


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
        st.markdown("<h3>Winners</h3>", unsafe_allow_html=True)
        for winner in _split_winners(winners):
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
