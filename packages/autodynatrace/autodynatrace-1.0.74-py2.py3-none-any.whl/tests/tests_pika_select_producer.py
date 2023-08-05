import autodynatrace

import time
import pika


def on_open(connection):
    connection.channel(on_open_callback=on_channel_open)


# Step #4
def on_channel_open(channel):

    try:
        while True:
            channel = connection.channel()
            channel.basic_publish(exchange="", routing_key="test", body=b"Test async.")
    finally:
        connection.close()


parameters = pika.URLParameters("amqp://localhost:5672/%2F")
connection = pika.SelectConnection(parameters=parameters, on_open_callback=on_open)


try:
    # Step #2 - Block on the IOLoop
    connection.ioloop.start()

# Catch a Keyboard Interrupt to make sure that the connection is closed cleanly
except KeyboardInterrupt:

    # Gracefully close the connection
    connection.close()

    # Start the IOLoop again so Pika can communicate, it will stop on its own when the connection is closed
    connection.ioloop.start()
