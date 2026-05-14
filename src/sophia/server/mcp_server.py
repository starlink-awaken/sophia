"""Sophia MCP Server — paradigm compilation and analysis via MCP protocol."""

from __future__ import annotations

import json
import os

from fastmcp import FastMCP

_AUTH_TOKEN = os.environ.get("SOPHIA_AUTH_TOKEN", "")

mcp = FastMCP(
    "Sophia — Research Paradigm Engine",
    mask_error_details=True,
)

_learner_instance = None


def _get_learner():
    global _learner_instance
    if _learner_instance is None:
        from sophia.learner import ParadigmLearner
        _learner_instance = ParadigmLearner()
    return _learner_instance


@mcp.tool()
def compile_paradigm(query: str, use_llm: bool = False) -> str:
    """Compile a research paradigm for a given question.

    Returns the paradigm program as JSON with operations, states, and transitions.
    Use when you need to determine the best research framework for a question.

    Args:
        query: The research question to analyze
        use_llm: Whether to use LLM for compilation (default: rule-based)
    """
    from sophia.compiler import compile_paradigm_sync
    if not query.strip():
        return json.dumps({"error": "Query must not be empty"})
    program = compile_paradigm_sync(query[:1000])
    return json.dumps(program.to_dict(), ensure_ascii=False, indent=2)


@mcp.tool()
def list_operations() -> str:
    """List all available atomic research operations with descriptions.

    Use when you need to understand what operations are available for building paradigms.
    """
    ops = {
        "DECOMPOSE": "Split question into sub-questions",
        "SEARCH": "Gather sources for a claim",
        "EXTRACT": "Extract entities/claims from text",
        "COMPARE": "Compare multiple claims/sources",
        "HYPOTHESIZE": "Generate tentative answer",
        "VERIFY": "Check claim against evidence",
        "SYNTHESIZE": "Combine claims into conclusion",
        "ELIMINATE": "Remove disproven hypothesis",
        "ITERATE": "Re-run with refined parameters",
        "CONCLUDE": "Finalize answer",
    }
    return json.dumps(ops, ensure_ascii=False, indent=2)


@mcp.tool()
def list_states() -> str:
    """List all research states in the paradigm state machine."""
    from sophia.symbols import ResearchState
    states = {s.name: s.value for s in ResearchState}
    return json.dumps(states, ensure_ascii=False, indent=2)


@mcp.tool()
def get_transitions() -> str:
    """Get the base transition rules between research states.

    Returns {from_state, operation, to_state, gate_function, on_fail} for each rule.
    """
    from sophia.symbols import BASE_TRANSITIONS
    rules = []
    for t in BASE_TRANSITIONS:
        rules.append({
            "from": t.from_state.value,
            "operation": t.operation.value,
            "to": t.to_state.value,
            "gate": t.gate.__name__,
            "on_fail": t.on_fail.value,
        })
    return json.dumps(rules, ensure_ascii=False, indent=2)


@mcp.tool()
def record_trace(query: str, paradigm_name: str, operations: str, quality_score: int = 80) -> str:
    """Record a research trace for future learning.

    Args:
        query: The research question
        paradigm_name: Name of the paradigm used
        operations: Comma-separated list of operation names used
        quality_score: Quality score (0-100) of the research
    """
    from sophia.learner import ResearchTrace
    from sophia.symbols import AtomicOp

    if not query.strip():
        return json.dumps({"error": "Query must not be empty"})
    if not paradigm_name.strip():
        return json.dumps({"error": "Paradigm name must not be empty"})
    if not 0 <= quality_score <= 100:
        return json.dumps({"error": "Quality score must be 0-100"})

    ops = [o.strip() for o in operations.split(",") if o.strip()]
    valid_ops = [op for op in ops if AtomicOp.from_string(op) is not None]
    if not valid_ops:
        return json.dumps({"error": f"No valid operations. Allowed: {[o.value for o in AtomicOp]}"})

    trace = ResearchTrace(query=query[:500], paradigm_name=paradigm_name[:200],
                          operations=valid_ops, quality_score=quality_score, completed=True)
    _get_learner().record(trace)
    return json.dumps({"status": "recorded", "query": query[:100], "ops": valid_ops})


@mcp.tool()
def get_effective_ops(domain_hint: str = "") -> str:
    """Get operation effectiveness scores based on past traces.

    Args:
        domain_hint: Optional domain filter for traces (min 4 chars)
    """
    if domain_hint and len(domain_hint) < 4:
        return json.dumps({})
    scores = _get_learner().get_effective_ops(domain_hint=domain_hint)
    return json.dumps(scores, ensure_ascii=False, indent=2)


@mcp.tool()
def suggest_ops(domain_hint: str = "") -> str:
    """Suggest the most effective operations based on learning history.

    Args:
        domain_hint: Optional domain filter (min 4 chars)
    """
    if domain_hint and len(domain_hint) < 4:
        return json.dumps([])
    ops = _get_learner().suggest_ops(domain_hint=domain_hint)
    return json.dumps(ops, ensure_ascii=False, indent=2)


@mcp.tool()
def suggest_paradigm(query: str) -> str:
    """Suggest an optimized paradigm based on learning from similar past queries.

    Args:
        query: The research question to optimize for
    """
    if not query.strip():
        return json.dumps({"error": "Query must not be empty"})
    suggestion = _get_learner().suggest_paradigm(query[:1000])
    return json.dumps(suggestion, ensure_ascii=False, indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
