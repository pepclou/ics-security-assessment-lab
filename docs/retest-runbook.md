# 보완 시험 실행 절차

상태: 작성 및 정적 검토. Docker에서 실행하지 않았으며 성공 결과가 아니다.
기존 원본 로그·PCAP은 보존한다. 새 결과는 새로운 Run ID로 저장한다.
대상은 소유한 가상 PLC 1대, TCP 5020, Unit ID 1이다.

## 1. 실행 환경 및 초기 상태

저장소 루트의 PowerShell에서 실행한다. `docker`가 PATH에 없다면 실제 Docker CLI 경로를 사용한다.

```powershell
$composeArgs = @('-f', 'lab/compose/compose.yaml', '-f', 'lab/compose/compose.verify.yaml')
$runId = Get-Date -Format 'yyyyMMdd-HHmmss'
$runDir = "evidence/retest/$runId"
New-Item -ItemType Directory -Path $runDir -ErrorAction Stop | Out-Null
docker version > "$runDir/docker-version.txt"
docker compose version > "$runDir/compose-version.txt"
docker compose @composeArgs --profile verify --profile capture config > "$runDir/effective-compose.yaml"
if ($LASTEXITCODE -ne 0) { throw 'Compose validation failed' }
docker compose @composeArgs ps > "$runDir/services.txt"
$plcId = docker compose @composeArgs ps -q openplc
$hmiId = docker compose @composeArgs ps -q fuxa
if (!$plcId -or !$hmiId) { throw 'Existing PLC/HMI containers required' }
docker inspect --format '{{json .NetworkSettings.Networks}}' $plcId > "$runDir/plc-networks.json"
docker inspect --format '{{json .NetworkSettings.Networks}}' $hmiId > "$runDir/hmi-networks.json"
docker inspect --format '{{.Image}}' $plcId > "$runDir/plc-image-id.txt"
docker inspect --format '{{.Image}}' $hmiId > "$runDir/hmi-image-id.txt"
$plcImage = docker inspect --format '{{.Image}}' $plcId
$hmiImage = docker inspect --format '{{.Image}}' $hmiId
docker image inspect --format '{{json .RepoDigests}}' $plcImage > "$runDir/plc-digests.json"
docker image inspect --format '{{json .RepoDigests}}' $hmiImage > "$runDir/hmi-digests.json"
```

현재 태그가 가리키는 이미지 대신 실행 중인 컨테이너의 Image ID를 사용한다.
Editor와 FUXA/플러그인의 실측 버전은 [환경 식별표](environment-record.md)에 수동 기록한다.
전체 inspect에는 환경변수 등 민감정보가 포함될 수 있으므로 위의 제한된 필드만 공개한다.

FUXA 연결 정상, 명령 OFF, 경보 OFF, 수위 0을 확인한다. PLC 소스 초기값은 50이므로 새 기동 직후 0이라고 가정하지 않는다. 정상 배수로 0이 될 때까지 기다린다.

## 2. 제어망에서 정상 읽기와 복원 경로 확인

```powershell
docker compose @composeArgs run --rm --no-deps baseline-probe > "$runDir/trusted-read-before.txt" 2>&1
```

성공 출력과 초기값을 직접 확인한다. 실패하면 후속 쓰기 시험을 진행하지 않는다.
`baseline-*`는 명시적으로 호출하는 임시 신뢰 도구이고, 기존 `modbus-*` 평가자 서비스는 계속 assessment에 있다.
개선 전 조건을 새로 재현할 필요가 있을 때만 `baseline-pump-check`를 실행한다. 이는 control에 있는 일반 client 역할이며 제품 인증 기능을 검증하는 시험은 아니다.

```powershell
docker compose @composeArgs run --rm --no-deps baseline-pump-check > "$runDir/shared-network-write.txt" 2>&1
```

`error`, `reset_error`, 다섯 checks 및 실제 종료 상태를 확인한다. `finally`는 OFF 복원 시도이며 강제 종료·통신 단절 시 보장이 아니다. 수위 전체를 이전 값으로 되돌리는 기능도 아니다.

복원이 필요하면 먼저 FUXA에서 OFF 후 명령·운전 상태가 모두 false인지 확인한다. 도구를 사용할 경우 접근 가능한 control의 다음 경로를 쓴다.

