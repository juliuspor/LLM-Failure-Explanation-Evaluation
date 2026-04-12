"""
Common utilities for scripts/ entrypoints.
Handles bootstrap (sys.path, dotenv) and shared CLI patterns.
"""

import os
import sys
from dotenv import load_dotenv


def ensure_project_root_on_syspath(script_file: str) -> None:
    """
    Insert the project root directory into sys.path.
    
    This ensures that imports like 'from src import ...' work correctly
    regardless of where the script is executed from.
    
    Args:
        script_file: Pass __file__ from the calling script.
    """
    script_dir = os.path.dirname(os.path.abspath(script_file))
    project_root = os.path.dirname(script_dir)
    if project_root not in sys.path:
        sys.path.insert(0, project_root)


def load_env(*, override: bool = False) -> None:
    """
    Load environment variables from .env file.
    
    Args:
        override: If True, existing environment variables will be overwritten
                 by values from .env. If False, existing values are preserved.
    """
    load_dotenv(override=override)


DEFAULT_LEVELS = "CODE,ERROR,TEST"


def add_defect_argument(parser, help_text="Defect ID (e.g., defect1_py)"):
    """
    Add the standard --defect/-d argument to an ArgumentParser.
    
    Args:
        parser: An argparse.ArgumentParser instance.
        help_text: Custom help text for the argument (default: "Defect ID (e.g., defect1_py)").
    """
    parser.add_argument(
        "-d", "--defect",
        help=help_text
    )


def add_levels_argument(parser, default=None, help_text="Comma-separated context levels (e.g., CODE,ERROR,TEST)"):
    """
    Add the standard --levels/-l argument to an ArgumentParser.
    
    Args:
        parser: An argparse.ArgumentParser instance.
        default: Default value for levels. If None, uses DEFAULT_LEVELS.
        help_text: Custom help text for the argument (default: "Comma-separated context levels (e.g., CODE,ERROR,TEST)").
    """
    if default is None:
        default = DEFAULT_LEVELS
    parser.add_argument(
        "-l", "--levels",
        default=default,
        help=help_text
    )


def add_runs_argument(parser):
    """
    Add the standard --runs argument to an ArgumentParser.
    
    Args:
        parser: An argparse.ArgumentParser instance.
    """
    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Number of runs (default: 1)"
    )
