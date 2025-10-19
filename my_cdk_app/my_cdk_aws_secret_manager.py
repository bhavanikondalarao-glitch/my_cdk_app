from aws_cdk import Stack
from aws_cdk import CfnOutput
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_secretsmanager  as secretsmanager
import json

from constructs import Construct
from aws_cdk import Stack


class MySecretManager(Stack):
    def __init__(self, scope: Construct, construct_id:str,*kwargs):
        super().__init__(scope, construct_id,*kwargs)

        secret = secretsmanager.Secret(
            self,f'my-secret-manager',
            secret_name = 'rds-master-password',
            description="Master password for RDS",
            generate_secret_string = secretsmanager.SecretStringGenerator(
        secret_string_template=json.dumps({"username": "postgres"}),
        generate_string_key="password",
        exclude_characters="/@\"",
        password_length= 32)


    
        )

        CfnOutput(self, "secret_manager", value=secret.secret_arn)




