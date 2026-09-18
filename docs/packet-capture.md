# FUXA–OpenPLC normal Modbus packet capture

Status: run on 2026-09-18. The 80-packet capture was validated as a short, idle-state Modbus read baseline. See the [packet evidence](../evidence/baseline/fuxa-openplc-pcap-2026-09-18.md). This capture is limited to the project-owned Docker lab and TCP port 5020.

The `modbus-capture` Compose profile uses the same network namespace as the running OpenPLC container. This places `tcpdump` on the interface that receives FUXA's Modbus requests. The capture service has no published port and only the `NET_RAW` capability; `-p` avoids promiscuous mode. It writes at most 80 matching packets to `evidence/baseline/fuxa-openplc-baseline.pcap` and then exits. It does not send Modbus requests or write PLC tags.

From the repository root in PowerShell, with `openplc` and `fuxa` already running and the FUXA tag values updating:

```powershell
docker compose -f lab/compose/compose.yaml config
docker compose -f lab/compose/compose.yaml --profile capture up -d --no-deps modbus-capture
docker compose -f lab/compose/compose.yaml ps -a modbus-capture
docker compose -f lab/compose/compose.yaml logs modbus-capture
Get-Item evidence/baseline/fuxa-openplc-baseline.pcap
```

The `config` check must succeed before running the service. The image may need to be pulled on first use. The capture should end after 80 TCP/5020 packets. Check the log for a packet count and confirm the file has nonzero size. If it remains running without packets, check the FUXA connection indicator and tag timestamps, then stop only the capture service. Do not recreate `openplc` to troubleshoot this step, since that can remove the currently uploaded PLC program.

The PCAP contains lab addresses and process values. Review it before publishing. Record the capture time, SHA-256, endpoint IPs, Unit ID, function codes, request/response pairing, wire offsets, and any exception responses. A file's existence alone is not proof of normal operation. This capture was parsed to check those fields; it contains only read polling during an idle interval, not pump commands or alarm transitions.

The network namespace approach follows [netshoot's Compose example](https://github.com/nicolaka/netshoot) and Docker's [`network_mode: service:{name}` definition](https://docs.docker.com/reference/compose-file/services/#network_mode). The `v0.16` tag is recorded in Compose; its actual image digest has not been recorded.
