from database import get_vessel_state, save_vessel_state

def is_inside_zone(latitude: float, longitude: float) -> bool:
    return (
        1.24 <= latitude <= 1.26
        and 103.80002 <= longitude <= 103.80004
    )


# print(is_inside_zone(1.25, 103.80001))  # False: before the zone
# print(is_inside_zone(1.25, 103.80003))  # True: inside
# print(is_inside_zone(1.25, 103.80005))  # False: beyond the zone
# print(is_inside_zone(1.30, 103.80003))  # False: latitude outside
# Each vessel gets its own remembered state.

def detect_transition(connection, mmsi: str, latitude: float, longitude: float):
    current_inside = is_inside_zone(latitude, longitude)
    previous_inside = get_vessel_state(connection, mmsi)  # None if unseen

    transition = None

    # TODO: If we have seen this vessel before:
    #   False -> True: set transition to "entered"
    #   True -> False: set transition to "exited"
    if previous_inside is not None:
        if previous_inside and not current_inside:
            transition = "exited"
        elif not previous_inside and current_inside:
            transition = "entered" 

    # TODO: Save current_inside in vessel_states under this MMSI.
    save_vessel_state(connection, mmsi, current_inside)
    return transition

# print(detect_transition("999000001", 1.25, 103.80001))
# print(detect_transition("999000001", 1.25, 103.80003))
# print(detect_transition("999000001", 1.25, 103.80003))
# print(detect_transition("999000001", 1.25, 103.80005))