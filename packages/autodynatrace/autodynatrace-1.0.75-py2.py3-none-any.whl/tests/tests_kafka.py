import autodynatrace
import time

from confluent_kafka import Consumer, Producer
from concurrent.futures import ThreadPoolExecutor

p = Producer({"bootstrap.servers": "192.168.15.101:32769"})
c = Consumer({"bootstrap.servers": "192.168.15.101:32769", "group.id": "mygroup2", "auto.offset.reset": "earliest"})
c.subscribe(["mytopic"])


@autodynatrace.trace
def produce():
    message = "Hello world!"
    print("Producing message '{}'".format(message))
    p.produce("mytopic", message.encode("utf-8"))


def producer():
    while True:
        produce()
        time.sleep(2)

@autodynatrace.trace
def consume():
    msg = c.poll(1.0)

    if msg is None:
        pass
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        pass

    print("Received Message: {}, Headers: {}".format(msg.value().decode("utf-8"), msg.headers()))

def consumer():
    try:
        while True:
            consume()

    except Exception as e:
        print("Ex {}".format(e))

    c.close()


def main():
    with ThreadPoolExecutor(max_workers=2) as e:
        e.submit(producer)
        e.submit(consumer)


if __name__ == "__main__":
    main()
