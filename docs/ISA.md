# Sophia — Product ISA v0.2.0

> Ideal State Artifact · E3 tier · 2026-05-13 · **STATUS: DELIVERED**

---

## Problem

Sophia v0.1.0 定义了符号系统但不具备完整产品能力：缺序列化往返、无可视化、无差异对比、无验证、无学习进化。作为独立产品，这些是基本需求。

## Vision

`sophia compile` → 编译范式 → `sophia export` → 状态图 → `sophia evolve` → 学习建议 → 迭代优化。CLI + MCP + TUI 三入口，Agent 和开发者都能用。

## Goal

Sophia v0.2.0 是**可编译、可导出、可验证、可对比、可进化的范式引擎**。

## Criteria

- [x] ISC-1: tests pass
- [x] ISC-2: `sophia compile --json` → 含 query 的可重编译 JSON
- [x] ISC-3: `to_mermaid()` → Mermaid stateDiagram-v2
- [x] ISC-4: `diff()` + `sophia diff a.json b.json` → 操作 delta
- [x] ISC-5: `sophia export --format mermaid` → 标准 Mermaid
- [x] ISC-6: `sophia mcp` → 8 tools
- [x] ISC-7: `sophia validate` → OK/FAIL + issues
- [x] ISC-8: Learner traces 持久化
- [x] ISC-9: `py.typed` marker
- [x] ISC-10: empty query → ValueError

## Features

| name | status |
|------|--------|
| mermaid-export | ✅ to_mermaid() + sophia export |
| diff-command | ✅ diff() + sophia diff |
| validate-command | ✅ validate() + sophia validate |
| evolve-command | ✅ suggest_paradigm() + sophia evolve |
| recompile-from-dict | ✅ query round-trip via recompile_from_dict() |
| similar-traces | ✅ find_similar_traces() |
| mcp-tools | ✅ 8 tools (compile/list/states/transitions/record/effective/suggest/paradigm) |
| pep561 | ✅ py.typed |
| empty-guard | ✅ ValueError |
| eliminate-transition | ✅ CLAIM→ELIMINATE→VERIFIED |

## Decisions

- 2026-05-13: `to_dict()` 增加 `include_query` 参数，解决 JSON 反序列化时转移规则丢失问题
- 2026-05-13: `recompile_from_dict()` 放在 compiler.py 而非 symbols.py，避免循环导入
- 2026-05-13: `suggest_paradigm()` 使用关键词重叠匹配相似追踪，domain_hint 做额外过滤
- 2026-05-13: ELIMINATE 转移: CLAIM→ELIMINATE→VERIFIED (gate: has_contradictions, fail: CONTRADICTION)

## Changelog

- **conjectured**: 5 固定范式定义 (types.py) 是必要的
- **refuted by**: 动态编译 (compiler.py) 产生同等效果且更灵活
- **learned**: 范式应该从原子操作编译而来，而非从模板实例化
- **criterion now**: ISC-3 (Mermaid), ISC-4 (Diff), ISC-7 (Validate) 均基于编译而非模板
