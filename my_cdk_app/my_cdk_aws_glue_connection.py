from aws_cdk import Stack
from aws_cdk import (
    aws_glue as glue,
    aws_iam as iam,
    aws_ec2 as ec2
)
from constructs import Construct
from aws_cdk import Tags


class GlueConnection(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # ✅ Import existing VPC
        existing_vpc = ec2.Vpc.from_lookup(
            self, "ExistingVPC", vpc_id="vpc-044196ca4f44d6644"
        )

        # ✅ Import existing Security Group (fix class name typo)
        existing_security_group = ec2.SecurityGroup.from_security_group_id(
            self,
            "ExistingSecurityGroup",
            security_group_id="sg-0b636aaf969e2889c"
        )

        # ✅ Choose a private subnet
        subnet_id = existing_vpc.public_subnets[0].subnet_id
       #subnet_id = existing_vpc.private_subnets[0].subnet_id

        # ✅ Create Glue connection
        glue_connection = glue.CfnConnection(
            self,
            "GlueConnection",
            catalog_id=self.account,  # ✅ fixed 'catlog_id' -> 'catalog_id'
            connection_input=glue.CfnConnection.ConnectionInputProperty(
                name="my-glue-connection",
                description="Glue connection for RDS connection",
                connection_type="JDBC",
                connection_properties={
                    "JDBC_CONNECTION_URL": "jdbc:postgresql://dummy-host:5432/fakedb",
                    "USERNAME": "fake_user",
                    "PASSWORD": "fake_password"
                },
                physical_connection_requirements=glue.CfnConnection.PhysicalConnectionRequirementsProperty(
                    subnet_id=subnet_id,
                    security_group_id_list=[existing_security_group.security_group_id]
                )
            )
        )
        Tags.of(glue_connection).add("Glue-connection-tag", "Production")
