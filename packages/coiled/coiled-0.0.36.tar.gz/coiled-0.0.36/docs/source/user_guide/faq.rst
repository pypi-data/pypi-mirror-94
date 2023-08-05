:notoc:

===
FAQ
===

.. dropdown:: How do I access my data?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    You can access many different file formats using Dask and related libraries.

    -   `Tabular data <https://docs.dask.org/en/latest/dataframe-create.html>`_
    -   `Array data <https://docs.dask.org/en/latest/array-creation.html>`_
    -   `Text data <https://docs.dask.org/en/latest/bag-creation.html>`_

    Large datasets should live on the cloud in services like S3 to avoid data
    transmission costs.

    Additionally, if you have small data locally you can use other Dask APIs, like
    Dask-ML or Dask Futures to do heavy computation on small datasets comfortably.


.. dropdown:: How do I install libraries into my Coiled clusters?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled helps you manage software environments both on your local machine
    and on cloud resources.  You can specify custom environments with conda or pip
    environments files with the ``coiled.create_software_environment`` function and
    Coiled will manage building Docker images for you that can then be used in Dask
    clusters or other jobs on the cloud.

    See :doc:`software_environment` for more information.


.. dropdown:: Can I run computation in my own cloud account?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes.  Coiled accounts run by default in our hosted AWS account, but for
    pricing or security reasons you may prefer to run things on your own
    account.

    See :doc:`backends` for more information.


.. dropdown:: Do I have to migrate my data to Coiled?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    No.  Your data stays in its native location(s).
    Coiled manages computation.  Coiled helps you get data from your existing data stores,
    process it, and write out to those same data stores.


.. dropdown:: Can I use Coiled to read private data on AWS?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes.  If you create a Coiled cluster from a location that has AWS credentials
    then Coiled will generate a secure token from those credentials and forward it
    to your Dask workers.  Your Dask workers will have the same rights and
    permissions that you have by default.

    Alternatively, for additional control Coiled can be deployed within your own AWS
    account and allow you to specify and manage IAM roles directly.

    See :doc:`security` for more information.


.. dropdown:: Is my computation and data secure?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled provides end-to-end network security with both cloud networking policies
    and with TLS encryption.  Coiled does not persist or store any of your data,
    except in memory as you are doing computations.

    You can also use Coiled to manage computation in your own account or on
    your own hardware (see the next question below)

    See :doc:`security` for more information.


.. dropdown:: How much does Coiled cost?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Coiled is currently in beta. During this time **Coiled is free for all beta users**.

    You will not be charged for any of the compute resources you use, however there is a limit of
    100 concurrently running cores per user. This policy will change in the future when Coiled is opened
    up to a broader audience, but until then we are happy to provide beta users cloud computing
    resources at no cost. Thank you for trying out Coiled!

    For more information on pricing, see `coiled.io/pricing
    <https://coiled.io/pricing>`_


