# Modbus TCP server setup and verification

Status: configuration prepared on 2026-09-16; runtime behavior has not been verified in this checkout.

## Configuration

`lab/compose/plugins.conf` enables the OpenPLC Runtime v4 `modbus_slave` plugin. `lab/compose/modbus_slave_config.json` binds it to `0.0.0.0:5020` inside the OpenPLC container. Compose mounts both files read-only. Port 5020 is not published to the host; FUXA can use `openplc:5020` on the Compose `control` network. The Editor still uses host `127.0.0.1:8443`.

The port differs from the initial architecture's tentative port 502. Both endpoints must use 5020 during this verification. The project should pin the working Runtime image digest after the actual image is checked.

## Verification on the Docker host

Run these commands from the repository root in PowerShell:

```powershell
docker compose -f lab/compose/compose.yaml config
docker compose -f lab/compose/compose.yaml up -d openplc
docker compose -f lab/compose/compose.yaml ps
docker compose -f lab/compose/compose.yaml logs --tail=150 openplc
docker compose -f lab/compose/compose.yaml exec openplc cat /workdir/plugins.conf
docker compose -f lab/compose/compose.yaml exec openplc cat /workdir/core/src/drivers/plugins/python/modbus_slave/modbus_slave_config.json
docker compose -f lab/compose/compose.yaml images
```

Confirm that the Runtime loaded `modbus_slave` and listens on port 5020. Deploy and start `tank_control` from the Editor if it is not already running. Check that the PLC program is running before interpreting zero or unchanging Modbus values.

Then run the read-only probe from the same Compose network:

```powershell
docker compose -f lab/compose/compose.yaml run --rm modbus-probe
```

The probe reads holding register offset 0 with function code 03 and coil offsets 0–2 with function code 01. It prints the returned values as JSON or exits with an error. It does not write a coil or change the PLC state. This one-time verification service runs only when explicitly targeted; it is not started by ordinary `docker compose up`.

## Tag contract to validate

These are expected mappings from the PLC addresses and the current OpenPLC plugin implementation, not observed results. Record the actual function code, wire offset, client display address, value, and response for each row.

| Tag | PLC address | Expected Modbus area | Expected wire offset | Intended HMI use |
| --- | --- | --- | ---: | --- |
| `tank_level` | `%QW0` | Holding register | 0 | Read |
| `pump_command` | `%QX0.0` | Coil | 0 | Read and write |
| `pump_running` | `%QX0.1` | Coil | 1 | Read |
| `high_level_alarm` | `%QX0.2` | Coil | 2 | Read |

First read the holding register and three coils. Then write only coil 0 in this isolated lab, read it back, and confirm the PLC logic changes `pump_running` and `tank_level`. Test the high-level alarm and a container restart. A successful Modbus write response alone does not prove the process state changed. Do not assume that a client label such as `40001` equals the wire offset `0`.

If the plugin does not start, compare the running image's plugin path, config schema, and logs with the checked-in files before changing settings. If values are wrong, inspect the PLC execution state and address interpretation before adding the HMI.

## Sources

- [OpenPLC default plugin configuration](https://github.com/Autonomy-Logic/openplc-runtime/blob/main/plugins_default.conf)
- [OpenPLC Modbus plugin implementation](https://github.com/Autonomy-Logic/openplc-runtime/blob/main/core/src/drivers/plugins/python/modbus_slave/simple_modbus.py)
- [OpenPLC Docker guidance](https://github.com/Autonomy-Logic/openplc-runtime/blob/main/docs/DOCKER.md)
