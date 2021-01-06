"""Allow configlib to be executable through `python -m configlib`."""
from __future__ import absolute_import

from .cli_scheduler import main

if __name__ == "__main__":  # pragma: no cover
    main()
