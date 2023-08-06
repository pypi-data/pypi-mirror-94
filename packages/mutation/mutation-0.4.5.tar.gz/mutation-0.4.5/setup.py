# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mutation']
install_requires = \
['Pygments>=2.7.4,<3.0.0',
 'aiostream>=0.4.1,<0.5.0',
 'astunparse>=1.6.3,<2.0.0',
 'docopt>=0.6.2,<0.7.0',
 'humanize>=3.2.0,<4.0.0',
 'lexode<1.0.0',
 'loguru>=0.5.3,<0.6.0',
 'lsm-db>=0.6.4,<0.7.0',
 'parso>=0.8.1,<0.9.0',
 'pathlib3x>=1.3.9,<2.0.0',
 'pytest-cov>=2.11.1,<3.0.0',
 'pytest-randomly>=3.5.0,<4.0.0',
 'pytest-xdist>=2.2.0,<3.0.0',
 'pytest>=6.2.1,<7.0.0',
 'python-ulid>=1.0.2,<2.0.0',
 'termcolor>=1.1.0,<2.0.0',
 'tqdm>=4.56.0,<5.0.0',
 'zstandard[cffi]>=0.15.1,<0.16.0']

entry_points = \
{'console_scripts': ['mutation = mutation:main'],
 u'pytest11': ['mutation = mutation']}

setup_kwargs = {
    'name': 'mutation',
    'version': '0.4.5',
    'description': 'test mutations for pytest.',
    'long_description': '# mutation\n\n**beta**\n\n`mutation` check that tests are robust.\n\n```sh\npip install mutation\nmutation play tests.py --include="src/*.py"\nmutation replay\n```\n\nBoth `--include` and `--exclude` are optional but highly recommended\nto avoid the production of useless mutations. `mutation` will only\nmutate code that has test coverage, hence it works better with a high\ncoverage.\n\n`mutation` will detect whether the tests can be run in parallel. It is\nrecommended to make the test suite work in parallel to speed up the\nwork of `mutation`.\n\nAlso, it is better to work with a random seed, otherwise add the\noption `--randomly-seed=n` that works.\n\n- [forge](https://git.sr.ht/~amirouche/mutation)\n',
    'author': 'Amirouche',
    'author_email': 'amirouche@hyper.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://git.sr.ht/~amirouche/mutation',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
