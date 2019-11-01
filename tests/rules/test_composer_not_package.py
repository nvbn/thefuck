import pytest
from thefuck.rules.composer_not_package import match, get_new_command
from thefuck.types import Command

# tested with composer version 1.9.0

# command:
# composer require laravel-nova-csv-import
# the one that started it all
case_original = ("composer require laravel-nova-csv-import", '\n'
                 '                                                   ''\n'
                 '  [InvalidArgumentException]                       ''\n'
                 '  Could not find package laravel-nova-csv-import.  ''\n'
                 '                                                   ''\n'
                 '  Did you mean this?                               ''\n'
                 '      simonhamp/laravel-nova-csv-import            ''\n'
                 '                                                   ''\n'
                 'require [--dev] [--prefer-source] [--prefer-dist] [--no-progress] [--no-suggest] [--no-update] [--no-scripts] [--update-no-dev] [--update-with-dependencies] [--update-with-all-dependencies] [--ignore-platform-reqs] [--prefer-stable] [--prefer-lowest] [--sort-packages] [-o|--optimize-autoloader] [-a|--classmap-authoritative] [--apcu-autoloader] [--] [<packages>]...''\n'
                 '\n')
case_original_expected = "composer require simonhamp/laravel-nova-csv-import"

# command:
# composer require datrack/elasticroute
case_single_suggestion = ("composer require datrack/elasticroute", '\n'
                          '                                                ''\n'
                          '  [InvalidArgumentException]                    ''\n'
                          '  Could not find package datrack/elasticroute.  ''\n'
                          '                                                ''\n'
                          '  Did you mean this?                            ''\n'
                          '      detrack/elasticroute                      ''\n'
                          '                                                ''\n'
                          'require [--dev] [--prefer-source] [--prefer-dist] [--no-progress] [--no-suggest] [--no-update] [--no-scripts] [--update-no-dev] [--update-with-dependencies] [--update-with-all-dependencies] [--ignore-platform-reqs] [--prefer-stable] [--prefer-lowest] [--sort-packages] [-o|--optimize-autoloader] [-a|--classmap-authoritative] [--apcu-autoloader] [--] [<packages>]...''\n'
                          '\n')
case_single_suggestion_expected = "composer require detrack/elasticroute"

# command:
# composer require potato
case_many_suggestions = ("composer require potato", '\n'
                         '                                  ''\n'
                         '  [InvalidArgumentException]      ''\n'
                         '  Could not find package potato.  ''\n'
                         '                                  ''\n'
                         '  Did you mean one of these?      ''\n'
                         '      drteam/potato               ''\n'
                         '      florence/potato             ''\n'
                         '      kola/potato-orm             ''\n'
                         '      jsyqw/potato-bot            ''\n'
                         '      vundi/potato-orm            ''\n'
                         '                                  ''\n\n'
                         'require [--dev] [--prefer-source] [--prefer-dist] [--no-progress] [--no-suggest] [--no-update] [--no-scripts] [--update-no-dev] [--update-with-dependencies] [--update-with-all-dependencies] [--ignore-platform-reqs] [--prefer-stable] [--prefer-lowest] [--sort-packages] [-o|--optimize-autoloader] [-a|--classmap-authoritative] [--apcu-autoloader] [--] [<packages>]...''\n'
                         '\n')
case_many_suggestions_expected = ["composer require drteam/potato",
                                  "composer require florence/potato",
                                  "composer require kola/potato-orm",
                                  "composer require jsyqw/potato-bot",
                                  "composer require vundi/potato-orm"]

# command:
# composer require datrack/elasticroute:*
case_single_package_with_version_constraint = ("composer require datrack/elasticroute:*", '\n'
                                               '                                                ''\n'
                                               '  [InvalidArgumentException]                    ''\n'
                                               '  Could not find package datrack/elasticroute.  ''\n'
                                               '                                                ''\n'
                                               '  Did you mean this?                            ''\n'
                                               '      detrack/elasticroute                      ''\n'
                                               '                                                ''\n\n'
                                               'require [--dev] [--prefer-source] [--prefer-dist] [--no-progress] [--no-suggest] [--no-update] [--no-scripts] [--update-no-dev] [--update-with-dependencies] [--update-with-all-dependencies] [--ignore-platform-reqs] [--prefer-stable] [--prefer-lowest] [--sort-packages] [-o|--optimize-autoloader] [-a|--classmap-authoritative] [--apcu-autoloader] [--] [<packages>]...''\n'
                                               '\n')
case_single_package_with_version_constraint_expected = "composer require detrack/elasticroute:*"


# command:
# composer require potato:*
case_single_package_with_version_constraint_many_suggestions = ("composer require potato:1.2.3", '\n'
                                                                '                                  ''\n'
                                                                '  [InvalidArgumentException]      ''\n'
                                                                '  Could not find package potato.  ''\n'
                                                                '                                  ''\n'
                                                                '  Did you mean one of these?      ''\n'
                                                                '      drteam/potato               ''\n'
                                                                '      florence/potato             ''\n'
                                                                '      kola/potato-orm             ''\n'
                                                                '      jsyqw/potato-bot            ''\n'
                                                                '      vundi/potato-orm            ''\n'
                                                                '                                  ''\n\n'
                                                                'require [--dev] [--prefer-source] [--prefer-dist] [--no-progress] [--no-suggest] [--no-update] [--no-scripts] [--update-no-dev] [--update-with-dependencies] [--update-with-all-dependencies] [--ignore-platform-reqs] [--prefer-stable] [--prefer-lowest] [--sort-packages] [-o|--optimize-autoloader] [-a|--classmap-authoritative] [--apcu-autoloader] [--] [<packages>]...''\n'

                                                                '\n'
                                                                )
case_single_package_with_version_constraint_many_suggestions_expected = ["composer require drteam/potato:1.2.3",
                                                                         "composer require florence/potato:1.2.3",
                                                                         "composer require kola/potato-orm:1.2.3",
                                                                         "composer require jsyqw/potato-bot:1.2.3",
                                                                         "composer require vundi/potato-orm:1.2.3"]


@pytest.mark.parametrize('command', [Command(*v) for v in [
    case_original,
    case_single_suggestion,
    case_many_suggestions,
    case_single_package_with_version_constraint,
    case_single_package_with_version_constraint_many_suggestions
]])
def test_match(command):
    assert match(command)


@pytest.mark.parametrize('command, new_command', [(Command(*t[0]), t[1]) for t in [
    (case_original, case_original_expected),
    (case_single_suggestion, case_single_suggestion_expected),
    (case_many_suggestions, case_many_suggestions_expected),
    (case_single_package_with_version_constraint, case_single_package_with_version_constraint_expected),
    (case_single_package_with_version_constraint_many_suggestions,
     case_single_package_with_version_constraint_many_suggestions_expected),
]])
def test_get_new_command(command, new_command):
    assert get_new_command(command) == new_command
