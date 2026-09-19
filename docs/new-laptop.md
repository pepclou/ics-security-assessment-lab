# 다른 노트북에서 추가 시험하기

기존 증거는 보존하고 새 노트북의 결과는 별도 Run ID로 기록한다. 새 노트북에서 개선 전 공유망 조건과 개선 후 격리망 조건을 모두 비교한다.

## 1. 작업본 받기

Git, Docker Desktop의 Linux 컨테이너 엔진, 호환되는 OpenPLC Editor v4를 준비한다.

```powershell
git clone https://github.com/pepclou/ics-security-assessment-lab.git
cd ics-security-assessment-lab
docker version
docker compose version
```

기존 clone이면 로컬 변경을 먼저 확인하고 `git pull --ff-only`로 받는다. 미커밋 작업을 덮어쓰지 않는다. Docker는 Client와 Server 모두 확인해야 한다.

## 2. PLC/HMI 재구축

```powershell
docker compose -f lab/compose/compose.yaml config --quiet
docker compose -f lab/compose/compose.yaml up -d openplc fuxa
```

- Editor에서 `lab/plc/tank_control`을 열고 Runtime `https://127.0.0.1:8443`에 연결한다. 새 Runtime의 계정 설정은 해당 버전 안내를 따른다.
- 프로젝트의 Modbus 서버가 `0.0.0.0:5020`으로 활성화되어 있는지 확인하고 Build & Upload 및 프로그램 시작을 수행한다. [설정 설명](modbus-setup.md)을 참고한다.
- FUXA `http://127.0.0.1:1881`에서 필요한 Modbus 플러그인을 설치하고 `lab/hmi/fuxa-project.json`을 불러온 뒤 저장한다. 주소 `openplc:5020`, Unit ID 1, 4개 태그를 확인한다. [FUXA 설명](fuxa-setup.md)을 참고한다.
- Git에는 Docker 볼륨·계정·설치된 플러그인이 포함되지 않는다. 새 환경에서 별도로 설정한다. 과거 관찰 기록은 현재 환경의 성공 증거가 아니다.
- 실행 이미지가 latest를 사용하므로 과거와 동일한 버전이라고 가정하지 않는다. 설치 실패가 발생하면 임의로 결과를 채우지 말고 버전과 오류를 기록한다.

## 3. 추가 시험

[재검증 실행서](retest-runbook.md)를 순서대로 수행한다. 새 overlay는 Docker에서 실행 검증 전이므로 첫 config 검증이 실패하면 중단하고 오류를 기록한다.

1. 실행 버전·컨테이너 IP·이미지 ID 수집.
2. 신뢰 경로 읽기, 명령 OFF·경보 OFF·수위 0 확인.
3. control의 임시 도구로 제한된 쓰기와 OFF 복원 확인.
4. assessment에서 PLC 실제 IP 직접 TCP 연결 대조 시험.
5. FUXA 정상 ON/OFF와 값 변화의 새 PCAP 확보.
6. [시험표](test-matrix.md)와 [환경표](environment-record.md)를 새 증거에 연결.

원본 PCAP·로그 파일에 덮어쓰지 않는다. TCP 실패만으로 PASS 처리하지 말고 같은 시점 신뢰 경로 성공·네트워크 구성을 함께 대조한다. 실제 설비나 회사 자료는 시험에 사용하지 않는다.
