.PHONY: setup snapshot test lint app evals check
setup:
	uv sync
snapshot:
	uv run triage snapshot
test:
	uv run pytest -q
lint:
	uv run ruff check . && uv run ruff format --check .
app:
	uv run streamlit run app/streamlit_app.py
evals:
	uv run python -m evals.run_evals
check: lint test evals
