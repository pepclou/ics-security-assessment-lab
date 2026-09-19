# AC-02 — Unauthenticated Modbus write validation — 2026-09-19 (Asia/Seoul)

Scope: project-owned Docker lab. Source role: ephemeral `modbus-pump-check` assessment container attached to the Compose `control` network. Target: `openplc:5020`, Unit ID 1. The assessment container had no FUXA session or PLC credential. Raw console evidence: [`ac-02-write-test-2026-09-19.txt`](ac-02-write-test-2026-09-19.txt), SHA-256 `8212C0190F94FF99F9D69F6722DC491121D57B7ADBF6F7FC620880D5BBC32701`.

Precondition reported by the operator: FUXA pump switch OFF, level below 80%, and no high-level alarm. The tool independently read the initial state before writing and was configured to restore the command OFF in a `finally` block.

Observed structured output:

- Before: `tank_level=0`, `pump_command=false`, `pump_running=false`, `high_level_alarm=false`.
- During the controlled write: `tank_level=3`, `pump_command=true`, `pump_running=true`, `high_level_alarm=false`.
- After automatic restoration: `tank_level=2`, `pump_command=false`, `pump_running=false`, `high_level_alarm=false`.
- All five checks were `true`: command accepted, running state observed, level increased, command restored OFF, and pump stopped after restoration.
- `error=null` and `reset_error=null`.

Result: PASS for the assessment hypothesis that a non-HMI container with access to the flat `control` network can read the process tags and write the pump command without an application credential. The accepted command caused the modeled process state to change, and the tool restored the command OFF.

Limitations: this is a deliberately vulnerable virtual lab, not a production PLC or external network. The test did not attempt discovery outside the declared target, persistence, repeated writes, alarm bypass, denial of service, or management-interface access. It demonstrates a network placement and endpoint access-control gap; it is not assigned a product CVE.
