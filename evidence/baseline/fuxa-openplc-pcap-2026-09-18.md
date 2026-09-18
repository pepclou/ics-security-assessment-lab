# FUXA–OpenPLC idle Modbus packet baseline — 2026-09-18 (Asia/Seoul)

Scope: project-owned Docker lab, TCP port 5020. The operator started the `modbus-capture` Compose service while OpenPLC and FUXA were running. The service shares OpenPLC's network namespace and passively captured up to 80 packets with `tcpdump`; it did not issue requests or change PLC tags. Source: [PCAP](fuxa-openplc-baseline.pcap), analyzed from the file's Ethernet, IPv4, TCP, and Modbus TCP headers and payloads.

- Capture window: 2026-09-18 10:27:40.756–10:27:53.767 KST (13.011 seconds).
- File: 7,192 bytes, classic little-endian PCAP, Ethernet link type.
- SHA-256: `4BF65A8C2A20F233E2C057CD886ED2F651E3AA003E9ECAF28D92AD91F1D168AE`.
- Captured TCP/5020 frames: 80. Of these, 54 contain one complete Modbus TCP ADU: 27 requests and 27 responses. The other 26 frames were not classified as complete ADUs by this parser.
- Endpoints in the capture: client `172.18.0.3:45072` → server `172.18.0.2:5020`. The server endpoint matches the configured OpenPLC Modbus listener. The client's FUXA identity is inferred from the Compose topology and polling pattern; the container IP was not independently verified.
- MBAP Unit ID: 1 in all 54 ADUs. Transaction IDs 37–63 each appear once in a request and once in a corresponding response. All 27 pairs have the same function code, with no pairing failures.
- Function 03, Read Holding Registers: 14 request/response pairs, wire start address 0, quantity 1. Each response contains one register with value 0. This maps to the FUXA `tank_level` display address `400001`.
- Function 01, Read Coils: 13 request/response pairs, wire start address 0, quantity 3. Each response's first coil byte is 0, consistent with `pump_command`, `pump_running`, and `high_level_alarm` all being 0 in this interval.
- No Modbus exception function code was present among the complete ADUs.

Result: a short idle-state read-polling baseline with complete request/response pairs and no observed exception responses. It does not show a pump write, changing level, alarm transition, access control, or recovery after restart. Those require separate evidence. Plain Modbus fields are visible in the packet payload, but this observation alone is not a vulnerability finding.
