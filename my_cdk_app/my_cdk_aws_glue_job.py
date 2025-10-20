from aws_cdk import Stack, CfnOutput
from aws_cdk import (
    aws_glue as glue,
    aws_iam as iam
)
from constructs import Construct


class GlueJobStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Existing IAM Role (replace with actual role ARN)
        existing_role = iam.Role.from_role_arn(
            self,
            "ExistingRole",
            role_arn="arn:aws:iam::047861165149:role/Nany"  # make sure this is a *role*, not *user*
        )

        # Create the Glue Job
        glue_job = glue.CfnJob(
            self, "MyGlueJob",
            role=existing_role.role_arn,
            command=glue.CfnJob.JobCommandProperty(
                name="glueetl",
                script_location="s3://ukdatalake-nanyvbkr-bucketname/scripts/dummy_script.py",
                python_version="3"
            ),
            description="Demo Glue job for interview example",
            glue_version="4.0",
            max_capacity=2.0,
            timeout=10,
            connections=glue.CfnJob.ConnectionsListProperty(
                connections=["my-glue-connection"]
            )
        )  # ✅ this closing parenthesis was missing!

        # Output Glue Job details
        ##CfnOutput(self, "GlueJobName", value=glue_job.name)
        #CfnOutput(self, "GlueJobArn", value=glue_job.ref)
