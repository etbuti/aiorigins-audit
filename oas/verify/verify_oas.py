#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import sys
from typing import Any, Dict, Optional, Tuple

def canonical_json_bytes(obj: Any) -> bytes:
    # OAS Canonical JSON v0.1 minimal: sort_keys + compact separators
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def verify_manifest_self_hash(manifest_path: str) -> Tuple[bool, str, str]:
    m = load_json(manifest_path)

    anchor = m.get("anchor", {})
    claimed = anchor.get("current_hash", "")
    if not claimed or not isinstance(claimed, str):
        return False, "", "manifest.anchor.current_hash missing"

    # compute self-hash with current_hash omitted
    m2 = json.loads(json.dumps(m))
    if "anchor" in m2 and isinstance(m2["anchor"], dict):
        m2["anchor"].pop("current_hash", None)

    computed = sha256_hex(canonical_json_bytes(m2))
    ok = (computed == claimed)
    return ok, computed, claimed

def parse_anchor_line(line: str) -> Optional[Tuple[int, str, str, str, str]]:
    # v0.1: seq ts hash prev_hash domain
    parts = line.strip().split()
    if len(parts) < 5:
        return None
    try:
        seq = int(parts[0])
    except:
        return None
    ts = parts[1]
    h = parts[2]
    prev = parts[3]
    dom = parts[4]
    return seq, ts, h, prev, dom

def verify_anchor_chain(anchor_log_path: str) -> Tuple[bool, str]:
    if not os.path.exists(anchor_log_path):
        return False, "anchor log not found"

    with open(anchor_log_path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]

    if not lines:
        return False, "anchor log is empty"

    prev_hash = None
    prev_seq = None
    for i, ln in enumerate(lines):
        parsed = parse_anchor_line(ln)
        if not parsed:
            return False, f"invalid anchor line format at line {i+1}"

        seq, ts, h, prev, dom = parsed

        if prev_seq is not None and seq != prev_seq + 1:
            return False, f"sequence break at line {i+1}: got {seq}, expected {prev_seq+1}"

        if prev_hash is None:
            # genesis: prev should be 64 zeros (recommended) but allow anything if you decide later
            prev_hash = h
            prev_seq = seq
            continue

        if prev != prev_hash:
            return False, f"prev_hash mismatch at line {i+1}: prev={prev[:12]}.. expected={prev_hash[:12]}.."

        prev_hash = h
        prev_seq = seq

    return True, "anchor chain OK"

def main():
    p = argparse.ArgumentParser(description="OAS v0.1 verifier (self-hash + optional chain checks)")
    p.add_argument("--manifest", required=True, help="Path to manifest.json")
    p.add_argument("--anchor-log", default="", help="Optional path to anchor.log (seq ts hash prev domain)")
    args = p.parse_args()

    ok, computed, claimed_or_err = verify_manifest_self_hash(args.manifest)
    if not ok:
        print("[FAIL] manifest self-hash")
        if computed:
            print("  computed:", computed)
            print("  claimed :", claimed_or_err)
        else:
            print("  error   :", claimed_or_err)
        sys.exit(2)

    print("[OK] manifest self-hash")
    print("  hash:", computed)

    if args.anchor_log:
        ok2, msg = verify_anchor_chain(args.anchor_log)
        if ok2:
            print("[OK] anchor chain:", msg)
        else:
            print("[WARN] anchor chain:", msg)
            # not hard-fail because you may not publish anchor log publicly yet

    print("DONE")

if __name__ == "__main__":
    main()
