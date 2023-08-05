build_harness
=============

A command line CI pipeline build harness utility for Python 3 projects based on known
best practices.

There are lots of accessories that are useful for establishing a high quality Python
pipeline and copy-pasting all the bits and pieces to initialize a new project is
tedious and error prone. This utility aims to streamline the creation of a project with
all the necessary development and pipeline dependencies and a ready to run pipeline.

**Why not just use CookieCutter?**

``build_harness`` complements the use of ``CookieCutter`` nicely - you can use
``build_harness`` to establish and maintain your Python project pipeline with minimal
effort and then focus on using ``CookieCutter`` to implement your business specific
customization of build, test and analysis options.

``build_harness`` also lends itself to being easily applied across multiple use cases,
from the pipeline itself, to ``pre-commit`` hooks, to developers manually running
specific components of the pipeline for test and debug.

.. contents::

.. section-numbering::


Installation
------------

The package is available from PyPI. Installing into a virtual environment is
recommended.

.. code-block::

   # A first time installation creating a virtual environment inside the project
   # directory
   cd my_project_repo
   python3 -m venv .venv; .venv/bin/pip install build_harness

Note that Ubuntu, for example, separates ``pip`` and ``venv`` installations from the
main Python installation and they are not installed by default, so if you are
working with a fresh Ubuntu install you will need something like this to acquire them.

.. code-block::

   sudo apt update && sudo apt install -y python3-pip python3-venv


Getting started
---------------

Installation makes a command line utility ``build-harness`` available in the virtual
environment. There are currently five groups of sub-commands available.

acceptance
   Run and manage Gherkin features and step files using the *behave* package.
formatting
   Format source code to PEP-8 standard using the *isort* and *black* packages.
install
   Install and manage project dependencies in the virtual environment. The install
   command will look for a virtual environment ``.venv`` in the project root directory
   and create it if needed. Then it installs and manages all the project dependencies
   there.
package
   Build wheel and sdist packages of the project.
publish
   Publish project artifacts to publication repositories such as PyPI and readthedocs.
static-analysis
   Run static analysis on source code; *pydocstyle*, *flake8* and *mypy* packages.
unit-test
   Run unit tests of the project using *pytest*.

Further options for these commands can be explored using the ``--help`` argument.

.. code-block::

   build-harness --help
   build-harness install --help

A quick summary of using each of the sub-commands.

.. code-block::

   # Install project dependencies into the virtual environment.
   build-harness install
   # Check if project dependencies are up to date in the virtual environment.
   build-harness install --check

.. code-block::

   # Format code to PEP-8 standards using isort, black.
   build-harness formatting
   # Fail (exit non-zero) if formatting needs to be applied.
   build-harness formatting --check

.. code-block::

   # Run pydocstyle, flake8 and mypy analysis on the project.
   build-harness static-analysis

.. code-block::

   # Run pytest on unit tests in the project.
   build-harness unit-test
   # Test that coverage passes the specified threshold.
   build-harness unit-test --check <int>

.. code-block::

   # Run Python behave on Gherkin based features.
   build-harness acceptance tests
   # Generate step file snippets for unimplemented features.
   build-harness acceptance snippets
   # Report where tags are used in feature files.
   build-harness acceptance tags


Concepts
--------

For now, the sub-commands are limited to a specific set of tools (the ones I have
found to be most useful).

Fine tuning configuration of the underlying tools is generally possible using
configuration files such as sections added to ``pyproject.toml`` or ``setup.cfg`` or
tool specific files in some cases.


Release Management
^^^^^^^^^^^^^^^^^^

Python has myriad ways of defining the release id of a project for publication and
almost all of them require some custom workflow from the user to make it work for
automation so it's really difficult to support all of them. For this reason the
default packaging option does nothing relating to the release id and assumes that
the user has done whatever is necessary for their workflow to correctly define the
release id for packaging.

There's a fairly useful survey of Python release control in the answers to this
`StackOverflow question <https://stackoverflow.com/questions/458550/standard-way-to-embed-version-into-python-package>`_.
The `setuptools_scm package <https://pypi.org/project/setuptools-scm/>`_ also has some
useful notes on different ways to control release id insertion to a package.

Having said that, the goal of this project is to have useful out-of-the-box
functionality as much as possible so described here are workflows that have been
integrated into the ``build_harness`` project.


VERSION file workflow
+++++++++++++++++++++

This is the workflow used by the ``build_harness`` project itself, so you can refer
to the source code for an example of how to implement this workflow.

* Install a simple text file named ``VERSION`` in the top-level Python package of
  your project.
* The file should be committed to source control with an acceptable "benign" release
  id that is readily identifiable as not a real release.
* The package reads the content of the VERSION file and applies it to the
  `__version__` variable in the package.
* Use the snippets below to set the Python ``__version__`` variable for the project
  from the content of the VERSION file.

Some Internet discussions on this topic recommend that the VERSION is not committed to
source control. The problem I have historically experienced is that this complicates the
local build because the developer must remember to create a useful "benign" VERSION
file for themselves otherwise their build will fail; if it's created locally and every
developer needs it, then why not just commit it to source control and avoid the
"toil"? If the pipeline somehow fails to update the VERSION file correctly, then at
least an invalid package is created with the benign release id that can be readily
identified as an error to fix.

The committed file should contain a default value that is readily recognisable as
having not been built by a pipeline. eg. If a developer builds the package locally it
should be clear that the package they built is not an official release (which should
only have been built by a pipeline).

A default value I have historically used is "0.0.0". Within the limitations defined
by PEP-440 another option could be "0.0.0+local".

For manual release definition you have to ensure that the content of the VERSION file
reflects the release id you are releasing. Doing this manually is error prone and
easily acquires a number of deficiencies with respect to how organizations often want
to organize their releases.

For automation the pipeline just needs to be able to update the content of the file
with the release id defined for a release; this is easily achieved by defining
semantic version tags on the repo (or some similar such rule that can be incorporated
into the pipeline code) as a formal release and having the pipeline update the
VERSION file with the tag text.

.. code-block::

   # top-level __init__.py
   """flit requires top-level docstring summary of project"""

   from ._version import acquire_version

   __version__ = acquire_version()

.. code-block::

   # _version.py
   import pathlib

   def acquire_version() -> str:
       """
       Acquire PEP-440 compliant version from VERSION file.

       Returns:
           Acquired version text.
       Raises:
           RuntimeError: If version is not valid.
       """
       here = pathlib.Path(__file__).parent
       version_file_path = (here / "VERSION").absolute()

       with open(version_file_path) as version_file:
           # Note that the release id is expected to be simple text;
           # no quotes, no comments, nothing in the file except the PEP-440 release id.
           version = version_file.read().strip()

       if not version:
           raise RuntimeError("Unable to acquire version")

       return version
