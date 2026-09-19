# PC 전환 인계

> 아래 내용에는 작성 당시의 미검증 상태가 포함된다. 현재 완료 결과는 [최종 기술 보고서](../reports/final-report.md)를 기준으로 하고, 새 PC에서는 이 문서의 복원 절차를 다시 검증해야 한다.

작성일: 2026-09-16. 이 문서는 현재 저장소 상태를 기준으로 한다. 기존 PC의 Docker Runtime과 FUXA 데이터는 이 작업 환경에서 직접 확인하지 못했다.

## 옮길 대상

| 대상 | 현재 위치 | 전환 방법 |
| --- | --- | --- |
| PLC 원본, Compose, Modbus 설정, 문서 | Git 저장소 | 변경 사항을 GitHub에 반영한 뒤 새 PC에서 clone |
| OpenPLC Runtime 계정·저장된 프로젝트·상태 | Docker의 `openplc_data` 볼륨 | 필요하면 기존 PC에서 별도 백업·복원. PLC 원본은 Git으로도 복원 가능 |
| FUXA 화면·태그·사용자 데이터 | Docker의 `fuxa_*` 볼륨 | FUXA 프로젝트 export 또는 볼륨 백업·복원 필요. 현재 Git에는 HMI 프로젝트가 없음 |
| Editor 설치와 로컬 설정 | PC별 환경 | 새 PC에 호환 버전을 설치하고 Git의 `lab/plc/tank_control`을 열어 연결 설정 확인 |
| 실습 증거 | `evidence/` 또는 기존 PC의 다른 위치 | 실제 파일을 확인해 개인 정보·인증정보를 제거한 공개본만 Git에 반영 |

Docker 볼륨은 Git clone으로 이동하지 않는다. Compose의 `name: ics-security-assessment-lab`를 유지하면 Compose가 만드는 볼륨 이름도 같은 프로젝트 이름을 기준으로 관리된다. 인증정보가 담긴 볼륨 백업 파일은 공개 저장소에 올리지 않는다.

## 기존 PC에서 마무리

1. 저장소의 미커밋 변경을 확인하고 필요한 내용만 commit/push한다. 현재 이 대화의 변경은 아직 원격에 게시되지 않았다.
2. Docker가 있는 PC에서 `docker compose -f lab/compose/compose.yaml ps`와 `docker compose -f lab/compose/compose.yaml images`를 기록한다. 두 이미지의 실제 digest와 OpenPLC Editor 버전을 기록한다. `latest`만으로는 동일한 환경을 보장할 수 없다.
3. FUXA에서 프로젝트 export 기능을 사용할 수 있으면 export 파일을 별도 보관한다. export가 안 되거나 사용자·설정까지 그대로 옮겨야 하면 Docker 볼륨을 백업한다.
4. 볼륨 백업 전 해당 Compose 서비스를 멈추고, 백업 뒤 원래 PC에서 정상 재시작 여부를 확인한다. 백업은 Git 저장소 밖에 보관하고 안전한 경로로 새 PC에 전달한다. Docker의 [볼륨 백업·복원 절차](https://docs.docker.com/engine/storage/volumes/#back-up-restore-or-migrate-data-volumes)를 따른다.
5. 증거·스크린샷·PCAP이 있다면 파일 목록과 민감정보 포함 여부를 확인한다.

## 새 PC에서 재구성

1. Git, OpenPLC Editor v4, Docker Desktop을 설치하고 Docker Engine이 동작하는지 확인한다. Windows에서는 Docker Desktop의 [WSL 2 안내](https://docs.docker.com/desktop/features/wsl/)를 확인한다.
2. `https://github.com/pepclou/ics-security-assessment-lab.git`을 clone하고, 저장소 루트에서 `docker compose -f lab/compose/compose.yaml config`로 설정을 검증한다.
3. 필요하다면 **첫 기동 전에** 기존 PC의 볼륨을 복원한다. 볼륨 복원은 새로 만든 데이터를 덮을 수 있으므로 대상 이름과 백업 내용을 먼저 확인한다. 볼륨을 옮기지 않는 경우 Runtime 계정과 FUXA 화면을 새로 설정해야 한다.
4. `docker compose -f lab/compose/compose.yaml up -d` 후 Editor에서 Runtime `127.0.0.1:8443` 연결과 PLC 프로그램 실행을 확인한다.
5. [`modbus-setup.md`](modbus-setup.md)에 따라 `openplc:5020` 응답과 태그 주소를 확인한다. 그다음 FUXA 화면과 데이터가 복원됐는지 확인한다.
6. 정상 연결, Modbus 응답, HMI 값 변화, 재시작 후 유지 여부를 새 PC에서 다시 기록한다. 이전 PC의 성공 보고를 새 PC의 검증 결과로 대신하지 않는다.

## 현재 인계 상태

- Git 저장소에는 PLC 프로그램과 Compose 구성, Modbus 서버 설정 초안이 있다.
- Editor 시뮬레이터와 Docker Runtime 연결 성공은 사용자 보고이며 저장소에 실행 증거가 없다.
- Modbus 응답, FUXA 동작, Docker 볼륨 백업은 아직 검증되지 않았다.
- 이 대화가 실행되는 환경에는 Docker CLI가 없어 볼륨을 대신 백업할 수 없다.
