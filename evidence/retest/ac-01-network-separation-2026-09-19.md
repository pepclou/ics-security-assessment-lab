# AC-01 network separation retest — 2026-09-19 (Asia/Seoul)

Scope: project-owned Docker lab. Policy change: `modbus-probe` and `modbus-pump-check` were moved from the shared `control` network to a separate internal `assessment` network. OpenPLC and FUXA remained on `control`; neither control service was recreated for this change.

## Blocked evaluator path

The operator validated the Compose model, then ran the same `modbus-pump-check` evaluator used for the before-state assessment. Raw output: [`ac-01-blocked-write-2026-09-19.txt`](ac-01-blocked-write-2026-09-19.txt), SHA-256 `4808020D8ED624017648B1F8975FCD90FE096C2FB874039E67E75EB9F1B4925E`.

Docker created the internal `assessment` network and the ephemeral evaluator container. The tool stopped at its first baseline read with `Baseline read failed: [Errno -3] Try again`. Because hostname resolution/connectivity failed before the tool obtained a socket response, it did not reach the Modbus read or write stage. Corrected result: hostname-resolution failure observed; direct-IP reachability not tested. This is not a complete network-isolation PASS.

## Allowed HMI path

After the blocked test, the operator reported that FUXA still updated and that an ON/OFF command sequence worked. The supplied [post-test screenshot](fuxa-allowed-path-2026-09-19.png) shows the saved MainView, command switch OFF, and level `12%`. Screenshot SHA-256: `4F41A87B310F1F0FBB90D8F6010065E80E36F180F297BF4A2DE3B1E7D5397B96`.

The screenshot supports HMI rendering, a displayed value, and the final displayed OFF state, but cannot prove data freshness; the ON transition and green running indication rely on the operator's observation because they are not shown in this single post-test image. Result: operator-reported PASS for allowed FUXA operation after separation.

## Conclusion and limits

Review correction: retest PARTIAL. Name-based access failed and HMI operation was operator-reported. Direct-IP isolation and post-change packet evidence remain outstanding. Original raw evidence and hashes are unchanged. The control is Docker network attachment, not endpoint authentication or function-code authorization. It does not protect against a client deliberately attached to `control`, compromise of FUXA, or a Docker-host administrator. The PowerShell `NativeCommandError` wrapper in the raw output was produced while capturing Docker progress written to stderr; the security-relevant failure is the tool's final baseline-read error.
