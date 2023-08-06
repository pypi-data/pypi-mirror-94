# plugin-foundation

This is a one-cli plugin to help create new DNX foundations.

![Build](https://github.com/DNXLabs/plugin-foundation/workflows/Build/badge.svg)
[![PyPI](https://badge.fury.io/py/one-cli-plugin-foundation.svg)](https://pypi.python.org/pypi/one-cli-plugin-foundation/)
[![LICENSE](https://img.shields.io/github/license/DNXLabs/plugin-foundation)](https://github.com/DNXLabs/plugin-foundation/blob/master/LICENSE)

## Configuration

```yaml
# one.yaml
required_version: ">= 0.7.1"

plugins:
  foundation:
    package: one-cli-plugin-foundation==0.0.1
    module: 'plugin_foundation'
```

## Usage

```bash
one foundation
```

## Development

#### Dependencies

- Python 3

#### Python Virtual Environment

```bash
# Create environment
python3 -m venv env

# To activate the environment
source env/bin/activate

# When you finish you can exit typing
deactivate
```

#### Install dependencies

```bash
pip3 install --editable .
```

## Author

Managed by [DNX Solutions](https://github.com/DNXLabs).

## License

Apache 2 Licensed. See [LICENSE](https://github.com/DNXLabs/plugin-foundation/blob/master/LICENSE) for full details.