Cimbolic Language & Parser
==========================

.. image:: https://img.shields.io/badge/status-under_development-green.svg

Custom mathematical language and parser library developed in and by
Cimplux_. Project started on 27th August 2019 by A. G. M. Imam Hossain
(imam.hossain@cimplux.com) and Sharif M. Tarik (s.tarik@cimplux.com).

Usage
-----

1.  Add "cimbolic" to your INSTALLED_APPS setting like this::

        INSTALLED_APPS = [
            ...
            'cimbolic',
        ]

2.  Run `python manage.py migrate` to create the *Variable* and *Formula*
    models.

3.  Create a file called *cimbolicsysvars.py* in your project's root directory
    and add system variables to it as shown in the example file provided.

4.  Run `python manage.py loadsysvars` to load the system variables into the
    datebase.

5.  For more info, ask Tarik or Imam.

Copyright
---------

Copyright (c) 2019 Cimplux_

All rights reserved.


.. _Cimplux: http://www.cimplux.com/
