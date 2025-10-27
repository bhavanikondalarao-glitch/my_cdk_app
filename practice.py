import json 
import subprocess

with open(f"Mys3stack_resources.json", "r") as resource_file:
    resources = json.load(resource_file)  # This gives you a Python dict
   
    resource_summary = resources.get("StackResourceSummaries", [])
   
    for resource_part in resource_summary:
      
       
        if not resource_part.get("LogicalResourceId") == 'CDKMetadata':
            if resource_part.get("ResourceType") == "AWS::S3::BucketPolicy":
                physical_id = resource_part.get("PhysicalResourceId")
                print(f"Bucket Policy Name: {physical_id}")
                logical_id = resource_part.get("LogicalResourceId")
                print(f"Logical Resource ID: {logical_id}")
                # Check if any tag value is "Production" and key does not start with "aws:cloudformation"
                with open("bucket_tags.txt", "w") as tag_file:
                    subprocess.run(f"aws s3api get-bucket-tagging --bucket {physical_id}", stdout=tag_file)
                with open("bucket_tags.txt", "r") as tag_file:
                    tags_response = json.load(tag_file)
                    print(f"tags_response: {tags_response}")
                    tags = tags_response.get("TagSet", [])
                    print(f"Tags for Bucket Policy {physical_id}: {tags}")
                    for tag_list in tags:
                        key = tag_list.get("Key")
                        value = tag_list.get("Value")
                        print(f"Key: {key}, Value: {value}")
                        if not key.startswith("aws:cloudformation:stack") and value == "Production":
                            print(f"Bucket Policy {physical_id} has a Production tag.")
                        else:
                            print(f"Bucket Policy {physical_id} does NOT have a Production tag.")
                   

###############################################
import subprocess
import json
with open("stacks.txt", "w") as outfile:
    subprocess.run(["cdk", "list", "--app=python app.py"], stdout=outfile, shell=True)
    
#aws cloudformation list-stack-resources --stack-name MyCdkAppStack

with open("stacks.txt", 'r') as f:
    for line in f:
        stack_name = line.strip()
        print(f"Resources in stack {stack_name}:")
        with open(f"{stack_name}_resources.json", "w") as resource_file:
            print(f"Fetching resources for stack: {stack_name}")
            subprocess.run(["aws", "cloudformation", "list-stack-resources", "--stack-name", stack_name], stdout=resource_file)
