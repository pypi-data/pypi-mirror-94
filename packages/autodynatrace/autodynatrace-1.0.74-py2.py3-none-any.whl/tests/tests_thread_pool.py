from threading import Thread
import time

import wrapt


@wrapt.patch_function_wrapper("threading", "Thread.start")
def dynatrace_start(wrapped, instance, args, kwargs):
    print("start, instance", instance)
    t0 = time.time()
    ret = wrapped(*args, **kwargs)
    print(time.time() - t0)
    return ret


@wrapt.patch_function_wrapper("threading", "Thread.run")
def dynatrace_run(wrapped, instance, args, kwargs):
    print("run instance", instance)
    return wrapped(*args, **kwargs)


class Worker(Thread):
    def __init__(self):
        super().__init__()
        self.start()

    def run(self) -> None:
        time.sleep(1)
        print("Done")


def main():
    w = Worker()


if __name__ == "__main__":
    main()
