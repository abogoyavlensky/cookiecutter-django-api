Django API boilerplate
===

## Requirements

- Python==3.6
- Django==2.x
- Django REST Framework==3.8

## Features

- `Docker Compose` local setup with minimal `docker`-image
- `Celery` with `Flower` configuration included
- Convenient `make`-commands to manage the project
- Fast testing `Gitlab CI` pipeline by default
- Testing with `py.test` and `django-dynamic-fixture`
- Checking lint, types and complexity with auto formatting
- Built-in API doc and `JWT`-auth by default
- Ability to generate actual db graph
- `django-debug-toolbar` and `django-silk` configured

## Installation

First of all, you need to install `cookiecutter` python package. And then
just run it pointed to the repository:

```bash
$ pip install cookiecutter
$ cookiecutter gh:abogoyavlensky/cookiecutter-django-api
```

Now, your project has been configured and ready for further development:

```bash
$ cd <project_name>
$ make help
$ make build
$ make detach
$ make manage createsuperuser
```

## Inspired by

- https://github.com/pydanny/cookiecutter-django
- https://github.com/wemake-services/wemake-django-template
- https://github.com/agconti/cookiecutter-django-rest
- https://github.com/ghrecommender/ghrecommender-backend
- https://github.com/github/scripts-to-rule-them-all


# TODO:

- [ ] Production build and CD
- [ ] Testing coverage up to 100%
- [ ] Use `django-configurations`
- [ ] Improve readme
- [ ] Add ability to choose between REST and GraphQL
