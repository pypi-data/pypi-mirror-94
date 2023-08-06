# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['drytoml', 'drytoml.app']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4.0,<0.5.0', 'tomlkit>=0.7.0,<0.8.0']

extras_require = \
{'all': ['black>=20.8b1,<21.0',
         'flakeheaven>=0.10.0-alpha.0,<0.11.0',
         'isort>=5.7.0,<6.0.0'],
 'black': ['black>=20.8b1,<21.0'],
 'dev': ['black>=20.8b1,<21.0',
         'flakeheaven>=0.10.0-alpha.0,<0.11.0',
         'isort>=5.7.0,<6.0.0',
         'pytest>=6.2.2,<7.0.0',
         'Sphinx>=3.4.3,<4.0.0',
         'pytest-cov>=2.11.1,<3.0.0',
         'sphinx-rtd-theme>=0.5.1,<0.6.0',
         'flake8-bandit>=2.1.2,<3.0.0',
         'flake8-bugbear>=20.11.1,<21.0.0',
         'flake8-builtins>=1.5.3,<2.0.0',
         'flake8-comprehensions>=3.3.1,<4.0.0',
         'darglint>=1.6.0,<2.0.0',
         'flake8-docstrings>=1.5.0,<2.0.0',
         'flake8-eradicate>=1.0.0,<2.0.0',
         'flake8-mutable>=1.2.0,<2.0.0',
         'flake8-debugger>=4.0.0,<5.0.0',
         'flake8-pytest-style>=1.3.0,<2.0.0',
         'pep8-naming>=0.11.1,<0.12.0',
         'pytest-html>=3.1.1,<4.0.0',
         'm2r2>=0.2.7,<0.3.0',
         'recommonmark>=0.7.1,<0.8.0',
         'commitizen>=2.14.2,<3.0.0',
         'pre-commit>=2.10.1,<3.0.0',
         'pylint>=2.6.0,<3.0.0'],
 'docs': ['Sphinx>=3.4.3,<4.0.0',
          'sphinx-rtd-theme>=0.5.1,<0.6.0',
          'm2r2>=0.2.7,<0.3.0',
          'recommonmark>=0.7.1,<0.8.0'],
 'flakehell': ['flakeheaven>=0.10.0-alpha.0,<0.11.0'],
 'format': ['black>=20.8b1,<21.0', 'isort>=5.7.0,<6.0.0'],
 'isort': ['isort>=5.7.0,<6.0.0'],
 'lint': ['black>=20.8b1,<21.0',
          'flakeheaven>=0.10.0-alpha.0,<0.11.0',
          'isort>=5.7.0,<6.0.0',
          'pytest>=6.2.2,<7.0.0',
          'flake8-bandit>=2.1.2,<3.0.0',
          'flake8-bugbear>=20.11.1,<21.0.0',
          'flake8-builtins>=1.5.3,<2.0.0',
          'flake8-comprehensions>=3.3.1,<4.0.0',
          'darglint>=1.6.0,<2.0.0',
          'flake8-docstrings>=1.5.0,<2.0.0',
          'flake8-eradicate>=1.0.0,<2.0.0',
          'flake8-mutable>=1.2.0,<2.0.0',
          'flake8-debugger>=4.0.0,<5.0.0',
          'flake8-pytest-style>=1.3.0,<2.0.0',
          'pep8-naming>=0.11.1,<0.12.0',
          'pylint>=2.6.0,<3.0.0'],
 'test': ['pytest>=6.2.2,<7.0.0',
          'pytest-cov>=2.11.1,<3.0.0',
          'pytest-html>=3.1.1,<4.0.0']}

entry_points = \
{'console_scripts': ['dry = drytoml.app:main']}

