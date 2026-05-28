.PHONY: install test lint build clean

install:
	pip install -e ".[quantum,test,dev]"
	pip install -r agents/requirements.txt 2>/dev/null || true

install-rust:
	cd native && cargo build --release

install-go:
	cd agentless && go build -o ../bin/agentless-discovery ./...

test:
	pytest tests/unit tests/integration -v --cov=src
	robot tests/robot/ 2>/dev/null || true

lint:
	ruff check src/ tests/ --fix
	mypy src/ --ignore-missing-imports
	cd agents && npx tsc --noEmit 2>/dev/null || true

benchmark:
	pytest tests/benchmark/ -v --benchmark-only

docker:
	docker build -t compliance-graph:latest .

build: install install-rust install-go
	python -m build

clean:
	rm -rf dist/ build/ *.egg-info __pycache__ .pytest_cache
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
	cd native && cargo clean 2>/dev/null || true
	cd agentless && go clean 2>/dev/null || true
