# Modbus pump command check — 2026-09-17 (Asia/Seoul)

Source: JSON pasted by the lab operator after running `docker compose -f lab/compose/compose.yaml run --rm modbus-pump-check`. Approximate local time: 08:06. The full terminal transcript, Runtime image digest, and packet capture were not saved.

The one-time check used Modbus function code 05 to set coil 0 (`pump_command`, `%QX0.0`) on, waited three seconds, then set it off. It read holding register 0 and coils 0–2 before, during, and after the command. The script attempted the off command in a `finally` block.

| Observation | Before | During command | After reset |
| --- | ---: | ---: | ---: |
| `pump_command` | false | true | false |
| `pump_running` | false | true | false |
| `tank_level` | 0 | 3 | 3 |
| `high_level_alarm` | false | false | false |

All five script checks returned `true`: command on during test, pump running during test, level increased during test, command off after reset, and pump stopped after reset. Both `error` and `reset_error` were `null`.

This verifies that the isolated lab accepted a Modbus write to coil 0 and the PLC logic produced the expected short-term response. It does not establish how long the command would persist under faults or whether any access control is adequate. No production system was involved.
