1. 최초 한번 반드시 실행

docker compose -f docker-compose.yaml up airflow-init


2. docker compose -f docker-compose.yaml up

3. localhost:8888
    airflow/airflow

✅ 요약: 실행 흐름
상황	명령어	설명
처음 설치한 날	docker compose -f docker-compose.yaml up airflow-init → 이후 docker compose -f docker-compose.yaml up	DB, 사용자, 로그 구조 초기화
다음부터는 매번	docker compose -f docker-compose.yaml up	Web UI 등 전체 서비스 실행
중간에 컨테이너 껐을 때	Ctrl + C 또는 Docker 종료 → 이후 docker compose up으로 재시작 가능	
정지할 때	Ctrl + C 또는 docker compose down	컨테이너 종료 (데이터는 유지됨)
