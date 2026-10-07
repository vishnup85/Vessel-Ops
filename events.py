from datetime import datetime, timedelta, timezone

START_TIME = datetime(2026, 10, 7, tzinfo=timezone.utc)


def generate_position(mmsi: str, sequence: int) -> dict:
    
    event_id = f"{mmsi}:{sequence}"
    timestamp = START_TIME + timedelta(seconds=sequence)
    latitude = 1.25
    longitude = round(103.80 + sequence * 0.00001, 5)
    speed_knots = 2.0
    return {
        "event_id": event_id,
        "timestamp": timestamp.isoformat(),
        "mmsi": mmsi,
        "sequence": sequence,
        "latitude": latitude,
        "longitude": longitude,
        "speed_knots": speed_knots,
    }


if __name__ == "__main__":
    print(generate_position("999000001", 0))
    print(generate_position("999000001", 1))