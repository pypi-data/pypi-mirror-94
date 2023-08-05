import autodynatrace
import pika


def on_message(channel, method_frame, header_frame, body):
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def consumer():
    parameters = pika.ConnectionParameters("192.168.15.101", 5672, "/")
    connection = pika.BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel.queue_declare(queue="test")
    channel.basic_consume("test", on_message)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()


def main():
    consumer()


if __name__ == "__main__":
    main()
