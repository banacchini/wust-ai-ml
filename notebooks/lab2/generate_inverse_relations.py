#!/usr/bin/env python3
"""Generate inverse relations for exact-candidate formulas.

Supports operations:
- mul: target = a * b            -> a = target / b, b = target / a
- reciprocal: target = 1 / a      -> a = 1 / target
- const_div: target = c / a       -> a = c / target
- one_minus: target = 1 - a       -> a = 1 - target

Usage:
  python generate_inverse_relations.py \
    --input notebooks/lab2/exact_candidate_relations.json \
    --output notebooks/lab2/exact_candidate_relations.json
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any


def _is_nonzero_guard(guard: dict[str, Any], attr: str) -> bool:
    return guard.get("type") == "nonzero" and guard.get("attr") == attr


def _make_nonzero_guard(attr: str, eps: float = 1e-12) -> dict[str, Any]:
    return {"type": "nonzero", "attr": attr, "eps": eps}


def _relation_key(rel: dict[str, Any]) -> tuple[Any, ...]:
    return (
        rel.get("target_attr"),
        rel.get("operation"),
        tuple(rel.get("inputs", [])),
        rel.get("const"),
    )


def _auto_id(target: str, op: str, inputs: list[str], const: float | None = None) -> str:
    parts = ["AUTO", target, "from"] + inputs + [op]
    if const is not None:
        parts.append(str(const).replace(".", "_"))
    return "_".join(parts)


def _inverse_relations(rel: dict[str, Any]) -> list[dict[str, Any]]:
    op = rel.get("operation")
    target = rel.get("target_attr")
    inputs = rel.get("inputs", [])
    guards = rel.get("guards", [])
    priority = int(rel.get("priority", 1))

    inverses: list[dict[str, Any]] = []

    if op == "mul" and len(inputs) == 2:
        a, b = inputs
        inv_a = {
            "id": _auto_id(a, "div", [target, b]),
            "target_attr": a,
            "operation": "div",
            "inputs": [target, b],
            "priority": priority + 1,
            "guards": [_make_nonzero_guard(b)],
            "notes": f"Auto inverse of {rel.get('id')}: {a} = {target} / {b}",
            "auto_generated": True,
            "generated_from": rel.get("id"),
        }
        inv_b = {
            "id": _auto_id(b, "div", [target, a]),
            "target_attr": b,
            "operation": "div",
            "inputs": [target, a],
            "priority": priority + 1,
            "guards": [_make_nonzero_guard(a)],
            "notes": f"Auto inverse of {rel.get('id')}: {b} = {target} / {a}",
            "auto_generated": True,
            "generated_from": rel.get("id"),
        }
        inverses.extend([inv_a, inv_b])

    elif op == "reciprocal" and len(inputs) == 1:
        x = inputs[0]
        inv = {
            "id": _auto_id(x, "reciprocal", [target]),
            "target_attr": x,
            "operation": "reciprocal",
            "inputs": [target],
            "priority": priority + 1,
            "guards": [_make_nonzero_guard(target)],
            "notes": f"Auto inverse of {rel.get('id')}: {x} = 1 / {target}",
            "auto_generated": True,
            "generated_from": rel.get("id"),
        }
        inverses.append(inv)

    elif op == "const_div" and len(inputs) == 1:
        x = inputs[0]
        const = float(rel.get("const"))
        inv = {
            "id": _auto_id(x, "const_div", [target], const=const),
            "target_attr": x,
            "operation": "const_div",
            "const": const,
            "inputs": [target],
            "priority": priority + 1,
            "guards": [_make_nonzero_guard(target)],
            "notes": f"Auto inverse of {rel.get('id')}: {x} = {const} / {target}",
            "auto_generated": True,
            "generated_from": rel.get("id"),
        }
        inverses.append(inv)

    elif op == "one_minus" and len(inputs) == 1:
        x = inputs[0]
        inv = {
            "id": _auto_id(x, "one_minus", [target]),
            "target_attr": x,
            "operation": "one_minus",
            "inputs": [target],
            "priority": priority + 1,
            "guards": copy.deepcopy(guards),
            "notes": f"Auto inverse of {rel.get('id')}: {x} = 1 - {target}",
            "auto_generated": True,
            "generated_from": rel.get("id"),
        }
        inverses.append(inv)

    return inverses


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate inverse candidate relations")
    parser.add_argument("--input", required=True, help="Path to source relations JSON")
    parser.add_argument("--output", required=True, help="Path to output relations JSON")
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)

    with in_path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    relations = payload.get("relations", [])
    existing_keys = {_relation_key(r) for r in relations}

    to_add: list[dict[str, Any]] = []
    for rel in relations:
        for inv in _inverse_relations(rel):
            key = _relation_key(inv)
            if key not in existing_keys:
                existing_keys.add(key)
                to_add.append(inv)

    payload.setdefault("metadata", {})
    payload["metadata"]["inverse_generation"] = {
        "added_relations": len(to_add),
        "input_relations": len(relations),
        "output_relations": len(relations) + len(to_add),
        "supported_ops": ["mul", "reciprocal", "const_div", "one_minus"],
        "generated_div_inverse": True,
    }

    payload["relations"] = relations + to_add

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"Input relations: {len(relations)}")
    print(f"Added inverse relations: {len(to_add)}")
    print(f"Output relations: {len(payload['relations'])}")
    print(f"Saved to: {out_path}")


if __name__ == "__main__":
    main()
