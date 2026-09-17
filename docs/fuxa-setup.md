# FUXA HMI connection and tag baseline

Status: the lab operator configured and saved the FUXA Modbus TCP connection and four tags on 2026-09-17. The live tag list showed values and timestamps. HMI controls, a normal-operation capture, alarm response, and restart recovery remain unverified.

## Recreate the connection

Start the Compose `openplc` and `fuxa` services. In FUXA, install the `modbus-serial` server plugin if it is not present. Open **Setup → Connections** and add an enabled `ModbusTCP` connection named `openplc_tank`:

| Setting | Value |
| --- | --- |
| Slave IP and Port | `openplc:5020` |
| Slave ID | `1` |
| Polling | `1 sec` |
| Connection timeout | `2000 ms` |

`openplc` is the Compose service name. The connection indicator turned green in the operator's UI. The exported project is [lab/hmi/fuxa-project.json](../lab/hmi/fuxa-project.json). FUXA's **Save Project As…** exports a JSON project; **Save Project** stores the current project internally. The export does not include FUXA user accounts or the installed server plugin. Keep the FUXA application volumes, and restore the plugin and authentication settings separately when moving to a new container. [FUXA Save/Load documentation](https://frangoteam.github.io/FUXA/HowTo-save-load-Project/)

## Tag mapping

The FUXA editor uses one-based address offsets. These four entries correspond to the zero-based Modbus offsets confirmed by the probe:

| FUXA tag | Register selection | Type | FUXA address offset | Wire offset | PLC address | Description |
| --- | --- | --- | ---: | ---: | --- | --- |
| `tank_level` | Holding Registers | `Int16` | 1 (`400001` shown) | 0 | `%QW0` | Tank level (0-100) |
| `pump_command` | Coil Status | `Bool` | 1 | 0 | `%QX0.0` | Pump start command |
| `pump_running` | Coil Status | `Bool` | 2 | 1 | `%QX0.1` | Pump running status |
| `high_level_alarm` | Coil Status | `Bool` | 3 | 2 | `%QX0.2` | High tank level alarm |

The operator's tag-list screenshot showed all four rows with value `0` and the same fresh timestamp. This verifies that FUXA displayed current tag values. It does not establish a full HMI operating baseline or prove the write control works from the FUXA screen. The separate Modbus pump check verified the PLC's command response.

Before publishing a new FUXA export, inspect it for credentials and private endpoints. This version contains the lab service address and tag definitions, but no user or password fields.
