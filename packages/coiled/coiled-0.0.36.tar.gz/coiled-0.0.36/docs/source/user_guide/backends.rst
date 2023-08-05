Backends
========

.. toctree::
   :maxdepth: 1
   :hidden:

   AWS <backends_aws>
   Kubernetes <backends_k8s>

Coiled manages launching Dask clusters and creating software environments for you.
A crucial part of this process is specifying exactly *where* Coiled should run
(e.g. should Coiled run on AWS or GCP).

By default, Coiled will run on AWS inside Coiled's own AWS account.
This makes it easy for you to get started quickly, without needing
to set up any additional infrastructure.
However, you can run Coiled on a variety of different systems to best suite your needs.

You can configure which system, or "backend", you want to Coiled run on in the "Team" page
for your Coiled account at ``https://cloud.coiled.io/<team-name>/team``.
More information about each backend is available below.

AWS
---

By default, Coiled will run on AWS inside Coiled's own AWS account.
This makes it easy for you to get started quickly, without needing
to set up any additional infrastructure.

However, you may prefer to run Coiled-managed computations within your own
infrastructure for security or billing purposes.
To facilitate this, you can also have Coiled run computations inside your own
AWS account.

.. link-button:: backends_aws
    :type: ref
    :text: Learn more about the AWS backend
    :classes: btn-outline-primary btn-block


Kubernetes
----------

You can have Coiled launch computations on a Kubernetes cluster that you control.
This is a good way to run Coiled on other cloud providers (e.g. AKS) or on-prem infrastructure.

.. link-button:: backends_k8s
    :type: ref
    :text: Learn more about the Kubernetes backend
    :classes: btn-outline-primary btn-block
