# Network remediation and retest

Status: segmentation configuration applied in the original lab; retest PARTIAL. [Original evidence and corrected interpretation](../evidence/retest/ac-01-network-separation-2026-09-19.md).

OpenPLC and FUXA remain on control. The original evaluator services use a separate internal assessment network. No normal service joins both; TCP 5020 has no host publishing. Only assessment has `internal: true`. Restricting control-network egress is not implemented.

The original execution failed in DNS resolution. It did not establish direct-IP isolation. A post-test HMI image and operator report exist; post-change packet verification does not.

Use the [current execution and recovery procedure](retest-runbook.md) to collect numeric-IP negative and trusted-path positive controls. Configuration validation alone is not runtime verification. A command failure alone is not security PASS.

If a test fails unexpectedly, stop the temporary evaluator and restore OFF through the trusted HMI or explicit baseline service. Do not routinely reconnect the untrusted evaluator as a recovery measure, recreate PLC/HMI, or delete volumes.
