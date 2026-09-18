# FUXA–OpenPLC pump operation packet baseline — 2026-09-18 (Asia/Seoul)

Scope: project-owned Docker lab, TCP port 5020. The operator started the passive `modbus-operation-capture` service, then switched the FUXA pump command ON for about 5 seconds and OFF. Source: [PCAP](fuxa-openplc-operation.pcap), parsed from Ethernet, IPv4, TCP, and complete Modbus TCP ADUs. This is a separate file from the [idle baseline](fuxa-openplc-pcap-2026-09-18.md).

- Analyzed ADU window: 2026-09-18 10:41:06.498–10:42:04.553 KST. File size: 32,247 bytes. SHA-256: `06CAD89595F8D9E982BBF358B03D4DB816971AED8DF5FEF4FA8178C9C3FA0325`.
- Captured TCP/5020 frames: 360. Complete Modbus TCP ADUs: 240, comprising 120 requests and 120 responses. All 120 transaction/Unit ID pairs have matching request and response function codes; no Modbus exception response was observed. The other 120 frames were not classified as complete ADUs by this parser.
- Endpoints: `172.18.0.3:45072` → `172.18.0.2:5020`, with responses in reverse. Unit ID 1. The client is consistent with FUXA's polling and the operator's switch action; its container IP was not independently verified.
- Read requests: 59 FC03 Holding Register reads at wire address 0, quantity 1 (`tank_level`); 59 FC01 Coil reads at wire address 0, quantity 3 (`pump_command`, `pump_running`, `high_level_alarm`).
- At 10:41:12.368, FC05 Write Single Coil transaction 123 wrote wire address 0, value `0xFF00` (ON). The response echoed the address and value at 10:41:12.369. At 10:41:18.854, transaction 138 wrote the same address, value `0x0000` (OFF); the response echoed it at 10:41:18.855.
- After the ON write, a coil-read response changed from byte `0x00` to `0x03` at 10:41:12.510. Bits 0 and 1 correspond to command and running status ON; bit 2 (alarm) remained 0. After the OFF write, the observed coil byte returned to `0x00` at 10:41:19.516.
- Holding-register responses showed level 0 before ON; values 1, 2, 3, 4, 5, and 6 during ON (last increase at 10:41:18.506); and 5, 4, 3, 2, 1, 0 after OFF (back to 0 at 10:41:24.510). This is consistent with the one-second increment/decrement logic in the [PLC program](../../lab/plc/tank_control/pous/programs/main.st).

Result: packet-supported PASS for one pump ON/OFF command sequence and the corresponding process-value and status changes in this lab. The PCAP does not test the 80% alarm transition, whether other network sources can write, access controls, or restart recovery. Visible Modbus fields are an observation, not by themselves a vulnerability finding.
