# Changelog

All notable changes to the Cimbolic project will be documented in this file.
This project uses [semantic versioning](https://semver.org/). The format of the
changelog is adapted from [Keep a Changelog](https://keepachangelog.com/).

## Unreleased

### Added
- A custom Django management command to list all the context keyword argument
names needed by specified variables.
- Support for context passing in the core parsing component.
- Support for context propagation in the Django models.
- This changelog. :)

### Changed
- API-breaking changes to system-sourced variable processing.
  - Changed the file name of cimbolicsysvars.py to cimbolic_vars.py.
  - Replaced all instances of "system-defined variables" (old terminology) with
  "system-sourced variables" (new terminology).
  - Accordingly, rename a few things and update their references.
- The Cimbolic language is now case-insensitive (except for variable names).
- The `source_model` field in the Variable model has been changed to a more
accurate `related_data_path` and added more processing for it.
- The management command `removeinactivevars` has been renamed to `flushvars`.
- Corrections in help texts and docstrings.

### Fixed
- Context getting lost during parsing of `named_variable` tokens.
- Index errors on MySQL due to large text fields.
