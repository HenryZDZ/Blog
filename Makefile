.PHONY: run test clean deploy

run:
	python3 run.py

test:
	python3 -m pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -f blog.db

deploy:
	gunicorn app:create_app\(\) -w 2 -b 127.0.0.1:8000
