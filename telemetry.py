from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from constants import CURRENT_DRIVERS, DEMO_DRIVER_BASE_PACE
from models import SessionConfig, SessionMeta

CACHE_DIR = Path(__file__).parent / ".fastf1_cache"


def load_session_data(config: SessionConfig) -> tuple[pd.DataFrame, SessionMeta]:
    if config.use_fastf1:
        data, meta = _try_load_fastf1_data(config)
        if not data.empty:
            return data, meta

    return _build_demo_session_data(config)


def _try_load_fastf1_data(config: SessionConfig) -> tuple[pd.DataFrame, SessionMeta]:
    try:
        import fastf1
    except ImportError:
        return pd.DataFrame(), _fallback_meta(config, "FastF1 is not installed yet.")

    try:
        CACHE_DIR.mkdir(exist_ok=True)
        fastf1.Cache.enable_cache(str(CACHE_DIR))
        session = _load_fastf1_session(
            config.year,
            config.grand_prix,
            config.session_type,
        )
        laps = session.laps.pick_drivers(config.driver).pick_quicklaps().copy()
        if laps.empty:
            laps = session.laps.pick_drivers(config.driver).copy()

        if laps.empty:
            return pd.DataFrame(), _fallback_meta(config, "No laps were found for the selected driver.")

        normalized = _normalize_fastf1_laps(laps)
        driver_info = _safe_get_driver(session, config.driver)
        event_name = str(session.event.get("EventName", config.grand_prix))
        circuit = str(session.event.get("Location", config.grand_prix))

        return normalized, SessionMeta(
            source="FastF1",
            event_name=f"{config.year} {event_name}",
            session_name=str(session.name),
            driver=_driver_display_name(config.driver, driver_info),
            team=str(driver_info.get("TeamName", "Unknown Team")),
            circuit=circuit,
            status="Live archive loaded",
            note="Timing data loaded through FastF1. Speed is speed-trap data where available.",
        )
    except Exception as exc:
        return pd.DataFrame(), _fallback_meta(config, f"FastF1 load failed: {exc}")


def _load_fastf1_session(year: int, grand_prix: str, session_type: str) -> Any:
    import fastf1

    session = fastf1.get_session(year, grand_prix, session_type)
    session.load(laps=True, telemetry=False, weather=True, messages=False)
    return session


def _normalize_fastf1_laps(laps: pd.DataFrame) -> pd.DataFrame:
    data = pd.DataFrame()
    data["Lap"] = laps["LapNumber"].astype(int)
    data["Lap Time"] = laps["LapTime"].dt.total_seconds().round(3)
    data["Sector 1"] = _timedelta_seconds(laps, "Sector1Time")
    data["Sector 2"] = _timedelta_seconds(laps, "Sector2Time")
    data["Sector 3"] = _timedelta_seconds(laps, "Sector3Time")
    data["Speed"] = _best_speed_column(laps)
    data["Tyre Life"] = pd.to_numeric(laps.get("TyreLife"), errors="coerce").round(0)
    data["Compound"] = laps.get("Compound", pd.Series(["Unknown"] * len(laps), index=laps.index)).fillna("Unknown")
    data["Position"] = pd.to_numeric(laps.get("Position"), errors="coerce")
    data["Stint"] = pd.to_numeric(laps.get("Stint"), errors="coerce")
    data["Track Status"] = laps.get("TrackStatus", pd.Series([""] * len(laps), index=laps.index)).astype(str)
    data["Is Accurate"] = laps.get("IsAccurate", pd.Series([False] * len(laps), index=laps.index)).fillna(False)
    return data.dropna(subset=["Lap Time"]).sort_values("Lap")


def _timedelta_seconds(laps: pd.DataFrame, column: str) -> pd.Series:
    if column not in laps:
        return pd.Series([np.nan] * len(laps), index=laps.index)
    return laps[column].dt.total_seconds().round(3)


def _best_speed_column(laps: pd.DataFrame) -> pd.Series:
    speed_columns = ["SpeedST", "SpeedFL", "SpeedI2", "SpeedI1"]
    available = [column for column in speed_columns if column in laps]
    if not available:
        return pd.Series([np.nan] * len(laps), index=laps.index)
    return laps[available].bfill(axis=1).iloc[:, 0].round(1)


def _safe_get_driver(session: Any, driver_code: str) -> dict[str, Any]:
    try:
        driver = session.get_driver(driver_code)
        return dict(driver)
    except Exception:
        return {}


def _driver_display_name(driver_code: str, driver_info: dict[str, Any]) -> str:
    full_name = driver_info.get("FullName")
    if full_name:
        return str(full_name)
    return CURRENT_DRIVERS.get(driver_code, driver_code)


def _fallback_meta(config: SessionConfig, note: str) -> SessionMeta:
    return SessionMeta(
        source="Demo fallback",
        event_name=f"{config.year} {config.grand_prix}",
        session_name=config.session_type,
        driver=CURRENT_DRIVERS.get(config.driver, config.driver),
        team="Fallback Timing Desk",
        circuit=config.grand_prix,
        status="Demo data active",
        note=note,
    )


def _build_demo_session_data(config: SessionConfig) -> tuple[pd.DataFrame, SessionMeta]:
    rng_seed = abs(hash((config.year, config.grand_prix, config.session_type, config.driver))) % (2**32)
    rng = np.random.default_rng(rng_seed)
    lap_count = 28 if config.session_type == "R" else 16
    lap_numbers = np.arange(1, lap_count + 1)
    base_pace = DEMO_DRIVER_BASE_PACE.get(config.driver, 90.0)

    lap_noise = rng.normal(0, 0.25, lap_count)
    tyre_degradation = np.linspace(0, lap_count * 0.045, lap_count)
    traffic = np.sin(lap_numbers / 3.2) * 0.18
    lap_time = base_pace + tyre_degradation + traffic + lap_noise
    sector_1 = lap_time * rng.normal(0.323, 0.004, lap_count)
    sector_2 = lap_time * rng.normal(0.371, 0.005, lap_count)
    sector_3 = lap_time - sector_1 - sector_2

    data = pd.DataFrame(
        {
            "Lap": lap_numbers,
            "Lap Time": lap_time.round(3),
            "Sector 1": sector_1.round(3),
            "Sector 2": sector_2.round(3),
            "Sector 3": sector_3.round(3),
            "Speed": np.clip(322 - tyre_degradation * 3 + rng.normal(0, 4, lap_count), 275, 342).round(1),
            "Tyre Life": np.clip(lap_numbers * 2.4, 1, 70).round(0),
            "Compound": np.where(lap_numbers < lap_count * 0.55, "MEDIUM", "HARD"),
            "Position": np.nan,
            "Stint": np.where(lap_numbers < lap_count * 0.55, 1, 2),
            "Track Status": "1",
            "Is Accurate": True,
        }
    )
    return data, _fallback_meta(
        config,
        "Showing deterministic demo data because FastF1 data is unavailable or disabled.",
    )
