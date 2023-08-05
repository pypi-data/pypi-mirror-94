import autodynatrace

import pika
import time


def producer():
    parameters = pika.ConnectionParameters("192.168.15.101", 5672, "/")
    connection = pika.BlockingConnection(parameters=parameters)
    try:
        while True:
            channel = connection.channel()
            print("Publish")
            channel.basic_publish(exchange="", routing_key="test", body=b"Test message.")
            time.sleep(2)
    finally:
        connection.close()

# docker run -d -p 5672:5672 -p 15672:15672 --name rabbitmq-management rabbitmq:management
def main():
    producer()


if __name__ == "__main__":
    main()
