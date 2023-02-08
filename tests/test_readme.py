def test_readme(source_root):
    with source_root.joinpath('README.md').open() as f:
        readme = f.read()

        bundled = source_root.joinpath('thefuck') \
                             .joinpath('rules') \
                             .glob('*.py')

        for rule in bundled:
            if rule.stem != '__init__':
                assert rule.stem in readme,\
                    f'Missing rule "{rule.stem}" in README.md'
