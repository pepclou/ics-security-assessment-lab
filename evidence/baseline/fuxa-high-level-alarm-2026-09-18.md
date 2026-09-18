# FUXA high-level alarm observation — 2026-09-18 (Asia/Seoul)

Scope: project-owned virtual tank and pump in OpenPLC Runtime v4, shown through FUXA MainView. Sources: the operator's report after a controlled run to the 80% threshold and the supplied [active-alarm screenshot](fuxa-high-level-alarm-2026-09-18.png). Screenshot SHA-256: `0ae4e42e588c3a3665cbfc4d452fd7ce8af46b215d77ad3e3647a3f8a3ac24bc`.

Test instructions given to the operator: start with the switch OFF and level below 80%; switch ON and observe the level until 80%; check for a red `high_level_alarm` LED and an extinguished green `pump_running` LED; then switch OFF and observe the alarm clearing as the level drops below 80%. The operator replied that this sequence worked. The screenshot shows `80%`, a red alarm indicator, an empty pump-running indicator, and the switch in its green ON position. It does not show the later OFF/cleared state. The response did not include a timestamped value series or a separate output transcript.

The [PLC source](../../lab/plc/tank_control/pous/programs/main.st) sets `high_level_alarm` at level 80 or higher, blocks `pump_running` while the alarm is active, and clears the alarm after the command is OFF and the level is below 80. The [FUXA export](../../lab/hmi/fuxa-project.json) maps the alarm LED to `high_level_alarm` with a 1–1 range and red fill. These settings explain the expected behavior; the operator report is the observation.

Result: screenshot-supported PASS for the active alarm display and extinguished pump-running indicator at `80%`; operator-reported PASS for clearing after OFF. The detailed transition timing, Modbus packets, and restart persistence remain unverified.
