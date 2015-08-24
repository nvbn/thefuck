from pathlib import Path


def test_readme():
    project_root = Path(__file__).parent.parent
    with project_root.joinpath('README.md').open() as f:
        readme = f.read()

        bundled = project_root \
            .joinpath('thefuck') \
            .joinpath('rules') \
            .glob('*.py')

        for rule in bundled:
            if rule.stem != '__init__':
                assert rule.stem in readme,\
                    'Missing rule "{}" in README.md'.format(rule.stem)
