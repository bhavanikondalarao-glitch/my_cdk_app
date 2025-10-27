#!/usr/bin/env python3
"""
Dynamic tag checker for CDK-deployed CloudFormation stacks.

Features:
- Runs `cdk list` (configurable) to discover stacks.
- Uses boto3 (preferred) to query CloudFormation resources and resource-specific tag APIs.
- Avoids temporary files; works with profile/region arguments.
- Extensible mapping for additional resource types.
"""
import argparse
import subprocess
import json
import re
import sys
from typing import Dict, List, Any, Optional
import boto3
from botocore.exceptions import ClientError

# Helper utilities
def run_cdk_list(cdk_app: str) -> list:
    cmd = ["cdk", "list", f"--app={cdk_app}"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print("cdk list failed:", proc.stderr.strip(), file=sys.stderr)
        sys.exit(proc.returncode)
    stacks = [ln.strip() for ln in proc.stdout.splitlines() if ln.strip()]
    return stacks

def make_session(profile: Optional[str], region: Optional[str]):
    if profile:
        session = boto3.Session(profile_name=profile, region_name=region)
    else:
        session = boto3.Session(region_name=region)
    return session

def list_stack_resources(cf, stack_name: str) -> List[Dict[str, Any]]:
    # handles a single page (CDK stacks usually small). add paginator if needed.
    paginator = cf.get_paginator("list_stack_resources")
    resources = []
    for page in paginator.paginate(StackName=stack_name):
        resources.extend(page.get("StackResourceSummaries", []))
    return resources

# Tag fetching functions for supported resource types.
def get_s3_bucket_tags(s3, bucket_name: str) -> Dict[str, str]:
    try:
        resp = s3.get_bucket_tagging(Bucket=bucket_name)
        tagset = resp.get("TagSet", [])
        return {t["Key"]: t["Value"] for t in tagset}
    except ClientError as e:
        # bucket may not have tagging or name may be wrong
        # print debug in a concise form
        # print(f"S3 tagging error for {bucket_name}: {e}", file=sys.stderr)
        return {}

def get_log_group_tags(logs, log_group_name: str) -> Dict[str, str]:
    try:
        resp = logs.list_tags_log_group(logGroupName=log_group_name)
        return resp.get("tags", {}) or {}
    except ClientError:
        return {}

def get_kms_tags(kms, key_id: str) -> Dict[str, str]:
    try:
        resp = kms.list_resource_tags(KeyId=key_id)
        tags = resp.get("Tags", [])
        return {t["TagKey"]: t["TagValue"] for t in tags}
    except ClientError:
        return {}

def get_glue_tags(glue, sts, region: str, account: str, job_name: str) -> Dict[str, str]:
    # Glue get_tags requires resource ARN: arn:aws:glue:{region}:{account}:job/{job_name}
    arn = f"arn:aws:glue:{region}:{account}:job/{job_name}"
    try:
        resp = glue.get_tags(ResourceArn=arn)
        return resp.get("Tags", {}) or {}
    except ClientError:
        return {}

def get_secretsmanager_tags(secretsmanager, secret_id: str) -> Dict[str, str]:
    try:
        resp = secretsmanager.list_tags_for_resource(SecretId=secret_id)
        tags = resp.get("Tags", [])
        return {t["Key"]: t["Value"] for t in tags}
    except ClientError:
        return {}

def get_ec2_tags(ec2, resource_id: str) -> Dict[str, str]:
    try:
        resp = ec2.describe_tags(Filters=[{"Name": "resource-id", "Values": [resource_id]}])
        tags = resp.get("Tags", [])
        return {t["Key"]: t["Value"] for t in tags}
    except ClientError:
        return {}

def has_production_tag(tags: Dict[str, str]) -> bool:
    for k, v in tags.items():
        if not k.startswith("aws:cloudformation") and v == "Production":
            return True
    return False

def _guess_bucket_from_physical_id(physical: str) -> str:
    # often the physical id is the bucket name, but sometimes an ARN is present.
    if physical.startswith("arn:"):
        # try to extract bucket name from arn or from resource path
        # arn:aws:s3:::my-bucket => last part
        parts = physical.split(":")
        # for S3 arn form, bucket name might be after triple colon
        if len(parts) >= 6:
            return parts[-1]
    # fallback: strip potential resource prefix
    return physical

def process_stack_resources(session, stack_name: str, resources: List[Dict[str, Any]], region: Optional[str]):
    cf = session.client("cloudformation")
    s3 = session.client("s3")
    logs = session.client("logs")
    kms = session.client("kms")
    glue = session.client("glue")
    secretsmanager = session.client("secretsmanager")
    ec2 = session.client("ec2")
    sts = session.client("sts")
    account = sts.get_caller_identity().get("Account")

    print(f"--- Stack: {stack_name} ---")
    for r in resources:
        logical = r.get("LogicalResourceId")
        if logical == "CDKMetadata":
            continue
        rtype = r.get("ResourceType")
        physical = r.get("PhysicalResourceId") or ""
        print(f"{rtype} -> logical={logical}, physical={physical}")

        tags = {}
        if rtype == "AWS::S3::BucketPolicy":
            # try to derive bucket name from the physical id
            bucket = _guess_bucket_from_physical_id(physical)
            tags = get_s3_bucket_tags(s3, bucket)
        elif rtype == "AWS::Logs::LogGroup":
            tags = get_log_group_tags(logs, physical)
        elif rtype == "AWS::KMS::Key":
            tags = get_kms_tags(kms, physical)
        elif rtype == "AWS::Glue::Job":
            tags = get_glue_tags(glue, sts, region or session.region_name, account, physical)
        elif rtype == "AWS::SecretsManager::Secret":
            tags = get_secretsmanager_tags(secretsmanager, physical)
        elif rtype == "AWS::EC2::SecurityGroup":
            tags = get_ec2_tags(ec2, physical)
        else:
            # unknown resource type can be extended easily
            continue

        if not tags:
            print("  No tags returned or access error.")
        else:
            print(f"  Tags: {json.dumps(tags)}")
            if has_production_tag(tags):
                print("  => Has Production tag (non-cloudformation key).")
            else:
                print("  => DOES NOT have Production tag (non-cloudformation key).")

def main():
    parser = argparse.ArgumentParser(description="Dynamic CDK stack tag checker")
    parser.add_argument("--app", default="python app.py", help="CDK --app value (example: \"python app.py\")")
    parser.add_argument("--profile", default=None, help="AWS profile name (optional)")
    parser.add_argument("--region", default=None, help="AWS region (optional)")
    parser.add_argument("--stacks", nargs="*", help="Optional list of stacks to check (overrides cdk list)")
    args = parser.parse_args()

    stacks = args.stacks or run_cdk_list(args.app)
    if not stacks:
        print("No stacks found.", file=sys.stderr)
        sys.exit(1)

    session = make_session(args.profile, args.region)
    cf = session.client("cloudformation")
    for stack in stacks:
        try:
            resources = list_stack_resources(cf, stack)
            process_stack_resources(session, stack, resources, args.region)
        except ClientError as e:
            print(f"Error processing stack {stack}: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()