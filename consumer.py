import json
import os
from confluent_kafka import Consumer
from detector import detect_transition

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": os.environ.get("KAFKA_GROUP_ID", "vessel-learning"),
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
    "max.poll.interval.ms": 1800000,
})

consumer.subscribe(["vessel.positions"])

try:
    while True:
        message = consumer.poll(timeout=1.0)

        if message is None:
            continue

        if message.error():
            print(f"Consumer error: {message.error()}")
            continue

        # TODO: Convert the message's JSON bytes into a Python dictionary.
        event = json.loads(message.value())
        transition = detect_transition(
            event["mmsi"],
            event["latitude"],
            event["longitude"],
        )

        if transition is not None:
            print(f"vessel={event['mmsi']} {transition}")

        print(
            f"vessel={event['mmsi']} "
            f"sequence={event['sequence']} "
            f"partition={message.partition()} "
            f"offset={message.offset()}"
        )
        if os.environ.get("CRASH_BEFORE_COMMIT") == "1":
            print("Simulated crash: processed, but not committed")
            raise RuntimeError("Simulated crash: processed, but not committed")

        consumer.commit(message=message, asynchronous=False)
        

except KeyboardInterrupt:
    print("Stopping consumer.")

finally:
    consumer.close()