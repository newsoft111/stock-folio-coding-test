## Introduce

- 스톡폴리오 과제


## Requirements

- Python 3.12


## Install

```bash
pip install poetry
poetry install
poetry run uvicorn main:app --reload --host=0.0.0.0 --port=8000
```


## Structure

- app/
  - api/
    - 모든 API 라우트 정의와 요청 핸들러를 포함합니다. FastAPI 라우터 로직이 이곳에 위치합니다.
  - core/
   - 핵심 애플리케이션 설정, 구성 및 애플리케이션 전체에서 사용되는 전역 상수나 열거형을 담고 있습니다.
  - db/
   - 데이터베이스 연결과 세션을 관리합니다. 데이터베이스 초기화 및 연결 풀링이 포함됩니다.
  - models/
   - 데이터베이스 테이블과 그 관계를 표현하는 SQLAlchemy ORM 모델을 정의합니다.
  - schemas/
    - 요청 및 응답 데이터의 검증과 직렬화에 사용되는 Pydantic 모델을 포함합니다.
  - services/
    - 애플리케이션의 핵심 비즈니스 로직을 구현합니다. 이 계층은 API 라우트와 데이터베이스 모델 사이에 위치합니다.
  - utils/
    - 유틸리티 함수, 헬퍼 클래스 및 애플리케이션의 여러 부분에서 공유되는 코드를 담고 있습니다.
- static/vidoes
  - 모든 영상 파일을 저장하는 디렉토리로, 다음을 포함합니다:
    - 원본 업로드된 파일
    - 처리된 파일 (예: trim, concat) 또는 실패한 파일



## Challenge
- 확장성 있는 영상 처리 파이프라인
  - 문제: 다양한 영상 처리 작업을 유연하게 추가하고 관리해야 함.
  - 해결 전략: 모듈화된 비디오 처리 서비스 구현.
  - 구현: VideoService 클래스에서 각 작업 유형별로 메서드를 분리하고, 새로운 작업 유형을 쉽게 추가할 수 있는 구조 설계.
