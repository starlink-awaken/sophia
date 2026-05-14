# Changelog

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
