# FUXA restart recovery observation — 2026-09-19 (Asia/Seoul)

Scope: project-owned Docker lab. The operator ran `docker compose -f lab/compose/compose.yaml restart fuxa`. The supplied terminal output showed the existing `ics-security-assessment-lab-fuxa-1` container restarting; it did not recreate OpenPLC or its volume. The operator then reported that the saved MainView, connection, values, and control behavior worked after refresh.

The supplied [post-restart screenshot](fuxa-restart-recovery-2026-09-19.png) shows the saved MainView at level `0%`, with the command switch OFF, the running indicator empty, and the alarm indicator in its default green state. Screenshot SHA-256: `47711716A7F23B292F3E0074C1DDC9A36C75B581713F56906651B72176431A48`.

The [saved FUXA export](../../lab/hmi/fuxa-project.json) maps `pump_running_led` to `pump_running` and colors it green only for value 1. It maps `high_level_alarm_led` to `high_level_alarm`, colors it red for value 1, and its SVG group has a green default fill. Therefore, the screenshot is consistent with level 0, pump not running, and no high-level alarm. The screenshot does not include the connection-settings page, container health details, or an independent post-restart packet capture; those parts rely on the operator report.

Result: operator-reported PASS for FUXA restart recovery, supported by a post-restart screenshot showing the persisted view and plausible live state. Usability observation: the two indicators have no visible labels, so their meaning is ambiguous without configuration knowledge. Add clear labels before treating this as an operator-ready HMI.
