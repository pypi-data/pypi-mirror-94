from snmp_api import Snmp
import autodynatrace
import time
from datetime import datetime


def cb(snmpEngine, sendRequestHandle, errorIndication, errorStatus, errorIndex, varBinds, cbCtx):
    print("cb")


@autodynatrace.trace
def query():
    conn = Snmp("localhost")
    for metric in conn.get_bulk(1 * ["1.3.6.1.2.1.2.2.1.10"]):
        print(metric)
    for a in conn.get(2 * ["1.3.6.1.2.1.2.2.1.10"]):
        pass
    conn.get_bulk_async(3 * ["1.3.6.1.2.1.2.2.1.10"], cb)
    conn.get_async(3 * ["1.3.6.1.2.1.2.2.1.10"], cb)
    conn.engine.transportDispatcher.runDispatcher()


def main():
    for i in range(200):
        query()
        time.sleep(10)


if __name__ == "__main__":
    main()
