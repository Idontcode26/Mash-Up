#!/usr/bin/env python3
"""Preflight for the Survivor Squad design sheets.

Lays every sheet over every other and lists:
  1. unfilled cells    null, missing or empty ("n/a" counts as filled)
  2. unverified cells  "fact" columns that hold a value the row's "verified" list does not name yet
  3. problems          references that point at nothing, unknown columns, duplicate keys, coverage gaps

Exit code 0 only when all three are empty. Run it before every build; build only when it is clean.

    python preflight.py          plain text
    python preflight.py --md     Markdown (this is how PREFLIGHT.md was made)

Column kinds (set per column in each sheet):
  design  our own decision; must be filled
  ref     points at a row in another sheet ("to": sheet name, or "*" for a "sheet.row" value); must resolve
  fact    something true about L4D2, RoR2 or Melty; must be filled AND checked. "check" says how:
            l4d2-files   look in the installed L4D2 files
            ror2-code    look in RoR2's own code or test in the running game
            melty-tools  ask Melty (game_info, validate_recipe, one_click_check, ...)
          After checking a fact, add its column name to that row's "verified" list.
"""
import glob
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
SLOTS = ["primary", "secondary", "utility", "special"]


def load():
    sheets = {}
    for path in sorted(glob.glob(os.path.join(HERE, "sheets", "*.json"))):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        sheets[data["sheet"]] = data
    return sheets


def empty(v):
    return v is None or v == "" or v == []


def as_list(v):
    return v if isinstance(v, list) else [v]


def split_ref(spec, ref):
    if spec["to"] == "*":
        target, _, key = ref.partition(".")
        return target, key
    return spec["to"], ref


def check(sheets):
    keys = {n: {r[s["key"]] for r in s["rows"]} for n, s in sheets.items()}
    unfilled = defaultdict(lambda: defaultdict(list))
    unverified = defaultdict(lambda: defaultdict(list))
    problems = []
    used = defaultdict(int)

    for name, s in sheets.items():
        cols = s["columns"]
        seen = set()
        for row in s["rows"]:
            rid = row.get(s["key"])
            where = f"{name}.{rid}"
            if rid in seen:
                problems.append(f"{where}: duplicate key")
            seen.add(rid)
            verified = set(row.get("verified", []))
            for c in row:
                if c not in cols and c != "verified":
                    problems.append(f"{where}: column '{c}' is not defined in the sheet")
            for c in verified:
                if cols.get(c, {}).get("kind") != "fact":
                    problems.append(f"{where}: 'verified' names '{c}', which is not a fact column")
            for c, spec in cols.items():
                v = row.get(c)
                kind = spec["kind"]
                if empty(v):
                    unfilled[spec.get("check", kind)][where].append(c)
                    continue
                if v == "n/a":
                    continue
                if kind == "ref":
                    for ref in as_list(v):
                        target, key = split_ref(spec, ref)
                        if target not in keys or key not in keys[target]:
                            problems.append(f"{where}.{c} -> '{ref}' does not exist")
                        else:
                            used[(target, key)] += 1
                elif kind == "fact" and c not in verified:
                    unverified[spec["check"]][where].append(c)

    # coverage: every survivor has all four slots; nothing is left unused
    for srow in sheets["survivors"]["rows"]:
        have = {r["slot"] for r in sheets["skills"]["rows"] if r["survivor"] == srow["id"]}
        for slot in SLOTS:
            if slot not in have:
                problems.append(f"survivors.{srow['id']}: no skill in the {slot} slot")
    for target in ("weapons", "throwables", "abilities", "assets"):
        for r in sheets[target]["rows"]:
            if used[(target, r["id"])] == 0:
                problems.append(f"{target}.{r['id']}: nothing refers to it")

    return unfilled, unverified, problems


def count(groups):
    return sum(len(cols) for rows in groups.values() for cols in rows.values())


def section(out, md, title, groups):
    total = count(groups)
    out.append(("## " if md else "\n== ") + f"{title}: {total} cells" + ("" if md else " =="))
    if not total:
        out.append("none")
        return
    for method in sorted(groups):
        rows = groups[method]
        out.append(("### " if md else "\n-- ") + f"{method}: {sum(len(c) for c in rows.values())} cells in {len(rows)} rows")
        for where in sorted(rows):
            out.append(("- " if md else "   ") + f"{where}: {', '.join(rows[where])}")


def main():
    md = "--md" in sys.argv
    sheets = load()
    unfilled, unverified, problems = check(sheets)
    out = []
    out.append("# Preflight" if md else "PREFLIGHT")
    out.append(f"{sum(len(s['rows']) for s in sheets.values())} rows in {len(sheets)} sheets")
    section(out, md, "Unfilled", unfilled)
    section(out, md, "Unverified", unverified)
    out.append(("## " if md else "\n== ") + f"Problems: {len(problems)}" + ("" if md else " =="))
    out.extend((("- " if md else "   ") + p) for p in problems) if problems else out.append("none")
    clean = not (count(unfilled) or count(unverified) or problems)
    out.append("")
    out.append("CLEAN: safe to build." if clean else "NOT CLEAN: fix the lists above before building.")
    print("\n".join(out))
    return 0 if clean else 1


if __name__ == "__main__":
    sys.exit(main())
