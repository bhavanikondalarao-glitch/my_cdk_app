from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iam as iam,
    CfnOutput,
    Duration
)
from constructs import Construct
from aws_cdk import Tags

class MyS3stack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Logging bucket for access logs
        log_bucket = s3.Bucket(self, "s3-log-bucket")

        # Main S3 bucket
        bucket = s3.Bucket(
            self,
            "nany-aws-s3",
            bucket_name="ukdatalake-nanyvbkr-bucketname",
            versioned=True,  # ✅ Correct keyword
            encryption=s3.BucketEncryption.S3_MANAGED,  # ✅ Fixed typo
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            server_access_logs_bucket=log_bucket,  # ✅ Correct property name
            server_access_logs_prefix="new_s3_logs"
        )

        # Add lifecycle rule
        bucket.add_lifecycle_rule(
            id="nany-id-for-life-cycle",
            enabled=True,
            expiration=Duration.days(30)
        )
        Tags.of(bucket).add("S3-tag", "Production")

        # Output bucket name
        CfnOutput(self, "BucketName", value=bucket.bucket_name)
