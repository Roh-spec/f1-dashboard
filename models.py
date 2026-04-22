from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SessionConfig:
    year: int
    grand_prix: str
    session_type: str
    driver: str
    use_fastf1: bool


@dataclass(frozen=True)
class SessionMeta:
    source: str
    event_name: str
    session_name: str
    driver: str
    team: str
    circuit: str
    status: str
    note: str = ""
