from tasks import add
import autodynatrace
import time


@autodynatrace.trace
def send_task():
    result = add.delay(3, 2)
    print(result)


def main():
    while True:
        send_task()
        time.sleep(10)


if __name__ == "__main__":
    main()
