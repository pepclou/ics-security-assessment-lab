# 포트폴리오 요약 — Modbus TCP 접근 경계 진단과 개선

## 한 줄 소개

OpenPLC·FUXA 가상 탱크 환경에서 정상 Modbus 통신을 패킷으로 기준화하고, 비인가 역할의 펌프 명령 변경을 재현한 뒤 Docker 네트워크 분리와 정상 운영 재검증까지 수행한 OT 보안 실습 프로젝트다.

## 문제

PLC, HMI와 평가 도구가 하나의 Docker 제어망을 공유했다. 이 구조에서 TCP 5020에 도달한 일반 client가 추가 권한 확인 없이 가상 펌프 명령을 변경할 수 있는지 증거가 필요했다. 단순 차단만 적용하면 정상 HMI까지 끊을 수 있으므로 개선 후 운영 유지도 함께 검증해야 했다.

## 수행 내용

- Structured Text로 수위·펌프·80% 고수위 경보 로직 구성
- FUXA에 Holding Register 1개와 Coil 3개를 연결하고 운전 화면 제작
- OpenPLC namespace에서 정지·운전 상태 PCAP 2개 확보
- Unit ID, FC01·FC03·FC05, wire offset, 값과 공정 상태를 연결해 분석
- 별도 평가 컨테이너에서 제한된 ON 쓰기와 자동 OFF 복원 수행
- 공유망의 무자격 명령 접근을 Finding AC-01로 작성
- 평가 도구를 별도 내부망으로 옮겨 PLC 경로 차단
- 같은 도구의 실패와 FUXA ON·OFF 정상 동작을 함께 재검증

## 핵심 결과

| 항목 | 결과 |
| --- | --- |
| 정상 통신 | 정지 요청·응답 27쌍, 운전 요청·응답 120쌍 분석 |
| 명령 해석 | FC05 Coil 0의 `0xFF00` ON과 `0x0000` OFF 확인 |
| 공정 연결 | Coil `0x00 → 0x03 → 0x00`, 수위 `0 → 6 → 0` 확인 |
| 보안 검증 | 일반 평가 client가 인증 없이 펌프 명령 변경 성공 |
| 개선 | 평가자 역할을 별도 internal 네트워크로 분리 |
| 재검증 | 평가자 첫 읽기 전 차단, FUXA 값 갱신·ON/OFF 유지 |

## 사용 기술

OpenPLC Runtime v4, OpenPLC Editor v4, IEC 61131-3 Structured Text, FUXA, Modbus TCP, Docker Compose, tcpdump/PCAP, Python socket 기반 제한 검증, Git/GitHub.

## 보여 주는 역량

- PLC와 HMI의 역할, 명령값과 실제 상태의 차이를 설명할 수 있다.
- 화면 주소와 Modbus wire offset을 구분하고 패킷 값과 태그를 연결할 수 있다.
- 관찰 사실, 위험 추정, 제품 취약점 주장을 구별한다.
- 안전한 초기 조건과 자동 복원 절차를 포함해 제한 검증을 수행한다.
- 보안조치의 차단 성공뿐 아니라 허용 업무의 정상 동작을 함께 확인한다.
- 원본 로그·PCAP·스크린샷의 해시와 한계를 기록해 결론의 범위를 관리한다.

## 면접에서 설명할 흐름

1. **왜 정상 기준선부터 만들었는가?** 공격처럼 보이는 쓰기와 정상 HMI 쓰기를 패킷·공정 상태로 비교하기 위해서다.
2. **무엇을 발견했는가?** 같은 제어망의 일반 client가 별도 자격증명 없이 Coil 0을 쓰고 가상 펌프 상태를 바꿀 수 있었다.
3. **왜 네트워크 분리를 선택했는가?** 현재 제품 구성에서 가장 작은 변경으로 허용된 FUXA 경로만 유지할 수 있었기 때문이다.
4. **어떻게 조치 효과를 증명했는가?** 같은 평가 도구는 첫 읽기 전에 실패했고, OpenPLC는 계속 실행되며 FUXA ON·OFF는 유지되는 것을 확인했다.
5. **무엇이 남았는가?** FUXA 침해와 신뢰망 내부 client, 평문 통신, 이미지 digest 미고정은 잔여 위험이다.

## 이력서용 문장

> OpenPLC·FUXA 기반 가상 제어환경에서 Modbus TCP 정상 PCAP을 분석하고, 공유 제어망의 무자격 펌프 명령 변경을 재현했다. 평가자 네트워크를 분리한 뒤 동일 경로 차단과 FUXA 정상 운전을 재검증하여 증거 기반 Finding과 Before/After 결과를 문서화했다.

## 주요 링크

- [최종 기술 보고서](final-report.md)
- [발견사항 AC-01](finding-ac-01.md)
- [운전 패킷 분석](../evidence/baseline/fuxa-openplc-operation-2026-09-18.md)
- [접근통제 평가](../evidence/assessment/ac-02-unauthenticated-write-2026-09-19.md)
- [개선 후 재검증](../evidence/retest/ac-01-network-separation-2026-09-19.md)
