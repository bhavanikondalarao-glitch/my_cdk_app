#!/usr/bin/env python3
import os

import aws_cdk as cdk


from my_cdk_app.my_cdk_app_stack import MyCdkAppStack
from my_cdk_app.awskmsStack import MyKMSStack
from my_cdk_app.my_cdk_aws_s3_stack import MyS3stack
from my_cdk_app.my_cdk_aws_secret_manager import MySecretManager
from my_cdk_app.my_cdk_aws_security_group import MySecurityGroup



app = cdk.App()


MyCdkAppStack(app, "MyCdkAppStack")
MyKMSStack(app, "MyKMSStack")
MyS3stack(app,"Mys3stack")
MySecretManager(app,"MySecretManager")
MySecurityGroup(app, "MySecurityGroup",env=cdk.Environment(
    account="047861165149",
    region="eu-north-1" 
))
   

app.synth()
