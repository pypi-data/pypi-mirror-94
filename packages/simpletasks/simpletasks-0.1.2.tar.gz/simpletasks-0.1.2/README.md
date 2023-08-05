# simpletasks

Simple tasks runner for Python.

This can be helpful to handle automated processes and make them available via command line interface via [click](https://click.palletsprojects.com/).

## Usage

Sample:

```python
import click
from simpletasks import Cli, CliParams, Task

@click.group()
def cli():
    pass

@Cli(cli, params=[click.argument("n", type=int), CliParams.progress()])
class FibonacciTask(Task):
    def compute(self, n: int) -> int:
        self.logger.debug(f"Called with n={n}")
        f1, f2 = 0, 1
        if n == 0:
            return f1
        if n == 1:
            return f2
        for _ in self.progress(range(1, n)):
            f1, f2 = f2, f1 + f2
        return f2

    def do(self) -> None:
        n = cast(int, self.options.get("n"))
        result = self.compute(n)
        print(f"f({n}) = {result}")

if __name__ == "__main__":
    cli()
```

Gives:
```bash
$ python sample/compute.py fibonacci 3 --no-progress
f(3) = 2
```

## Contributing

To initialize the environment:
```
poetry install --no-root
poetry install -E click -E tqdm
```

To run tests (including linting and code formatting checks), please run:
```
poetry run pytest --mypy --flake8 && poetry run black --check .
```
