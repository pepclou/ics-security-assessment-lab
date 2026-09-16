# PLC upload observation — 2026-09-17 (Asia/Seoul)

Source: OpenPLC Editor console lines pasted by the lab operator. The full console export, Editor version, image digest, and post-upload PLC state were not captured.

| Time shown in Editor | Observation | Meaning |
| --- | --- | --- |
| 07:46:02 | `Build complete: build/new_libplc.so`; `Build finished successfully` | Runtime compiled the uploaded PLC program |
| 07:46:02 | `Compilation completed successfully (exit code: 0)`; `PLC started`; `Upload complete` | Upload and start were reported successful; sustained operation is not yet verified |
| 07:46:02 | `Disabled plugin 'modbus_slave' (no config file found)`; `Failed to save updated plugin configuration` | Modbus server was not enabled by this upload |

The PLC program has five variables in the Editor project: `tank_level`, `pump_command`, `pump_running`, `high_level_alarm`, and `one_second`. An earlier compile failed because the first variable was accidentally named `LocalVartank_level`; that name was corrected before the successful upload.

The Runtime's RETAIN message says the Editor-generated runtime headers predate retain support, but the program builds and runs normally. This lab currently has no RETAIN variables. The message suggests Editor v4.2.12 or later for retain support; no upgrade was performed as part of this observation.

This is a lab deployment observation, not a Modbus communication result or a security finding.
