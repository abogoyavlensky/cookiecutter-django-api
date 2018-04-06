# {{cookiecutter.project_name}}

## Requirements

* Python 3.6.4
* Django 2.x
* Django rest framework 3.8

## Local developemnt using Docker

Before you start please install docker and docker-compose on the host.
Then you could perfom serveral command using `make`:

```bash
$ make build
$ make detach [service]  # now you could open http://localhost:8000/
$ make logs [service]
$ make stop
```

To run tests, check linting you have next command:
```bash
$ make test api  # Run test and recreate db every time
$ make watch api # Run tests in watching mode using already created db
$ make fmt api # Autoformatting and linting source code
```

All available commands you could check at running:

```bash
$ make help
```

## Install git-hook on pre-commit

To install git-hook you should install python package `pre-commit`
(https://pre-commit.com/) and run it locally:

```bash
$ pip install pre-commit
$ pre-commit install
```
