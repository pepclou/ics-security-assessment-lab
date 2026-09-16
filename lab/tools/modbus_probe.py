"""Read the tank tags over Modbus TCP from the isolated Compose network."""

import argparse
import json
import socket
import struct
import sys


def receive_exact(connection, size):
    data = bytearray()
    while len(data) < size:
        chunk = connection.recv(size - len(data))
        if not chunk:
            raise ConnectionError("Modbus server closed the connection")
        data.extend(chunk)
    return bytes(data)


def request(connection, transaction_id, unit_id, function_code, address, count):
    pdu = struct.pack(">BHH", function_code, address, count)
    frame = struct.pack(">HHHB", transaction_id, 0, len(pdu) + 1, unit_id) + pdu
    connection.sendall(frame)

    reply_header = receive_exact(connection, 7)
    reply_id, protocol_id, reply_length, reply_unit = struct.unpack(">HHHB", reply_header)
    if reply_id != transaction_id or protocol_id != 0 or reply_unit != unit_id:
        raise ValueError("Modbus response header does not match the request")
    if reply_length < 2 or reply_length > 254:
        raise ValueError(f"Invalid Modbus response length: {reply_length}")

    reply_pdu = receive_exact(connection, reply_length - 1)
    if reply_pdu[0] == function_code | 0x80:
        code = reply_pdu[1] if len(reply_pdu) > 1 else None
        raise ValueError(f"Modbus exception for function {function_code}: {code}")
    if reply_pdu[0] != function_code:
        raise ValueError(f"Unexpected Modbus function code: {reply_pdu[0]}")
    return reply_pdu


def read_tank(host, port, unit_id, timeout):
    with socket.create_connection((host, port), timeout=timeout) as connection:
        connection.settimeout(timeout)
        registers = request(connection, 1, unit_id, 3, 0, 1)
        if len(registers) != 4 or registers[1] != 2:
            raise ValueError("Invalid holding register response")
        tank_level = struct.unpack(">H", registers[2:4])[0]

        coils = request(connection, 2, unit_id, 1, 0, 3)
        if len(coils) != 3 or coils[1] != 1:
            raise ValueError("Invalid coil response")
        bits = coils[2]

    return {
        "host": host,
        "port": port,
        "unit_id": unit_id,
        "tank_level": tank_level,
        "pump_command": bool(bits & 0x01),
        "pump_running": bool(bits & 0x02),
        "high_level_alarm": bool(bits & 0x04),
        "addresses": {"holding_register": 0, "coils": [0, 1, 2]},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="openplc")
    parser.add_argument("--port", type=int, default=5020)
    parser.add_argument("--unit-id", type=int, default=1)
    parser.add_argument("--timeout", type=float, default=3.0)
    args = parser.parse_args()

    try:
        result = read_tank(args.host, args.port, args.unit_id, args.timeout)
    except (OSError, ValueError) as error:
        print(f"Modbus probe failed: {error}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
