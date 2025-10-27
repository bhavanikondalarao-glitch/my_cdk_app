from aws_cdk import (
    # Duration,
    Stack,
    aws_s3 as s3,
    aws_logs as logs,
    CfnOutput
    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk.aws_logs import RetentionDays
from aws_cdk import Tags

class MyCdkAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cloud_watch = logs.LogGroup(self,f"cloud-watch",
                                    log_group_name="Nany-log-watch-group",
                                    retention=RetentionDays.ONE_WEEK)
        
        CfnOutput(self, "CloudWatchLogGroupArn",
            value=cloud_watch.log_group_arn,
            description="ARN of the CloudWatch Log Group")
        Tags.of(cloud_watch).add("cloudwatch-tag", "Production")



      

