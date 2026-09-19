# ICS Security Assessment Lab — Modbus TCP Security Assessment & Remediation

> 이 문서는 2026-09-14에 작성한 초기 계획과 선택 근거를 보존한 기록이다. 실제 수행 결과와 현재 판정은 [최종 기술 보고서](../reports/final-report.md)를 기준으로 한다.

## 문서 상태

Architecture v0.1 / Day 1 설계 / 조사일: 2026-09-14 (Asia/Seoul).
이 문서는 계획이다. 환경 구축, 통신 성공, 취약점 발견 또는 조치 성공을 주장하지 않는다.

## 현재 저장소 점검

- 확인 경로: `C:\Users\clope\Documents\Codex\2026-09-14\referenced-chatgpt-conversation-this-is-an`
- `git status --short --branch`와 `git status --porcelain=v1`: 모두 `fatal: not a git repository (or any of the parent directories): .git`.
- 기존 구조: 비어 있는 `outputs/`, `work/`. 숨김 파일을 포함한 파일 검색에서 프로젝트 파일이 발견되지 않았다.
- 현재 경로 및 확인한 상위 경로에서 AGENTS.md가 발견되지 않았다.
- Git 저장소가 아니므로 branch, remote, staged/unstaged 변경, merge 상태는 확인 불가다. 이를 clean 상태로 해석하지 않는다.
- 신규 결과 경로 `outputs/ics-security-assessment-lab/`는 생성 전 존재하지 않았다. 기존 파일 덮어쓰기나 Git 초기화는 하지 않는다.
- 실제 저장소 경로는 사용자에게 요청했다. 아래 골격은 이 대화의 결과물이며, 기존 저장소에 통합되었다고 볼 수 없다. 추후 통합 시 동일 경로 파일을 먼저 비교하고 충돌 파일은 보존한다.
- 참조 대화의 캐시가 중간에서 잘렸고 전체 대화를 읽는 도구는 제공되지 않았다. 이번 사용자가 명시한 FIRST TASK 범위를 기준으로 작성했다.

## 목표와 직무 연결

지원자가 작은 제조제어환경의 자산과 통신을 이해하고, 관찰한 증거로 문제를 설명하며, 조치 후 정상 운영까지 재확인할 수 있음을 보여 준다. 기존 Web/CVE 프로젝트와 구별되는 핵심은 PLC/HMI 역할, 산업 프로토콜 분석, 접근통제, 공정 영향 설명이다. **최종 산출물은 인더포레스트 지원에 바로 사용할 수 있는 포트폴리오**여야 한다. 실습 환경이나 기술 보고서만 완성한 상태는 프로젝트 완료가 아니다.

전체 프로젝트는 5일을 목표로 하되, 이번 작업은 Day 1 문서와 디렉터리 골격에서 끝난다. 하루 작업시간과 Docker 설치 여부는 미확인이다. 일정은 보장치가 아닌 상대적 난이도 판단이다.

## 후보 비교

아래 평가는 공식 기능과 프로젝트 범위를 바탕으로 한 설계 판단이며 직접 실행한 벤치마크가 아니다. C도 동일한 재현성 조건을 위해 Docker Compose로 두 서비스를 관리한다고 가정한다. Python HMI는 최소한 상태 표시와 조작 화면을 가진 자체 제작 HMI로 정의한다. 단순 polling 스크립트는 HMI 완성으로 세지 않는다.

| 기준 | A: OpenPLC + FUXA + Compose | B: OpenPLC + Python HMI + Compose | C: Python Modbus PLC Simulator + FUXA |
| --- | --- | --- | --- |
| 5일 내 구현 가능성 | 중상: 제어 로직 1개와 화면 1개로 제한하면 유리. Editor 연동이 관문 | 중: PLC 학습과 화면 개발을 동시에 해야 함 | 중상: 프로토콜 서버는 작게 만들 수 있으나 공정 모델은 직접 정의해야 함 |
| 재현성 | 중상: 이미지, Editor 버전, PLC 원본, FUXA export를 함께 고정해야 함 | 중: 여기에 Python/UI 의존성과 자체 코드 관리가 추가됨 | 중상: Python 패키지/API와 FUXA 설정을 고정하면 단순함 |
| Docker 안정성 | 중상 예상: 공식 배포 경로 있음. 이 PC에서 미검증 | 중 예상: OpenPLC와 자체 HMI 이미지 모두 점검 필요 | 중상 예상: 비교적 가벼우나 Python 이미지/시뮬레이터 검증 필요 |
| PLC/HMI 개념 표현력 | 높음: IEC 제어 프로그램과 시각화 역할을 분리 | 중상: PLC는 분명하지만 화면 설계 품질에 좌우됨 | 중: HMI는 분명하나 일반 Modbus 서버가 PLC scan/IEC 실행을 입증하지 않음 |
| Modbus 패킷 분석 | 높음: 정상 HMI polling과 응답 분석 가능 | 높음: polling을 직접 설명하기 쉬움 | 높음: 서버/클라이언트 요청·응답 분석 가능 |
| 향후 보안진단 | 높음: HMI/PLC 경계, 관리면, 접근통제 | 중상: 자체 HMI 결함과 OT 문제를 구분해야 함 | 중상: 프로토콜/접근통제 검증에 적합. 실제 PLC 제품 결함으로 일반화 불가 |
| Troubleshooting 위험 | 중: v3/v4 혼용, tag mapping, 캡처 위치 | 높음: A의 PLC 문제에 UI와 Python 디버깅 추가 | 중: API 변경, 공정 갱신, 주소와 자료형 해석 |
| Portfolio 가치 | 높음: PLC 로직–HMI–패킷–조치의 연결이 명확 | 중상: Python 역량을 보이지만 기존 포트폴리오와 중복 | 중상: 5일 결과 확보에 유리하나 PLC 경험 주장의 범위가 좁음 |

