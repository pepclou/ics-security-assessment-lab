# Network remediation and retest

Status: applied and retested on 2026-09-19. See the [retest evidence](../evidence/retest/ac-01-network-separation-2026-09-19.md).

## Change

OpenPLC and FUXA remain on the existing `control` network. The temporary `modbus-probe` and `modbus-pump-check` evaluator services are moved to a separate internal `assessment` network. No service joins both networks, TCP 5020 remains unpublished on the host, and the capture services continue to observe the OpenPLC namespace without creating a routed bridge.

This change removes the evaluator's Docker network path to OpenPLC. It is a network allowlist by attachment, not Modbus function-code filtering or endpoint authentication. FUXA remains a trusted client, so compromise of FUXA remains residual risk.

## Apply without recreating the control services

From the repository root in PowerShell:

```powershell
$dockerCli = "$env:LOCALAPPDATA\Programs\DockerDesktop\resources\bin\docker.exe"
& $dockerCli compose -f lab/compose/compose.yaml --profile verify --profile capture config --quiet
& $dockerCli compose -f lab/compose/compose.yaml --profile verify run --rm modbus-pump-check
```

The first command validates the complete Compose model. The second creates only the temporary evaluator and its `assessment` network; it must not recreate `openplc` or `fuxa`. The retest passes when the evaluator fails before a Modbus command is accepted because `openplc` cannot be resolved or reached from `assessment`.

After the blocked evaluator test, confirm in FUXA that the connection remains green, the level still updates, and one ON/OFF command works. This proves that OpenPLC remained available to the allowed HMI while the evaluator path was removed.

## Rollback

If an unexpected effect occurs, stop the evaluator. Revert the two evaluator service attachments from `assessment` to `control` in Compose. The control containers do not need to be recreated for either the change or rollback because their service definitions and existing network attachment are unchanged.
