import wrapt
import paramiko
import time

import autodynatrace

def main():
    while True:
        c = paramiko.SSHClient()
        c.load_system_host_keys()
        c.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        c.connect("192.168.15.222", port=22, username="vagrant", password="1vagrant")
        c.exec_command("ls")
        c.close()
        time.sleep(2)


if __name__ == '__main__':
    main()
