# ICS Security Assessment Lab

가상 탱크·펌프 제어 환경에서 **Modbus TCP 통신과 접근 경계를 진단하고, 개선 후 정상 운영까지 재검증**하는 실습 프로젝트입니다. 보안 컨설팅 업무의 흐름인 범위 설정 → 자산·통신 파악 → 증거 기반 발견사항 → 개선안 → 재검증 → 보고를 보여주는 것이 목표입니다.

이 환경은 OpenPLC Runtime v4, OpenPLC Editor v4, FUXA HMI, Docker Compose로 구성합니다. 실제 설비나 고객 환경을 진단한 결과로 해석하지 않습니다.

## 현재 상태

| 항목 | 상태 | 근거 또는 다음 확인 |
| --- | --- | --- |
| 범위·구성·진단 방법 | 문서 작성 | [`docs/`](docs/) |
| 가상 탱크 PLC 프로그램·Compose | 저장소에 작성 | [`lab/plc/tank_control/`](lab/plc/tank_control/), [`lab/compose/`](lab/compose/) |
| Editor 시뮬레이터·Docker Runtime 연결, PLC 업로드 | 사용자 실행 로그로 컴파일·업로드·시작 확인 | Runtime 이미지 digest와 지속 실행 상태는 미확인 |
| Modbus TCP 서버 | 읽기 및 펌프 명령 쓰기·상태 변화 확인 | [`evidence/baseline/`](evidence/baseline/) |
| FUXA Modbus 연결·태그 읽기 | 연결 표시와 4개 태그 값·갱신 시각 확인 | [`evidence/baseline/fuxa-tags-2026-09-17.md`](evidence/baseline/fuxa-tags-2026-09-17.md) |
| FUXA 운전 화면 | 수위·펌프 명령·상태와 80% 경보 동작을 사용자 관찰로 확인 | [`evidence/baseline/fuxa-mainview-2026-09-18.md`](evidence/baseline/fuxa-mainview-2026-09-18.md), [`경보 관찰`](evidence/baseline/fuxa-high-level-alarm-2026-09-18.md) |
| 정상 패킷 | 정지 상태의 Modbus 읽기 요청·응답 27쌍 확인 | [`패킷 분석`](evidence/baseline/fuxa-openplc-pcap-2026-09-18.md) |
| 보안 평가·개선·재검증 | 미실시 | 정상 기준 확보 후 진행 |

**현재 성과를 취약점 발견이나 조치 성공으로 주장하지 않습니다.** Modbus 읽기·쓰기, 짧은 공정 상태 변화, FUXA의 태그 값과 수동 운전 화면 반응, 정지 상태의 정상 읽기 패킷을 확인했습니다. 운전 중 패킷과 보안 통제는 아직 검증하지 않았습니다.

## 컨설팅 관점의 평가 질문

1. 어떤 자산과 서비스가 실제로 존재하며, 누가 PLC에 접근할 수 있는가?
2. 정상 HMI 요청·응답과 운전 상태는 무엇인가?
3. 일반 Modbus TCP에서 관찰한 값과 쓰기 동작은 무엇이며, 어떤 접근 경계가 필요한가?
4. 통제를 적용한 뒤 비인가 경로는 차단되고 정상 HMI 운전은 유지되는가?

관찰 사실, 위험 추정, 실제 검증 결과를 구분합니다. 평가 범위는 소유한 Docker 실습 환경과 가상 태그로 제한합니다. 실제 설비의 안전성이나 IEC 62443 준수를 주장하지 않습니다.

## 저장소 길잡이

| 경로 | 내용 |
| --- | --- |
| [`docs/project-scope.md`](docs/project-scope.md) | 목표, 범위, 일정과 포트폴리오 완료 기준 |
| [`docs/architecture.md`](docs/architecture.md) | 역할, 통신 방향, 네트워크 경계 |
| [`docs/methodology.md`](docs/methodology.md) | 평가 체크리스트, 중단 조건, 증거·보고 기준 |
| [`docs/modbus-setup.md`](docs/modbus-setup.md) | 다음 실행 작업과 태그별 예상 주소 |
| [`docs/pc-transfer.md`](docs/pc-transfer.md) | 다른 PC로 옮길 때의 저장소·Docker 데이터 인계 |
| [`docs/fuxa-setup.md`](docs/fuxa-setup.md) | FUXA 연결·태그 주소·복원 절차 |
| [`docs/packet-capture.md`](docs/packet-capture.md) | FUXA↔PLC 정상 Modbus 패킷 캡처 절차 |
| [`lab/compose/compose.yaml`](lab/compose/compose.yaml) | OpenPLC·FUXA 컨테이너 설정 |
| [`lab/plc/tank_control/`](lab/plc/tank_control/) | 제어 프로그램 원본 |
| [`evidence/`](evidence/) | 정상 기준, 평가, 개선, 재검증 증거를 저장할 위치 |

## 다음 완료 기준

운전 중 패킷과 재시작 후 복원을 baseline으로 확보하고, 이후 접근 경계 평가·개선·재검증을 진행합니다.

Runtime과 FUXA의 `latest` 태그는 아직 정확한 이미지 digest로 고정하지 않았습니다. 재현 절차와 최종 결과는 실측 버전·증거를 확보한 뒤 갱신합니다.
