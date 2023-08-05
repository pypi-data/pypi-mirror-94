# import autodynatrace
import subprocess


def go():
    print(subprocess.call(["sleep", "1"]))
    print(subprocess.check_output(["sleep", "1"]))


def main():
    while True:
        go()


if __name__ == "__main__":
    main()
