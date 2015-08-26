from tests.utils import root


def test_readme():
    with root.joinpath('README.md').open() as f:
        readme = f.read()

        bundled = root \
            .joinpath('thefuck') \
            .joinpath('rules') \
            .glob('*.py')

        for rule in bundled:
            if rule.stem != '__init__':
                assert rule.stem in readme,\
                    'Missing rule "{}" in README.md'.format(rule.stem)
