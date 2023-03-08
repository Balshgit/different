import pkgutil
from pathlib import Path


def load_all_models() -> None:
    """Load all models from this folder."""
    root_dir = Path(__file__).resolve().parent
    modules = pkgutil.walk_packages(
        path=[str(root_dir)],
        prefix="db.models.",
    )
    for module in modules:
        __import__(module.name)
