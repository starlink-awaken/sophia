# Sophia — Design Document v0.2.0

---

## 设计哲学

### 图灵机类比

| 图灵机概念 | Sophia v0.2.0 对应 |
|-----------|-------------------|
| 状态集合 Q | `ResearchState` (12) |
| 字母表 Σ | `AtomicOp` (10), 新增 `from_string(s)` |
| 转移函数 δ | `TransitionRule` (13, 新增 ELIMINATE) |
| 纸带 | research context dict |
| 停机条件 | `terminal_states = [CONCLUSION]` 或 `max_iterations` |
| 程序 | `ParadigmProgram` (可序列化、可验证、可导出) |
| 编译器 | `compile_paradigm` / `compile_paradigm_sync` / `recompile_from_dict` |
| 学习器 | `ParadigmLearner` (新增 suggest_paradigm, find_similar_traces) |

### 新增设计原则

4. **可导出性**：`to_mermaid()` 将范式程序转为标准状态图，可直接嵌入文档。
5. **可对比性**：`diff()` 返回两个范式程序的操作差异，支持 A/B 测试。
6. **可进化性**：`suggest_paradigm(query)` 从相似历史追踪中学习最优操作序列。

## 状态转移图 (更新)

```
                    ┌─────────┐
                    │ QUESTION │
                    └────┬────┘ DECOMPOSE
                    ┌────▼────────┐
                    │ DECOMPOSED  │
                    └────┬────────┘ HYPOTHESIZE
                    ┌────▼────────┐
                    │ HYPOTHESIS  │
                    └────┬────────┘ SEARCH
                    ┌────▼────────┐
                    │  SEARCHING  │◄──────────────┐
                    └────┬────────┘               │ EXTRACT  │
                    ┌────▼────────┐               │
                    │  EVIDENCE   │               │
                    └────┬────────┘               │ VERIFY   │
                    ┌────▼────────┐               │
                    │  VERIFIED   │               │
                    └──┬───┬───┬──┘               │
          COMPARE ┌───┘   │   └─── ELIMINATE (new)│
          ┌───────▼──┐   │       ┌──────────┐    │
          │   CLAIM  │◄──┘       │          │    │
          └──┬───┬───┘           │          │    │
    VERIFY ┌─┘   └─┐ SYNTHESIZE  │          │    │
  ┌───────▼──┐ ┌───▼──────────┐  │          │    │
  │CONTRADICT│ │  SYNTHESIS   │  │          │    │
  └──┬───┬───┘ └───┬─────┬────┘  │          │    │
     │   │         │     │ CONCLUDE│        │    │
     │   │    ┌────┘     │        │          │    │
     │   │    │    ┌─────▼──┐ ┌──▼────────┐ │    │
     │   │    │    │  GAP   │ │CONCLUSION │ │    │
     │   │    │    └───┬────┘ └───────────┘ │    │
     │   │    │        │ ITERATE            │    │
     └───┴────┴────────┴────────────────────┘    │
                                                  │
                   ←←← 迭代循环 ←←←────────────────┘
```

## 学习回路设计

```
                   ┌──────────────────┐
                   │  record(trace)   │ ← 每次研究执行后调用
                   └────────┬─────────┘
                            │ 写入 JSON 文件
                   ┌────────▼─────────┐
                   │  _load_traces()  │ ← mtime 缓存, 最多 500 条
                   └────────┬─────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
     ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
     │effective_ops│ │get_patterns │ │find_similar │
     │ 有效性评分   │ │ 模式可靠性   │ │ 相似追踪     │
     └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
            │               │               │
            └───────────────┼───────────────┘
                            │
                   ┌────────▼─────────┐
                   │suggest_paradigm  │ ← 聚合: 推荐+置信度+参考案例
                   └──────────────────┘
```

## 序列化设计

```
ParadigmProgram
  │
  ├── to_dict(include_query="...")
  │     → {"name","description","ops":[...],"state_count","transition_count","query"}
  │
  ├── from_dict(data, transitions?)
  │     → 从 ops 列表重建 (无转移规则, 需额外传入)
  │
  ├── recompile_from_dict(data)       ← 在 compiler.py 中 (避免循环导入)
  │     → 有 query 则重新编译 (完整恢复转移规则)
  │     → 无 query 则回退 from_dict
  │
  └── to_mermaid()
        → stateDiagram-v2 格式
```
