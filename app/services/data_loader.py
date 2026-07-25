from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.circuit import Circuit
from app.models.driver import Driver
from app.models.team import Team
from app.models.race import Race
from app.models.session import Session
from app.models.lap import Lap
from app.models.telemetry import Telemetry
from app.models.pit_stop import PitStop

from app.services.fastf1_client import (
    get_season_calendar,
    get_session,
    extract_laps,
    extract_telemetry,
    extract_pit_stops,
)


class DataLoader:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _get_or_create(self, model, filter_kwargs, defaults):
        stmt = select(model).filter_by(**filter_kwargs)
        result = await self.db.execute(stmt)
        obj = result.scalar_one_or_none()
        if obj:
            for k, v in defaults.items():
                setattr(obj, k, v)
            return obj
        obj = model(**{**filter_kwargs, **defaults})
        self.db.add(obj)
        return obj

    async def _ensure_circuit(self, circuit_key: int, name: str, location=None, country=None, lat=None, lon=None):
        return await self._get_or_create(Circuit, {"circuit_key": circuit_key}, {
            "name": name, "location": location, "country": country, "latitude": lat, "longitude": lon
        })

    async def _ensure_driver(self, driver_number: int, name: str, team_name: str, nationality=None, headshot_url=None):
        return await self._get_or_create(Driver, {"driver_number": driver_number}, {
            "name": name, "team": team_name, "nationality": nationality, "headshot_url": headshot_url
        })

    async def sync_race(self, year: int, round_num: int):
        schedule = get_season_calendar(year)
        event_row = schedule[schedule["RoundNumber"] == round_num]
        if event_row.empty:
            return
        event = event_row.iloc[0].to_dict()

        location = event.get("Location") or {}
        circuit_key = int(location.get("CircuitKey", 0)) if isinstance(location, dict) else 0
        circuit_name = location.get("CircuitName", event.get("EventName", "")) if isinstance(location, dict) else event.get("EventName", "")
        circuit_location = location.get("Locality") if isinstance(location, dict) else None
        circuit_country = location.get("Country") if isinstance(location, dict) else None
        lat = float(location.get("Latitude")) if isinstance(location, dict) and location.get("Latitude") is not None else None
        lon = float(location.get("Longitude")) if isinstance(location, dict) and location.get("Longitude") is not None else None

        circuit = await self._ensure_circuit(circuit_key, circuit_name, circuit_location, circuit_country, lat, lon)
        await self.db.flush()

        race = await self._get_or_create(Race, {"season": year, "round": round_num}, {
            "name": event.get("EventName", ""),
            "date": event.get("EventDate").isoformat() if event.get("EventDate") is not None else None,
            "time": event.get("Session1Time").isoformat() if event.get("Session1Time") is not None else None,
            "circuit_id": circuit.circuit_id,
        })

        session_types = ["Practice 1", "Practice 2", "Practice 3", "Qualifying", "Sprint", "Race"]
        for st in session_types:
            try:
                s = get_session(year, round_num, st)
            except Exception:
                continue
            session_date = None
            session_time = None
            try:
                session_date = s.event.get("EventDate").isoformat() if s.event.get("EventDate") is not None else None
                session_time = s.date.isoformat() if s.date is not None else None
            except Exception:
                pass
            sess = await self._get_or_create(Session, {"race_id": race.race_id, "session_type": st}, {
                "date": session_date,
                "time": session_time,
            })
            await self.db.flush()

            for lap in extract_laps(s):
                driver_number = lap.get("driver_number")
                if driver_number is None:
                    continue
                driver = await self._ensure_driver(driver_number, f"Driver {driver_number}", "")
                lap_entry = Lap(
                    session_id=sess.session_id,
                    driver_id=driver.driver_id,
                    lap_number=lap["lap_number"],
                    lap_time=lap["lap_time"],
                    sector1_time=lap["sector1_time"],
                    sector2_time=lap["sector2_time"],
                    sector3_time=lap["sector3_time"],
                    tyre_compound=lap["tyre_compound"],
                    tyre_age=lap["tyre_age"],
                    weather=lap["weather"],
                )
                self.db.add(lap_entry)
                await self.db.flush()

                for tel in extract_telemetry(s, driver_number):
                    self.db.add(Telemetry(
                        lap_id=lap_entry.lap_id,
                        driver_id=driver.driver_id,
                        session_id=sess.session_id,
                        timestamp=tel["timestamp"],
                        speed=tel["speed"],
                        rpm=tel["rpm"],
                        gear=tel["gear"],
                        throttle=tel["throttle"],
                        brake=tel["brake"],
                        drs=tel["drs"],
                        distance=tel["distance"],
                        source=tel["source"],
                    ))

            for ps in extract_pit_stops(s):
                driver_number = ps.get("driver_number")
                if driver_number is None:
                    continue
                driver = await self._ensure_driver(driver_number, f"Driver {driver_number}", "")
                self.db.add(PitStop(
                    session_id=sess.session_id,
                    driver_id=driver.driver_id,
                    lap=ps["lap"],
                    stop_duration=ps["stop_duration"],
                    time_of_day=ps["time_of_day"],
                ))

    async def sync_all_2026(self):
        schedule = get_season_calendar(2026)
        for _, event in schedule.iterrows():
            try:
                await self.sync_race(2026, int(event["RoundNumber"]))
            except Exception as e:
                print(f"Failed to sync round {event['RoundNumber']}: {e}")
