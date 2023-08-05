"""
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

Use `autoraServerless` to opt in Amazon Aurora Serverless cluster. Please note only some regions are supported, check [Supported features in Amazon Aurora by AWS Region and Aurora DB engine](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.AuroraFeaturesRegionsDBEngines.grids.html) for availability.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
KeyCloak(stack, "KeyCloak",
    autora_serverless=True
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
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_certificatemanager
import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_rds
import aws_cdk.aws_secretsmanager
import aws_cdk.core


class ContainerService(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-keycloak.ContainerService",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        certificate: aws_cdk.aws_certificatemanager.ICertificate,
        database: "Database",
        keycloak_secret: aws_cdk.aws_secretsmanager.ISecret,
        vpc: aws_cdk.aws_ec2.IVpc,
        bastion: typing.Optional[builtins.bool] = None,
        circuit_breaker: typing.Optional[builtins.bool] = None,
        node_count: typing.Optional[jsii.Number] = None,
        private_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        public_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param certificate: The ACM certificate.
        :param database: The RDS database for the service.
        :param keycloak_secret: The secrets manager secret for the keycloak.
        :param vpc: The VPC for the service.
        :param bastion: Whether to create the bastion host. Default: false
        :param circuit_breaker: Whether to enable the ECS service deployment circuit breaker. Default: false
        :param node_count: Number of keycloak node in the cluster. Default: 1
        :param private_subnets: VPC subnets for keycloak service.
        :param public_subnets: VPC public subnets for ALB.
        :param stickiness_cookie_duration: The sticky session duration for the keycloak workload with ALB. Default: - one day
        """
        props = ContainerServiceProps(
            certificate=certificate,
            database=database,
            keycloak_secret=keycloak_secret,
            vpc=vpc,
            bastion=bastion,
            circuit_breaker=circuit_breaker,
            node_count=node_count,
            private_subnets=private_subnets,
            public_subnets=public_subnets,
            stickiness_cookie_duration=stickiness_cookie_duration,
        )

        jsii.create(ContainerService, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.FargateService:
        return typing.cast(aws_cdk.aws_ecs.FargateService, jsii.get(self, "service"))


@jsii.data_type(
    jsii_type="cdk-keycloak.ContainerServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate": "certificate",
        "database": "database",
        "keycloak_secret": "keycloakSecret",
        "vpc": "vpc",
        "bastion": "bastion",
        "circuit_breaker": "circuitBreaker",
        "node_count": "nodeCount",
        "private_subnets": "privateSubnets",
        "public_subnets": "publicSubnets",
        "stickiness_cookie_duration": "stickinessCookieDuration",
    },
)
class ContainerServiceProps:
    def __init__(
        self,
        *,
        certificate: aws_cdk.aws_certificatemanager.ICertificate,
        database: "Database",
        keycloak_secret: aws_cdk.aws_secretsmanager.ISecret,
        vpc: aws_cdk.aws_ec2.IVpc,
        bastion: typing.Optional[builtins.bool] = None,
        circuit_breaker: typing.Optional[builtins.bool] = None,
        node_count: typing.Optional[jsii.Number] = None,
        private_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        public_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> None:
        """
        :param certificate: The ACM certificate.
        :param database: The RDS database for the service.
        :param keycloak_secret: The secrets manager secret for the keycloak.
        :param vpc: The VPC for the service.
        :param bastion: Whether to create the bastion host. Default: false
        :param circuit_breaker: Whether to enable the ECS service deployment circuit breaker. Default: false
        :param node_count: Number of keycloak node in the cluster. Default: 1
        :param private_subnets: VPC subnets for keycloak service.
        :param public_subnets: VPC public subnets for ALB.
        :param stickiness_cookie_duration: The sticky session duration for the keycloak workload with ALB. Default: - one day
        """
        if isinstance(private_subnets, dict):
            private_subnets = aws_cdk.aws_ec2.SubnetSelection(**private_subnets)
        if isinstance(public_subnets, dict):
            public_subnets = aws_cdk.aws_ec2.SubnetSelection(**public_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "certificate": certificate,
            "database": database,
            "keycloak_secret": keycloak_secret,
            "vpc": vpc,
        }
        if bastion is not None:
            self._values["bastion"] = bastion
        if circuit_breaker is not None:
            self._values["circuit_breaker"] = circuit_breaker
        if node_count is not None:
            self._values["node_count"] = node_count
        if private_subnets is not None:
            self._values["private_subnets"] = private_subnets
        if public_subnets is not None:
            self._values["public_subnets"] = public_subnets
        if stickiness_cookie_duration is not None:
            self._values["stickiness_cookie_duration"] = stickiness_cookie_duration

    @builtins.property
    def certificate(self) -> aws_cdk.aws_certificatemanager.ICertificate:
        """The ACM certificate."""
        result = self._values.get("certificate")
        assert result is not None, "Required property 'certificate' is missing"
        return typing.cast(aws_cdk.aws_certificatemanager.ICertificate, result)

    @builtins.property
    def database(self) -> "Database":
        """The RDS database for the service."""
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast("Database", result)

    @builtins.property
    def keycloak_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        """The secrets manager secret for the keycloak."""
        result = self._values.get("keycloak_secret")
        assert result is not None, "Required property 'keycloak_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC for the service."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def bastion(self) -> typing.Optional[builtins.bool]:
        """Whether to create the bastion host.

        :default: false
        """
        result = self._values.get("bastion")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def circuit_breaker(self) -> typing.Optional[builtins.bool]:
        """Whether to enable the ECS service deployment circuit breaker.

        :default: false
        """
        result = self._values.get("circuit_breaker")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        """Number of keycloak node in the cluster.

        :default: 1
        """
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def private_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """VPC subnets for keycloak service."""
        result = self._values.get("private_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def public_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """VPC public subnets for ALB."""
        result = self._values.get("public_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def stickiness_cookie_duration(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The sticky session duration for the keycloak workload with ALB.

        :default: - one day
        """
        result = self._values.get("stickiness_cookie_duration")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Database(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-keycloak.Database",
):
    """Represents the database instance or database cluster."""

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        aurora_serverless: typing.Optional[builtins.bool] = None,
        database_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        engine: typing.Optional[aws_cdk.aws_rds.IInstanceEngine] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param vpc: The VPC for the database.
        :param aurora_serverless: enable aurora serverless. Default: false
        :param database_subnets: VPC subnets for database.
        :param engine: The database instance engine. Default: - MySQL 8.0.21
        :param instance_type: The database instance type. Default: r5.large
        """
        props = DatabaseProps(
            vpc=vpc,
            aurora_serverless=aurora_serverless,
            database_subnets=database_subnets,
            engine=engine,
            instance_type=instance_type,
        )

        jsii.create(Database, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterEndpointHostname")
    def cluster_endpoint_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterEndpointHostname"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clusterIdentifier"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return typing.cast(aws_cdk.aws_ec2.Connections, jsii.get(self, "connections"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="secret")
    def secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, jsii.get(self, "secret"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        return typing.cast(aws_cdk.aws_ec2.IVpc, jsii.get(self, "vpc"))


@jsii.data_type(
    jsii_type="cdk-keycloak.DatabaseCofig",
    jsii_struct_bases=[],
    name_mapping={
        "connections": "connections",
        "endpoint": "endpoint",
        "identifier": "identifier",
        "secret": "secret",
    },
)
class DatabaseCofig:
    def __init__(
        self,
        *,
        connections: aws_cdk.aws_ec2.Connections,
        endpoint: builtins.str,
        identifier: builtins.str,
        secret: aws_cdk.aws_secretsmanager.ISecret,
    ) -> None:
        """Database configuration.

        :param connections: The database connnections.
        :param endpoint: The endpoint address for the database.
        :param identifier: The databasae identifier.
        :param secret: The database secret.
        """
        self._values: typing.Dict[str, typing.Any] = {
            "connections": connections,
            "endpoint": endpoint,
            "identifier": identifier,
            "secret": secret,
        }

    @builtins.property
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """The database connnections."""
        result = self._values.get("connections")
        assert result is not None, "Required property 'connections' is missing"
        return typing.cast(aws_cdk.aws_ec2.Connections, result)

    @builtins.property
    def endpoint(self) -> builtins.str:
        """The endpoint address for the database."""
        result = self._values.get("endpoint")
        assert result is not None, "Required property 'endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identifier(self) -> builtins.str:
        """The databasae identifier."""
        result = self._values.get("identifier")
        assert result is not None, "Required property 'identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        """The database secret."""
        result = self._values.get("secret")
        assert result is not None, "Required property 'secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseCofig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-keycloak.DatabaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "aurora_serverless": "auroraServerless",
        "database_subnets": "databaseSubnets",
        "engine": "engine",
        "instance_type": "instanceType",
    },
)
class DatabaseProps:
    def __init__(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        aurora_serverless: typing.Optional[builtins.bool] = None,
        database_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        engine: typing.Optional[aws_cdk.aws_rds.IInstanceEngine] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
    ) -> None:
        """
        :param vpc: The VPC for the database.
        :param aurora_serverless: enable aurora serverless. Default: false
        :param database_subnets: VPC subnets for database.
        :param engine: The database instance engine. Default: - MySQL 8.0.21
        :param instance_type: The database instance type. Default: r5.large
        """
        if isinstance(database_subnets, dict):
            database_subnets = aws_cdk.aws_ec2.SubnetSelection(**database_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "vpc": vpc,
        }
        if aurora_serverless is not None:
            self._values["aurora_serverless"] = aurora_serverless
        if database_subnets is not None:
            self._values["database_subnets"] = database_subnets
        if engine is not None:
            self._values["engine"] = engine
        if instance_type is not None:
            self._values["instance_type"] = instance_type

    @builtins.property
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        """The VPC for the database."""
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(aws_cdk.aws_ec2.IVpc, result)

    @builtins.property
    def aurora_serverless(self) -> typing.Optional[builtins.bool]:
        """enable aurora serverless.

        :default: false
        """
        result = self._values.get("aurora_serverless")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def database_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """VPC subnets for database."""
        result = self._values.get("database_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def engine(self) -> typing.Optional[aws_cdk.aws_rds.IInstanceEngine]:
        """The database instance engine.

        :default: - MySQL 8.0.21
        """
        result = self._values.get("engine")
        return typing.cast(typing.Optional[aws_cdk.aws_rds.IInstanceEngine], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """The database instance type.

        :default: r5.large
        """
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.InstanceType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-keycloak.KeyCloadProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_arn": "certificateArn",
        "aurora_serverless": "auroraServerless",
        "bastion": "bastion",
        "database_instance_type": "databaseInstanceType",
        "database_subnets": "databaseSubnets",
        "engine": "engine",
        "node_count": "nodeCount",
        "private_subnets": "privateSubnets",
        "public_subnets": "publicSubnets",
        "stickiness_cookie_duration": "stickinessCookieDuration",
        "vpc": "vpc",
    },
)
class KeyCloadProps:
    def __init__(
        self,
        *,
        certificate_arn: builtins.str,
        aurora_serverless: typing.Optional[builtins.bool] = None,
        bastion: typing.Optional[builtins.bool] = None,
        database_instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        database_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        engine: typing.Optional[aws_cdk.aws_rds.IInstanceEngine] = None,
        node_count: typing.Optional[jsii.Number] = None,
        private_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        public_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param certificate_arn: ACM certificate ARN to import.
        :param aurora_serverless: Whether to use aurora serverless. When enabled, the ``databaseInstanceType`` and ``engine`` will be ignored. The ``rds.DatabaseClusterEngine.AURORA_MYSQL`` will be used as the default cluster engine instead. Default: false
        :param bastion: Create a bastion host for debugging or trouble-shooting. Default: false
        :param database_instance_type: Database instance type. Default: r5.large
        :param database_subnets: VPC subnets for database. Default: - VPC isolated subnets
        :param engine: The database instance engine. Default: - MySQL 8.0.21
        :param node_count: Number of keycloak node in the cluster. Default: 2
        :param private_subnets: VPC private subnets for keycloak service. Default: - VPC private subnets
        :param public_subnets: VPC public subnets for ALB. Default: - VPC public subnets
        :param stickiness_cookie_duration: The sticky session duration for the keycloak workload with ALB. Default: - one day
        :param vpc: VPC for the workload.
        """
        if isinstance(database_subnets, dict):
            database_subnets = aws_cdk.aws_ec2.SubnetSelection(**database_subnets)
        if isinstance(private_subnets, dict):
            private_subnets = aws_cdk.aws_ec2.SubnetSelection(**private_subnets)
        if isinstance(public_subnets, dict):
            public_subnets = aws_cdk.aws_ec2.SubnetSelection(**public_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "certificate_arn": certificate_arn,
        }
        if aurora_serverless is not None:
            self._values["aurora_serverless"] = aurora_serverless
        if bastion is not None:
            self._values["bastion"] = bastion
        if database_instance_type is not None:
            self._values["database_instance_type"] = database_instance_type
        if database_subnets is not None:
            self._values["database_subnets"] = database_subnets
        if engine is not None:
            self._values["engine"] = engine
        if node_count is not None:
            self._values["node_count"] = node_count
        if private_subnets is not None:
            self._values["private_subnets"] = private_subnets
        if public_subnets is not None:
            self._values["public_subnets"] = public_subnets
        if stickiness_cookie_duration is not None:
            self._values["stickiness_cookie_duration"] = stickiness_cookie_duration
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def certificate_arn(self) -> builtins.str:
        """ACM certificate ARN to import."""
        result = self._values.get("certificate_arn")
        assert result is not None, "Required property 'certificate_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aurora_serverless(self) -> typing.Optional[builtins.bool]:
        """Whether to use aurora serverless.

        When enabled, the ``databaseInstanceType`` and
        ``engine`` will be ignored. The ``rds.DatabaseClusterEngine.AURORA_MYSQL`` will be used as
        the default cluster engine instead.

        :default: false
        """
        result = self._values.get("aurora_serverless")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bastion(self) -> typing.Optional[builtins.bool]:
        """Create a bastion host for debugging or trouble-shooting.

        :default: false
        """
        result = self._values.get("bastion")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def database_instance_type(self) -> typing.Optional[aws_cdk.aws_ec2.InstanceType]:
        """Database instance type.

        :default: r5.large
        """
        result = self._values.get("database_instance_type")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.InstanceType], result)

    @builtins.property
    def database_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """VPC subnets for database.

        :default: - VPC isolated subnets
        """
        result = self._values.get("database_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def engine(self) -> typing.Optional[aws_cdk.aws_rds.IInstanceEngine]:
        """The database instance engine.

        :default: - MySQL 8.0.21
        """
        result = self._values.get("engine")
        return typing.cast(typing.Optional[aws_cdk.aws_rds.IInstanceEngine], result)

    @builtins.property
    def node_count(self) -> typing.Optional[jsii.Number]:
        """Number of keycloak node in the cluster.

        :default: 2
        """
        result = self._values.get("node_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def private_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """VPC private subnets for keycloak service.

        :default: - VPC private subnets
        """
        result = self._values.get("private_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def public_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        """VPC public subnets for ALB.

        :default: - VPC public subnets
        """
        result = self._values.get("public_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    @builtins.property
    def stickiness_cookie_duration(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The sticky session duration for the keycloak workload with ALB.

        :default: - one day
        """
        result = self._values.get("stickiness_cookie_duration")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """VPC for the workload."""
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyCloadProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KeyCloak(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-keycloak.KeyCloak",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        certificate_arn: builtins.str,
        aurora_serverless: typing.Optional[builtins.bool] = None,
        bastion: typing.Optional[builtins.bool] = None,
        database_instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        database_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        engine: typing.Optional[aws_cdk.aws_rds.IInstanceEngine] = None,
        node_count: typing.Optional[jsii.Number] = None,
        private_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        public_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param certificate_arn: ACM certificate ARN to import.
        :param aurora_serverless: Whether to use aurora serverless. When enabled, the ``databaseInstanceType`` and ``engine`` will be ignored. The ``rds.DatabaseClusterEngine.AURORA_MYSQL`` will be used as the default cluster engine instead. Default: false
        :param bastion: Create a bastion host for debugging or trouble-shooting. Default: false
        :param database_instance_type: Database instance type. Default: r5.large
        :param database_subnets: VPC subnets for database. Default: - VPC isolated subnets
        :param engine: The database instance engine. Default: - MySQL 8.0.21
        :param node_count: Number of keycloak node in the cluster. Default: 2
        :param private_subnets: VPC private subnets for keycloak service. Default: - VPC private subnets
        :param public_subnets: VPC public subnets for ALB. Default: - VPC public subnets
        :param stickiness_cookie_duration: The sticky session duration for the keycloak workload with ALB. Default: - one day
        :param vpc: VPC for the workload.
        """
        props = KeyCloadProps(
            certificate_arn=certificate_arn,
            aurora_serverless=aurora_serverless,
            bastion=bastion,
            database_instance_type=database_instance_type,
            database_subnets=database_subnets,
            engine=engine,
            node_count=node_count,
            private_subnets=private_subnets,
            public_subnets=public_subnets,
            stickiness_cookie_duration=stickiness_cookie_duration,
            vpc=vpc,
        )

        jsii.create(KeyCloak, self, [scope, id, props])

    @jsii.member(jsii_name="addDatabase")
    def add_database(
        self,
        *,
        vpc: aws_cdk.aws_ec2.IVpc,
        aurora_serverless: typing.Optional[builtins.bool] = None,
        database_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        engine: typing.Optional[aws_cdk.aws_rds.IInstanceEngine] = None,
        instance_type: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
    ) -> Database:
        """
        :param vpc: The VPC for the database.
        :param aurora_serverless: enable aurora serverless. Default: false
        :param database_subnets: VPC subnets for database.
        :param engine: The database instance engine. Default: - MySQL 8.0.21
        :param instance_type: The database instance type. Default: r5.large
        """
        props = DatabaseProps(
            vpc=vpc,
            aurora_serverless=aurora_serverless,
            database_subnets=database_subnets,
            engine=engine,
            instance_type=instance_type,
        )

        return typing.cast(Database, jsii.invoke(self, "addDatabase", [props]))

    @jsii.member(jsii_name="addKeyCloakContainerService")
    def add_key_cloak_container_service(
        self,
        *,
        certificate: aws_cdk.aws_certificatemanager.ICertificate,
        database: Database,
        keycloak_secret: aws_cdk.aws_secretsmanager.ISecret,
        vpc: aws_cdk.aws_ec2.IVpc,
        bastion: typing.Optional[builtins.bool] = None,
        circuit_breaker: typing.Optional[builtins.bool] = None,
        node_count: typing.Optional[jsii.Number] = None,
        private_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        public_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
        stickiness_cookie_duration: typing.Optional[aws_cdk.core.Duration] = None,
    ) -> ContainerService:
        """
        :param certificate: The ACM certificate.
        :param database: The RDS database for the service.
        :param keycloak_secret: The secrets manager secret for the keycloak.
        :param vpc: The VPC for the service.
        :param bastion: Whether to create the bastion host. Default: false
        :param circuit_breaker: Whether to enable the ECS service deployment circuit breaker. Default: false
        :param node_count: Number of keycloak node in the cluster. Default: 1
        :param private_subnets: VPC subnets for keycloak service.
        :param public_subnets: VPC public subnets for ALB.
        :param stickiness_cookie_duration: The sticky session duration for the keycloak workload with ALB. Default: - one day
        """
        props = ContainerServiceProps(
            certificate=certificate,
            database=database,
            keycloak_secret=keycloak_secret,
            vpc=vpc,
            bastion=bastion,
            circuit_breaker=circuit_breaker,
            node_count=node_count,
            private_subnets=private_subnets,
            public_subnets=public_subnets,
            stickiness_cookie_duration=stickiness_cookie_duration,
        )

        return typing.cast(ContainerService, jsii.invoke(self, "addKeyCloakContainerService", [props]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        return typing.cast(aws_cdk.aws_ec2.IVpc, jsii.get(self, "vpc"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="db")
    def db(self) -> typing.Optional[Database]:
        return typing.cast(typing.Optional[Database], jsii.get(self, "db"))


__all__ = [
    "ContainerService",
    "ContainerServiceProps",
    "Database",
    "DatabaseCofig",
    "DatabaseProps",
    "KeyCloadProps",
    "KeyCloak",
]

publication.publish()
