# glue job creation is happeing in this file



from aws_cdk import Stack
from aws_cdk import (
    aws_glue as glue,
    aws_iam as iam,
    aws_ec2 as ec2
)
from constructs import Construct
from aws_cdk  import CfnOuput


class GlueJobStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)
        existing_role = iam.Role.from_role_arn(self,"Existing-role",role_arn="arn:aws:iam::047861165149:user/Nany")


        glue_job = glue.CfnJob(
            self, "MyGlueJob",
            role=existing_role.role_arn,
            command=glue.CfnJob.JobCommandProperty(
                name="glueetl",
                script_location="s3://ukdatalake-nanyvbkr-bucketname/scripts/dummy_script.py"
                python_version="3"
            )
            description="Demo Glue job for interview example",
            glue_version="4.0",  # Example version
            max_capacity=2.0,    # 2 DPUs
            timeout=10 

        
)





                               
                               
                               ,)

