import psycopg


def get_connection():
    return psycopg.connect(
        host="localhost",
        port=5433,
        dbname="vessel_ops",
        user="vessel",
        password="vessel_local",
    )



def get_vessel_state(connection, mmsi: str) -> bool | None:
    cursor = connection.execute(
        "SELECT inside_zone FROM vessel_states WHERE mmsi = %s;",
        (mmsi,),
    )
    row = cursor.fetchone()

    if row is None:
        return None  # We haven't seen this vessel before.

    return row[0]  # True or False


def save_vessel_state(connection, mmsi: str, inside_zone: bool):
    connection.execute(
        """
        INSERT INTO vessel_states (mmsi, inside_zone)
        VALUES (%s, %s)
        ON CONFLICT (mmsi)
        DO UPDATE SET inside_zone = EXCLUDED.inside_zone;
        """,
        (mmsi, inside_zone),
    )

if __name__ == "__main__":
    with get_connection() as connection:
        save_vessel_state(connection, "test-vessel", True)

    # Open a separate connection to read the saved value.
    with get_connection() as connection:
        state = get_vessel_state(connection, "test-vessel")
        print("Saved state:", state)



