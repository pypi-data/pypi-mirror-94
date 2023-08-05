import oneagent

import autodynatrace

oneagent.initialize()
sdk = oneagent.get_sdk()

from concurrent.futures import ThreadPoolExecutor
import time


class Sleeper:
    def sleep(self):
        time.sleep(1)

    def __call__(self, *args, **kwargs):
        print(1)


class Normal:
    def sleep(self):
        time.sleep(1)

@autodynatrace.trace
def test():
    s = Sleeper()
    with ThreadPoolExecutor(max_workers=5) as e:
        for i in range(3):
            e.submit(s)

    n = Normal()
    with ThreadPoolExecutor(max_workers=5) as e:
        for i in range(3):
            e.submit(n.sleep)

import os

def main():
    os.environ["DT_CUSTOM_PROP"] = "Department=Acceptance"
    while True:
        test()
        time.sleep(30)


if __name__ == "__main__":
    main()
