# 시험 환경 식별표

이 표의 미확인은 과거 시험 기록의 한계다. 지금 확보한 값은 새 Run ID로 분리한다.

| 항목 | 기존 시험 기록 | 새 시험 시 기록할 내용 |
|---|---|---|
| 원본 저장소 | c274e6ceeaea6d01e0e0b69405f171c9af34b979에서 검토 | 실제 실행한 배포본 commit 또는 파일 SHA-256 |
| OS/WSL | Windows, 상세 버전 미확인 | OS 빌드·WSL 버전 |
| Docker Desktop | 시작 관찰에 4.91.0 기재 | 실제 표시값 |
| Engine/Compose | 미확인 | docker version / compose version |
| OpenPLC | v4 계열, latest 태그 | 실행 컨테이너 Image ID·RepoDigest·제품 버전 |
| FUXA | latest 태그 | 실행 Image ID·RepoDigest·제품 버전 |
| Editor | v4 계열, 정확 버전 미확인 | About 화면 또는 설치 버전 |
| Modbus 플러그인 | 설치 및 연결 관찰, 버전 미확인 | 실제 설치 버전·설정 |
| 평가 도구 | 저장소 Python 도구, python:3.12-alpine | 도구 SHA-256·Python 이미지 ID |
| PCAP | 정지·운전 원본과 SHA-256 기록 | 새 파일명·기간·출발 역할·해시 |
| PLC/HMI 원본 | 저장소에 존재; 당시 배포본과 해시 대조 없음 | 실제 업로드/export와 해시 대응 |
| 초기 수위 | 소스 초기값 50, 평가 시 읽기값 0 | 실제 안정화 절차와 초기값 |

한계: 저장소 커밋은 문서를 식별할 뿐, 그 커밋의 모든 파일이 당시 컨테이너에 배포되었다는 증거는 아니다. 새 digest를 과거 시험 값으로 채워 넣지 않는다.

수집 명령은 [재검증 실행서](retest-runbook.md)를 따른다. 컨테이너 전체 설정이나 볼륨을 공개하지 않고 필요한 필드만 저장한다.
