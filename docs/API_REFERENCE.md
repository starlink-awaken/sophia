# Sophia — CLI, Python API & MCP Reference

> 面向机器（AI Agent / MCP Client / 开发者）：完整参考

---

## CLI Reference

```bash
sophia compile <query>           # 编译研究范式
  --json                         # JSON 输出

sophia ops                       # 列出 10 个原子操作
sophia states                    # 列出 12 个研究状态
sophia transitions               # 列出 13 条转移规则

sophia export <file>             # 导出范式
  --format json|mermaid          # 输出格式

sophia diff <a.json> <b.json>    # 范式差异对比
sophia validate <file.json>      # 验证程序完整性

sophia evolve <query>            # 基于历史数据建议优化
sophia learn <trace_dir>         # 从追踪目录学习

sophia mcp                       # 启动 MCP server
sophia tui                       # 交互式终端
```

---

## MCP Server

### 启动

```bash
sophia mcp                      # 启动 MCP server (stdio)
sophia-mcp                      # 直接调用
```

### 工具列表

#### 1. compile_paradigm

```
Params:  query (str, required), use_llm (bool, optional)
Returns: JSON string — ParadigmProgram as dict
```

```json
// Request
{"method":"tools/call","params":{"name":"compile_paradigm","arguments":{"query":"Compare Rust vs Go"}}}

// Response
{
  "name": "comparative_analysis",
  "operations": ["DECOMPOSE", "SEARCH", "EXTRACT", "COMPARE", "SYNTHESIZE", "CONCLUDE"],
  "states": ["QUESTION", "DECOMPOSED", "SEARCHING", "EVIDENCE", "SYNTHESIS", "CONCLUSION"],
  "transitions": [
    {"from": "QUESTION", "operation": "DECOMPOSE", "to": "DECOMPOSED"},
    {"from": "DECOMPOSED", "operation": "SEARCH", "to": "SEARCHING"},
    {"from": "SEARCHING", "operation": "EXTRACT", "to": "EVIDENCE"},
    {"from": "EVIDENCE", "operation": "COMPARE", "to": "SYNTHESIS"},
    {"from": "SYNTHESIS", "operation": "CONCLUDE", "to": "CONCLUSION"}
  ]
}
```

---

#### 2. list_operations

```
Params:  none
Returns: JSON object — {OP_NAME: description, ...}
```

```json
{
  "DECOMPOSE": "Split question into sub-questions",
  "SEARCH": "Gather sources for a claim",
  "EXTRACT": "Extract entities/claims from text",
  "COMPARE": "Compare multiple claims/sources",
  "HYPOTHESIZE": "Generate tentative answer",
  "VERIFY": "Check claim against evidence",
  "SYNTHESIZE": "Combine claims into conclusion",
  "ELIMINATE": "Remove disproven hypothesis",
  "ITERATE": "Re-run with refined parameters",
  "CONCLUDE": "Finalize answer"
}
```

---

#### 3. list_states

```
Params:  none
Returns: JSON object — {STATE_NAME: description, ...}
```

---

#### 4. get_transitions

```
Params:  none
Returns: JSON array — [{from, operation, to, gate, on_fail}, ...]
```

---

#### 5. record_trace

记录一次研究追踪，用于学习优化。

```
Params:
  query          (str, required)  — 研究问题 (max 500 chars)
  paradigm_name  (str, required)  — 范式名称 (max 200 chars)
  operations     (str, required)  — 逗号分隔的操作名
  quality_score  (int, optional)  — 质量评分 0-100 (default: 80)

Validation:
  - query must be non-empty
  - paradigm_name must be non-empty
  - quality_score must be 0-100
  - operations are validated against AtomicOp enum (invalid ops are dropped)
```

```json
// Request
{"method":"tools/call","params":{"name":"record_trace","arguments":{
  "query": "Compare Rust vs Go for backend",
  "paradigm_name": "comparative_analysis",
  "operations": "DECOMPOSE,SEARCH,EXTRACT,COMPARE,SYNTHESIZE,CONCLUDE",
  "quality_score": 85
}}}

// Response
{"status": "recorded", "query": "Compare Rust vs Go for backend", "ops": ["DECOMPOSE", "SEARCH", "EXTRACT", "COMPARE", "SYNTHESIZE", "CONCLUDE"]}
```

