#!/usr/bin/env python3
"""
Pipeline link 2 — source-verifier.

For each slide in a clarity-gate run, verifies citations against three sources:

  1. URL'd citations — HTTP HEAD/GET via urllib (in parallel via ThreadPoolExecutor).
     Returns status: verified | fetch_failed | 404.

  2. Named-author quotes — full-text search inside the dossier file for
     verbatim match. Returns status: verified | mismatch | not_in_dossier.

  3. Numeric precision claims — extracted via the aggregator's
     extract_precision_claims, checked against dossier content for substring
     match. Returns status: verified | mismatch | not_in_dossier.

Scope: skill-level mechanisms only (memory/known-failure-mechanisms.json).
Does NOT load project-level patterns — those flow to the Expert prompt, not
here. (Review decision Q3, v2-pipeline.md §source-verifier-scope.)

Halt: confirmed mismatch on a named-author quote OR URL'd citation 404.

Outputs:  <run_dir>/source-verification.json

Usage:  python3 source-verifier.py <run_dir>
"""
from __future__ import annotations

import importlib.util
import ipaddress
import json
import re
import socket
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

SKILL_MEMORY = Path.home() / ".claude/commands/agentic-slides/memory/known-failure-mechanisms.json"
AGGREGATOR_PATH = Path.home() / ".claude/commands/agentic-slides/scripts/clarity-gate-aggregator.py"
USER_AGENT = "Mozilla/5.0 (clarity-gate source-verifier)"
HTTP_TIMEOUT = 8


def is_safe_url(url: str) -> tuple[bool, str]:
    """SSRF guard. Reject non-http(s) schemes and private/loopback/link-local hosts.
    Returns (ok, reason)."""
    try:
        p = urllib.parse.urlparse(url)
    except Exception as e:
        return False, f"unparseable: {e}"
    if p.scheme.lower() not in ("http", "https"):
        return False, f"scheme '{p.scheme}' not allowed (http/https only)"
    host = (p.hostname or "").lower()
    if not host:
        return False, "no host"
    if host in ("localhost", "metadata", "metadata.google.internal"):
        return False, f"banned hostname '{host}'"
    # Resolve to an IP and reject private/loopback/link-local/multicast.
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror as e:
        return False, f"DNS failure: {e}"
    for info in infos:
        ip = info[4][0]
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return False, f"unparseable IP {ip}"
        if addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_multicast or addr.is_reserved or addr.is_unspecified:
            return False, f"host {host} resolves to non-public IP {ip}"
    return True, "ok"


def _import_aggregator():
    """Import aggregator as a module to reuse extract_precision_claims."""
    spec = importlib.util.spec_from_file_location("clarity_gate_aggregator", AGGREGATOR_PATH)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def fetch_url(url: str) -> dict:
    """HEAD-then-GET fallback. Returns status dict.

    SSRF guard fires before any network call: rejects non-http(s) schemes,
    localhost, and any hostname that resolves to a private/loopback/link-local IP.
    """
    ok, reason = is_safe_url(url)
    if not ok:
        return {"fetch_status": "blocked_ssrf_guard", "url": url, "error": reason}
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
            return {"fetch_status": "verified", "http_status": resp.status, "url": url}
    except urllib.error.HTTPError as e:
        # Some hosts reject HEAD — retry with GET
        if e.code in (403, 405):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
                with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                    return {"fetch_status": "verified", "http_status": resp.status, "url": url}
            except Exception as exc:
                return {"fetch_status": "fetch_failed", "url": url, "error": str(exc)}
        if e.code == 404:
            return {"fetch_status": "404", "url": url, "error": "Not Found"}
        return {"fetch_status": "fetch_failed", "url": url, "error": f"HTTP {e.code}"}
    except urllib.error.URLError as e:
        return {"fetch_status": "fetch_failed", "url": url, "error": str(e.reason)}
    except Exception as e:
        return {"fetch_status": "fetch_failed", "url": url, "error": str(e)}


URL_PATTERN = re.compile(r"https?://[^\s\)\"\']+")
QUOTE_PATTERN = re.compile(r'"([^"]{20,400})"')


def extract_urls(text: str) -> list[str]:
    return list(dict.fromkeys(URL_PATTERN.findall(text or "")))


def extract_quotes(text: str) -> list[str]:
    return list(dict.fromkeys(QUOTE_PATTERN.findall(text or "")))


