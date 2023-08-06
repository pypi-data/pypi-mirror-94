# Changelog #

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] ##

### Added ###

### Changed ###

### Deprecated ###

### Removed ###

### Fixed ###

### Security ###

## [0.4.1] 2021-02-10 ##

### Added ###

* Versioning support (experimental). The version db.Version class can
  represents particular entity versions and also the complete history of an
  entity.
* Automated documentation builds: `make doc`

### Changed ###

### Deprecated ###

### Removed ###

### Fixed ###

* deepcopy of `_Messages` objects

### Security ###

## [0.4.0] - 2020-07-17##

### Added ###

* `[Entity|Container].get_property_values` for deeply nested references, e.g.
  from results of SELECT queries.
* two new `password_method`s for the `pycaosdb.ini` and the
  `configure_connection` function: `unauthenticated` for staying
  unauthenticated (and using the anonymous user) and `auth_token`. If
  `password_method == "auth_token"` the `auth_token` option is required as
  well.
* Empty string support (See caosdb-server#33)

### Changed ###

* `get_property` method also accepts instances of properties now, e.g.
  `record.get_property(Property(name="length"))`
* the value of properties is parsed to python types (int, float, boolean) when
  setting the value with the setter and when the datatype changes. Before this
  change, the value was parsed to python types only when parsing an xml and
  only for int and float.

### Deprecated ###

* Setting the `auth_token` option without setting the `password_method` to
  `auth_token`. This affects both the `pycaosdb.ini` and the
  `configure_connection` function. During the deprecation phase it will be
  assumed that `password_method` is `auth_token` if the the `auth_token` is
  set.

### Removed ###

### Fixed ###

- Replaced deprecated Logger.warn() method.

### Security ###

## [0.3.0] - 2020-04-24##

### Added ###

* `apiutils.apply_to_ids` -- a helper which applies a function to all ids which
  are used by an entity (own entity, parents, properties, references etc.).

### Changed ###

### Deprecated ###

### Fixed ###

* import bugs in apiutils

## [0.2.4] -- 2020-04-23

### Added

- An `auth_token` parameter for `caosdb.configure_connection(...)`. This
  parameter accepts a plain text auth token (which can only be issued by the
  CaosDB Server). Under the hood, auth tokens are stored plain, instead of
  urlencoded now.
- New type of exception: `ConfigurationException` for misconfigurations.
- Some unit tests, mainly for the `caosdb.connection.authentication` module
- Advanced setup.py for easy versioning and publication as pypi repository.
- `caosdb.apiutils` has new functions `id_query` and
  `retrieve_entities_with_ids`
- New exception: `EntityDoesNotExistError`
- `RELEASE_GUIDELINES.md` with release instructions.
- More documentation and tests.

### Changed

- [pytest](https://docs.pytest.org/en/latest/) is the new preferred unit test
  frame work.
- If a password is specified in the configuration even though the
  password_method is not set to `plain`, a warning is logged.
- Under the hood, the password of from a `pass` or `keyring` call is not stored
  anymore. Instead the password is requested each time a login is necessary.
- Always load system default CA repository into the ssl context.
- Datatypes are now in `caosdb.common.datatype` (though still available in the
  main `caosdb` namespace).
- Logging to stdout is now more configurable.

### Deprecated

- Unit test frame work: [Nose](https://nose.readthedocs.io/en/latest/) should
  not be used anymore. Please use [pytest](https://docs.pytest.org/en/latest/)
  instead.

### Fixed

- #1 - Problems with pass as a credentials provider
- #3 - Python client does login before the first request to circumvent problems
  with anonymous role.
- Many other fixes


## [0.1.0] - 2018-10-09 ##

Tag `v0.1` - Commit 6fc0dcaa


### Added
- everything
