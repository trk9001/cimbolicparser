# Cimbolic Language & Parser

[![Cimbolic package in CimbolicReleases@Release feed in Azure Artifacts][artifact-badge]][artifact-feed]
[![Azure Pipelines build status][build-badge]][build-status]
![Project status][status-badge]

[Cimbolic] is a custom mathematical language and parser library consisting of
variables and their associated formulae (pairs of conditions and arithmetic
rules). The project is under development in and by [Cimplux].

Other details:
- Project type: Reusable Django application
- Project starting date: 27 August 2019
- Contributors:
    - [A. G. M. Imam Hossain](mailto:imam.hossain@cimplux.com "Contact via e-mail")
    - [Sharif M. Tarik](mailto:s.tarik@cimplux.com "Contact via e-mail")


## Usage

### Setting up

1. Install the source distribution using `pip`.

2. Add Cimbolic to your `INSTALLED_APPS` in settings.py:

        INSTALLED_APPS = [
            # your other apps here
            'cimbolic',
        ]

3. Run `python manage.py migrate` to create the *Variable* and *Formula*
tables.

### Defining system variables

1. Create a file called cimbolicsysvars.py in your project's root directory
and add system variables to it as shown in the example file provided.

2. Run `python manage.py loadsysvars` to load the system variables into the
database.

3. For more info, please ask the contributors directly.

### Managing user-defined variables

1. For info, please ask the contributors directly.


## To be done

- [x] Set up versioning
- [ ] Write tests using `pytest` (see *pytest-django*)
- [x] Confirm stakeholders in README.md
- [x] Set up CI/CD and hosting
- [ ] Set up a git flow workflow
- [ ] Add docs


## Copyright

Copyright (c) 2019 [Cimplux]  
All rights reserved.


[artifact-badge]: https://feeds.dev.azure.com/Cimplux/_apis/public/Packaging/Feeds/b2509e07-88c2-45b0-9f25-79d1b9ca8675@7f465cf9-3d62-437d-8c61-d77d970a0b79/Packages/34a821e7-25bc-415b-8091-ef287e5a844c/Badge
[artifact-feed]: https://dev.azure.com/Cimplux/CimbolicParser/_packaging?_a=package&feed=b2509e07-88c2-45b0-9f25-79d1b9ca8675%407f465cf9-3d62-437d-8c61-d77d970a0b79&package=34a821e7-25bc-415b-8091-ef287e5a844c&preferRelease=true
[build-badge]: https://dev.azure.com/Cimplux/CimbolicParser/_apis/build/status/CimbolicParser?branchName=master
[build-status]: https://dev.azure.com/Cimplux/CimbolicParser/_build/latest?definitionId=1&branchName=master
[status-badge]: https://img.shields.io/badge/status-under_development-green.svg
[Cimbolic]: https://dev.azure.com/Cimplux/CimbolicParser "View the repository on Azure DevOps"
[Cimplux]: http://www.cimplux.com "Visit the Cimplux homepage"
