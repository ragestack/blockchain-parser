import runpy
import sys
from importlib import resources


def main() -> None:
    """
    CLI entrypoint for the PyPI package 'blockchain-scalpel'.

    Executes the bundled 'blockchain-parser.py' script as if the user ran:
        python blockchain-parser.py <args...>
    """
    try:
        script = resources.files("blockchain_scalpel").joinpath("blockchain-parser.py")
    except Exception:
        print("Error: cannot locate bundled 'blockchain-parser.py'.", file=sys.stderr)
        raise SystemExit(2)

    if not script.is_file():
        print("Error: bundled 'blockchain-parser.py' not found.", file=sys.stderr)
        raise SystemExit(2)

    # Make argv[0] look like the original script name
    if len(sys.argv) > 0:
        sys.argv[0] = "blockchain-parser.py"

    runpy.run_path(str(script), run_name="__main__")
