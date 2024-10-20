# 구직 정보 웹 스크래퍼

이 프로젝트는 사용자가 입력한 검색어를 기반으로 Wanted 웹사이트에서 채용 공고를 스크래핑하여 결과를 보여주는 웹입니다. Flask와 Playwright를 사용하여 동적인 웹 환경을 처리하고, HTML, CSS, JavaScript로 프론트엔드를 구성했습니다.

## 기능

- **검색 기능**: 사용자가 입력한 키워드에 따라 관련 채용 공고를 검색합니다.
- **로딩 인디케이터**: 검색 진행 중에는 로딩 메시지를 표시합니다.
- **결과 페이지네이션**: 검색 결과를 페이지 단위로 나누어 보여줍니다.
- **모바일 반응형 디자인**: 다양한 화면 크기에 맞춰 디자인이 조정됩니다.

## 요구 사항

- Python 3.7+
- Flask
- Playwright
- BeautifulSoup4
- CSS 및 JavaScript

## 설치 방법

1. **저장소 클론하기**:

   ```bash
   git clone https://github.com/yourusername/job-scraper.git
   cd job-scraper

   ```

2. **가상 환경 만들기(선택 사항)**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows에서는 `venv\Scripts\activate` 사용

   ```

3. **필요한 패키지 설치**:
   ```bash
   pip install Flask playwright beautifulsoup4
   playwright install
   ```

## 파일 구조

- **rlok.py**: 애플리케이션의 주요 백엔드 로직을 처리하는 Flask 서버 코드입니다.
- **templates/**: 사용자 인터페이스를 구성하는 HTML,CSS와 JavaScript 파일들이 위치합니다.
  - **index.html**: 사용자가 검색할 수 있는 메인 페이지입니다.

이 구조는 애플리케이션의 백엔드와 프론트엔드를 효과적으로 분리하여 관리합니다.