근거: [OpenPLC v4](https://github.com/Autonomy-Logic/openplc-runtime), [FUXA](https://github.com/frangoteam/FUXA), [PyModbus](https://github.com/pymodbus-dev/pymodbus), [Compose 네트워크](https://docs.docker.com/compose/how-tos/networking/). 세부 출처와 참고 범위는 [sources.md](../references/sources.md)에 기록한다.

## Decision

**A: OpenPLC Runtime v4 + OpenPLC Editor v4 + FUXA + Docker Compose를 추천한다.** Editor는 엔지니어링 도구이며 상시 컨테이너 서비스는 PLC와 HMI 두 개다. 이미 PLC/HMI 교육 경험이 있으므로 자체 UI 개발보다 제어와 진단 증거에 시간을 쓰는 편이 목적에 맞다.

B는 Python 초급 상태에서 UI·통신·제어를 함께 디버깅해야 하므로 제외한다. C는 유력한 축소 대안이지만 이번 핵심인 PLC 프로그램 실행과 HMI 분리를 A보다 약하게 보여 준다. 이번 선택은 A 한 개이며 C를 병행 구현하지 않는다.

OpenPLC v3는 공식 저장소에 EOL이 명시되어 있어 신규 설계 기본값에서 제외한다. v4는 Editor와 HTTPS 관리 API를 사용하므로 v3의 브라우저 관리 화면/포트 설명을 그대로 적용하지 않는다. [v3 공식 상태](https://github.com/thiagoralves/OpenPLC_v3)

## 범위

- 설계 대상: 가상 탱크 1개, 가상 펌프 1개, PLC 1개, HMI 화면 1개, Modbus TCP, 평가자 역할 1개.
- 이번 산출물: 이 문서, architecture.md, methodology.md, references/sources.md, 비어 있는 구현·증거·보고서 폴더.
- 이번 제외: Docker 설치/실행, 이미지 다운로드, Compose/Dockerfile 작성, PLC/HMI 구현, 스캔, 공격 코드, 자동화 코드, 외부 코드·설정 복제.
- 전체 최소 범위에서 제외: 실제 설비, 인터넷 대상 진단, DoS, CVE exploit, 다중 공정, OPC UA, Kubernetes, SIEM/IDS 구축, 모바일·클라우드 진단.

## 5일 경계와 일정 위험

| 일차 | 향후 목표 | 완료 판단 |
| --- | --- | --- |
| Day 1 — 이번 작업 | 비교·선택·설계·골격 | 문서 4개와 범위 점검 |
| Day 2 — 미착수 | 최소 정상 공정과 HMI 통신 | 상태 변화와 Modbus 응답, 재시작 후 복원 |
| Day 3 — 미착수 | 자산·서비스·정상 패킷·체크리스트 | 관찰 증거와 가설 분리 |
| Day 4 — 미착수 | 제한 검증과 접근통제 개선 | 허용/차단 경로 및 공정 영향 기록 |
| Day 5 — 미착수 | 재검증·기술 보고서·지원용 포트폴리오 편집 | Before/After, 정상 운영 증거, 제출용 요약본 |

## 지원용 최종 산출물

- 공개 저장소: 처음 보는 검토자가 목적, 실행 범위, 결과, 재현 방법을 찾을 수 있는 README와 필요한 문서·설정. 비밀정보와 개인 이메일은 포함하지 않는다.
- 기술 보고서: 범위와 방법, 자산·통신, 정상 기준, 발견사항별 증거·원인·공정 영향·위험도, 개선 내용, 같은 조건의 재검증, 한계와 잔여 위험.
- 지원용 요약본: 한눈에 읽히는 문제→검증→개선→결과, 본인의 역할, 사용 도구, 직무 요구사항과 연결되는 역량. 보고서·증거로 이어지는 링크를 포함한다.
- 설명 준비: 구성도, Modbus 요청·응답 한 쌍, 대표 발견사항, 조치 후 정상 운영을 지원자가 스스로 설명할 수 있어야 한다.

실행·발견·개선이 실제로 확인되기 전에는 성공 사례처럼 쓰지 않는다. 공개 저장소에 올리기 전에는 PCAP, 화면, 로그에 개인 정보나 인증 정보가 들어 있지 않은지 확인한다.

Day 2 초반 최대 2시간을 버전·Editor 연결·Modbus mapping 확인에 배정하는 것을 제안한다. 해결되지 않으면 원인과 로그를 남기고 일정/스택 결정을 재검토한다. 자동으로 다른 스택을 설치하거나 범위를 늘리지 않는다. 주요 위험은 미확정 버전 조합, 호스트 자원, Windows Docker 캡처 경로, Modbus 주소 오해다.

## Day 1 Definition of Done

- 세 후보를 8개 기준으로 비교하고 추천 1개와 제외 이유를 기록한다.
- 구성요소, 통신 방향, 경계, 캡처 지점, 최소 공정과 미확정 항목을 문서화한다.
- 진단→증거→원인→위험→조치→재검증 흐름을 정의한다.
- 참고 URL, 확인 가능한 License, 참고 내용과 한계를 남긴다.
- 기존 파일을 보존하고 문서 4개와 빈 폴더용 .gitkeep 외 구현물을 생성하지 않는다.
- 실제 Git 저장소 점검/통합은 경로 미제공으로 미완료임을 명시한다.
