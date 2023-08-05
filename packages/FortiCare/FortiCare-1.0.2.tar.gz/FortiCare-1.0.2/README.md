# Internal documentation

## Structure

There are two main directories:
- `FortiCare` : This is only the library (with supporting files)
- `FortiCareCli` : This is only the CLI utility (with supporting files)

To distribute with PyPI there are also two setup files, one for each "project":
- `setup-forticare.py`
- `setup-forticarecli.py`

Version number is shared and stored in file `VERSION` that is automatically loaded from each setup file.

There is also Makefile that currently contains following targets:
- `upload-test-forticare` : PyPI test: Prepare and upload PyPI files for FortiCare library
- `upload-test-forticarecli` : PyPI test: Prepare and upload PyPI files for CLI tool
- `upload-test` : PyPI test: Calls `upload-test-forticare` and `upload-test-forticarecli`

- `upload-production` Equivalent of previous for uploading to production PyPI repository (*Be carefull!*).

- `clean` : cleanup the directory from temporary upload files

## FortiCare library

This library is installed by `pip3` to standard directory where other modules are stored on the operating system.

It can be used by any tool by simply importing everything from the module:

```python
from FortiCare.FortiCare import *

fc = FortiCare("C93P-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX")
fc.GetAssets()
```

## FortiCareCli tool

This tool is now called `fccli` and is automatically installed by `pip3` to the directory from where it can be easily executed by user. It's been renamed to be more compliant with other installed programs (+ for some reason it cannot have the same name as the package (?) ).

`FortiCareCli` package forces the same version of the `FortiCare` library package when installing it using `pip3`.

## Development complications

Because of splitting the code between two different modules, it is now a little more complicated to develop on the local copy:

```
oho@local:~/APIteam/forticare-registration/FortiCareCli$ ./fccli
Traceback (most recent call last):
  File "/Users/oho/APIteam/forticare-registration/FortiCareCli/./fccli", line 9, in <module>
    from FortiCareCli import customLogging
ModuleNotFoundError: No module named 'FortiCareCli'
```

It can be workarounded by specifying the PYTHONPATH environment variable to point to the base directory of the Git repository:

```
oho@local:~/APIteam/forticare-registration/FortiCareCli$ export PYTHONPATH=~/APIteam/forticare-registration

oho@local:~/APIteam/forticare-registration/FortiCareCli$ ./fccli
usage: fccli [-h] [-v] [-u URL] [-p PROXY] (-c CONFIG_FILE | -t TOKEN) {download,registerunits,registervm,get,expire,list,description} ...
fccli: error: one of the arguments -c/--config -t/--token is required
```

There are no such problems on the target host when packages are installed via `pip3`.

## Uploading

To upload to PyPI there must be file `~/.pypirc` (Linux, MacOS) or `%HOME%\.pypirc` (Windows) with the right repository and access token:

```
[distutils]
index-servers =
    forticare-registration-test
    forticare-registration-production

[forticare-registration-test]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

[forticare-registration-production]
repository = https://upload.pypi.org/legacy/
username = __token__
password = pypi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

This is for test PyPI repository.

When uploading to the production repository, make sure to update `url` field in both setup files as well (at this moment there is no need for dedicated website, so we will keep everything on PyPI).