```powershell
docker compose @composeArgs run --rm --no-deps baseline-pump-check python /tools/modbus_pump_check.py --reset
```

모든 신뢰 경로가 끊기면 쓰기를 반복하지 않는다. 가상 실습 운영자가 Runtime 프로그램 정지 등 수동 조치를 수행하고 상태를 확인한 뒤 다시 시작한다. `down -v`로 데이터를 지우지 않는다.

## 3. DNS와 IP 직접 접속을 구분

```powershell
$plcNetworks = docker inspect --format '{{json .NetworkSettings.Networks}}' $plcId | ConvertFrom-Json
$plcIp = $plcNetworks.'ics-security-assessment-lab_control'.IPAddress
if (!$plcIp) { throw 'Verify actual control network name and PLC IP before continuing' }
docker compose @composeArgs run --rm --no-deps isolated-tcp-check > "$runDir/isolated-dns.txt" 2>&1
docker compose @composeArgs run --rm --no-deps isolated-tcp-check python /tools/tcp_boundary_check.py --host $plcIp > "$runDir/isolated-ip.txt" 2>&1
docker compose @composeArgs run --rm --no-deps trusted-tcp-check python /tools/tcp_boundary_check.py --host $plcIp > "$runDir/trusted-ip.txt" 2>&1
```

세 명령은 각각 JSON을 출력해야 한다. Docker 실행 자체의 오류를 차단으로 세지 않는다.
이 도구는 연결만 시도하고 Modbus 데이터는 보내지 않는다. DNS 실패는 exit 2, TCP 실패는 exit 3, 연결 성공은 exit 0이며 이 값 자체가 보안 PASS 판정은 아니다.
격리 IP 실패 + 신뢰 IP 성공 + 실행 네트워크 확인이 일치해야 네트워크 차단 근거로 쓴다. Connection refused는 서비스 미기동·잘못된 포트 또는 reject 가능성을 구분해야 하고, timeout만으로 방화벽 규칙을 특정하지 않는다.
IP 접속 성공 시 보완 실패로 기록하고 그 상태에서 쓰기 시험을 하지 않는다.

## 4. 조치 후 HMI 회귀 증거

새 PowerShell 창에서 같은 composeArgs를 정의하고 고유 파일명을 지정한다. 캡처 전에 같은 이름의 파일이 없는지 확인한다.

```powershell
docker compose @composeArgs run --rm --no-deps retest-capture tcpdump -i eth0 -p -nn -s 0 -U -c 600 -w /capture/REPLACE-RUN-ID-hmi-after.pcap tcp port 5020
```

REPLACE-RUN-ID를 이번 runId로 바꾼다. 최대 600프레임의 상한은 최소 60초를 보장하지 않는다.
정상 HMI에서 약 3초 ON 후 OFF한다. 명령·운전 상태·수위 변화와 시각을 기록하고, 갱신 중단이나 예상치 못한 상태가 나타나면 중단 및 복원한다.
600프레임 전에 통신이 멈추면 캡처만 Ctrl+C로 종료한다. 캡처를 끝내려고 PLC를 재생성하지 않는다.
목표 관찰 구간 60초 이상을 충족하지 않으면 편차로 기록한다.

PCAP에서 FC05 요청·응답뿐 아니라 FC01 운전 상태와 FC03 수위 변화도 확인한다. 동시 실행한 baseline 도구 트래픽과 FUXA 트래픽을 출발 IP로 구분한다.
화면 원본에 명령·상태 이름과 관찰 시각을 함께 남긴다. 정지 화면 한 장만으로 갱신이나 ON 전환을 확정하지 않는다.

## 5. 판정 및 증거 보존

```powershell
Get-ChildItem -LiteralPath $runDir -File | Get-FileHash -Algorithm SHA256 | Select-Object Path,Hash | Export-Csv "$runDir/hashes.csv" -NoTypeInformation
```

PCAP은 별도 retest 루트에 생성되므로 해당 파일 해시도 기록한다. 시험자, 시간대, 정확한 명령, 출발/대상, 기대·실제 결과, 종료 상태를 [시험 결과표](test-matrix.md)에 연결한다.
원본에 민감정보가 있으면 공개용 사본과 그 해시를 분리한다. 과거 실행 결과를 새 시험 결과로 바꾸지 않는다.
