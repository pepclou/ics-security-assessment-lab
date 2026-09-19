# Finding AC-01 — Unrestricted Modbus command access inside the control network

## Summary

Any container attached to the current shared Docker `control` network can reach the OpenPLC Modbus service and issue a pump command without a FUXA or PLC application credential. A controlled assessment container reproduced the condition and changed the modeled process state.

## Rating

**High within this lab's trust model.** Network access to the shared control segment is required, which limits exposure. Once present, a client can directly change an operational command and influence process state without another authorization step. This rating applies only to the virtual lab; it is not a claim about physical safety impact.

## Evidence

- Assessment record: [`AC-02 unauthenticated write`](../evidence/assessment/ac-02-unauthenticated-write-2026-09-19.md).
- Raw output: [`ac-02-write-test-2026-09-19.txt`](../evidence/assessment/ac-02-write-test-2026-09-19.txt).
- Baseline comparison: [`FUXA pump operation packets`](../evidence/baseline/fuxa-openplc-operation-2026-09-18.md).

The assessment container read an initial OFF state, wrote the command ON, observed `pump_running=true` and the level rise from 0 to 3, then restored the command OFF and observed the pump stop. No FUXA session or PLC credential was supplied.

## Root cause

OpenPLC, FUXA, and the assessment services share one Docker bridge network. Reachability to TCP 5020 is effectively the authorization boundary. The current Modbus endpoint accepts the tested read and write function codes from any client that can reach it.

## Recommendation

Place OpenPLC and FUXA on a dedicated internal control network and remove general assessment workloads from that network. Give the evaluator a separate network with no route or shared attachment to OpenPLC. Keep TCP 5020 unpublished on the host. This network control should allow FUXA polling and commands while preventing the same assessment container from reaching the PLC.

Treat FUXA as a trusted Modbus client: segmentation does not prevent misuse if the FUXA backend is compromised. Where the product and operational design support it, add protocol-aware enforcement or authenticated secure transport as a separate defense.

## Retest criteria

1. From the separated evaluator role, the same read/write test fails before any command is accepted.
2. OpenPLC remains running; failure is caused by the access boundary rather than service shutdown.
3. FUXA continues polling and can perform the baseline ON/OFF sequence.
4. The command is OFF and the pump is stopped after testing.

Status: **Open — remediation and retest not yet performed.**
