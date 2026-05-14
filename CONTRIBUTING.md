# Contributing to Sophia

Sophia is the symbolic research paradigm engine powering Minerva's research methodology. Contributions are welcome.

## How to Contribute

### Reporting Bugs
Open an issue with: Sophia version, Python version, steps to reproduce, expected vs actual output.

### Pull Requests
1. Fork and create a feature branch from `main`.
2. Install dev deps: `pip install -e ".[dev]"`.
3. Run linting: `ruff check src/sophia/ --select F`.
4. Run tests: `pytest tests/ -q`.
5. Install pre-commit hooks: `pre-commit install`.
6. Use conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`).
7. Push and open a PR against `main`.

## Development Setup

```bash
git clone https://github.com/minerva/sophia.git
cd sophia
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
```

## Architecture

- `symbols.py` — 12 states, 10 atomic ops, 13 transition rules, ParadigmProgram
- `compiler.py` — dual-channel compiler (rule-based + LLM-enhanced)
- `learner.py` — learning loop with trace recording and paradigm suggestions
- `cli.py` — 11 CLI commands
- `server/mcp_server.py` — 8 MCP tools
- `tui/app.py` — Rich interactive terminal explorer

## Testing

```bash
pytest tests/ -q
pytest tests/ --cov=src/sophia --cov-report=term-missing
```

## License

MIT. By contributing, you agree that your contributions will be licensed under MIT.
