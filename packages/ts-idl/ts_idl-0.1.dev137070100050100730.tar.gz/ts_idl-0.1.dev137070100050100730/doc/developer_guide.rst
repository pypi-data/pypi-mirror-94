.. py:currentmodule:: lsst.ts.idl

.. _lsst.ts.idl.developer_guide:

###############
Developer Guide
###############

Developers are expected to manually maintain the Python enumeration modules in ``lsst.ts.idl.enums``,
updating them as the enumerations in ``ts_xml`` are updated.

Build and Test
==============

This is a pure python package.
You can build IDL files (see the :ref:`user guide <lsst.ts.idl.user_guide>` for instructions), run unit tests and build documentation.

.. code-block:: bash

    setup -r .
    pytest -v  # to run tests
    package-docs clean; package-docs build  # to build the documentation

Contributing
============

``ts_idl`` is developed at https://github.com/lsst-ts/ts_idl.
You can find Jira issues for this package using `labels=ts_idl <https://jira.lsstcorp.org/issues/?jql=project%20%3D%20DM%20AND%20labels%20%20%3D%20ts_idl>`_..
