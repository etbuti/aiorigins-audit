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
    
    # signatures do not participate in proof hash
    m2.pop("signatures", None)

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
        lines = [ln.strip() for ln in f.readlines() if ln.strip() and not ln.strip().startswith("#")]
        
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
            prev_hash = h
            prev_seq = seq
            continue

        if prev != prev_hash:
            return False, f"prev_hash mismatch at line {i+1}: prev={prev[:12]}.. expected={prev_hash[:12]}.."

        prev_hash = h
        prev_seq = seq

    return True, "anchor chain OK"

def verify_manifest_anchor_presence(manifest_path: str, anchor_log_path: str) -> Tuple[bool, str]:
    m = load_json(manifest_path)
    seq = m.get("anchor", {}).get("anchor_sequence", None)
    cur = m.get("anchor", {}).get("current_hash", "")
    prev = m.get("anchor", {}).get("previous_hash", "")
    dom = m.get("target", {}).get("domain", "")

    if not isinstance(seq, int) or not cur or not prev or not dom:
        return False, "manifest missing anchor_sequence/current_hash/previous_hash/target.domain"

    if not os.path.exists(anchor_log_path):
        return False, "anchor log not found"

    with open(anchor_log_path, "r", encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            parsed = parse_anchor_line(ln)
            if not parsed:
                continue
            s, ts, h, p, d = parsed
            if s == seq:
                if h != cur:
                    return False, f"anchor seq {seq} hash mismatch"
                if p != prev:
                    return False, f"anchor seq {seq} prev_hash mismatch"
                if d != dom:
                    return False, f"anchor seq {seq} domain mismatch"
                return True, f"anchor presence OK (seq {seq})"

    return False, f"anchor seq {seq} not found in anchor log"
    
def verify_anchor_sample_log(anchor_log_path: str, sample_manifest_path: str) -> Tuple[bool, str]:
    if not os.path.exists(anchor_log_path):
        return False, "anchor log not found"
    if not os.path.exists(sample_manifest_path):
        return False, "anchor sample manifest not found"

    sm = load_json(sample_manifest_path)
    want = sm.get("sample", {}).get("sha256", "")
    want_bytes = sm.get("sample", {}).get("bytes", None)
    want_lines = sm.get("sample", {}).get("lines", None)

    if not want:
        return False, "sample manifest missing sample.sha256"

    with open(anchor_log_path, "rb") as f:
        data = f.read()
    got = sha256_hex(data)

    if got != want:
        return False, "anchor.sample.log sha256 mismatch"

    # optional checks
    if isinstance(want_bytes, int) and len(data) != want_bytes:
        return False, f"anchor.sample.log bytes mismatch (got {len(data)} expected {want_bytes})"

    if isinstance(want_lines, int):
        # count non-empty lines excluding comments
        text = data.decode("utf-8", errors="replace")
        lines = [ln for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
        if len(lines) != want_lines:
            return False, f"anchor.sample.log lines mismatch (got {len(lines)} expected {want_lines})"

    return True, "anchor sample log OK"
    
def verify_artifacts(manifest_path: str, root_dir: str) -> Tuple[bool, str]:
    m = load_json(manifest_path)
    artifacts = m.get("artifacts", [])
    if not artifacts:
        return True, "no artifacts listed (skip)"

    for i, a in enumerate(artifacts):
        rel = a.get("path")
        claimed_hash = a.get("sha256")
        claimed_bytes = a.get("bytes")
        if not rel or not claimed_hash:
            return False, f"artifact[{i}] missing path/sha256"

        p = os.path.join(root_dir, rel)
        if not os.path.exists(p):
            return False, f"artifact[{i}] not found: {rel}"

        with open(p, "rb") as f:
            data = f.read()

        h = sha256_hex(data)
        if h != claimed_hash:
            return False, f"artifact[{i}] sha256 mismatch: {rel}"

        if isinstance(claimed_bytes, int) and len(data) != claimed_bytes:
            return False, f"artifact[{i}] bytes mismatch: {rel} (got {len(data)} expected {claimed_bytes})"

    return True, "artifacts OK"

def main():
    p = argparse.ArgumentParser(description="OAS v0.1 verifier (self-hash + optional artifact/chain checks)")
    p.add_argument("--manifest", required=True, help="Path to manifest.json")
    p.add_argument("--root", default="", help="Optional report root dir to verify artifacts (e.g. '.' where artifacts/ lives)")
    p.add_argument("--anchor-log", default="", help="Optional path to anchor.log (seq ts hash prev domain)")
    p.add_argument("--anchor-sample-manifest", default="",
                   help="Optional anchor sample manifest json to verify anchor log sha256/bytes/lines")
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

    if args.root:
        ok3, msg3 = verify_artifacts(args.manifest, args.root)
        if ok3:
            print("[OK] artifacts:", msg3)
        else:
            print("[FAIL] artifacts:", msg3)
            sys.exit(3)

    if args.anchor_log:
        if args.anchor_sample_manifest:
            okS, msgS = verify_anchor_sample_log(args.anchor_log, args.anchor_sample_manifest)
            if okS:
                print("[OK] anchor sample:", msgS)
            else:
                print("[FAIL] anchor sample:", msgS)
                sys.exit(5)

        okp, msgp = verify_manifest_anchor_presence(args.manifest, args.anchor_log)
        if okp:
            print("[OK] anchor presence:", msgp)
        else:
            print("[FAIL] anchor presence:", msgp)
            sys.exit(4)

        ok2, msg = verify_anchor_chain(args.anchor_log)
        if ok2:
            print("[OK] anchor chain:", msg)
        else:
            print("[WARN] anchor chain:", msg)

    print("DONE")
if __name__ == "__main__":
    main()
