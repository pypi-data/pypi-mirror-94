# Typed Settings

[![PyPI](https://img.shields.io/pypi/v/typed-settings)](https://pypi.org/project/typed-settings/)
[![PyPI - License](https://img.shields.io/pypi/l/typed-settings)](https://pypi.org/project/typed-settings/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/typed-settings)](https://pypi.org/project/typed-settings/)
[![Documentation Status](https://readthedocs.org/projects/typed-settings/badge/?version=latest)](https://typed-settings.readthedocs.io/en/latest/?badge=latest)
[![Gitlab pipeline status](https://img.shields.io/gitlab/pipeline/sscherfke/typed-settings/main)](https://gitlab.com/sscherfke/typed-settings/-/pipelines/charts)
[![Gitlab code coverage](https://img.shields.io/gitlab/coverage/sscherfke/typed-settings/main)](https://gitlab.com/sscherfke/typed-settings/-/graphs/main/charts)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Typed Settings allows you to cleanly structure your settings with [attrs](https://www.attrs.org) classes.
Type annotations will be used to automatically convert values to the proper type.
You can currently load settings from these sources:

- TOML files (multiple, if you want to).  Paths can be statically specified or dynamically set via an environment variable.
- Environment variables
- [click](https://click.palletsprojects.com) command line options

You can use Typed settings, e.g., for

- server processes
- containerized apps
- command line applications

The documentation contains a [full list](https://typed-settings.readthedocs.io/en/latest/why.html#comprehensive-list-of-features) of all features.


## Installation

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

```console
$ python -m pip install typed-settings
```

## Examples

### Hello, World!, with env. vars.

This is a very simple example that demonstrates how you can load settings from environment variables.

```python
# example.py
import typed_settings as ts

@ts.settings
class Settings:
    option: str

settings = ts.load_settings(cls=Settings, appname="example")
print(settings)
```

```console
$ EXAMPLE_OPTION="Hello, World!" python example.py
Settings(option='Hello, World!')
```


### Nested classes and config files

Settings classes can be nested.
Config files define a different section for each class.

```python
# example.py
import click

import typed_settings as ts

@ts.settings
class Host:
    name: str
    port: int = ts.option(converter=int)

@ts.settings(kw_only=True)
class Settings:
    host: Host
    endpoint: str
    retries: int = 3

settings = ts.load_settings(
    cls=Settings, appname='example', config_files=['settings.toml']
)
print(settings)
```

```toml
# settings.toml
[example]
endpoint = "/spam"

[example.host]
name = "example.com"
port = 443
```

```console
$ python example.py
Settings(host=Host(name='example.com', port=443), endpoint='/spam', retries=3)
```


### Click

Optionally, click options can be generated for each option.  Config files and environment variables will still be read and can be overriden by passing command line options.


```python
# example.py
import click
import typed_settings as ts

@ts.settings
class Settings:
    a_str: str = "default"
    an_int: int = 3

@click.command()
@ts.click_options(Settings, 'example')
def main(settings):
    print(settings)

if __name__ == '__main__':
    main()
```

```console
$ python example.py --help
Usage: example.py [OPTIONS]

Options:
  --a-str TEXT      [default: default]
  --an-int INTEGER  [default: 3]
  --help            Show this message and exit.
$ python example.py --a-str=spam --an-int=1
Settings(a_str='spam', an_int=1)
```


## Features

- Settings are defined as type-hinted `attrs` classes.

- Typed Settings’ `settings` decorator adds automatic type converstion for option values and makes your settings class frozen (immutable) by default.

- Settings can currently be loaded from:

  - TOML files
  - Environment variables
  - click Commaoptions

- Paths to settings files can be “hard-coded” into your code or specified via an environment variable.

- Order of precedence:

  - Default value from settings class
  - First file from hard-coded config files list
  - ...
  - Last file from hard-coded config files list
  - First file from config files env var
  - ...
  - Last file from config files env var
  - Environment variable `{PREFIX}_{SETTING_NAME}`
  - (Value passed to Click option)

- Config files are “optional” by default – no error is raised if a specified file does not exist.

- Config files can be marked as mandatory by prefixing them with an `!`.
