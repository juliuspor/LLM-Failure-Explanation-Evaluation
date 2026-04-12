from __future__ import annotations

import argparse
import json
import secrets
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate magic-link tokens for the user study.")
    parser.add_argument("--n", type=int, default=8, help="Number of participant tokens to generate.")
    parser.add_argument("--base-url", required=True, help="Cloud Run base URL, e.g. https://service-xyz.run.app")
    parser.add_argument("--out", type=Path, default=None, help="Optional output JSON file for tokens/links.")
    args = parser.parse_args()

    base = args.base_url.rstrip("/")
    tokens = []
    for _ in range(args.n):
        tok = secrets.token_urlsafe(32)
        tokens.append({"token": tok, "url": f"{base}/t/{tok}"})

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "count": len(tokens),
        "tokens": tokens,
    }

    print(json.dumps(payload, indent=2))
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

