from difflib import get_close_matches


def fix_git_command(git_command):
    git_possible = ['clone', 'init', 'add', 'mv', 'reset', 'rm', 'bisect',
                    'grep', 'log', 'show', 'status', 'branch', 'checkout',
                    'commit', 'diff', 'merge', 'rebase', 'tag', 'fetch',
                    'pull', 'push']
    if git_command not in git_possible[0]:
        close_match = get_close_matches(git_command, git_possible)
        if len(close_match) > 0:
            return close_match[0]
        else:
            return git_command
    else:
        return git_command
