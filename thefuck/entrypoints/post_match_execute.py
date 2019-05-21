from thefuck.types import Rule
from pathlib import Path


def post_match_execute(known_args):
    """Executes post match funtion. Used when `thefuck` called with `--post-match` argument."""
    # check the first flag to see what rule
    rule = Rule.from_path(Path(known_args.command[0]))
    rule.post_match(known_args.command[1], known_args.command[2])
