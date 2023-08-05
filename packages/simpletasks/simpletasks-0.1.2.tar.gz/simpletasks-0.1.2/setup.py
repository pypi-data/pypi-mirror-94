# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpletasks']

package_data = \
{'': ['*']}

extras_require = \
{'click': ['click>=7.1.2,<8.0.0'], 'tqdm': ['tqdm>=4.54.1,<5.0.0']}

setup_kwargs = {
    'name': 'simpletasks',
    'version': '0.1.2',
    'description': 'A simple library to run one task, or multiples ones in sequence or parallel',
    'long_description': '# simpletasks\n\nSimple tasks runner for Python.\n\nThis can be helpful to handle automated processes and make them available via command line interface via [click](https://click.palletsprojects.com/).\n\n## Usage\n\nSample:\n\n```python\nimport click\nfrom simpletasks import Cli, CliParams, Task\n\n@click.group()\ndef cli():\n    pass\n\n@Cli(cli, params=[click.argument("n", type=int), CliParams.progress()])\nclass FibonacciTask(Task):\n    def compute(self, n: int) -> int:\n        self.logger.debug(f"Called with n={n}")\n        f1, f2 = 0, 1\n        if n == 0:\n            return f1\n        if n == 1:\n            return f2\n        for _ in self.progress(range(1, n)):\n            f1, f2 = f2, f1 + f2\n        return f2\n\n    def do(self) -> None:\n        n = cast(int, self.options.get("n"))\n        result = self.compute(n)\n        print(f"f({n}) = {result}")\n\nif __name__ == "__main__":\n    cli()\n```\n\nGives:\n```bash\n$ python sample/compute.py fibonacci 3 --no-progress\nf(3) = 2\n```\n\n## Contributing\n\nTo initialize the environment:\n```\npoetry install --no-root\npoetry install -E click -E tqdm\n```\n\nTo run tests (including linting and code formatting checks), please run:\n```\npoetry run pytest --mypy --flake8 && poetry run black --check .\n```\n',
    'author': 'Thomas Muguet',
    'author_email': 'thomas.muguet@upowa.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/upOwa/simpletasks',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
