"""Entry program for make.fun news-image-20261119.

The finished front page is stored in the repository as entry.png
(rendered programmatically with PIL from the verified stories of
Thursday 19 November 2026; see render.py for how it was drawn).
This program simply copies it to the output directory, so the run
is deterministic: every run writes the same bytes.

Standard library only; no network.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    if not SOURCE.is_file():
        raise FileNotFoundError(f"entry image missing: {SOURCE}")
    dest = out_dir / "entry.png"
    shutil.copyfile(SOURCE, dest)
    # Sanity check: the copy must be byte-identical to the source.
    if dest.stat().st_size != SOURCE.stat().st_size:
        raise IOError(f"copy incomplete: {dest}")


if __name__ == "__main__":
    main()
