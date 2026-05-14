# Sophia — Symbolic Research Paradigm Engine

> 将研究过程形式化为可编程、可编译、可学习、可进化的符号系统
>
> *Sophia: Greek goddess of wisdom. The engine that gives Minerva her strategic intelligence.*

[English](#english) | [中文](#chinese)

---

## English

### Overview

Sophia is a **symbolic research paradigm engine**. It doesn't provide fixed research templates — it provides a **formal language** for describing, compiling, evolving, and learning research processes.

**Core insight:** Research paradigm = state machine program. 12 states × 10 atomic operations × 13 transition rules → compiler → executable paradigm program → learning loop → evolution suggestions.

### Quick Start

```bash
pip install sophia

# CLI
sophia compile "Compare Rust vs Go for backend"     # compile paradigm
sophia compile "Compare Rust vs Go" --json           # JSON output
sophia evolve "Compare Flutter vs React Native"     # learning evolution suggestions
sophia export program.json --format mermaid          # export state diagram
sophia diff a.json b.json                            # paradigm diff
sophia validate program.json                         # validate integrity

# TUI
sophia tui                 # interactive terminal explorer

# MCP
sophia mcp                 # 8 MCP tools for Agent integration
```

### Python API

```python
from sophia import *

# Compile
prog = compile_paradigm_sync("Compare Rust vs Go")    # sync, zero deps
prog = await compile_paradigm(llm_client, "query")     # async, LLM-enhanced

# Serialize & visualize
json_str = json.dumps(prog.to_dict(include_query="..."))
mermaid = prog.to_mermaid()                            # Mermaid state diagram
delta = prog.diff(other_prog)                          # paradigm difference

# Validate
prog.validate()  # → [] (no issues) or specific error list

# Learning loop
learner = ParadigmLearner(trace_dir="~/my_traces")
learner.record(ResearchTrace(query="...", operations=["SEARCH","VERIFY"], quality_score=85))
suggestion = learner.suggest_paradigm("Compare Flutter vs React Native")
# → {recommended_ops, confidence, sample_count, top_traces}
```

### Architecture

```
Problem Analysis → Compiler → ParadigmProgram → to_mermaid() / to_dict() / diff()
                         ↑                    ↓
                    ┌────┘              record(trace)
                    │                       ↓
              Learning Loop ←── Evolution ←── suggest_paradigm()
```

### Components

| Module | Lines | Responsibility |
|--------|-------|---------------|
| `symbols.py` | 190+ | 12 states · 10 operations · 13 transitions · ParadigmProgram + validate/diff/to_mermaid |
| `compiler.py` | 140+ | Dual-channel compiler + recompile_from_dict |
| `learner.py` | 160+ | Learning loop: record/effectiveness scoring/similar traces/suggest_paradigm |
| `cli.py` | 160+ | 11 commands: compile/ops/states/transitions/evolve/export/diff/validate/learn/mcp/tui |
| `server/mcp_server.py` | 130+ | 8 MCP tools |
| `tui/app.py` | 100+ | Rich interactive explorer |

### State Transition Diagram

```
QUESTION → DECOMPOSED → HYPOTHESIS → SEARCHING → EVIDENCE → VERIFIED → CLAIM
                                                                     ↓
                                              CONTRADICTION ← VERIFY ┤
                                                   ↓                  ↓ SYNTHESIZE
                                              SYNTHESIZE          SYNTHESIS
                                                   ↓                  ↓
                                                   └──────────────────┼──→ CONCLUSION
                                                                      │
                                              GAP ←───────────────────┘
                                               │ ITERATE
                                               └──→ SEARCHING (loop)
```

### Research States (12)

`QUESTION`, `DECOMPOSED`, `HYPOTHESIS`, `SEARCHING`, `EVIDENCE`, `VERIFIED`, `CONTRADICTION`, `SYNTHESIS`, `CLAIM`, `CONCLUSION`, `GAP`, `ITERATE`

### Atomic Operations (10)

`SEARCH`, `DECOMPOSE`, `VERIFY`, `SYNTHESIZE`, `HYPOTHESIZE`, `EXTRACT`, `COMPARE`, `ELIMINATE`, `ITERATE`, `CONCLUDE`

### CLI Commands

```bash
sophia compile <query>        # compile paradigm from query
sophia ops                    # list all atomic operations
sophia states                 # list all research states
sophia transitions            # list all transition rules
sophia evolve <query>         # suggest paradigm evolution
sophia export <file>          # export as JSON/Mermaid
sophia diff <a> <b>           # diff two paradigm programs
sophia validate <file>        # validate program integrity
sophia learn <trace-dir>      # run learning loop
sophia mcp                    # start MCP server
sophia tui                    # interactive TUI
```

### MCP Tools (8)

| Tool | Function |
|------|----------|
| `compile_paradigm` | Compile a research paradigm from a query |
| `list_states` | List all 12 research states |
| `list_operations` | List all 10 atomic operations |
| `list_transitions` | List all 13 transition rules |
| `validate_program` | Validate a paradigm program |
| `export_mermaid` | Export program as Mermaid diagram |
| `suggest_evolution` | Suggest paradigm evolution |
| `get_trace_stats` | Get learning trace statistics |

### Installation

```bash
pip install sophia
# or from source:
pip install -e .
```

### Documentation

- [Design Doc](docs/DESIGN.md) — design philosophy, Turing machine analogy, state transition diagram
- [Architecture](docs/ARCHITECTURE.md) — component decomposition, dependency graph, integration patterns
- [Product ISA](docs/ISA.md) — ideal state, features, decision log

### Version

**v0.2.0** — 2026-05-13

### Related Projects

- [Minerva](https://github.com/minerva/minerva) — local-first deep research system powered by Sophia
- [Agora](https://github.com/minerva/agora) — MCP service convergence hub

### License

MIT

---

## 中文

### 概述

Sophia 是一个**符号化研究范式引擎**。它不提供固定的研究模板，而是提供一套**形式语言**来描述、编译、演化和学习研究过程。

**核心理念**：研究范式 = 状态机程序。12 个状态 × 10 个原子操作 × 13 条转移规则 → 编译器 → 可执行范式程序 → 学习回路 → 进化建议。

### 快速开始

```bash
pip install sophia

# CLI
sophia compile "比较 Rust 和 Go 做后端开发"     # 编译范式
sophia compile "比较 Rust 和 Go" --json           # JSON 输出
sophia evolve "比较 Flutter 和 React Native"     # 学习进化建议
sophia export program.json --format mermaid        # 导出状态图
sophia diff a.json b.json                          # 范式差异对比
sophia validate program.json                       # 验证完整性

# TUI
sophia tui                 # 交互式终端探索

# MCP
sophia mcp                 # 8 个 MCP Tools 供 Agent 调用
```

### 研究状态（12）

`QUESTION`（问题）、`DECOMPOSED`（已分解）、`HYPOTHESIS`（假设）、`SEARCHING`（搜索中）、`EVIDENCE`（证据）、`VERIFIED`（已验证）、`CONTRADICTION`（矛盾）、`SYNTHESIS`（综合）、`CLAIM`（主张）、`CONCLUSION`（结论）、`GAP`（缺口）、`ITERATE`（迭代）

### 原子操作（10）

`SEARCH`（搜索）、`DECOMPOSE`（分解）、`VERIFY`（验证）、`SYNTHESIZE`（综合）、`HYPOTHESIZE`（假设）、`EXTRACT`（提取）、`COMPARE`（比较）、`ELIMINATE`（消除）、`ITERATE`（迭代）、`CONCLUDE`（总结）

### 组件

| 模块 | 行数 | 职责 |
|------|------|------|
| `symbols.py` | 190+ | 12 状态 · 10 操作 · 13 转移 · ParadigmProgram + validate/diff/to_mermaid |
| `compiler.py` | 140+ | 双通道编译器 + recompile_from_dict |
| `learner.py` | 160+ | 学习回路: record/有效性评分/相似追踪/suggest_paradigm |
| `cli.py` | 160+ | 11 命令: compile/ops/states/transitions/evolve/export/diff/validate/learn/mcp/tui |
| `server/mcp_server.py` | 130+ | 8 MCP tools |
| `tui/app.py` | 100+ | Rich 交互界面 |

### 许可证

MIT
