"""Resolve one lab target and attempt one TCP connection; sends no Modbus data."""
import argparse
import datetime
import ipaddress
import json
import socket


def check(host, port, timeout):
    result = {"timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "host": host, "port": port, "application_payload_sent": False}
    try:
        ipaddress.ip_address(host)
        numeric = True
    except ValueError:
        numeric = False
    try:
        addresses = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM,
                                      flags=socket.AI_NUMERICHOST if numeric else 0)
    except socket.gaierror as exc:
        result.update(stage="resolution", outcome="failed", error=str(exc))
        return result, 2
    family, kind, protocol, _, address = addresses[0]
    result.update(resolved_addresses=sorted({a[4][0] for a in addresses}),
                  attempted_address=address[0], numeric_target=numeric)
    try:
        with socket.socket(family, kind, protocol) as connection:
            connection.settimeout(timeout)
            connection.connect(address)
        result.update(stage="tcp", outcome="connected")
        return result, 0
    except OSError as exc:
        result.update(stage="tcp", outcome="failed", error_type=type(exc).__name__,
                      error=str(exc), errno=exc.errno)
        return result, 3


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", type=int, default=5020)
    parser.add_argument("--timeout", type=float, default=3.0)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535 or not 0 < args.timeout <= 10:
        parser.error("port must be 1..65535 and timeout must be >0 and <=10")
    output, code = check(args.host, args.port, args.timeout)
    print(json.dumps(output, ensure_ascii=False, sort_keys=True))
    raise SystemExit(code)
