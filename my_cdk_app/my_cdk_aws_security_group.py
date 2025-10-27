from aws_cdk import Stack
from aws_cdk import aws_ec2 as ec2
from constructs import Construct

from aws_cdk import CfnOutput
from aws_cdk import Tags

class MySecurityGroup(Stack):
    def __init__(self, scope:Construct, construct_id: str, **kwargs ):
        super().__init__(scope,construct_id,**kwargs)

        security_group = ec2.SecurityGroup(self, f"my-security-group",
                          security_group_name=f"nany-security-group-{construct_id}",
                           vpc= ec2.Vpc.from_lookup(self, "existing-vpc",vpc_id="vpc-044196ca4f44d6644"),
                           )
        security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(), # who is conncted to your resource
            connection=ec2.Port.tcp(22), # what kind of network traffic is allowed
            description="Allow SSH acess anywhere"

        )
        security_group.add_egress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.all_traffic(),
            description = "Allow all outbound trafiic"
        )
        Tags.of(security_group).add("Security-group-tag", "Production")

        CfnOutput(self,'security-group-output',value=security_group.security_group_id )