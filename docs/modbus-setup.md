# Modbus TCP server setup and verification

Status: historical setup findings are retained below. For current stage-specific commands and recovery, use [the retest runbook](retest-runbook.md). Alarm and FUXA restart observations were added later; see the final report.

## Configuration

Create the Modbus TCP server in OpenPLC Editor v4: use the project tree `+` menu, choose **Server → Modbus / TCP**, and enable it. Set the network interface to `0.0.0.0` and port to `5020`. Confirm the buffer mapping includes at least `%QX` bits 0–2 and `%QW` register 0. Save the project and use **Build & Upload** again. The Editor-generated `conf/modbus_slave.json` is what enables the plugin during upload.

The earlier Compose version mounted `plugins.conf` and `modbus_slave_config.json` read-only. This conflicted with the Runtime's upload process: the 2026-09-17 log said `Disabled plugin 'modbus_slave' (no config file found)` and `Failed to save updated plugin configuration`. Those mounts were removed as a historical deployment correction. Container recreation and re-upload belong only to that deployment repair, not routine verification of the current running lab.

Port 5020 is not published to the host; FUXA and the explicit trusted baseline probe can use `openplc:5020` on control; base evaluator services are isolated on assessment. The Editor still uses host `127.0.0.1:8443`.

The port differs from the initial architecture's tentative port 502. Both endpoints must use 5020 during this verification. The project should pin the working Runtime image digest after the actual image is checked.

## Current verification and recovery

Use [the retest runbook](retest-runbook.md). The base Compose intentionally isolates `modbus-probe` and `modbus-pump-check`; those services cannot serve as a normal-path probe or recovery tool. The additive `compose.verify.yaml` supplies explicit, temporary `baseline-*` services on control. It does not move the isolated evaluator back to control.

Do not force-recreate a running PLC as a routine verification step. Re-upload is a separate deployment operation. `finally` attempts OFF; process termination or network loss can prevent restoration. Use the trusted recovery path in the runbook and verify both command and running state.

## Tag contract to validate

These are expected mappings from the PLC addresses and the current OpenPLC plugin implementation, not observed results. Record the actual function code, wire offset, client display address, value, and response for each row.

| Tag | PLC address | Expected Modbus area | Expected wire offset | Intended HMI use |
| --- | --- | --- | ---: | --- |
| `tank_level` | `%QW0` | Holding register | 0 | Read |
| `pump_command` | `%QX0.0` | Coil | 0 | Read and write |
| `pump_running` | `%QX0.1` | Coil | 1 | Read |
| `high_level_alarm` | `%QX0.2` | Coil | 2 | Read |

The first read of the holding register and three coils succeeded; see `evidence/baseline/modbus-read-2026-09-17.md`. The pump check confirmed a coil 0 write, `pump_running` becoming true, `tank_level` rising from 0 to 3, and a return to stopped after reset; see `evidence/baseline/modbus-pump-write-2026-09-17.md`. Test the high-level alarm and a container restart separately. A successful Modbus write response alone does not prove the process state changed. Do not assume that a client label such as `40001` equals the wire offset `0`.

If the plugin does not start, check that the Editor project contains the Modbus server and that the upload produced `conf/modbus_slave.json`; inspect Runtime logs. If values are wrong, inspect the PLC execution state and address interpretation before adding the HMI.

## Sources

- [OpenPLC default plugin configuration](https://github.com/Autonomy-Logic/openplc-runtime/blob/main/plugins_default.conf)
- [OpenPLC Modbus plugin implementation](https://github.com/Autonomy-Logic/openplc-runtime/blob/main/core/src/drivers/plugins/python/modbus_slave/simple_modbus.py)
- [OpenPLC Docker guidance](https://github.com/Autonomy-Logic/openplc-runtime/blob/main/docs/DOCKER.md)
- [OpenPLC Editor Modbus server example](https://edge.autonomylogic.com/docs/openplc-editor/examples/modbus-slave-outputs/)
