from pathlib import Path


def test_readme():
    with open('README.md') as f:
        readme = f.read()

        bundled = Path(__file__).parent.parent \
            .joinpath('thefuck') \
            .joinpath('rules') \
            .glob('*.py')

        for rule in bundled:
            if rule.stem != '__init__' and rule.stem not in readme:
                raise Exception('Missing rule "{}" in README.md'.format(rule.stem))


if __name__ == '__main__':
    test_readme()
