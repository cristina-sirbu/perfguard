run:
	./mvnw spring-boot:run

test:
	locust --headless --users 10 --spawn-rate 2 --host=http://localhost:8080 --run-time 10s

detect:
	python regression_detector.py

alert: detect

export:
	python perfguard_exporter.py

up:
	docker-compose up -d

dashboard:
	open http://localhost:3000

baseline:
	cp latest_results.csv baseline.csv

all: run test alert
