# Makefile for Credit Card Approval Prediction

.PHONY: install test lint run clean docker-build docker-run

install:
	pip install -e .
	pip install -r requirements.txt

test:
	pytest tests/ -v --cov=src --cov=flask_app --cov-report=term-missing

lint:
	flake8 src/ flask_app/ tests/ --max-line-length=120

run:
	python flask_app/app.py

docker-build:
	docker build -t credit-card-approval .

docker-run:
	docker run -p 5000:5000 credit-card-approval

clean:
	rmdir /s /q build dist credit_card_approval_prediction.egg-info .pytest_cache .cov_report
	del /q /s *.pyc *.pyo
