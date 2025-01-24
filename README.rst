Open edX Filters Samples
########################

|ci-badge| |license-badge|

A ready-to-use repository illustrating how to use Open edX Filters to modify the behavior of the Open edX platform. It serves as a starting point for more advanced use cases. Explore `Real-Life Use Cases for Open edX Filters`_ to see more complex implementations from the Open edX Community.

.. _Real-Life Use Cases for Open edX Filters: https://docs.openedx.org/projects/openedx-filters/en/latest/reference/real-life-use-cases.html

Purpose
********

This repository demonstrates how to use Open edX Filters to modify the behavior of the Open edX platform. Filters are a powerful feature that allows developers to modify the behavior of the platform without directly changing the Open edX core. This can be useful for a variety of use cases, such as:

- Customizing the user experience
- Implementing custom business logic
- Etc.

Getting Started with Development
********************************

Please see the Open edX documentation for `guidance on Python development`_ in this repo.

.. _guidance on Python development: https://docs.openedx.org/en/latest/developers/how-tos/get-ready-for-python-dev.html

Deploying
*********

See the Usage section below for instructions on how to deploy this plugin. Also, see the `Tutor documentation`_ for more information on deploying extra requirements.

Getting Help
************

Documentation
=============

Refer to the `Open edX Filters documentation`_ to learn about implementing and working with filters. This documentation details how to use the repository as a testing tool for Open edX filters, they are not meant to be used in production environments.

You can review the rendered documentation at `https://edunext.github.io/openedx-filters-samples/`_.

Features
--------

- **Pipeline Steps**: Available pipeline steps are listed in the ``pipeline.py`` file.
- **Different Use Cases**: The repository includes a variety of use cases to illustrate how filters can be used.
- **Customizable**: Easily extend the repository to handle additional use cases.
- **Ready-to-Use**: Install the repository in your Open edX image and start using filters right away.

Supported Filters
-----------------

These are the filters that are currently supported in this repository: `Pipeline Steps <https://edunext.github.io/openedx-filters-samples/pipeline-steps.html>`_

How Does it Work?
-----------------

This repository provides a set of pipeline steps that can be used to modify the behavior of the Open edX platform. Each pipeline step is a Python class that implements a specific behavior. The pipeline steps are then added to the filter configuration in the Open edX settings which are later executed when the filter is triggered.

Usage
-----

To use this plugin, follow these steps:

1. Install the plugin in your Open edX image using Tutor's ``OPENEDX_EXTRA_PIP_REQUIREMENTS`` configuration setting:

.. code-block:: yaml

    OPENEDX_EXTRA_PIP_REQUIREMENTS:
    - git+https://github.com/edunext/openedx-filters-samples.git@X.Y.Z

2. Launch the Open edX platform to apply the changes:

.. code-block:: bash

     tutor local launch

3. Create and enable an Inline Tutor plugin to configure the filter you want to use. For example, to enable the ``StopEnrollment`` pipeline step for the ``org.openedx.learning.course.enrollment.started.v1`` filter, add the following code to the plugin:

.. code-block:: python

     # Location plugins/openedx-filters.py
     from tutor import hooks

     hooks.Filters.ENV_PATCHES.add_item(
         (
             "openedx-lms-common-settings",
     """
     OPEN_EDX_FILTERS_CONFIG = {
             "org.openedx.learning.course.enrollment.started.v1": {
                 "fail_silently": False,
                 "pipeline": [
                     "openedx_filters_samples.pipeline.StopEnrollment"
                 ]
             },
         }
     """
         )
     )

.. code-block:: bash

     tutor plugins enable openedx-filters

4. Trigger the filter by enrolling in a course. The filter will be applied and the pipeline step will be executed stopping the enrollment process.

How to Extend this Repository
-----------------------------

This repository is a starting point for Open edX developers:

- You can add new filter pipeline step by following the structure in `pipeline.py`_.
- Custom logic can be implemented in the pipeline step to test the behavior of the filter in the Open edX platform.

For details on extending Open edX with Open edX Filters, see also:

- `Open edX Filters Documentation`_
- `Hooks Extension Framework`_

The openedx-filters-samples repository is here to give developers the tools implement new filters and test them with pipeline steps in a safe environment.

More Help
=========

If you're having trouble, we have discussion forums at
https://discuss.openedx.org where you can connect with others in the
community.

Our real-time conversations are on Slack. You can request a `Slack
invitation`_, then join our `community Slack workspace`_.

For anything non-trivial, the best path is to open an issue in this
repository with as many details about the issue you are facing as you
can provide.

https://github.com/edunext/openedx-filters-samples/issues

For more information about these options, see the `Getting Help <https://openedx.org/getting-help>`__ page.

.. _Slack invitation: https://openedx.org/slack
.. _community Slack workspace: https://openedx.slack.com/

License
*******

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see `LICENSE.txt <LICENSE.txt>`_ for details.

Contributing
************

Contributions are very welcome.
Please read `How To Contribute <https://openedx.org/r/how-to-contribute>`_ for details.

This project is currently accepting all types of contributions, bug fixes,
security fixes, maintenance work, or new features.  However, please make sure
to discuss your new feature idea with the maintainers before beginning development
to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing
your idea.

The Open edX Code of Conduct
****************************

All community members are expected to follow the `Open edX Code of Conduct`_.

.. _Open edX Code of Conduct: https://openedx.org/code-of-conduct/

People
******

This repository is currently being maintained by the eduNEXT team. See the `CODEOWNERS <.github/CODEOWNERS>`_ file for details.

Reporting Security Issues
*************************

Please do not report security issues in public. Please email security@edunext.co.

.. _Hooks Extension Framework: https://open-edx-proposals.readthedocs.io/en/latest/oep-0050-hooks-extension-framework.html
.. _Open edX Filters Documentation: https://docs.openedx.org/projects/openedx-filters/en/latest/
.. _Tutor plugin: https://docs.tutor.edly.io/plugins/intro.html#plugins
.. _Tutor documentation: https://docs.tutor.edly.io/
.. _pipeline.py: openedx_filters_samples/pipeline.py

.. |ci-badge| image:: https://github.com/eduNEXT/openedx-filters-samples/workflows/Python%20CI/badge.svg?branch=main
    :target: https://github.com/eduNEXT/openedx-filters-samples/actions
    :alt: CI

.. |license-badge| image:: https://img.shields.io/github/license/eduNEXT/openedx-filters-samples.svg
    :target: https://github.com/eduNEXT/openedx-filters-samples/blob/main/LICENSE.txt
    :alt: License
