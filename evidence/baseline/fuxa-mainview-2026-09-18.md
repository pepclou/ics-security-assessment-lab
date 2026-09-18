# FUXA MainView command and status observation — 2026-09-18 (Asia/Seoul)

Source: operator-provided [preview screenshot at rest](fuxa-mainview-off-2026-09-17.png), exported FUXA project, and the operator's report during a brief manual switch test. Screenshot SHA-256: `3ea99eb5593ff936cfc936baabb930502c57be043c629d4888eeed760407b9c0`.

The preview screenshot showed `0%` and an empty pump-status circle. The exported project contained `tank_level_display` bound to `tank_level`, `pump_running_led` bound to `pump_running`, and `pump_command_switch` bound to `pump_command` with OFF=0 and ON=1.

In the first test, the operator reported that switching ON raised the tank level but the LED stayed empty. We compared the project export and found that the LED's 1–1 range had an empty `color` value. A corrected export changed that value to `#22c55e` and kept all other JSON fields equal. After loading it, the operator affirmed that the LED turned green with the pump on and returned to an empty circle after switching off.

The later FUXA export added `high_level_alarm_led`, bound to the `high_level_alarm` tag with a 1–1 range and red `#f90127ff` fill. Export SHA-256: `da2428fc99ad856972618bf0a225ce8a4d6c16e94fd9c253ebe8eaa4879ce061`. The operator subsequently reported that the alarm sequence worked; see [high-level alarm observation](fuxa-high-level-alarm-2026-09-18.md).

The pump run result is an operator observation, not an independently captured trace of the ON interval. The attempted separate Docker pump-check command did not return a result during this session, so it is not counted as another successful test. Packet-level timing and restart recovery remain to be tested.
