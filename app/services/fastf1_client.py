import fastf1
from pathlib import Path

from app.config import settings


def _ensure_cache():
    path = Path(settings.FASTF1_CACHE_DIR)
    path.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(str(path))


def get_season_calendar(year: int):
    _ensure_cache()
    schedule = fastf1.get_event_schedule(year, include_testing=False)
    return schedule


def get_session(year: int, round_num: int, session_name: str):
    _ensure_cache()
    session = fastf1.get_session(year, round_num, session_name)
    session.load()
    return session


def extract_laps(session):
    rows = []
    for driver_code, _ in session.laps.groupby("Driver"):
        try:
            laps = session.laps.pick_driver(driver_code)
        except Exception:
            continue
        for _, lap in laps.iterrows():
            rows.append({
                "driver_number": int(lap["DriverNumber"]) if lap.get("DriverNumber") is not None else None,
                "lap_number": int(lap["LapNumber"]) if lap.get("LapNumber") is not None else None,
                "lap_time": lap["LapTime"].total_seconds() if lap.get("LapTime") is not None else None,
                "sector1_time": lap["Sector1Time"].total_seconds() if lap.get("Sector1Time") is not None else None,
                "sector2_time": lap["Sector2Time"].total_seconds() if lap.get("Sector2Time") is not None else None,
                "sector3_time": lap["Sector3Time"].total_seconds() if lap.get("Sector3Time") is not None else None,
                "tyre_compound": lap.get("Compound"),
                "tyre_age": int(lap["TyreLife"]) if lap.get("TyreLife") is not None else None,
                "weather": str(lap.get("Weather")) if lap.get("Weather") is not None else None,
            })
    return rows


def extract_telemetry(session, driver_number: int):
    rows = []
    try:
        tel = session.car_data[driver_number]
        for _, row in tel.iterrows():
            rows.append({
                "timestamp": float(row["Time"].total_seconds()) if row.get("Time") is not None else 0.0,
                "speed": float(row["Speed"]) if row.get("Speed") is not None else None,
                "rpm": float(row["RPM"]) if row.get("RPM") is not None else None,
                "gear": int(row["nGear"]) if row.get("nGear") is not None else None,
                "throttle": float(row["Throttle"]) if row.get("Throttle") is not None else None,
                "brake": float(row["Brake"]) if row.get("Brake") is not None else None,
                "drs": int(row["DRS"]) if row.get("DRS") is not None else None,
                "distance": float(row["Distance"]) if row.get("Distance") is not None else None,
                "source": "car_data",
            })
    except Exception:
        pass
    return rows


def extract_pit_stops(session):
    rows = []
    try:
        for _, ps in session.pit_stops.iterrows():
            rows.append({
                "driver_number": int(ps["DriverNumber"]) if ps.get("DriverNumber") is not None else None,
                "lap": int(ps["LapNumber"]) if ps.get("LapNumber") is not None else None,
                "stop_duration": ps["StopDuration"].total_seconds() if ps.get("StopDuration") is not None else None,
                "time_of_day": ps["Time"].total_seconds() if ps.get("Time") is not None else None,
            })
    except Exception:
        pass
    return rows
