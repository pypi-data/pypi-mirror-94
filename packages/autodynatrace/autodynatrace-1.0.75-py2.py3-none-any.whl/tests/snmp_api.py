from concurrent.futures import ThreadPoolExecutor, wait
import json
import logging
from datetime import timedelta, datetime
import re
from typing import List, Dict, Generator, Optional

import oneagent

sdk = oneagent.get_sdk()

import pysnmp.hlapi.asyncore as snmp_async
import pysnmp.hlapi as snmp

default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.DEBUG)

AUTHORIZATION_PROTOCOLS = {
    "md5": snmp.usmHMACMD5AuthProtocol,
    "sha": snmp.usmHMACSHAAuthProtocol,
    "sha224": snmp.usmHMAC128SHA224AuthProtocol,
    "sha256": snmp.usmHMAC192SHA256AuthProtocol,
    "sha384": snmp.usmHMAC256SHA384AuthProtocol,
    "sha512": snmp.usmHMAC384SHA512AuthProtocol,
    "noauth": snmp.usmNoAuthProtocol,
}

PRIVACY_PROTOCOLS = {
    "des": snmp.usmDESPrivProtocol,
    "3des": snmp.usm3DESEDEPrivProtocol,
    "aes": snmp.usmAesCfb128Protocol,
    "aes192": snmp.usmAesCfb192Protocol,
    "aes256": snmp.usmAesCfb256Protocol,
    "nopriv": snmp.usmNoPrivProtocol,
}


def uptime_to_date(uptime: int):
    return timedelta(milliseconds=int(uptime) * 10)


class Varbind:
    def __init__(self, key: str, value):
        self.key = key
        self.value = value

    def __str__(self):
        return f"Varbind({self.key}, {self.value})"

    def __repr__(self):
        return self.__str__()


class Metric:
    def __init__(self, key, value, dimensions: Optional[Dict[str, str]], metric_type="absolute"):
        self.key = key
        self.value = value
        self.dimensions = dimensions
        self.metric_type = metric_type

    def __str__(self):
        return f"Metric({self.key}, {self.dimensions}, {self.value} ({self.metric_type}))"

    def __repr__(self):
        return self.__str__()


class Property:
    def __init__(self, key, value):
        self.key: str = key
        self.value: str = str(value)

    def __str__(self):
        return f"Property({self.key}, {self.value})"

    def __repr__(self):
        return self.__str__()


