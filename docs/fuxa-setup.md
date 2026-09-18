# FUXA HMI connection and tag baseline

Status: the lab operator configured the FUXA Modbus TCP connection and four tags on 2026-09-17. The live tag list showed values and timestamps. On 2026-09-18, the operator reported that the MainView pump switch raised the tank level and that the corrected `pump_running` LED changed to green on run and back to an empty circle on stop. The operator also reported that the high-level alarm sequence worked at the 80% threshold. A normal-operation packet capture and restart recovery remain unverified.

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

The operator's tag-list screenshot showed all four rows with value `0` and the same fresh timestamp. This verifies that FUXA displayed current tag values. That screenshot alone does not establish a full HMI operating baseline or prove the write control works from the FUXA screen. The separate Modbus pump check verified the PLC's command response.

## MainView controls

The exported project contains four view items:

| Item | Source tag | Behavior |
| --- | --- | --- |
| `tank_level_display` | `tank_level` | Displays the level with `%`; `0%` was observed in preview. |
| `pump_running_led` | `pump_running` | Green `#22c55e` for value 1; empty circle for value 0. |
| `pump_command_switch` | `pump_command` | Writes 1 on ON and 0 on OFF. |
| `high_level_alarm_led` | `high_level_alarm` | Red `#f90127ff` for value 1; the operator reported that it lit at the alarm threshold. |

The first pump LED configuration had a 1–1 range but an empty range color in the export, although the edit canvas looked green. We corrected only that range color in the exported JSON and the operator loaded it into FUXA. The operator reported green on run and empty on stop after the correction. The separate alarm LED was exported with the correct tag and nonempty red range color. A screenshot shows the active alarm at `80%`; see [alarm observation](../evidence/baseline/fuxa-high-level-alarm-2026-09-18.md). A packet trace of that transition has not been supplied.

Before publishing a new FUXA export, inspect it for credentials and private endpoints. This version contains the lab service address and tag definitions, but no user or password fields.
