# 재고 관리 시스템 (Stock Management System)

메가커피 마천역점을 위한 Django 기반 재고 관리 웹 애플리케이션입니다.

## 주요 기능

- **재고 CRUD** — 품목 추가, 조회, 수정, 삭제
- **재고 실사** — 이전/다음 탐색이 가능한 실사 전용 폼 (증가/감소 버튼 포함)
- **검색** — 품목명 기반 실시간 검색
- **위치별 그룹화** — 창고, 냉장실, 냉동실, 쇼케이스 등 보관 위치별 아코디언 뷰
- **CSV 가져오기/내보내기** — 대량 데이터 일괄 처리
- **공유 기능** — 읽기 전용 재고 목록 URL, QR 코드 생성, 클립보드 텍스트 복사
- **반응형 UI** — Bootstrap 5 기반 모바일 지원

## 기술 스택

| 구분 | 기술 |
|------|------|
| Backend | Django 4.2 |
| Database | SQLite3 |
| Frontend | Bootstrap 5.3.3, jQuery 3.6.0 |
| Image | Pillow, qrcode |
| Server | Nginx + uWSGI |
| Hosting | AWS EC2 |

## 프로젝트 구조

```
django-project/
├── erpsite/              # 프로젝트 설정
│   ├── settings.py
│   ├── urls.py
│   └── views.py
├── stock/                # 재고 관리 앱
│   ├── migrations/
│   ├── templates/stock/
│   ├── static/stock/css/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
├── templates/            # 공통 템플릿 (base, home, 404)
├── .config/
│   ├── nginx/            # Nginx 설정
│   └── uwsgi/            # uWSGI 설정
└── requirements.txt
```

## 데이터 모델

### Item

| 필드 | 타입 | 설명 |
|------|------|------|
| `itemCode` | IntegerField | 자동 생성 고유 코드 |
| `typeOfItem` | CharField | 품목 유형 (디저트, MD, 시즌, 재고, 시럽 등) |
| `name` | CharField | 품목명 (최대 30자) |
| `units` | IntegerField | 단위 수량 |
| `place` | CharField | 보관 위치 |
| `amountOfBulk` | FloatField | 박스/묶음 수량 |
| `amountOfEach` | FloatField | 낱개 수량 |
| `lastTimeSaved` | DateTimeField | 마지막 수정 시각 (자동) |

## URL 구성

| URL | 기능 |
|-----|------|
| `/` | 홈 |
| `/stock/list/` | 재고 목록 (검색 포함) |
| `/stock/create_item` | 품목 추가 |
| `/stock/update_item/<pk>` | 품목 정보 수정 |
| `/stock/update_item_each/<pk>` | 수량 수정 |
| `/stock/investigate_item/<pk>` | 재고 실사 |
| `/stock/share_list/` | 위치별 공유 목록 |
| `/stock/readonly_list/` | 공개 읽기 전용 목록 |
| `/stock/generate_qr/` | QR 코드 생성 |
| `/stock/upload_csv/` | CSV 가져오기 |
| `/stock/export_csv/` | CSV 내보내기 |

## 설치 및 실행

### 요구 사항

- Python 3.10+
- pip

### 로컬 실행

```bash
# 저장소 클론
git clone https://github.com/your-username/django-project.git
cd django-project

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션
python manage.py migrate

# 개발 서버 실행
python manage.py runserver
```

서버 실행 후 `http://127.0.0.1:8000` 에서 접근 가능합니다.

### 환경 설정

`erpsite/settings.py`에서 다음 항목을 프로덕션 환경에 맞게 수정하세요.

```python
SECRET_KEY = '...'       # 안전한 비밀 키로 교체
DEBUG = False            # 프로덕션에서는 False 유지
ALLOWED_HOSTS = [...]    # 실제 도메인/IP로 교체
```

## 배포 (Production)

Nginx + uWSGI 조합으로 AWS EC2에 배포됩니다.

```
Browser → Nginx (port 80) → uWSGI socket → Django
```

- Nginx 설정: `.config/nginx/erpsite.conf`
- uWSGI 설정: `.config/uwsgi/erpsite.ini`
- Systemd 서비스: `.config/uwsgi/uwsgi.service`

정적 파일 수집:

```bash
python manage.py collectstatic
```

## CSV 포맷

가져오기 CSV는 다음 컬럼 순서를 따릅니다.

```
itemCode, typeOfItem, name, units, place, amountOfBulk, amountOfEach
```

> 주의: CSV 가져오기 시 기존 데이터가 전부 삭제됩니다.