class Snmp:
    def __init__(
        self,
        host: str,
        port: int = 161,
        community: str = "public",
        version: int = 2,
        username: str = None,
        auth_password: str = None,
        auth_protocol: str = None,
        priv_password: str = None,
        priv_protocol: str = None,
        non_repeaters: int = 0,
        max_repetitions: int = 100,
        timeout=10,
        logger: logging.Logger = default_logger,
    ):
        self.host = host
        self.port = port
        self._non_repeaters = non_repeaters
        self._max_repetitions = max_repetitions
        self._timeout = timeout
        self._auth = snmp.CommunityData(community)
        if version == 3:
            self.auth = snmp.UsmUserData(
                username,
                auth_password,
                priv_password,
                AUTHORIZATION_PROTOCOLS.get(auth_protocol, None),
                PRIVACY_PROTOCOLS.get(priv_protocol, None),
            )

        self.engine = snmp.SnmpEngine()
        self.transport = snmp.UdpTransportTarget((self.host, self.port), timeout=self._timeout)
        self.context = snmp.ContextData()
        self._logger = logger

    def get_bulk_async(self, oids, cb):
        query_varbinds = [snmp.ObjectType(snmp.ObjectIdentity(oid)) for oid in oids]
        return snmp_async.bulkCmd(
            self.engine,
            self._auth,
            self.transport,
            self.context,
            self._non_repeaters,
            self._max_repetitions,
            *query_varbinds,
            lexicographicMode=False,
            cbFun=cb,
            cbCtx=(),
        )

    def get(self, oids) -> List[List[Varbind]]:
        self._logger.debug(f"Attempting to obtain oids: {oids}")
        query_varbinds = [snmp.ObjectType(snmp.ObjectIdentity(oid)) for oid in oids]
        for error, error_status, error_index, varbinds in snmp.getCmd(
            self.engine, self._auth, self.transport, self.context, *query_varbinds, lexicographicMode=False,
        ):
            if error is None and not error_status:
                ret = []
                for varbind in varbinds:
                    if isinstance(varbind, snmp.ObjectType):
                        ret.append(Varbind(*varbind.prettyPrint().split(" = ")))
                    else:
                        ret.append(None)
                yield ret
            else:
                self._logger.error(
                    f"Could not obtain OIDs '{oids}', error: '{error}', error_index: '{error_index}', error_status: '{error_status}'"
                )

    def get_async(self, oids, cb):
        self._logger.debug(f"Attempting to obtain oids: {oids}")
        query_varbinds = [snmp.ObjectType(snmp.ObjectIdentity(oid)) for oid in oids]
        return snmp_async.getCmd(
            self.engine, self._auth, self.transport, self.context, *query_varbinds, lexicographicMode=False, cbFun=cb
        )

    def get_bulk(self, oids) -> List[List[Varbind]]:
        with sdk.trace_custom_service("API.get_bulk", "SNMP"):
            self._logger.debug(f"Attempting to obtain oids: {oids}")
            query_varbinds = [snmp.ObjectType(snmp.ObjectIdentity(oid)) for oid in oids]

            for error, error_status, error_index, varbinds in snmp.bulkCmd(
                self.engine,
                self._auth,
                self.transport,
                self.context,
                self._non_repeaters,
                self._max_repetitions,
                *query_varbinds,
                lexicographicMode=False,
            ):

                if error is None and not error_status:
                    ret = []
                    for varbind in varbinds:
                        if isinstance(varbind, snmp.ObjectType):
                            ret.append(Varbind(*varbind.prettyPrint().split(" = ")))
                        else:
                            ret.append(None)
                    yield ret
                else:
                    self._logger.error(
                        f"Could not obtain OIDs '{oids}', error: '{error}', error_index: '{error_index}', error_status: '{error_status}'"
                    )

    def get_properties(self, custom_properties) -> Generator[Property, None, None]:
        keys = [prop["key"] for prop in custom_properties]
        oids = [prop["oid"] for prop in custom_properties]
        for varbinds in self.get_bulk(oids):
            for i, varbind in enumerate(varbinds):
                if varbind is not None:
                    name = keys[i]
                    value = varbind.value
                    if name == "System uptime":
                        value = uptime_to_date(value)
                    yield Property(name, value)

    def calculate_formula(
        self, metric_key: str, metrics: List[Metric], formula: str, dynatrace_dimensions=None, metric_type="absolute"
    ):
        parsed_formula = formula
        for metric in metrics:
            parsed_formula = parsed_formula.replace(f"{{{metric.key}}}", metric.value)
        if validate_formula(parsed_formula):
            value = eval(parsed_formula)
            self._logger.info(f"Original formula: '{formula}', Parsed formula: {parsed_formula}, Result: {value}")
            return Metric(metric_key, value, dynatrace_dimensions, metric_type)

    def get_metrics(self, metric_json):
        try:
            source = metric_json.get("source", None)
            metric_dimensions = metric_json["timeseries"].get("dimensions", [])
            metric_key = metric_json.get("timeseries").get("key")

            if source is not None:

                # Fields are simple metrics without dimensions
                for field in source.get("fields", []):
                    values = field.get("values", [])
                    value_oids = [value["oid"] for value in values]
                    value_keys = [value["key"] for value in values]

                    for ret in self.get_bulk(value_oids):
                        for key, val in zip(value_keys, ret):
                            yield Metric(key, val.value, None)

                # Tables are metrics that iterate an SNMP table
                for table in source.get("tables", []):

                    # Sometimes there is no snmp table with names, example CPUs
                    # This variable allows us to use the OID index of the value as the dimension value
                    # For instance, the CPU at 1.3.6.1.4.1.9.9.109.1.1.1.1.7.1 would be "1" because it ends in ".1"
                    index_as_dimension = table.get("indexAsDimension", False)

                    dimensions = table.get("dimensions", [])
                    values = table.get("values", [])

                    # We need to gather the OIDs to build the query
                    dimension_oids = [dimension["oid"] for dimension in dimensions]
                    value_oids = [value["oid"] for value in values]
                    query = dimension_oids + value_oids

                    # We also need to gather the keys to set as the Metric keys and dimension names
                    dimension_keys = [dimension["key"] for dimension in dimensions]
                    value_keys = [value["key"] for value in values]

                    for ret in self.get_bulk(query):
                        # The first len(dimensions) objects are dimensions
                        dimensions_return = ret[: len(dimensions)]

                        # The ones after the dimensions are values
                        values_return = ret[len(dimensions) :]

                        # TODO: Implement formula option
                        dynatrace_dimensions = {}
                        for dim_key, dim in zip(dimension_keys, dimensions_return):
                            # Build the Dynatrace dimension format
                            dynatrace_dimensions[dim_key] = dim.value

                        if index_as_dimension:
                            for metric_dimension in metric_dimensions:
                                # Grab the last index of the OID, if we are not grabbing dimension names from SNMP
                                dynatrace_dimensions.update({metric_dimension: i.key.split(".")[-1] for i in values_return})

                        metrics = []
                        for i, (val_key, val) in enumerate(zip(value_keys, values_return)):
                            metrics.append(Metric(val_key, val.value, dynatrace_dimensions, source["type"]))

                        if table.get("formula", False):
                            yield self.calculate_formula(
                                metric_key, metrics, table.get("formula"), dynatrace_dimensions, source["type"]
                            )
                        else:
                            yield from metrics

        except Exception as e:
            self._logger.exception(f"Error processing metric {metric_json}, error: {e}")

    def query_from_plugin_json(self, plugin_json) -> Generator[Metric, None, None]:
        pool = ThreadPoolExecutor(max_workers=10)
        tasks = []
        for metric in plugin_json["metrics"]:
            tasks.append(pool.submit(self.get_metrics, metric))

        done, not_done = wait(tasks, timeout=self._timeout)
        print(done)
        for task in done:
            try:
                yield from task.result()
            except Exception as e:
                self._logger.error(f"Error gettings metrics: {e}")

        for task in not_done:
            self._logger.warning(f"SNMP collection did not finish in time for {task}")


def validate_formula(formula: str):
    return not re.findall("[a-zA-Z]]", formula)


def main():
    conn = Snmp("ec2-35-153-49-252.compute-1.amazonaws.com")
    with open("plugin.json") as f:
        plugin_json = json.load(f)

    for metric in conn.query_from_plugin_json(plugin_json):
        print(metric)

    # custom_properties = plugin_json.get("customProperties", [])
    # for prop in conn.get_properties(custom_properties):
    #    print(prop)


if __name__ == "__main__":
    main()
