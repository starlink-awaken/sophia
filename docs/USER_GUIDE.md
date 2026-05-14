# Sophia — 用户使用指南

> 面向人类用户：理解范式引擎、使用场景、实践案例

---

## 目录

1. [核心概念](#核心概念)
2. [快速上手](#快速上手)
3. [场景一：为研究问题选择最佳方法](#场景一为研究问题选择最佳方法)
4. [场景二：可视化研究过程](#场景二可视化研究过程)
5. [场景三：对比不同研究方案](#场景三对比不同研究方案)
6. [场景四：从历史研究中学习优化](#场景四从历史研究中学习优化)
7. [交互式终端探索](#交互式终端探索)

---

## 核心概念

Sophia 把研究过程看作**状态机**：

```
研究问题 → 分解 → 假设 → 搜索 → 证据 → 验证 → 结论
                          ↑                    ↓
                      迭代循环 ← 缺口 ← 矛盾发现
```

**12 个研究状态**：QUESTION → DECOMPOSED → HYPOTHESIS → SEARCHING → EVIDENCE → VERIFIED → CONTRADICTION → SYNTHESIS → CLAIM → CONCLUSION → GAP → ITERATE

**10 个原子操作**：SEARCH（搜索）、DECOMPOSE（分解）、VERIFY（验证）、SYNTHESIZE（综合）、HYPOTHESIZE（假设）、EXTRACT（提取）、COMPARE（比较）、ELIMINATE（消除）、ITERATE（迭代）、CONCLUDE（总结）

---

## 快速上手

```bash
pip install sophia

# 看看 Sophia 如何理解你的研究问题
sophia compile "对比 Rust 和 Go 在后端开发中的优劣"
```

输出：
```
Paradigm: comparative_analysis
Operations: DECOMPOSE → SEARCH → EXTRACT → COMPARE → SYNTHESIZE → CONCLUDE
States: 6
Transitions: 5
```

---

## 场景一：为研究问题选择最佳方法

**你是研究者，想确保自己用了正确的分析方法。**

```bash
# 编译范式 — Sophia 分析问题并推荐操作序列
sophia compile "评估微服务架构 vs 单体架构在创业公司的适用性"

# 导出 JSON — 给程序或 Agent 使用
sophia compile "评估微服务架构" --json > my_paradigm.json

# 查看推荐的操作
cat my_paradigm.json | python3 -c "import json,sys;d=json.load(sys.stdin);print('\n'.join(d['operations']))"
```

**输出解读：**
- `paradigm: comparative_analysis` — Sophia 认为这是对比分析
- `operations: [DECOMPOSE, SEARCH, COMPARE, SYNTHESIZE, CONCLUDE]` — 推荐 5 步操作
- Sophia 不建议 HYPOTHESIZE（不适合对比场景），不会做无意义的假设

---

## 场景二：可视化研究过程

**你需要在论文或演示中展示研究方法。**

```bash
# 导出 Mermaid 状态图
sophia export my_paradigm.json --format mermaid

# 会生成类似这样的图：
# stateDiagram-v2
#   [*] --> QUESTION
#   QUESTION --> DECOMPOSED : DECOMPOSE
#   DECOMPOSED --> SEARCHING : SEARCH
#   SEARCHING --> EVIDENCE : success
#   EVIDENCE --> VERIFIED : VERIFY
#   ...
```

将 Mermaid 代码粘贴到 Markdown 文件中（GitHub、Notion、Obsidian 均原生支持），即可看到状态转换图。

---

## 场景三：对比不同研究方案

**你有两个研究计划，想知道区别在哪。**

```bash
# 分别编译
sophia compile "AI 安全对齐技术综述" --json > plan_a.json
sophia compile "RLHF vs Constitutional AI 对比" --json > plan_b.json

# 对比差异
sophia diff plan_a.json plan_b.json
```

输出：
```
Operations: literature_review → comparative_analysis
+ COMPARE
- EXTRACT (replaced by COMPARE)
States: 5 → 6 (+1)
```

---

## 场景四：从历史研究中学习优化

**你已经做了很多研究，想从经验中找出最佳实践。**

```bash
# 记录一次研究的追踪
sophia learn ~/my_traces/    # 学习目录中的历史追踪

# 获取演化建议
sophia evolve "AI 安全对齐技术综述"
```

输出：
```json
{
  "recommended_ops": ["DECOMPOSE", "SEARCH", "EXTRACT", "VERIFY", "SYNTHESIZE", "CONCLUDE"],
  "confidence": 0.85,
  "sample_count": 12,
  "based_on": "12 similar traces (average quality: 82/100)"
}
```

**解读：** 基于 12 次类似研究的历史数据（平均质量 82 分），Sophia 建议比默认方案多一步 VERIFY。这说明在该领域，验证步骤能显著提升研究质量。

---

## 交互式终端探索

```bash
sophia tui
```

进入交互界面，可以：
- 浏览所有 12 个研究状态
- 查看 10 个原子操作的说明
- 探索 13 条转移规则
- 实时编译范式并查看结果

键盘操作：
- `↑↓` 导航
- `Enter` 选择
- `q` 返回
- `Ctrl+C` 退出

---

## 常见问题

**Q: Sophia 和 Minerva 是什么关系？**
A: Sophia 是方法论引擎，Minerva 是研究执行引擎。Minerva 内置调用 `sophia.compile_paradigm_sync()` 来分析每个研究问题。

**Q: Sophia 需要 LLM 吗？**
A: 核心编译器是**纯规则驱动**的，无需 LLM，零依赖。异步编译路径可选配 LLM 增强。

**Q: 如何自定义转移规则？**
A: 通过 Python API 构建自定义 ParadigmProgram，或修改 BASE_TRANSITIONS 后重新编译。

**Q: 追踪数据存在哪？**
A: 默认 `~/sophia/traces/`。每个追踪独立 JSON 文件，可直接查看和编辑。