with open(f"stacks.txt", 'r') as f:
    for stack in f:
        stack_name = stack.strip() 
        with open(f"{stack_name}_resources.json", "r") as resource_file:
            resources = json.load(resource_file)  # This gives you a Python dict
            print(resources)
            resource_summary = resources.get("StackResourceSummaries", [])
            for resource_part in resource_summary:
               if not resource_part.get("LogicalResourceId") == 'CDKMetadata':
                # check for s3 bucket tags
                if resource_part.get("ResourceType") == "AWS::S3::BucketPolicy":
                    physical_id = resource_part.get("PhysicalResourceId")
                    print(f"Bucket Policy Name: {physical_id}")
                    logical_id = resource_part.get("LogicalResourceId")
                    print(f"Logical Resource ID: {logical_id}")
                    # Check if any tag value is "Production" and key does not start with "aws:cloudformation"
                    with open("bucket_tags.txt", "w") as tag_file:
                        subprocess.run(f"aws s3api get-bucket-tagging --bucket {physical_id}", stdout=tag_file)
                    with open("bucket_tags.txt", "r") as tag_file:
                        tags_response = json.load(tag_file)
                        print(f"tags_response: {tags_response}")
                        tags = tags_response.get("TagSet", [])
                        print(f"Tags for Bucket Policy {physical_id}: {tags}")
                        for tag_list in tags:
                            key = tag_list.get("Key")
                            value = tag_list.get("Value")
                            print(f"Key: {key}, Value: {value}")
                            if not key.startswith("aws:cloudformation:stack") and value == "Production":
                                print(f"Bucket Policy {physical_id} has a Production tag.")
                            else:
                                print(f"Bucket Policy {physical_id} does NOT have a Production tag.")
                # check for log group tags
                if resource_part.get("ResourceType") == "AWS::Logs::LogGroup":
                    physical_id = resource_part.get("PhysicalResourceId")
                    print(f"Log Group Name: {physical_id}")
                    logical_id = resource_part.get("LogicalResourceId")
                    print(f"Logical Resource ID: {logical_id}")
                    # Check if any tag value is "Production" and key does not start with "aws:cloudformation"
                    with open("loggroup_tags.txt", "w") as tag_file:
                        subprocess.run(f"aws logs list-tags-log-group --log-group-name {physical_id}", stdout=tag_file)
                    with open("loggroup_tags.txt", "r") as tag_file:
                        tags_response = json.load(tag_file)
                        tags = tags_response.get("tags", {})
                        print(f"Tags for Log Group {physical_id}: {tags}")
                        found_production = any(
                            not key.startswith("aws:cloudformation") and value == "Production"
                            for key, value in tags.items()
                        )
                        if found_production:
                            print(f"Log Group {physical_id} has a Production tag.")
                        else:
                            print(f"Log Group {physical_id} does NOT have a Production tag.")

                # check for KMS key tags
                if resource_part.get("ResourceType") == "AWS::KMS::Key":
                    physical_id = resource_part.get("PhysicalResourceId")
                    print(f"KMS Key ID: {physical_id}")
                    logical_id = resource_part.get("LogicalResourceId")
                    print(f"Logical Resource ID: {logical_id}")
                    # Check if any tag value is "Production" and key does not start with "aws:cloudformation"
                    with open("kms_tags.txt", "w") as tag_file:
                        subprocess.run(f"aws kms list-resource-tags --key-id {physical_id}", stdout=tag_file)
                    with open("kms_tags.txt", "r") as tag_file:
                        tags_response = json.load(tag_file)
                        tags = tags_response.get("Tags", [])
                        print(f"Tags for KMS Key {physical_id}: {tags}")
                        for tag_list in tags:
                            key = tag_list.get("TagKey")
                            value = tag_list.get("TagValue")
                            print(f"Key: {key}, Value: {value}")
                            if not key.startswith("aws:cloudformation:stack") and value == "Production":
                                print(f"KMS Key {physical_id} has a Production tag.")
                            else:
                                print(f"KMS Key {physical_id} does NOT have a Production tag.")

                #check for glue job tags
                if resource_part.get("ResourceType") == "AWS::Glue::Job":
                    physical_id = resource_part.get("PhysicalResourceId")
                    print(f"Glue Job Name: {physical_id}")
                    logical_id = resource_part.get("LogicalResourceId")
                    print(f"Logical Resource ID: {logical_id}")
                    # Check if any tag value is "Production" and key does not start with "aws:cloudformation"
                    with open("gluejob_tags.txt", "w") as tag_file:
                        subprocess.run(f"aws glue get-tags --resource-arn arn:aws:glue:region:account-id:job/{physical_id}", stdout=tag_file)
                    with open("gluejob_tags.txt", "r") as tag_file:
                        tags_response = json.load(tag_file)
                        tags = tags_response.get("Tags", {})
                        print(f"Tags for Glue Job {physical_id}: {tags}")
                        found_production = any(
                            not key.startswith("aws:cloudformation") and value == "Production"
                            for key, value in tags.items()
                        )
                        if found_production:
                            print(f"Glue Job {physical_id} has a Production tag.")
                        else:
                            print(f"Glue Job {physical_id} does NOT have a Production tag.")

               # check for secret manger secret tags
                if resource_part.get("ResourceType") == "AWS::SecretsManager::Secret":
                    physical_id = resource_part.get("PhysicalResourceId")
                    print(f"Secrets Manager Secret ARN: {physical_id}")
                    logical_id = resource_part.get("LogicalResourceId")
                    print(f"Logical Resource ID: {logical_id}")
                    # Check if any tag value is "Production" and key does not start with "aws:cloudformation"
                    with open("secretsmanager_tags.txt", "w") as tag_file:
                        subprocess.run(f"aws secretsmanager list-tags-for-resource --secret-id {physical_id}", stdout=tag_file)
                    with open("secretsmanager_tags.txt", "r") as tag_file:
                        tags_response = json.load(tag_file)
                        tags = tags_response.get("Tags", [])
                        print(f"Tags for Secrets Manager Secret {physical_id}: {tags}")
                        for tag_list in tags:
                            key = tag_list.get("Key")
                            value = tag_list.get("Value")
                            print(f"Key: {key}, Value: {value}")
                            if not key.startswith("aws:cloudformation:stack") and value == "Production":
                                print(f"Secrets Manager Secret {physical_id} has a Production tag.")
                            else:
                                print(f"Secrets Manager Secret {physical_id} does NOT have a Production tag.")
                                # If no Production tag is found, check for other tags
                # check for security group tags
                if resource_part.get("ResourceType") == "AWS::EC2::SecurityGroup":
                    physical_id = resource_part.get("PhysicalResourceId")
                    print(f"Security Group ID: {physical_id}")
                    logical_id = resource_part.get("LogicalResourceId")
                    print(f"Logical Resource ID: {logical_id}")
                    # Check if any tag value is "Production" and key does not start with "aws:cloudformation"
                    with open("securitygroup_tags.txt", "w") as tag_file:
                        subprocess.run(f"aws ec2 describe-tags --filters Name=resource-id,Values={physical_id}", stdout=tag_file)
                    with open("securitygroup_tags.txt", "r") as tag_file:
                        tags_response = json.load(tag_file)
                        tags = tags_response.get("Tags", [])
                        print(f"Tags for Security Group {physical_id}: {tags}")
                        for tag_list in tags:
                            key = tag_list.get("Key")
                            value = tag_list.get("Value")
                            print(f"Key: {key}, Value: {value}")
                            if not key.startswith("aws:cloudformation:stack") and value == "Production":
                                print(f"Security Group {physical_id} has a Production tag.")
                            else:
                                print(f"Security Group {physical_id} does NOT have a Production tag.")
              