---

#### 6. get_effective_ops

```
Params:  domain_hint (str, optional)  — 领域过滤 (min 4 chars for privacy)
Returns: JSON object — {op_name: effectiveness_score, ...}
```

---

#### 7. suggest_ops

```
Params:  domain_hint (str, optional)  — 领域过滤 (min 4 chars)
Returns: JSON array — [op_name, ...]  ranked by effectiveness
```

---

#### 8. suggest_paradigm

```
Params:  query (str, required)  — max 1000 chars
Returns: JSON object — {recommended_ops, confidence, sample_count, top_traces}
```

```json
{
  "recommended_ops": ["DECOMPOSE", "SEARCH", "VERIFY", "SYNTHESIZE", "CONCLUDE"],
  "confidence": 0.82,
  "sample_count": 5
}
```

---

### 错误响应

```json
{"error": "Query must not be empty"}
{"error": "Quality score must be 0-100"}
{"error": "No valid operations. Allowed: [...]"}
```

---

## Python API

### 编译范式

```python
from sophia import compile_paradigm_sync, compile_paradigm

# 同步编译（纯规则，零依赖）
prog = compile_paradigm_sync("Compare Rust vs Go for backend")
print(prog.name)         # "comparative_analysis"
print(prog.operations)   # [DECOMPOSE, SEARCH, EXTRACT, COMPARE, SYNTHESIZE, CONCLUDE]
print(prog.state_count)  # 6

# 异步编译（可选 LLM 增强）
prog = await compile_paradigm(llm_client, "Compare Rust vs Go")
```

### 序列化

```python
# JSON 往返
data = prog.to_dict(include_query="Compare Rust vs Go")
json_str = json.dumps(data)

from sophia.compiler import recompile_from_dict
prog2 = recompile_from_dict(json.loads(json_str))

# Mermaid 状态图
mermaid = prog.to_mermaid()

# 程序差异对比
delta = prog.diff(other_prog)
print(delta)  # {"shared_ops": [...], "a_only": [...], "b_only": [...]}
```

### 验证

```python
issues = prog.validate()
if issues:
    for issue in issues:
        print(f"⚠ {issue}")
else:
    print("✅ Program is valid")
```

### 学习回路

```python
from sophia.learner import ParadigmLearner, ResearchTrace

learner = ParadigmLearner(trace_dir="~/my_traces")

# 记录一次研究
trace = ResearchTrace(
    query="Compare Flutter vs React Native",
    paradigm_name="comparative_analysis",
    operations=["DECOMPOSE", "SEARCH", "COMPARE", "SYNTHESIZE", "CONCLUDE"],
    quality_score=88,
    completed=True,
)
learner.record(trace)

# 获取操作有效性评分
scores = learner.get_effective_ops(domain_hint="mobile")
# → {"COMPARE": 88.0, "DECOMPOSE": 85.0, "SEARCH": 82.0, ...}

# 推荐最优操作
ops = learner.suggest_ops(domain_hint="mobile")
# → ["COMPARE", "DECOMPOSE", "SEARCH", "SYNTHESIZE", "CONCLUDE"]

# 范式建议
suggestion = learner.suggest_paradigm("Compare Swift vs Kotlin")
# → {recommended_ops: [...], confidence: 0.88, sample_count: 3, top_traces: [...]}

# 查找相似追踪
similar = learner.find_similar_traces("Compare Swift vs Kotlin", top_k=3)
```

### 自定义范式程序

```python
from sophia.symbols import ParadigmProgram, ResearchState, AtomicOp, TransitionRule

custom = ParadigmProgram(
    name="custom_analysis",
    operations=[AtomicOp.SEARCH, AtomicOp.VERIFY, AtomicOp.CONCLUDE],
    states=[ResearchState.QUESTION, ResearchState.SEARCHING, ResearchState.VERIFIED, ResearchState.CONCLUSION],
    transitions=[
        TransitionRule(ResearchState.QUESTION, AtomicOp.SEARCH, ResearchState.SEARCHING),
        TransitionRule(ResearchState.SEARCHING, AtomicOp.VERIFY, ResearchState.VERIFIED),
        TransitionRule(ResearchState.VERIFIED, AtomicOp.CONCLUDE, ResearchState.CONCLUSION),
    ],
)
custom.validate()  # → []
```
