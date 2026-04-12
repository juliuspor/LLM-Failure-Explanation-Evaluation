from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Export user-study data from a GCS bucket.")
    parser.add_argument("--bucket", required=True, help="GCS bucket name")
    parser.add_argument("--prefix", default="user_study/", help="Prefix to export (default: user_study/)")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory (default: user_study/exports/<timestamp>)",
    )
    args = parser.parse_args()

    out_dir = args.out_dir
    if out_dir is None:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_dir = Path("user_study") / "exports" / ts
    out_dir.mkdir(parents=True, exist_ok=True)

    from google.cloud import storage  # type: ignore

    client = storage.Client()
    bucket = client.bucket(args.bucket)
    blobs = list(client.list_blobs(bucket, prefix=args.prefix))
    if not blobs:
        print(f"No objects found for prefix {args.prefix!r} in bucket {args.bucket!r}")
        return 1

    for blob in blobs:
        rel = Path(blob.name)
        dest = out_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        blob.download_to_filename(str(dest))

    print(f"Exported {len(blobs)} objects to {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

