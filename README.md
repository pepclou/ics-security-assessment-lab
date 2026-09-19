# Modbus TCP 접근통제 진단 — 인더포레스트 지원용

OpenPLC·FUXA 가상 탱크에서 정상 통신과 비인가 역할의 운전 명령 변경을 분석한 개인 OT 보안 실습이다. 범위·증거·원인·개선·재검증 판단을 보여준다.

**현재 상태: 진단 재현 및 분리 구성 완료, 재검증 부분 완료.** DNS 실패는 확인했지만 IP 직접 차단은 미검증이다. 조치 후 FUXA 동작은 운영자 보고와 정지 화면으로 뒷받침되며 독립적인 PCAP은 없다. Runtime/FUXA digest와 Editor 버전도 과거 시험에 대해 미확인이다.

## 먼저 볼 문서

1. [지원용 요약](reports/portfolio-summary.md)
2. [기술 보고서](reports/final-report.md)
3. [Finding AC-01](reports/finding-ac-01.md)
4. [시험 결과·증거 추적표](docs/test-matrix.md)
5. [현재 실행 및 복원 절차](docs/retest-runbook.md)
6. [시험 환경 식별표](docs/environment-record.md)

## 핵심 증거

- [정지 PCAP 분석](evidence/baseline/fuxa-openplc-pcap-2026-09-18.md): 요청·응답 27쌍
- [운전 PCAP 분석](evidence/baseline/fuxa-openplc-operation-2026-09-18.md): 120쌍, ON/OFF 및 상태 변화
- [별도 client 쓰기 시험](evidence/assessment/ac-02-unauthenticated-write-2026-09-19.md): 명령 변경과 OFF 복원
- [재검증 기록](evidence/retest/ac-01-network-separation-2026-09-19.md): 원본 보존, DNS 실패의 해석 정정

## 실행 구성

[기본 Compose](lab/compose/compose.yaml)는 개선 후 상태다. 기본 evaluator는 assessment에 있어 정상 읽기·복원용으로 사용하지 않는다. [검증용 추가 구성](lab/compose/compose.verify.yaml)은 control의 임시 baseline 도구와 연결 시험·새 PCAP 캡처를 제공한다. 새 구성은 아직 Docker 실행 검증 전이다.

## 범위

소유한 가상 환경만 평가했다. 실제 PLC·물리 안전성·IEC 62443 준수·블랙박스 모의해킹·새로운 제품 취약점 발견을 주장하지 않는다. 일반 Modbus 특성과 배치 문제를 구별한다. 기존 [초기 설계](docs/architecture.md)와 [계획](docs/project-scope.md)은 역사적 문서이며 현재 실행서는 위 링크를 따른다.

원본 기준: pepclou/ics-security-assessment-lab 커밋 c274e6ceeaea6d01e0e0b69405f171c9af34b979. 이 보완본은 추가 시험을 위한 문서와 도구를 포함한다. 새 실험 성공 결과를 추가한 것은 아니다.

## 다른 노트북에서 이어하기

[새 노트북 시작 안내](docs/new-laptop.md)를 따른다.

## 별도 회사용 프로젝트

[투씨에스지용 구축·기술지원 설계](portfolio-tracks/twocsg-ot-monitoring/README.md)는 별도 트랙이며 아직 구축 성과가 없는 계획 단계다.
