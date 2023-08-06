# terra-pandas
Import and export Terra data tables to Pandas DataFrames.

## Installation

From the CLI:
```
pip install terra-pandas
```

In a Jupyter notebook (note the ipython magic "[%pip](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-pip)"):
```
%pip install terra-pandas
```

## Upgrading

It is often useful to keep up to date with new features and bug fixes. Installing the latest version of
terra-pandas depends on your host environment.

From any Jupyter notebook, use the following (and note the leading "%")
```
%pip install --upgrade --no-cache-dir terra-pandas
```

From the CLI on standard Terra notebook runtimes, which are available using the terminal button in the Terra user
interface, use
```
/usr/local/bin/pip install --upgrade --no-cache-dir terra-pandas
```
Note that all standard notebook runtimes on Terra are based on
[this Docker image](https://github.com/databiosphere/terra-docker#terra-base-images).

For other environments, it is often enough to do
```
pip install --upgrade --no-cache-dir terra-pandas
```

## Credentials
Much of the terra-pandas functionality requires credentialed access through a Google Cloud Platform account.
Credentials are already available when running in a Terra notebook environment. Otherwise, credentials may be obtained
with the command
```
gcloud auth application-default login
```

## Tests

## Release
The commands mentioned in `common.mk` file are used for the release process.
Steps:
- if you don't have a [PyPI](https://pypi.org/) account, please create one
- you should be a collaborator in PyPI for Terra Notebook Utils. If you are not, please ask Brian Hannafious to add
you as a collaborator
- follow the setup instructions as mentioned in `Tests` section above for env Prod; make sure you have access
to the DRS urls, workspaces and buckets
- run `make all_test` from inside the docker container created in `Local Development` section.
Once tests pass, you can move to the release step
- Release:
    - For non-breaking API changes, use `make release_patch`
    - For breaking API changes, use `make release_minor`
    - For a major release, use `make release_major`

If a release needs to be rolled back for some reason, please contact Brian Hannafious for help.

## Links
Project home page [GitHub](https://github.com/xbrianh/terra-pandas)
Package distribution [PyPI](https://pypi.org/project/terra-pandas)

### Bugs
Please report bugs, issues, feature requests, etc. on [GitHub](https://github.com/xbrianh/terra-pandas).