def verify_quote_in_dossier(quote: str, dossier_norm: str) -> dict:
    """Substring search. Caller passes pre-normalized dossier text (whitespace collapsed)
    so we don't re-normalize a 200KB+ string per quote."""
    if not quote:
        return {"fetch_status": "not_in_dossier", "quote": quote}
    norm = re.sub(r"\s+", " ", quote.strip())
    if norm in dossier_norm:
        return {"fetch_status": "verified", "quote": quote[:120]}
    # Try a leading-30-char match as a "partial verbatim" signal
    head = norm[:30]
    if head and head in dossier_norm:
        return {"fetch_status": "mismatch", "quote": quote[:120],
                "note": "leading 30 chars match dossier but full quote diverges — likely paraphrase shipped as verbatim"}
    return {"fetch_status": "not_in_dossier", "quote": quote[:120]}


def verify_numeric_in_dossier(claim: dict, dossier_norm_lower: str) -> dict:
    """Caller passes pre-lowercased normalized dossier (built once in main())."""
    value = claim["value"]
    if value.lower() in dossier_norm_lower:
        return {"fetch_status": "verified", **claim}
    return {"fetch_status": "not_in_dossier", **claim,
            "note": "numeric claim not found in dossier — verify against original source"}


# Slide block extraction — mirrors auto-applier.py:slide_id_to_marker_candidates verbatim.
# If you change this function, change the twin in auto-applier.py at the same time.
# Intentional duplication per plan §C (let-s-pick-this-up-functional-ember.md): two CLI tools, ~15 lines, simplicity > premature extraction.
# Trigger to extract into deck_utils.py: when a third script needs the same logic.
def slide_id_to_marker_candidates(slide_id: str) -> list[str]:
    """Manifest 'S10C' may appear as 'Slide 10C' or 'Slide 10b' in deck. Try both."""
    digits = re.sub(r"^S", "", slide_id)
    m = re.match(r"^(\d+)([A-Za-z]*)$", digits)
    if not m:
        return [f"## Slide {digits}:"]
    num, suffix = m.group(1), m.group(2)
    out = [f"## Slide {int(num)}{suffix}:"]
    # Closer-slide convention: manifest 'C' suffix often appears as 'b' in deck.
    if suffix.lower() == "c":
        out.append(f"## Slide {int(num)}b:")
    return out


def extract_slide_block(deck_text: str, slide_id: str) -> str | None:
    for marker in slide_id_to_marker_candidates(slide_id):
        start = deck_text.find(marker)
        if start == -1:
            continue
        rest = deck_text[start:]
        end_rule = rest.find("\n---\n")
        end_next = rest.find("\n## Slide ", 1)
        candidates = [e for e in (end_rule, end_next) if e != -1]
        if not candidates:
            return rest
        return rest[: min(candidates)]
    return None


def verify_slide(slide_id: str, block: str, dossier_norm: str, dossier_norm_lower: str, aggregator) -> dict:
    """Return per-slide verification record (citations list)."""
    urls = extract_urls(block)
    quotes = extract_quotes(block)
    numerics = aggregator.extract_precision_claims(block)

    citations: list[dict] = []
    # URLs verified in parallel by the caller; here we just stub the records
    for u in urls:
        citations.append({"kind": "url", "url": u, "fetch_status": "pending"})
    for q in quotes:
        citations.append({"kind": "quote", **verify_quote_in_dossier(q, dossier_norm)})
    for n in numerics:
        citations.append({"kind": "numeric", **verify_numeric_in_dossier(n, dossier_norm_lower)})
    return {"slide_id": slide_id, "citations": citations}


def _assert_safe_deck_path(deck_path: Path, run_dir: Path) -> None:
    """Reject path traversal. deck_path must resolve under the same project root
    that contains run_dir, and must end in .md."""
    resolved = deck_path.resolve()
    if resolved.suffix.lower() != ".md":
        raise ValueError(f"deck_path {resolved} is not a .md file")
    # Project root: parent of `.clarity-gate/` (which contains run_dir)
    project_root = run_dir.resolve().parent.parent
    try:
        resolved.relative_to(project_root)
    except ValueError:
        raise ValueError(f"deck_path {resolved} is not inside project root {project_root}")


def _gate_halted(aggregate: dict) -> str | None:
    """Inspect aggregate.json for a halt signal from link 1. Returns reason or None."""
    if aggregate.get("critical_failures"):
        return f"gate critical_failures: {aggregate['critical_failures']}"
    verdict = (aggregate.get("deck_verdict") or "").upper()
    if "CRITICAL FAILURES" in verdict or "REDRAFT DECK" in verdict:
        return f"gate verdict: {aggregate.get('deck_verdict')}"
    return None


