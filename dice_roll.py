#!/usr/bin/env python3
"""
MCP Dice Server (stdio)

Tools:
- roll(expression: str, seed: int|None = None, max_dice: int = 200, max_sides: int = 10000) -> dict

Expression grammar (simple, safe):
- Terms separated by + or -
- A term is either:
  - integer modifier:  +3  -2
  - dice: NdM, dM, Nd%, d%, d100, Nd100
Examples:
  d20
  2d6+3
  1d8 + 2d6 - 2
  d% + 10
"""

from __future__ import annotations

import os
import re
import random
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union, Dict, Any

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("dice")

# ---------------- Parsing ----------------

_TOKEN_RE = re.compile(r"""
    (?P<sign>[+-]) |
    (?P<dice>(?:(?P<n>\d+)?d(?P<sides>%|\d+))) |
    (?P<int>\d+) |
    (?P<ws>\s+) |
    (?P<bad>.)
""", re.IGNORECASE | re.VERBOSE)


@dataclass
class DiceTerm:
    sign: int            # +1 or -1
    n: int               # number of dice
    sides: int           # sides (percentile => 100)
    raw: str             # original token text


@dataclass
class IntTerm:
    sign: int
    value: int
    raw: str


Term = Union[DiceTerm, IntTerm]


class ParseError(ValueError):
    pass


def _parse_expression(expr: str) -> List[Term]:
    if not isinstance(expr, str) or not expr.strip():
        raise ParseError("Expression must be a non-empty string")

    terms: List[Term] = []
    sign = +1
    saw_any = False

    pos = 0
    for m in _TOKEN_RE.finditer(expr):
        kind = m.lastgroup
        text = m.group(0)
        pos = m.end()

        if kind == "ws":
            continue

        if kind == "sign":
            sign = +1 if text == "+" else -1
            continue

        if kind == "dice":
            saw_any = True
            n_str = m.group("n")
            sides_str = m.group("sides")

            n = int(n_str) if n_str else 1
            if sides_str == "%":
                sides = 100
            else:
                sides = int(sides_str)

            terms.append(DiceTerm(sign=sign, n=n, sides=sides, raw=text))
            sign = +1
            continue

        if kind == "int":
            saw_any = True
            terms.append(IntTerm(sign=sign, value=int(text), raw=text))
            sign = +1
            continue

        if kind == "bad":
            raise ParseError(f"Unexpected character: {text!r}")

    if not saw_any:
        raise ParseError("No dice or numbers found in expression")

    # Quick sanity: expression should be fully tokenized
    if pos != len(expr):
        raise ParseError("Could not parse entire expression")

    return terms


# ---------------- Rolling ----------------

def _roll_die(rng: random.Random, sides: int) -> int:
    # sides already normalized for percentile
    return rng.randint(1, sides)


def _validate_limits(terms: List[Term], max_dice: int, max_sides: int) -> None:
    total_dice = 0
    for t in terms:
        if isinstance(t, DiceTerm):
            if t.n <= 0:
                raise ValueError("Dice count must be >= 1")
            if t.sides <= 1:
                raise ValueError("Dice sides must be >= 2")
            if t.sides > max_sides:
                raise ValueError(f"Dice sides too large (>{max_sides})")
            total_dice += t.n

    if total_dice > max_dice:
        raise ValueError(f"Too many dice (>{max_dice})")


def _format_term(t: Term) -> str:
    s = "+" if t.sign >= 0 else "-"
    if isinstance(t, DiceTerm):
        # Prefer d% formatting if sides=100 and raw used %
        if "d%" in t.raw.lower():
            core = f"{t.n}d%" if t.n != 1 else "d%"
        else:
            core = f"{t.n}d{t.sides}" if t.n != 1 else f"d{t.sides}"
        return f"{s}{core}"
    else:
        return f"{s}{t.value}"


@mcp.tool()
def roll(
    expression: str,
    seed: Optional[int] = None,
    max_dice: int = 200,
    max_sides: int = 10000,
) -> Dict[str, Any]:
    """
    Roll dice from a simple expression like: "2d6+1d8-2" or "d20" or "d%+10".
    Returns structured JSON for agents.
    """
    terms = _parse_expression(expression)
    _validate_limits(terms, max_dice=max_dice, max_sides=max_sides)

    rng = random.Random(seed) if seed is not None else random.Random()

    breakdown: List[Dict[str, Any]] = []
    total = 0

    normalized_expr = "".join(_format_term(t) for t in terms)
    # Normalize leading "+" away for readability
    if normalized_expr.startswith("+"):
        normalized_expr = normalized_expr[1:]

    for t in terms:
        if isinstance(t, DiceTerm):
            rolls = [_roll_die(rng, t.sides) for _ in range(t.n)]
            subtotal = sum(rolls) * t.sign
            total += subtotal
            breakdown.append(
                {
                    "type": "dice",
                    "term": _format_term(t).lstrip("+"),
                    "sign": t.sign,
                    "count": t.n,
                    "sides": t.sides,
                    "rolls": rolls,
                    "subtotal": subtotal,
                }
            )
        else:
            subtotal = t.value * t.sign
            total += subtotal
            breakdown.append(
                {
                    "type": "modifier",
                    "term": _format_term(t).lstrip("+"),
                    "sign": t.sign,
                    "value": t.value,
                    "subtotal": subtotal,
                }
            )

    return {
        "expression": expression,
        "normalized": normalized_expr,
        "seed": seed,
        "total": total,
        "breakdown": breakdown,
    }


def main() -> None:
    # FastMCP uses stdio by default in most setups; this starts the MCP server.
    mcp.run()


if __name__ == "__main__":
    main()