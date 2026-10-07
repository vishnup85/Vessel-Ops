import json
from confluent_kafka import Producer
from events import generate_position


def delivery_report(error, message):
    if error is not None:
        print(f"Delivery failed: {error}")
    else:
        print(
            f"Delivered key={message.key().decode('utf-8')} "
            f"partition={message.partition()} "
            f"offset={message.offset()}"
        )


producer = Producer({
    "bootstrap.servers": "localhost:9092",
    "message.timeout.ms": 10000,
})

# TODO: Generate an event for vessel "999000001", sequence 0.
vessels = ["999000001", "999000002", "999000003"]

for sequence in range(6):
    for mmsi in vessels:
        # 1. Generate an event using mmsi and sequence.
        event = generate_position(mmsi, sequence)

        # 2. Queue it using your existing producer.produce(...) code.
        producer.produce(
            topic="vessel.positions",
            key=event["mmsi"],
            value=json.dumps(event),
            on_delivery=delivery_report,
        )

# Keep flush OUTSIDE both loops.
remaining = producer.flush(timeout=15)

if remaining:
    print(f"{remaining} message(s) still waiting for delivery.")
