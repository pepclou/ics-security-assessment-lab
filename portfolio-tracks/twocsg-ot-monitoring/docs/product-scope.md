# 공식 근거와 상용 제품 경험의 경계

확인일: 2026-09-19. 공고 요구는 사용자가 제공한 투씨에스지 채용 이미지 기준이며 현재 채용 상태를 새로 확정한 문서는 아니다.

| 대상 | 확인한 공개 내용 | 이번 프로젝트와 관계 |
|---|---|---|
| Nozomi Guardian | 수동 트래픽 분석과 SPAN/TAP 기반 가시성, 데모 요청 페이지 | 수집 배치·운영 개념 참고. 라이선스·설치 이미지 확보 미확인 |
| TXOne EdgeIPS | 산업망 보호 및 inline/offline 모드 관련 공식 안내 | 수동 모니터링과 inline 차단의 차이 학습. 제품 실행 경험 없음 |
| SSenStone | 첨부 공고에 제품사명 존재 | 이번 작업에서 특정 제품·기능·실습 가능성 미확인 |
| Suricata | Modbus 기능코드·접근 유형·Unit ID 규칙, PCAP 입력 옵션 | 공개 도구 기반 실습 후보. 상용 OT 제품과 동등 기능 주장 금지 |

출처:

- [Guardian 공식 제품 소개](https://www.nozominetworks.com/platform/guardian)
- [EdgeIPS 제품 소개](https://www.txone.com/products/network-security/edgeips/)
- [EdgeIPS inline/offline 안내](https://help.txone.com/docs/how-to-configure-inline-offline-modes-for-edgeips-edgeips-pro)
- [Suricata Modbus 규칙 문서](https://docs.suricata.io/en/suricata-8.0.1/rules/modbus-keyword.html)
- [Suricata 명령행 옵션](https://docs.suricata.io/en/suricata-8.0.1/command-line-options.html)

열람한 문서 버전 8.0.1을 설치 완료 버전이나 최신 버전으로 취급하지 않는다. 실제 설치 시 지원되는 안정 릴리스를 확인한다. Suricata의 Modbus address 규칙은 해당 문서에서 1부터 시작하므로 wire offset 0과 혼동하지 않는다.

설치 권한이나 평가판 요청이 필요해지면 그 시점에 사용자와 경로를 결정한다. 공개 데모 영상 시청을 제품 구축 경험으로 기록하지 않는다.
