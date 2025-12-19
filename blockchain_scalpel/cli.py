import runpy
import sys
from pathlib import Path


def main() -> None:
    """
    CLI entrypoint for the PyPI package 'blockchain-scalpel'.

    Executes 'blockchain-parser.py' as if the user ran:
        python blockchain-parser.py <args...>

    Keeps sys.argv intact (arguments are passed through).
    """
    repo_root = Path(__file__).resolve().parent.parent
    target = repo_root / "blockchain-parser.py"

    if not target.exists():
        print("Error: 'blockchain-parser.py' was not found next to the package.", file=sys.stderr)
        raise SystemExit(2)

    # Make usage/help messages look natural.
    # After this, script sees argv like: ["blockchain-parser.py", "./blocks", "./result"]
    if len(sys.argv) > 0:
        sys.argv[0] = str(target)

    runpy.run_path(str(target), run_name="__main__")