.. dropdown:: Does Coiled support other clouds?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Today Coiled provides full support for AWS with GCP and Azure in the works
    (we're aiming for Q2 2021).
    In the meantime, you can set up your own Kubernetes cluster on GKE or AKS
    and have Coiled manage that.


.. dropdown:: How can I report a feature request, bug, etc?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Please `open an issue <https://github.com/coiled/feedback/issues/new>`_ on the
    `Coiled issue tracker <https://github.com/coiled/feedback>`_. Feel free to report bugs, submit
    feature requests, ask questions, or provide other input. Your feedback is valued and will help influence
    the future of Coiled.

    For generic questions, please join our `Coiled Community Slack <https://join.slack.com/t/coiled-users/shared_invite/zt-hx1fnr7k-In~Q8ui3XkQfvQon0yN5WQ>`_ where you can ask questions and interact with our engineers and with the Coiled community.


.. dropdown:: How do I invite my colleagues / students / ...?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    We're glad that you're having a good time and want to invite colleagues or
    students.  Coiled is currently open access, so your colleagues can join
    without any special setup.

    Additionally, if you want to organize a team account send a quick e-mail to
    hello@coiled.io with a team name and we'll set you up as an administrator
    over your new team.

    See :doc:`teams` for more information.


.. dropdown:: Why do I get Version Mismatch warnings?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    When running cloud computations from your local machine we need to ensure some
    level of consistency between your local and remote environments.  For example
    your Python versions should match, and if you want to use a library like
    PyTorch or Pandas remotely we should probably also install it locally.  When
    Dask notices a mismatch, it will tell you with a warning.

    Matching versions can be challenging if handled manually.  Fortunately Coiled
    provides services to help build and maintain software environments that match
    across local and remote environments.

    See the :doc:`software_environment` documentation for more information.


.. dropdown:: Does Coiled support GPUs?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes, but GPU support is only available today to paying users.


.. dropdown:: Can I use Coiled from Sagemaker/VS Code/PyCharm/...?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes, you can use Coiled from anywhere that you can use Python.
    Coiled is agnostic to user environment.


.. dropdown:: Does Coiled support Jupyter notebooks?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes, see the Notebooks tab in the application for example notebooks for
    notes on how to get started.  You may also want to try some of our
    notebooks at `cloud.coiled.io/examples/notebooks <https://cloud.coiled.io/examples/notebooks>`_.

    Coiled can run and manage arbitrary Python processes in the cloud,
    including Jupyter notebooks.  Note that today Coiled does not yet persist
    user state across notebook sessions.


.. dropdown:: Can I run Coiled on-prem?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    There are two types of on-prem that we support.  For those looking to run
    Coiled in your own cloud account, we support that today.  See the question
    "Can I run computation in my own account?" above.

    For those looking to run Coiled on your own machines in your own data
    center, we would love to hear from you.  Please contact sales@coiled.io to
    start a conversation with us.
    If by on-prem you mean "in yo.


.. dropdown:: Why do I need a local software environment?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    When performing distributed computation with Dask, you’ll create a :class:`distributed.Client`
    object which connects your local Python process (e.g. your laptop) to your remote Dask cluster
    (e.g. running on AWS). Dask ``Client`` s are the user-facing entry point for submitting tasks to
    a Dask cluster. When using a ``Client`` to submit tasks to your cluster, Dask will package up and send data,
    functions, and other Python objects needed for your computations *from* your local Python process
    where your ``Client`` is running *to* your remote Dask cluster in order for them to be executed.

    This means that if you want to run a function on your Dask cluster, for example NumPy’s :func:`numpy.mean`
    function, then you must have NumPy installed in your local Python process so Dask can send the ``numpy.mean``
    function from your local Dask ``Client`` to the workers in your Dask cluster. For this reason,
    it’s recommended to have the same libraries installed on both your local machine and on the remote
    workers in your cluster.

    See the :doc:`software_environment` section for more details on how to easily
    synchronize your local and remote software environments using Coiled.


.. _why-should-packages-match:


.. dropdown:: How can I stay up to date?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    You might want to `sign up for our newsletter <https://coiled.io>`_, and follow us on `Twitter <https://twitter.com/coiledhq>`_ or `LinkedIn <https://www.linkedin.com/company/coiled-computing/>`_.


.. dropdown:: Can I use Coiled to do machine learning / data science / ... ?
    :container: mb-2
    :title: bg-white text-black text-left h6
    :body: bg-white
    :animate: fade-in

    Yes!  Coiled builds on the popular PyData ecosystem of tools, and Dask in
    particular.  To learn more about what you can do with Dask and Python see the
    following links:

    -   `Dask <https://dask.org>`_
    -   `Dask Examples <https://examples.dask.org>`_

    You may also want to check out our `Youtube channel
    <https://youtube.com/c/Coiled>`_ for interviews with community members using
    Python at scale.