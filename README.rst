openedx-filters-samples
=============================

|ci-badge| |license-badge|


Overview
---------

Used to create Open edX Filters steps for testing purposes.


Open edX Filters Steps
----------------------

+-------------------------------------+
| Filter steps                        |
+=====================================+
| `ModifyUsernameBeforeRegistration`_ |
+-------------------------------------+
| `ModifyUserProfileBeforeLogin`_     |
+-------------------------------------+
| `ModifyModeBeforeEnrollment`_       |
+-------------------------------------+
| `NoopFilter`_                       |
+-------------------------------------+
| `StopEnrollment`_                   |
+-------------------------------------+
| `StopRegister`_                     |
+-------------------------------------+
| `StopLogin`_                        |
+-------------------------------------+

Development Workflow
--------------------

One Time Setup
~~~~~~~~~~~~~~
.. code-block:: bash

  # Clone the repository
  git clone git@github.com:edx/openedx-filters-samples.git
  cd openedx-filters-samples

  virtualenv -p python3.8 openedx-filters-samples


Every time you develop something in this repo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. code-block:: bash

  # Activate the virtualenv
  source venv/bin/activate

  # Grab the latest code
  git checkout main
  git pull

  # Install/update the dev requirements
  make requirements

  # Run the tests and quality checks (to verify the status before you make any changes)
  make validate

  # Make a new branch for your changes
  git checkout -b <your_github_username>/<short_description>

  # Using your favorite editor, edit the code to make your change.
  vim …

  # Run your new tests
  pytest ./path/to/new/tests

  # Run all the tests and quality checks
  make validate

  # Commit all your changes
  git commit …
  git push

  # Open a PR and ask for review.

License
-------

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.


.. |ci-badge| image:: https://github.com/eduNEXT/openedx-filters-samples/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/eduNEXT/openedx-filters-samples/actions
    :alt: CI

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/openedx-filters-samples.svg
    :target: https://github.com/eduNEXT/openedx-filters-samples/blob/main/LICENSE.txt
    :alt: License

.. _ModifyUsernameBeforeRegistration: https://github.com/eduNEXT/openedx-filters-samples/blob/b7e6e32c577df9e107081bb4835bd48ccd808dfd/openedx_filters_samples/samples/pipeline.py#L16
.. _ModifyUserProfileBeforeLogin: https://github.com/eduNEXT/openedx-filters-samples/blob/b7e6e32c577df9e107081bb4835bd48ccd808dfd/openedx_filters_samples/samples/pipeline.py#L41
.. _ModifyModeBeforeEnrollment: https://github.com/eduNEXT/openedx-filters-samples/blob/b7e6e32c577df9e107081bb4835bd48ccd808dfd/openedx_filters_samples/samples/pipeline.py#L63
.. _NoopFilter: https://github.com/eduNEXT/openedx-filters-samples/blob/b7e6e32c577df9e107081bb4835bd48ccd808dfd/openedx_filters_samples/samples/pipeline.py#L86
.. _StopEnrollment: https://github.com/eduNEXT/openedx-filters-samples/blob/b7e6e32c577df9e107081bb4835bd48ccd808dfd/openedx_filters_samples/samples/pipeline.py#L108
.. _StopRegister: https://github.com/eduNEXT/openedx-filters-samples/blob/b7e6e32c577df9e107081bb4835bd48ccd808dfd/openedx_filters_samples/samples/pipeline.py#L130
.. _StopLogin: https://github.com/eduNEXT/openedx-filters-samples/blob/b7e6e32c577df9e107081bb4835bd48ccd808dfd/openedx_filters_samples/samples/pipeline.py#L152
