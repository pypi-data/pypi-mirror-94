[![NPM version](https://badge.fury.io/js/cdk-keycloak.svg)](https://badge.fury.io/js/cdk-keycloak)
[![PyPI version](https://badge.fury.io/py/cdk-keycloak.svg)](https://badge.fury.io/py/cdk-keycloak)
![Release](https://github.com/pahud/cdk-keycloak/workflows/Release/badge.svg?branch=main)

# `cdk-keycloak`

CDK construct library that allows you to create KeyCloak service on AWS in TypeScript or Python

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_keycloak import KeyCloak

app = cdk.App()

env = {
    "region": process.env.CDK_DEFAULT_REGION,
    "account": process.env.CDK_DEFAULT_ACCOUNT
}

stack = cdk.Stack(app, "keycloak-demo", env=env)
KeyCloak(stack, "KeyCloak",
    certificate_arn="arn:aws:acm:us-east-1:123456789012:certificate/293cf875-ca98-4c2e-a797-e1cf6df2553c"
)
```

# Aurora Serverless support

The `KeyCloak` construct provisions the **Amaozn RDS cluster for MySQL** with **2** database instances under the hood, to opt in **Amazon Aurora Serverless**, use `auroraServerless` to opt in Amazon Aurora Serverless cluster. Please note only some regions are supported, check [Supported features in Amazon Aurora by AWS Region and Aurora DB engine](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.AuroraFeaturesRegionsDBEngines.grids.html) for availability.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
KeyCloak(stack, "KeyCloak",
    certificate_arn=certificate_arn,
    aurora_serverless=True
)
```

Behind the scene, a default RDS cluster for MySQL with 2 database instances will be created.

# Opt-in for Single RDS instance

To create single RDS instance for your testing or development environment, use `singleDbInstance` to turn on the
single db instance deployment.

Plesae note this is not recommended for production environment.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
KeyCloak(stack, "KeyCloak",
    certificate_arn=certificate_arn,
    single_db_instance=True
)
```

# Service Auto Scaling

Define `autoScaleTask` for the ecs service task autoscaling. For example:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
KeyCloak(stack, "KeyCloak",
    aurora_serverless=True,
    node_count=2,
    auto_scale_task={
        "min": 2,
        "max": 10,
        "target_cpu_utilization": 60
    }
)
```

# Deploy in existing Vpc Subnets

You can deploy the workload in the existing Vpc and subnets. The `publicSubnets` are for the ALB, `privateSubnets` for the keycloak container tasks and `databaseSubnets` for the database.

The best practice is to specify isolated subnets for `databaseSubnets`, however, in some cases might have no existing isolates subnets then the private subnets are also acceptable.

Consider the sample below:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
KeyCloak(stack, "KeyCloak",
    certificate_arn="arn:aws:acm:us-east-1:123456789012:certificate/293cf875-ca98-4c2e-a797-e1cf6df2553c",
    vpc=ec2.Vpc.from_lookup(stack, "Vpc", vpc_id="vpc-0417e46d"),
    public_subnets={
        "subnets": [
            ec2.Subnet.from_subnet_id(stack, "pub-1a", "subnet-5bbe7b32"),
            ec2.Subnet.from_subnet_id(stack, "pub-1b", "subnet-0428367c"),
            ec2.Subnet.from_subnet_id(stack, "pub-1c", "subnet-1586a75f")
        ]
    },
    private_subnets={
        "subnets": [
            ec2.Subnet.from_subnet_id(stack, "priv-1a", "subnet-0e9460dbcfc4cf6ee"),
            ec2.Subnet.from_subnet_id(stack, "priv-1b", "subnet-0562f666bdf5c29af"),
            ec2.Subnet.from_subnet_id(stack, "priv-1c", "subnet-00ab15c0022872f06")
        ]
    },
    database_subnets={
        "subnets": [
            ec2.Subnet.from_subnet_id(stack, "db-1a", "subnet-0e9460dbcfc4cf6ee"),
            ec2.Subnet.from_subnet_id(stack, "db-1b", "subnet-0562f666bdf5c29af"),
            ec2.Subnet.from_subnet_id(stack, "db-1c", "subnet-00ab15c0022872f06")
        ]
    }
)
```
