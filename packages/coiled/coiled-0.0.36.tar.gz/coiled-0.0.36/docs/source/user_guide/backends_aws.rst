AWS Backend
===========

Using Coiled's AWS account
--------------------------

By default your computations run inside Coiled's AWS account.
This makes it easy for you to get started quickly, without needing
to set up any additional infrastructure.


Using your own AWS account
--------------------------

You can have Coiled run computations in your own AWS account.
This allows you to take advantage of any business or security arrangements
(such as startup credits or custom data access controls) you already have.

To do this,
`create an access key ID and secret access key <https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys>`_
and add them to the "Cloud Backend Options" section of the Team page of your Coiled account.

From now on, clusters you create with Coiled will be launched in your AWS account.

.. note::

    The AWS credentials you supply must be long-lived (not temporary) tokens, and have sufficient permissions
    to allow Coiled to set up management infrastructure and create & launch compute resources from within
    your AWS account.

    Also, note that if you have not used AWS Elastic Container Service in this
    account before, you may need to `create the necessary service-linked IAM role <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using-service-linked-roles.html>`_
    -- we cannot yet create it automatically.

For the full set of required permissions, click the dropdown below.

.. dropdown:: Click to see the full set of required permissions
  :title: bg-white

  **Setup***

  * iam:CreateRole
  * iam:AttachRolePolicy
  * iam:TagRole
  * iam:DeleteRole
  * ecs:CreateCluster
  * ec2:CreateVpc
  * ec2:ModifyVpcAttribute
  * ec2:CreateInternetGateway
  * ec2:AttachInternetGateway
  * ec2:CreateVpcPeeringConnection
  * ec2:CreateRouteTable
  * ec2:CreateRoute
  * ec2:CreateSubnet
  * ec2:AssociateRouteTable
  * ec2:ModifySubnetAttribute
  * ec2:AllocateAddress
  * ec2:CreateNatGateway

  **Ongoing***

  * sts:GetCallerIdentity
  * iam:GetRole
  * iam:PassRole
  * ecs:RegisterTaskDefinition
  * ecs:RunTask
  * ecs:ListTasks
  * ecs:DescribeTasks
  * ecs:DescribeClusters
  * ecs:StopTask
  * ecs:ListTaskDefinitions
  * ecs:DescribeTaskDefinition
  * ecs:ListClusters
  * ecr:DescribeImages
  * ecr:ListImages
  * ecr:DescribeRepositories
  * ecr:CreateRepository
  * ecr:GetAuthorizationToken
  * ecr:InitiateLayerUpload
  * ecr:UploadLayerPart
  * ecr:CompleteLayerUpload
  * ecr:PutImage
  * ecr:BatchCheckLayerAvailability
  * ecr:GetDownloadUrlForLayer
  * ecr:GetRepositoryPolicy
  * ecr:BatchGetImage
  * ec2:DescribeSubnets
  * ec2:CreateSecurityGroup
  * ec2:AuthorizeSecurityGroupIngress
  * ec2:CreateTags
  * ec2:DescribeSecurityGroups
  * ec2:DeleteSecurityGroup
  * ec2:DescribeVpcs
  * ec2:DescribeRouteTables
  * ec2:DescribeVpcPeeringConnections
  * ec2:DescribeAvailabilityZones
  * ec2:DescribeNatGateways
  * ec2:DescribeNetworkInterfaces
  * logs:CreateLogGroup
  * logs:PutRetentionPolicy
  * logs:GetLogEvents

The below JSON template lists all the above permissions and can be used to `create the required IAM policy directly <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create-console.html#access_policies_create-json-editor>`_.

.. dropdown:: IAM policy template
  :title: bg-white

  .. code-block:: json

        {
            "Statement": [
                {
                    "Sid": "Setup",
                    "Effect": "Allow",
                    "Resource": "*",
                    "Action": [
                        "iam:CreateRole",
                        "iam:TagRole",
                        "iam:AttachRolePolicy",
                        "iam:DeleteRole",
                        "ecs:CreateCluster",
                        "ec2:CreateVpc",
                        "ec2:ModifyVpcAttribute",
                        "ec2:CreateInternetGateway",
                        "ec2:AttachInternetGateway",
                        "ec2:CreateVpcPeeringConnection",
                        "ec2:CreateRouteTable",
                        "ec2:CreateRoute",
                        "ec2:CreateSubnet",
                        "ec2:AssociateRouteTable",
                        "ec2:ModifySubnetAttribute",
                        "ec2:AllocateAddress",
                        "ec2:CreateNatGateway"
                    ]
                },
                {

                    "Sid": "Ongoing",
                    "Effect": "Allow",
                    "Resource": "*",
                    "Action": [
                        "sts:GetCallerIdentity",
                        "iam:GetRole",
                        "iam:PassRole",
                        "ecs:RegisterTaskDefinition",
                        "ecs:RunTask",
                        "ecs:ListTasks",
                        "ecs:DescribeTasks",
                        "ecs:DescribeClusters",
                        "ecs:StopTask",
                        "ecs:ListTaskDefinitions",
                        "ecs:DescribeTaskDefinition",
                        "ecs:ListClusters",
                        "ecr:DescribeImages",
                        "ecr:ListImages",
                        "ecr:DescribeRepositories",
                        "ecr:CreateRepository",
                        "ecr:GetAuthorizationToken",
                        "ecr:InitiateLayerUpload",
                        "ecr:UploadLayerPart",
                        "ecr:CompleteLayerUpload",
                        "ecr:PutImage",
                        "ecr:BatchCheckLayerAvailability",
                        "ecr:GetDownloadUrlForLayer",
                        "ecr:GetRepositoryPolicy",
                        "ecr:BatchGetImage",
                        "ec2:DescribeSubnets",
                        "ec2:CreateSecurityGroup",
                        "ec2:AuthorizeSecurityGroupIngress",
                        "ec2:CreateTags",
                        "ec2:DescribeSecurityGroups",
                        "ec2:DeleteSecurityGroup",
                        "ec2:DescribeVpcs",
                        "ec2:DescribeRouteTables",
                        "ec2:DescribeVpcPeeringConnections",
                        "ec2:DescribeAvailabilityZones",
                        "ec2:DescribeNatGateways",
                        "ec2:DescribeNetworkInterfaces",
                        "logs:CreateLogGroup",
                        "logs:PutRetentionPolicy",
                        "logs:GetLogEvents"
                    ]
                }
            ],
            "Version": "2012-10-17"
        }

Backend options
---------------

There are several AWS-specific options you can specify (listed below) to customize Coiled's behavior.
Additionally, the next section contains an example of how to configure these options in practice.

.. list-table::
   :widths: 25 50 25
   :header-rows: 1

   * - Name
     - Description
     - Default
   * - ``region``
     - AWS region to create resources in
     - ``us-east-2``
   * - ``fargate_spot``
     - Whether or not to use spot instances for cluster workers
     - ``False``

Example
^^^^^^^

You can specify backend options directly in Python:

.. code-block::

    import coiled

    cluster = coiled.Cluster(backend_options={"region": "us-west-1", "fargate_spot": True})

Or save them to your :ref:`Coiled configuration file <configuration>`:

.. code-block:: yaml

    # ~/.config/dask/coiled.yaml

    coiled:
      backend-options:
        region: us-west-1
        fargate-spot: True

to have them used as the default value for the ``backend_options=`` keyword:

.. code-block::

    import coiled

    cluster = coiled.Cluster()