def main(run_dir_str: str) -> int:
    run_dir = Path(run_dir_str)
    manifest_path = run_dir / "run-manifest.json"
    aggregate_path = run_dir / "aggregate.json"
    if not manifest_path.exists():
        print(f"FATAL: run-manifest.json missing in {run_dir}", file=sys.stderr)
        return 2
    if not aggregate_path.exists():
        print(f"FATAL: aggregate.json missing in {run_dir} — gate (link 1) didn't produce output", file=sys.stderr)
        return 2
    manifest = json.loads(manifest_path.read_text())
    aggregate = json.loads(aggregate_path.read_text())

    # Halt cascade from link 1 — if the gate flagged critical failures, don't proceed.
    halt = _gate_halted(aggregate)
    if halt:
        print(f"FATAL: gate halt — {halt}", file=sys.stderr)
        return 2

    deck_path = Path(manifest["deck_path"])
    try:
        _assert_safe_deck_path(deck_path, run_dir)
    except ValueError as e:
        print(f"FATAL: unsafe deck_path — {e}", file=sys.stderr)
        return 2
    dossier_path = Path(manifest.get("source_dossier_path", ""))
    if not deck_path.exists():
        print(f"FATAL: deck file {deck_path} not found", file=sys.stderr)
        return 2

    deck_text = deck_path.read_text()
    # Normalize the dossier ONCE here, not per quote inside verify_quote_in_dossier
    # (caught by perf review — was 60× redundant work on a 30-slide deck).
    dossier_text = dossier_path.read_text() if dossier_path.exists() else ""
    dossier_norm = re.sub(r"\s+", " ", dossier_text)
    dossier_norm_lower = dossier_norm.lower()

    aggregator = _import_aggregator()

    # Load skill-level mechanisms (currently no-op for source-verifier, but
    # this is the place where Step 7's promoted rules would land).
    skill_mechanisms: list[dict[str, Any]] = []
    if SKILL_MEMORY.exists():
        skill_mechanisms = json.loads(SKILL_MEMORY.read_text()).get("mechanisms", [])

    slides_in_scope = manifest["slides_in_scope"]
    per_slide: list[dict] = []
    all_urls: list[tuple[str, str]] = []   # (slide_id, url)

    for sid in slides_in_scope:
        block = extract_slide_block(deck_text, sid)
        if block is None:
            per_slide.append({"slide_id": sid, "citations": [{"kind": "error", "error": "slide not found in deck"}]})
            continue
        record = verify_slide(sid, block, dossier_norm, dossier_norm_lower, aggregator)
        per_slide.append(record)
        for c in record["citations"]:
            if c["kind"] == "url":
                all_urls.append((sid, c["url"]))

    # Parallel HTTP fetches — ThreadPoolExecutor for I/O concurrency.
    fetch_results: dict[str, dict] = {}
    if all_urls:
        unique_urls = list({u for _, u in all_urls})
        with ThreadPoolExecutor(max_workers=10) as ex:
            for url, result in zip(unique_urls, ex.map(fetch_url, unique_urls)):
                fetch_results[url] = result

    # Fold fetch results back into per_slide records
    for slide_record in per_slide:
        for c in slide_record["citations"]:
            if c["kind"] == "url":
                c.update(fetch_results.get(c["url"], {"fetch_status": "fetch_failed", "error": "no result"}))

    # Halt decision
    halt_reasons: list[str] = []
    for s in per_slide:
        for c in s["citations"]:
            if c["kind"] == "quote" and c["fetch_status"] == "mismatch":
                halt_reasons.append(f"{s['slide_id']}: quote mismatch (paraphrase shipped as verbatim?)")
            if c["kind"] == "url" and c["fetch_status"] == "404":
                halt_reasons.append(f"{s['slide_id']}: cited URL returned 404 — {c['url']}")

    output = {
        "run_id": manifest["run_id"],
        "deck_id": manifest["deck_id"],
        "skill_mechanisms_loaded": len(skill_mechanisms),
        "fetch_count": len(fetch_results),
        "halt_reasons": halt_reasons,
        "slides": per_slide,
    }
    (run_dir / "source-verification.json").write_text(json.dumps(output, indent=2))

    print(f"WROTE: {run_dir / 'source-verification.json'}")
    print(f"  {len(per_slide)} slide(s) checked · {len(fetch_results)} URL(s) fetched · "
          f"{sum(1 for s in per_slide for c in s['citations'] if c.get('fetch_status') == 'verified')} verified")
    if halt_reasons:
        print(f"HALT: {len(halt_reasons)} reason(s):", file=sys.stderr)
        for r in halt_reasons:
            print(f"  - {r}", file=sys.stderr)
        return 4
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: source-verifier.py <run_dir>", file=sys.stderr)
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
