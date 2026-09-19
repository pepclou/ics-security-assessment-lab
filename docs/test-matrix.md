# 시험 결과 및 증거 추적표

기존 실행: 2026-09-17~19. 문서 리뷰와 추가 시험 설계: 2026-09-19.
PASS는 해당 행의 제한된 명제에만 적용한다. PARTIAL은 일부 관찰만 존재, NOT TESTED는 실행 증거 없음이다.
시험 AC-01/AC-02는 원인이 같아 보고서 Finding AC-01 하나로 묶는다.

| 시험 ID | 목적·사전조건 | 기대 결과 | 실제 결과 | 판정 | 증거·연결 |
|---|---|---|---|---|---|
| AS-01 | 등록된 PLC/HMI 서비스 식별 | 실행 자산·IP·버전과 구성 대응 | Modbus 응답과 구성 존재; 실행 IP 역할·정확 버전은 독립 식별 부족 | PARTIAL | [시작 기록](../evidence/baseline/runtime-startup-2026-09-17.md), [환경표](environment-record.md) |
| MB-01 | 가상망의 정상 Modbus 평문 분석 | 기능코드·주소·값을 원본에서 확인 | 정지 27쌍, 운전 120쌍, FC01/03/05 및 값 확인 | PASS(표본 범위) | [정지](../evidence/baseline/fuxa-openplc-pcap-2026-09-18.md), [운전](../evidence/baseline/fuxa-openplc-operation-2026-09-18.md) |
| AC-01 | 일반 client가 control에서 PLC에 도달하는가 | 초기 읽기 응답 수신 | 초기 태그 읽기 성공 | PASS(가설 재현) | [평가 원본](../evidence/assessment/ac-02-write-test-2026-09-19.txt), Finding AC-01 |
| AC-02 | 명령 OFF·경보 OFF에서 제한된 쓰기 | ON 후 상태/수위 변화, OFF 후 정지 | 수위 0→3→2, checks 5개 true, 오류 없음 | PASS(가설 재현) | [평가 기록](../evidence/assessment/ac-02-unauthenticated-write-2026-09-19.md), Finding AC-01 |
| MG-01 | 관리면의 실제 노출 경계 확인 | 허용 출발점 성공·비허용 출발점 실패 | loopback 게시 설정만 확인; 연결 대조 시험 없음 | NOT TESTED(설정 검토만) | [Compose](../lab/compose/compose.yaml) |
| RT-DNS | assessment에서 서비스명 해석 | 이름 기반 접속 실패 관찰 | Errno -3 | 관찰 확인(격리 PASS 아님) | [재검증 원본](../evidence/retest/ac-01-blocked-write-2026-09-19.txt) |
| RT-IP | 동일 시점 PLC IP, 신뢰/비신뢰 역할 | 비신뢰 TCP 실패·신뢰 TCP 성공 | 아직 실행하지 않음 | NOT TESTED | [실행서 3단계](retest-runbook.md) |
| OP-01 | 분리 후 HMI 읽기·제어 유지 | ON/OFF·값 갱신·정지 확인 | 운영자 보고와 정지 화면; 조치 후 PCAP 없음 | PARTIAL | [재검증 기록](../evidence/retest/ac-01-network-separation-2026-09-19.md) |
| AL-01 | 수위 80 경보 및 OFF 후 해제 | 경보 ON·펌프 정지, 조건 충족 시 해제 | 활성 화면 있음; 해제는 운영자 보고 | PARTIAL | [경보 기록](../evidence/baseline/fuxa-high-level-alarm-2026-09-18.md) |
| REC-01 | FUXA 재시작 후 복원 | 화면·연결·제어 복원 | 운영자 보고와 화면 | PARTIAL | [복원 기록](../evidence/baseline/fuxa-restart-recovery-2026-09-19.md) |

## 계획 대비 편차

- 방법론은 60초 기준선을 제안했으나 실제 정지 13.011초, 운전 약 58초다. 요청·응답 사례 검증에는 사용하되 60초 관찰 기준 충족이나 장시간 안정성으로 표현하지 않는다. 향후 시험에서는 최소 구간과 프레임 상한을 별도로 관리한다.
- 패킷 IP가 FUXA/PLC라는 해석은 기존 구성·패턴과 일치하지만 실행 컨테이너 inspect로 독립 확인하지 않았다.
- MG-01은 현재 구성 검토만 했고 전체 관리면 보안평가를 완료하지 않았다.
- 새 검증 overlay와 TCP 연결 도구는 이번에 작성했다. 기존 시험 시점에 사용한 도구로 소급하지 않는다.

## Finding 종결 기준

RT-IP 대조 시험, OP-01 시계열 증거, 실행 환경 식별, 종료 상태 확인을 연결한 후 Finding AC-01의 종결 여부를 결정한다. DNS 실패만으로 종결하지 않는다. 남은 신뢰망 내부 client와 FUXA 침해 위험은 종결 후에도 잔여 위험이다.