setup_kwargs = {
    'name': 'drytoml',
    'version': '0.1.2',
    'description': 'Keep toml configuration centralized and personalizable',
    'long_description': '# drytoml\n\nKeep toml configuration centralized and personalizable.\n\n`drytoml` enables having `.toml` files referencing any content from another `.toml`\nfile. You can reference the whole file, a specific table, or in general anything\nreachable by a sequence of `getitem` calls (eg `["tool", "poetry", "source", 0, "url"]`)\n\nInspired by `flakehell` and `nitpick`, drytoml main motivation is to have several\nprojects share a common, centralized configuration defining codestyles, but still\nallowing granular control wherever is required.\n\nIMPORTANT: if you want to manually control transclusions and modify files by hand, you\nshould use other tools, like [nitpick](https://pypi.org/project/nitpick/).\n\n## Usage\n\n`drytoml` has two main usages:\n\n1. Use a file as a reference to create an transcluded one:\n\n    ```toml\n    # contents of pyproject.dry.toml\n    ...\n    [tool.black]\n    __extends = "../../common/black.toml"\n    target-version = [\'py37\']\n    include = \'\\.pyi?$\'\n    include = \'\\.pyi?$\'\n    ...\n    ```\n\n    ```toml\n    # contents of ../../common/black.toml\n    [tool.black]\n    line-length = 100\n    ```\n\n   ```console\n   $ dry export --file=pyproject.dry.toml > pyproject.toml\n   ```\n\n    ```toml\n    # contents of pyproject.toml\n    [tool.black]\n    line-length = 100\n    target-version = [\'py37\']\n    include = \'\\.pyi?$\'\n    ```\n\n2. Use included wrappers, allowing you to use your current configuration\n\n   Instead of this:\n\n   ```console\n   $ black .\n   All done! ✨ 🍰 ✨\n   14 files left unchanged.\n   ```\n\n   You would run this\n   ```console\n   $ dry black\n   reformatted /path/to/cwd/file_with_potentially_long_lines.py\n   reformatted /path/to/cwd/another_file_with_potentially_long_lines.py\n   All done! ✨ 🍰 ✨\n   2 files reformatted, 12 files left unchanged.\n   ```\n\n\nTransclusion works with relative/absolute paths and urls. Internally\n`drytoml` uses [tomlkit](https://pypi.org/project/tomlkit/) to merge the\ncorresponding sections between the local and referenced `.toml`.\n\n\nFor the moment, the following wrappers are supported:\n\n* [x] [black](https://github.com/psf/black)\n* [x] [isort](https://pycqa.github.io/isort/)\n* [x] [flakehell, flake8helled](https://github.com/life4/flakehell) *\n* [ ] docformatter\n* [ ] pytest\n\n- NOTE: flakehell project was archived. This requires using a custom fork from\n  [here](https://github.com/pwoolvett/flakehell)\n- NOTE flakehell already implements similar funcionality, using a `base` key inside\n  `[tool.flakehell]`\n\n## Setup\n\n    Install as usual, with `pip`, `poetry`, etc:\n\n### Prerequisites\n\n### Install\n\n## Usage\n\n## FAQ\n\n**Q: I want to use a different key**\n\n   A: Use the `--key` flag (when using `dry` form cli, or initialize\n   `drytoml.parser.Parser` using the `extend_key` kwarg.\n\n\n**Q: I changed a referenced toml upstream (eg in github) but still get the same result.**\n\n   A: Run `dry cache clear --help` to see available options.\n\n## Contribute\n\n* Use the devcontainer, `act` command to run github actions locally\n* install locally with pip `pip install .[dev]` or poetry `poetry install -E dev`\n\n\n1. Create issue\n\n1. clone\n\n1. Setup Dev environment\n\n   * The easiest way is to use the provided devcontainer inside vscode, which already\n     contains everything pre-installed. You must open the cloned directory using the\n     [remote-containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).\n     Just run `poetry shell` or prepend any command with `poetry run` to ensure commands\n     run inside the virtual environment.\n\n   * Using poetry: `poetry install -E dev`\n\n   * Using pip (>20 recommended): `pip install .[dev]`\n\n   The next steps assume you have already activated the venv.\n\n1. Install pre-commit hook (skip if using devcontainer)\n\n   ```console\n   pre-commit install --hook-type commit-msg\n   ```\n\n   * Commits in every branch except those starting with `wip/` must be compliant to\n     [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/).\n\n   * Commit using `cz` to ensure compliance.\n\n1. Add tests to code\n\n1. Run check(s)\n\n\n   Useful tip: To debug your code, a useful tool is using `drytoml -v explain`\n\n   * Manually, executing the check from inside a venv\n\n     For example, to generate the documentation:\n  \n     ```console\n     sphinx-apidoc \\\n       --templatedir=docs/src/templates \\\n       --separate \\\n       --module-first \\\n       --force \\\n       -o docs/src/apidoc src/drytoml\n     ```\n\n     and then\n\n     ```console\n     sphinx-build docs/src docs/build\n     ```\n\n      See the different checks in `.github/workflows`\n\n   * Locally with [act](https://github.com/nektos/act) (Already installed in the\n     devcontainer)\n\n     For example, to emulate a PR run for the docs workflow:\n  \n     ```console\n     act -W .github/workflows/docs.yml pull_request\n     ```\n\n   * Remotely, by pushing to an open PR\n\n\n\n\n1. Create PR\n\n## TODO\n\ncheck out current development [here](https://github.com/pwoolvett/drytoml/projects/2)\n',
    'author': 'Pablo Woolvett',
    'author_email': 'pablowoolvett@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
