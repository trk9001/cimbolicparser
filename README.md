# Cimbolic Language & Parser

![Project status][status-badge]

[Cimbolic] is a custom mathematical language and parser library consisting of
variables and their associated formulae (pairs of conditions and arithmetic
rules). The project is under development in and by [Cimplux].

Other details:
- Project type: Reusable Django application
- Project starting date: 27 August 2019
- Stakeholders:
    - [Raihan Ahmed Dip](mailto:raihan.dip@cimplux.com "Contact via e-mail")
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

- [ ] Set up versioning
- [ ] Write tests using `pytest` (see *pytest-django*)
- [ ] Confirm stakeholders in README.md
- [ ] Set up CI/CD and hosting


## Copyright

Copyright (c) 2019 [Cimplux]  
All rights reserved.


[status-badge]: https://img.shields.io/badge/status-under_development-green.svg
[Cimbolic]: https://dev.azure.com/Cimplux/CimbolicParser "View the repository on Azure DevOps"
[Cimplux]: http://www.cimplux.com "Visit the Cimplux homepage"
