# Contributing to Pycecream


## Suggesting new features / Reporting An Issue

First, check to see if there's an existing issue/pull request for the
bug/feature. All issues are at https://github.com/dstarkey23/pycecream/issues and pull reqs are at
https://github.com/dstarkey23/pycecream/pull.

If there isn't an existing issue there, please file an issue. The
ideal report includes:

-  A description of the problem/suggestion.
-  How to recreate the bug (including the version on your python interpreter).
-  If possible, create a pull request with a (failing) test case
   demonstrating what's wrong. This makes the process for fixing bugs
   quicker & gets issues resolved sooner.

## Setting up your environment

First, clone the repo, then `cd` into the repo.

```bash
$ git@github.com:dstarkey23/pycecream.git
$ cd pycecream
```

create a new virtual environment
```bash
$ python3.7 -m venv venv
```

activate your environment
```bash
$ . venv/bin/activate
```

install the required dependencies
```
$ pip install -e .[tests]
```

run tests
```
$ python setup.py test
```

serve documentation
```bash
$ ./docs/serve_docs.sh
```
…and view the docs at http://localhost:8000 in your web browser.


:tada: Now you're ready to create a new branch, add a feature or fix a bug, then send us a pull request! :tada:

## Contributing Code

A good pull request:
-  Is clear.
-  Follows the existing style of the code base (PEP-8).
-  Has comments included as needed.
-  A test case that demonstrates the previous flaw that now passes with
   the included patch, or demonstrates the newly added feature.



## Style guide

#### Commit message formatting
We adopt the [Conventional Commits](https://www.conventionalcommits.org) convention to format commit messages.


#### Documentation
We're using [Pydocmd](https://github.com/NiklasRosenstein/pydoc-markdown)
to automatically generate docs.

Documentation should follow the [Google Documentation Style Guide](https://developers.google.com/style/api-reference-comments)

