# Preacher: Web API Verification without Coding

[![PyPI version](https://badge.fury.io/py/preacher.svg)][PyPI]
[![Documentation Status](https://readthedocs.org/projects/preacher/badge/?version=latest)][Read the Docs]
[![CircleCI](https://circleci.com/gh/ymoch/preacher.svg?style=svg)][Circle CI]
[![Codecov](https://codecov.io/gh/ymoch/preacher/branch/master/graph/badge.svg)][Codecov]
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ymoch/preacher.svg?logo=lgtm&logoWidth=18)][LGTM]

Preacher verifies API servers,
which requests to the servers and verify the responses along to given scenarios.

Test scenarios are written only in [YAML][] declaratively, without coding.
In spite of that, Preacher can validate your web API flexibly,
which enables you to test using real (neither mocks nor sandboxes) backends.

- Responses are analyzed [jq][] or [XPath][] queries
- Validation rules are based on [Hamcrest][] (implemented by [PyHamcrest][]).

The full documentation is available at [preacher.readthedocs.io][Read the Docs].

## Targets

- Flexible validation to test with real backends: neither mocks nor sandboxes.
  - Matcher-based validation.
- CI Friendly to automate easily.
  - A CLI application and YAML-based scenarios.

## Usage

First, install Preacher.

The most basic way to install Preacher is using `pip`. Supports only Python 3.7+.

```sh
$ pip install preacher
$ preacher-cli --version
```

Instead of `pip`, Docker images are also available on
[Docker Hub](https://hub.docker.com/r/ymoch/preacher)
as `ymoch/preacher`.
By default, the container working directory is `/work`,
and the host directory may be mounted here.

```sh
$ docker pull ymock/preacher
$ docker run -v $PWD:/work ymoch/preacher preacher-cli --version
```

Second, write your own scenario.

```yaml
# scenario.yml
label: An example of a scenario
cases:
  - label: An example of a case
    request: /path/to/foo
    response:
      status_code: 200
      body:
        - describe: .foo
          should:
            equal: bar
```

Then, run ``preacher-cli`` command.

```sh
$ preacher-cli -u http://your.domain.com/base scenario.yml
```

For more information such as grammer of scenarios,
see [the full documentation][Read the Docs].

## License

[![MIT License](https://img.shields.io/badge/License-MIT-brightgreen.svg)][MIT License]

Copyright (c) 2019 Yu MOCHIZUKI


[YAML]: https://yaml.org/
[jq]: https://stedolan.github.io/jq/
[XPath]: https://www.w3.org/TR/xpath/all/
[Hamcrest]: http://hamcrest.org/
[PyHamcrest]: https://pyhamcrest.readthedocs.io/
[MIT License]: https://opensource.org/licenses/MIT

[Read the Docs]: https://preacher.readthedocs.io/
[PyPI]: https://badge.fury.io/py/preacher
[Circle CI]: https://circleci.com/gh/ymoch/preacher
[Codecov]: https://codecov.io/gh/ymoch/preacher
[LGTM]: https://lgtm.com/projects/g/ymoch/preacher/context:python
