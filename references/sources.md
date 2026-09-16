# GitHub / Official References

프로젝트: ICS Security Assessment Lab — Modbus TCP Security Assessment & Remediation

열람일: 2026-09-14. 공식 자료를 기능 근거로 우선 사용하고 공개 실습 저장소는 범위·증거 구성 사례로만 참고했다. 아래 URL의 main/master/dev는 변할 수 있으며 실행 호환성을 보증하지 않는다. 코드, Compose 설정, 제어 프로그램, 이미지, PCAP을 복제하지 않았다. 문서와 비교표는 이 프로젝트 목적에 맞춰 새로 작성했다.

## 공식 자료

| ID | URL | License 확인 | 무엇을 참고했는지 / 한계 |
| --- | --- | --- | --- |
| O1 | https://github.com/Autonomy-Logic/openplc-runtime | MIT; https://github.com/Autonomy-Logic/openplc-runtime/blob/main/LICENSE | v4의 IEC 실행, Editor 관리 API, Docker 지원, Modbus plugin 구조. 실제 연동 미검증 |
| O2 | https://github.com/Autonomy-Logic/openplc-runtime/blob/main/docs/DOCKER.md | 저장소 MIT; 배포 이미지 의존성 전체는 별도 미검토 | 공식 이미지 배포와 영속성 확인 필요성. 예제 명령·설정은 복제하지 않음 |
| O3 | https://github.com/thiagoralves/OpenPLC_v3 | 저장소 GPL-3.0 표기 확인 | EOL 및 v4 대체 안내. 예전 실습의 v3 관리 방식과 현재 설계를 혼용하지 않기 위해 확인 |
| O4 | https://github.com/frangoteam/FUXA | MIT; https://github.com/frangoteam/FUXA/blob/master/LICENSE | HMI/SCADA 시각화, Modbus TCP, Docker 실행 및 프로젝트 영속성 |
| O5 | https://frangoteam.github.io/FUXA/ | 문서 별도 License 미확인; O4 코드 License와 구별 | 공식 문서 진입점. 후속 버전별 설정 확인용 |
| O6 | https://github.com/pymodbus-dev/pymodbus | BSD 3개 조항 확인; https://github.com/pymodbus-dev/pymodbus/blob/dev/LICENSE | B/C의 client·server·simulator 기능과 API 변경 위험. 일반 서버와 PLC runtime의 차이 판단 |
| O7 | https://www.modbus.org/modbus-specifications | 웹 문서 재사용 License 미확인 | Application Protocol 및 Modbus Security 안내. 일반 Modbus와 보안 확장을 구분 |
| O8 | https://docs.docker.com/compose/how-tos/networking/ | 해당 페이지 재사용 License 미확인 | 서비스 이름 기반 통신과 컨테이너/호스트 포트 구별 |
| O9 | https://docs.docker.com/reference/compose-file/networks/ | 해당 페이지 재사용 License 미확인 | internal 네트워크와 서비스 연결 경계의 설계 근거 |
| O10 | https://docs.docker.com/compose/how-tos/startup-order/ | 해당 페이지 재사용 License 미확인 | 시작 순서와 준비 상태의 차이 |
| O11 | https://www.wireshark.org/docs/dfref/m/mbtcp.html | 문서 별도 License 미확인 | MBTCP Transaction ID·Unit ID 등 패킷 해석 필드 |
| O12 | https://www.wireshark.org/docs/dfref/m/modbus.html | 문서 별도 License 미확인 | Modbus Function Code·주소·예외 등 해석 필드 |

License 미확인은 자유 복제 가능이라는 뜻이 아니다. 확인된 코드 License도 해당 프로젝트의 모든 의존성이나 별도 문서에 자동 적용된다고 가정하지 않는다. 이번에는 링크와 독자적 요약만 사용했다.

## 사용자 제시 공개 GitHub 후보

| ID | URL | License 확인 | 무엇을 참고했는지 | 채택하지 않은 부분 / 근거 한계 |
| --- | --- | --- | --- | --- |
| G1 | https://github.com/alidakwar/ICS-Lab | 열람한 루트/README에서 미확인 | HMI→PLC 통신과 분리 전후 증거 구성 | pfSense·다중 영역·Zeek·Suricata는 5일 최소 범위를 넘음. README 결과를 본인 검증으로 간주하지 않음 |
| G2 | https://github.com/hakim-hub10/ais-lab2-ics | 열람한 루트/README에서 미확인 | OpenPLC·Docker·Modbus 캡처 흐름. 이미지 부재로 HMI 대체를 했다는 사례 | polling 도구는 완성된 시각적 HMI와 다름. v3 방식의 관리 정보는 v4에 적용하지 않음 |
| G3 | https://github.com/andercodder/ot-ics-cyber-lab | 열람한 루트/README에서 미확인 | 구성도·PCAP·writeup을 연결하는 결과물 구성 | Labshock·DMZ·SIEM 범위 제외. README에 진행 중으로 표시된 항목을 완성 사례로 세지 않음 |
| G4 | https://github.com/404saint/ics-ot-homelab | 열람한 루트/README에서 미확인 | OpenPLC와 FUXA를 함께 배치한 사례 | Ignition 추가 구성과 공격 코드는 범위 제외. 이 사례만으로 현재 버전의 Compose 호환성을 입증하지 못함 |
| G5 | https://github.com/bsuar6/ics-modbus-lab | 열람한 루트/README에서 미확인 | 관리면 노출·포트 충돌·개선 기록이라는 문제 분류 | OS 서비스 종료나 설치 절차를 복제하지 않음. v3/v4 포트 설명 혼용 가능성이 있어 공식 자료 우선 |

## 자료에서 내린 판단과 아직 모르는 것

A 추천은 공식 기능과 사용자의 PLC/HMI 교육 경험, Python 초급, 5일 제한을 종합한 판단이다. G4는 조합의 공개 사례일 뿐 이 호스트에서의 재현 성공 증거가 아니다. A/B/C 모두 직접 실행하지 않았으므로 안정성과 소요 시간은 예상치다.

OpenPLC Editor/runtime의 정확한 호환 버전, FUXA tag mapping, Modbus plugin 기본 설정, 이미지 digest, 호스트 캡처 방식은 후속 구현에서 확인할 항목이다. 불명확한 버전을 임의로 고정하거나 다른 프로젝트의 설정을 가져와 검증된 것처럼 제시하지 않았다.
