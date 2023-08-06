===================
django-randomfields
===================

.. image:: https://github.com/thenewguy/django-randomfields/workflows/Build,%20Test,%20and%20Release%20sdist/badge.svg
    :target: https://github.com/thenewguy/django-randomfields/actions?query=workflow%3A%22Build%2C+Test%2C+and+Release+sdist%22

.. image:: https://ci.appveyor.com/api/projects/status/r8wtlr4lhfip4ukg/branch/master?svg=true
    :target: https://ci.appveyor.com/project/thenewguy/django-randomfields

.. image:: https://coveralls.io/repos/github/thenewguy/django-randomfields/badge.svg?branch=master
  :target: https://coveralls.io/github/thenewguy/django-randomfields?branch=master

.. image:: https://badge.fury.io/py/django-randomfields.svg
  :target: http://badge.fury.io/py/django-randomfields

============
testing
============

cd vagrant/
vagrant up
vagrant ssh
cd /vagrant/

# note we move TOX_WORK_DIR outside of the vagrant synced folder to increase performance
TOX_WORK_DIR=/tmp tox -vv

-- or test one environment and skip the coverage report --

SUPPRESS_COVERAGE_REPORT="--suppress-coverage-report" TOX_WORK_DIR="/tmp" tox -vv -e py36-django-20 

-- an example to run a specific test --

tox -e py36 -- -o randomfields.tests.test_string_fields.SaveTests.test_identifier_expected_val
ues_primary_key_by_fieldname
