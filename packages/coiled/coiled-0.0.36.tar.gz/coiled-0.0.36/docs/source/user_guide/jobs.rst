:notoc:

====
Jobs
====

In addition to managing and deploying Dask clusters, Coiled also supports running
other Python applications. This allows you to run a Python script, nightly batch job,
or some other custom process on the cloud.

.. note::

   Coiled jobs are currently experimental with new features under active development

.. currentmodule:: coiled


Job configurations
------------------

Much like a :ref:`cluster configuration <cluster-config>` is a template for a Dask
cluster you can launch with Coiled, a **job configuration** is a template for some other
process, or job, you can launch with Coiled.

Job configurations are created with the :func:`coiled.create_job_configuration` function,
which takes several keyword arguments allowing you to specify details about your application,
as well as any software or hardware resources required by your application:

- ``name``: Name used to identify the job configuration.
- ``command``: Command to run as part of the job configuration.
- ``software``: Name of a :ref:`software environment <software-envs>` needed to run the ``command``.
- ``cpu``: Number of CPUs to allocate.
- ``memory``: Amount of memory to allocate.
- ``files``: Local files to upload for use in the job configuration
- ``ports``: List of any ports that the application exposes

.. note::

    Currently any directory structure for uploaded ``files`` will be removed and files
    will be placed in the working directory of the Jupyter session.
    For example, ``/path/to/my_app.py`` will appear as ``my_app.py`` in the
    running job configuration.

For example, below is a job configuration for running a custom ``my_app.py`` Python script:

.. code-block:: python

   import coiled

   # Create a software environment with the libraries needed
   # for this application
   coiled.create_software_environment(
       name="my-software-env",
       pip=["dask", "xarray", "numba"],
   )

   # Create a job configuration for a custom application.
   # Here the application consists of a "my_app.py" Python script.
   coiled.create_job_configuration(
       name="my-application",
       command=["python", "my_app.py"],
       software="my-software-env",
       cpu=4,
       memory="16 GiB",
       files=["my_app.py"],
       ports=[8888, 8889],
   )

Managing jobs
-------------

Once you've created a job configuration, you can then launch a **job**
which is a running instance of a job configuration. To launch a job,
use the :func:`coiled.start_job` function:

.. code-block:: python

   import coiled

   # Launch a job specified by the "my-application" job configuration
   coiled.start_job(configuration="my-application")

Additionally, you can get information about each on your running jobs
with the :func:`coiled.list_jobs` function:

.. code-block:: python

   # List all running jobs
   coiled.list_jobs()

This will output a dictionary whose keys are unique names for each
running job and whose values contain metadata related to the job
(e.g. what job configuration it's using):

.. code-block::

   {"job-27151b85-a": {"id": 195,
                       "account": ...,
                       "status": "running",
                       "configuration": "my-application"},
   }

If you need to terminate a running job you can use the :func:`coiled.stop_job`
function:

.. code-block:: python

   # Stop a running job
   coiled.stop_job(name="job-27151b85-a")
