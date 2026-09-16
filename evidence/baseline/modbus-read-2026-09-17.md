# Modbus TCP read baseline — 2026-09-17 (Asia/Seoul)

Source: output pasted by the lab operator after running `docker compose -f lab/compose/compose.yaml run --rm modbus-probe` from the repository root. Approximate local time: 07:59. The full terminal transcript, container image digest, and packet capture were not saved.

The Editor build and upload at 07:56:44 reported `modbus_slave` enabled, `conf/modbus_slave.json` copied into the Runtime plugin path, `Compilation completed successfully`, `PLC started`, and `Upload complete`. The generated config sets `0.0.0.0:5020`, includes `%QW` holding registers 0–1023, and `%QX` coils 0–8191.

Read-only probe result:

```json
{"addresses":{"coils":[0,1,2],"holding_register":0},"high_level_alarm":false,"host":"openplc","port":5020,"pump_command":false,"pump_running":false,"tank_level":0,"unit_id":1}
```

The successful response confirms that a Modbus TCP server answered from the Compose network at `openplc:5020` and that function codes 03 and 01 returned the requested offsets. The `tank_level` value is a single observation; it does not establish that the tank simulation is changing correctly. No Modbus write, FUXA communication, packet capture, or security assessment has been performed yet.
