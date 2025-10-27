from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    aws_logs as logs,
    CfnOutput,
    aws_kms as kms,
    aws_iam as iam  

    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk.aws_logs import RetentionDays
from aws_cdk import Tags

class MyKMSStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kargs):
        super().__init__(scope,construct_id,**kargs)

        KMS_KEY = kms.Key(self, f"my-kms-keys",
                           description = "KMS keys for glue job secrets",
                          
                           #enable      = True,
                           enable_key_rotation = True,
                           key_spec = kms.KeySpec.SYMMETRIC_DEFAULT,
                           multi_region = False)
                           #policy = 'json_data')
        kms.Alias(self,"MYALIASKEY",alias_name="alias/glue-key",target_key=KMS_KEY)
         # Add a tag to the bucket
        Tags.of(KMS_KEY).add("KMS-tag", "Production")

        CfnOutput(self, "id-kms-key",value = KMS_KEY.key_arn)

