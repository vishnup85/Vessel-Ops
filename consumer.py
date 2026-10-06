import json

from confluent_kafka import Consumer


consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "vessel-replay-demo",
    "auto.offset.reset": "earliest",
    "enable.auto.commit": False,
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

        print(
            f"vessel={event['mmsi']} "
            f"sequence={event['sequence']} "
            f"partition={message.partition()} "
            f"offset={message.offset()}"
        )
        

except KeyboardInterrupt:
    print("Stopping consumer.")

finally:
    consumer.close()