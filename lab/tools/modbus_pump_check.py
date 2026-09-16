"""Briefly exercise the pump command in the isolated lab, then reset it."""

import argparse
import json
import socket
import struct
import sys
import time

from modbus_probe import read_tank, request


def write_pump_command(host, port, unit_id, timeout, enabled):
    value = 0xFF00 if enabled else 0x0000
    with socket.create_connection((host, port), timeout=timeout) as connection:
        connection.settimeout(timeout)
        reply = request(connection, 3, unit_id, 5, 0, value)
    expected = struct.pack(">BHH", 5, 0, value)
    if reply != expected:
        raise ValueError(f"Coil write acknowledgement mismatch: {reply.hex()}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="openplc")
    parser.add_argument("--port", type=int, default=5020)
    parser.add_argument("--unit-id", type=int, default=1)
    parser.add_argument("--timeout", type=float, default=3.0)
    parser.add_argument("--reset", action="store_true", help="Only turn pump command off")
    args = parser.parse_args()
    target = (args.host, args.port, args.unit_id, args.timeout)

    if args.reset:
        try:
            write_pump_command(*target, False)
            print(json.dumps({"reset": read_tank(*target)}, sort_keys=True))
            return 0
        except (OSError, ValueError) as error:
            print(f"Pump reset failed: {error}", file=sys.stderr)
            return 1

    try:
        before = read_tank(*target)
    except (OSError, ValueError) as error:
        print(f"Baseline read failed: {error}", file=sys.stderr)
        return 1
    if before["pump_command"] or before["high_level_alarm"]:
        print(
            "Pump check skipped: command is already on or high-level alarm is active. "
            "No write was sent.",
            file=sys.stderr,
        )
        return 2

    during = None
    after = None
    error = None
    reset_error = None
    try:
        write_pump_command(*target, True)
        time.sleep(3)
        during = read_tank(*target)
    except (OSError, ValueError) as exc:
        error = str(exc)
    finally:
        try:
            write_pump_command(*target, False)
            time.sleep(0.2)
            after = read_tank(*target)
        except (OSError, ValueError) as exc:
            reset_error = str(exc)

    checks = {
        "command_on_during_test": bool(during and during["pump_command"]),
        "pump_running_during_test": bool(during and during["pump_running"]),
        "level_increased_during_test": bool(
            during and during["tank_level"] > before["tank_level"]
        ),
        "command_off_after_reset": bool(after and not after["pump_command"]),
        "pump_stopped_after_reset": bool(after and not after["pump_running"]),
    }
    print(
        json.dumps(
            {
                "before": before,
                "during": during,
                "after": after,
                "checks": checks,
                "error": error,
                "reset_error": reset_error,
            },
            sort_keys=True,
        )
    )
    if error or reset_error or not all(checks.values()):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
