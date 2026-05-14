# Sophia — Architecture Document v0.2.0

---

## 一、项目概述

Sophia 是一个**符号化研究范式引擎**。代码 500+ 行 Python，零核心依赖，3 入口 (CLI/MCP/TUI)。

## 二、组件矩阵

| 组件 | 文件 | 行数 | 核心职责 |
|------|------|------|---------|
| 符号系统 | `symbols.py` | 190+ | 12 状态 · 10 操作 · 13 转移 · ParadigmProgram · validate/diff/to_mermaid |
| 编译器 | `compiler.py` | 140+ | compile_paradigm (async+sync) · recompile_from_dict · 预构建操作集 |
| 学习回路 | `learner.py` | 160+ | record · get_effective_ops · find_similar_traces · suggest_paradigm · get_patterns |
| CLI | `cli.py` | 170+ | 9 命令: compile/ops/states/transitions/evolve/export/diff/validate/learn/mcp/tui |
| MCP | `server/mcp_server.py` | 140+ | 8 FastMCP tools |
| TUI | `tui/app.py` | 100+ | Rich 交互界面 |
| 公共 API | `__init__.py` | 35 | 统一导出 |

## 三、依赖图

```
__init__.py ──→ symbols.py (零外部依赖)
            ├──→ compiler.py → symbols.py
            ├──→ learner.py (零外部依赖)
            ├──→ cli.py → compiler + learner + symbols + server + tui
            ├──→ server/mcp_server.py → compiler + learner
            └──→ tui/app.py → compiler + learner + symbols
```

## 四、ParadigmProgram 完整 API

```
ParadigmProgram
  ├── validate() → list[str]              问题列表 (空=通过)
  ├── state_count → int                    状态数 (属性)
  ├── to_dict(include_query="") → dict    JSON 序列化
  ├── from_dict(data, transitions?) → cls  反序列化
  ├── to_mermaid() → str                   Mermaid stateDiagram-v2
  └── diff(other) → dict                   {added_ops, removed_ops, common_ops}
```

## 五、学习回路 API

```
ParadigmLearner(trace_dir)
  ├── record(ResearchTrace)                写入追踪
  ├── _load_traces(limit) → list[dict]     mtime 缓存加载
  ├── get_effective_ops(domain, min) → dict  操作有效性评分
  ├── find_similar_traces(query, top_k)    关键词匹配相似追踪
  ├── suggest_ops(domain, top_k) → list    推荐操作
  ├── suggest_paradigm(query) → dict       推荐完整范式 + 置信度 + 参考案例
  └── get_patterns() → list[dict]          转移规则可靠性
```

## 六、CLI 命令矩阵

| 命令 | 输入 | 输出 |
|------|------|------|
| `compile "query"` | 自然语言问题 | 范式程序 (操作序列+状态+转移) |
| `compile "query" --json` | 同上 | JSON (含 query 用于重编译) |
| `evolve "query"` | 自然语言问题 | 默认 vs 学习推荐 + 参考案例 |
| `export p.json --format mermaid` | JSON 文件 | Mermaid 状态图 |
| `diff a.json b.json` | 2 个 JSON 文件 | 操作差异 delta |
| `validate p.json` | JSON 文件 | OK / FAIL + issues |
| `ops / states / transitions` | — | 系统清单 |
| `learn --domain "AI"` | 可选过滤 | 操作有效性评分 |
| `mcp / tui` | — | 启动服务器/界面 |

## 七、MCP Tools (8 个)

| Tool | 输入 | 输出 |
|------|------|------|
| `compile_paradigm` | query | Paradigm JSON |
| `list_operations` | — | 10 操作 + 描述 |
| `list_states` | — | 12 状态 |
| `get_transitions` | — | 13 转移规则 |
| `record_trace` | query, ops, quality | 确认 |
| `get_effective_ops` | domain_hint | 评分 dict |
| `suggest_ops` | domain_hint | 推荐列表 |
| `suggest_paradigm` | query | 推荐+置信度+参考案例 |

## 八、关键设计决策

1. **Gate functions 使用 dict** — 不定义 ResearchContext 类型，保持零依赖
2. **编译器双通道** — LLM 优先, 规则回退, 异步同步双接口
3. **序列化只保存 ops 不保存 transitions** — gate functions (Callable) 不可序列化, 通过 query 重编译恢复
4. **recompile_from_dict 在 compiler.py** — 避免 symbols.py → compiler.py 循环导入
5. **学习回路 mtime 缓存** — 避免每次查询重读磁盘
6. **相似追踪用关键词重叠** — 简单有效, 不需要 embedding
