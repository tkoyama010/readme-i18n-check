"""Entry point for ``python -m check_readme_i18n``."""

from __future__ import annotations

import logging
import sys

from check_readme_i18n import main

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        stream=sys.stderr,
    )
    raise SystemExit(main())
