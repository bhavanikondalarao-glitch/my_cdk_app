from aws_cdk import (
    Stack,
    aws_logs as logs,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
    aws_iam as iam,
    aws_s3 as s3,
    aws_kms as kms, aws_s3_notifications as s3n
)
from constructs import Construct

from aws_cdk import CfnOutput


class MySnsTopic(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # existing bucket import
        existing_bucket = s3.Bucket.from_bucket_name(
            self, "ExistingBucket", "ukdatalake-nanyvbkr-bucketname"
        )

        # import existing KMS key
        existing_key = kms.Alias.from_alias_name(
            self,
            "ExistingKey",
            "glue-key",
        )

        # create SNS topic
        topic = sns.Topic(
            self,
            "MyTopic",
            display_name="My First Topic",
            topic_name=f"nany-topic-{construct_id}",
            master_key=existing_key,
        )

        # define SNS topic policy statement
        policy_statement = iam.PolicyStatement(
            actions=["SNS:Publish"],
            principals=[iam.AnyPrincipal()],
            resources=[topic.topic_arn],
            conditions={
                "ArnEquals": {
                    "aws:SourceArn": f"arn:aws:s3:::{existing_bucket.bucket_name}"
                }
            },
        )


        existing_bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED,
            s3n.SnsDestination(topic)
        )

        # add statement to topic resource policy
        topic.add_to_resource_policy(policy_statement)

        # add subscription
        topic.add_subscription(subscriptions.EmailSubscription("bhavanikondalarao@gmail.com"))

        CfnOutput(self, "SnsTopicOutput", value=topic.topic_arn)
