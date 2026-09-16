# Runtime startup observation — 2026-09-17 (Asia/Seoul)

Source: Docker Desktop 4.91.0 container view for `ics-security-assessment-lab-openplc-1`. The container was started from `ghcr.io/autonomy-logic/openplc-runtime:latest` after a fresh Docker Desktop installation. The image digest and Editor version were not captured. Container log timestamps displayed `2026-09-16 22:27` and may use a different timezone from this note.

| Observation | Evidence from the container view | Interpretation |
| --- | --- | --- |
| Container | `Running`; host port `127.0.0.1:8443` mapped to container port `8443` | Container is running; this does not prove PLC logic or Modbus is running |
| Management API | Repeated `GET /api/version HTTP/1.1` responses with status `200` | HTTPS management service answers its health request |
| Modbus plugin | `[MODBUS_SLAVE] Runtime arguments extracted successfully`; `[PLUGIN]: All plugins initialized (not started)` | Plugin initialization succeeded; server listening was not observed |
| PLC program | `No libplc_*.so file found in ./build`; `PLC State: EMPTY`; `State transition to RUNNING failed` | No compiled PLC project is loaded in this fresh Runtime |

Later on 2026-09-17, the operator connected OpenPLC Editor and uploaded the PLC program. See `plc-upload-2026-09-17.md`. The Modbus server was disabled during that upload. Record the Runtime image digest and Editor version during the next verification. Do not record Runtime credentials in this public repository.

This is a startup observation, not a security finding or evidence of successful Modbus communication.
