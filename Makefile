.PHONY: setup snapshot test lint app evals check note
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
note:  # design note PDF (needs pandoc and Google Chrome)
	uv run python scripts/make_diagram.py
	pandoc docs/DESIGN_NOTE.md -s --embed-resources --resource-path=docs --css docs/note.css -o docs/DESIGN_NOTE.html
	"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=docs/DESIGN_NOTE.pdf docs/DESIGN_NOTE.html
	rm docs/DESIGN_NOTE.html
