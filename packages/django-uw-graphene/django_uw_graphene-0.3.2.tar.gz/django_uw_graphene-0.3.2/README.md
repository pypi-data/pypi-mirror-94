# Django UW Graphene
[![Built with Spacemacs](https://cdn.rawgit.com/syl20bnr/spacemacs/442d025779da2f62fc86c2082703697714db6514/assets/spacemacs-badge.svg)](http://spacemacs.org)

## Description

This package extends the [graphene-django](https://github.com/graphql-python/graphene-django) interface for a streamlined query and mutation integration.

## Installation

1. Install: `pip install django-uw-graphene`
2. add to INSTALLED_APPS:
```python
    INSTALLED_APPS = [
        ...
        'uw_graphene',
    ]
```

## Details

Some API design decisions:
  * Based on [Relay](https://relay.dev/)
  * [`totalCount` was implemented as an ExtendedConnection](docs/index.md#queries)
  * A base interface for CRUD mutations was implemented:
    * [GlobalId to Instance "auto fetching", including custom resolvers](docs/index.md#globalid-to-instance-auto-fetching)
    * [Null value handling](docs/index.md#null-value-handling) 
    * [Custom error handling](docs/index.md#error-handling)

## Documentation

This library is intended to be used on top of [graphene-django](https://github.com/graphql-python/graphene-django), here are some useful links:
  * [graphene-django](https://docs.graphene-python.org/projects/django/en/latest/)
  * [graphene](https://docs.graphene-python.org/en/latest/)
  * [Relay](https://relay.dev/docs/en/graphql-server-specification.html)

A More extensive documentation is available [here](docs/index.md).

## TODO
  * [ ] Review `test_utils`
