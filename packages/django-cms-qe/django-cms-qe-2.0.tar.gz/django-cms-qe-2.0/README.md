# Django CMS QE

Django CMS Quick & Easy provides all important modules to run new page
without a lot of coding. Aims to do it very easily and securely.

For more information please read [documentation](<https://websites.pages.nic.cz/django-cms-qe>) or [GitLab](https://gitlab.nic.cz/websites/django-cms-qe).

## Development

To prepare your dev envrionment run this command:

    make prepare-dev  (run with apt get update)
    make prepare-env

To run tests or lint use this commands:

    make test
    make lint

To run only particular test:

    make test=cms_qe_table/tests/test_utils.py test

To run example use this command:

    make run-example


To call other Django commands:

    make cmd  (List django commands, same like --help)
    make cmd=dbshell cmd
    make cmd='createsuperuser --username=dave --email=dave@rd.foo' cmd

To find more useful commands, run just `make`.
