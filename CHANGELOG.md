# Changelog

## [0.2.1] — 2026-05-15

### Fixed
- Trace hash collision: sha256 + uuid4 (was 16-bit hash, collision rate ~1/65536)
- LLM prompt injection hardening: query sanitized in `<QUERY>` delimiters
- CI: pip-audit dependency vulnerability scan + mypy type checking

### Added
- SECURITY.md
- PyPI classifiers + project.urls

## [0.2.0] — 2026-05-13

### Added
- `to_mermaid()` Mermaid state diagram export
- `diff()` paradigm difference comparison
- `validate()` program validation
- `recompile_from_dict()` JSON recompilation
- `suggest_paradigm()` learning evolution suggestions
- `find_similar_traces()` similar trace queries
- `sophia evolve` CLI command
- `sophia export/diff/validate` CLI commands
- ELIMINATE transition rule completion
- PEP 561 `py.typed` marker
- Empty input protection

### Changed
- `ParadigmProgram` with full serialization support
- CLI expanded from 7 to 11 commands

## [0.1.0] — 2026-05-13

### Added
- 12 ResearchState definitions
- 10 AtomicOp definitions
- 13 BASE_TRANSITIONS canonical rule set
- Dual-channel compiler (rule-based sync + LLM-enhanced async)
- `ParadigmLearner` with learning loop
- 7 CLI commands via Rich
- 8 MCP server tools
- Interactive TUI explorer
- 27 tests
