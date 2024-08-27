import boto3

class VMManager:
    def __init__(self):
        self.ec2_client = boto3.client('ec2')

    def create(self, resource):
        config = resource['config']
        print(f"Creating VM: {resource['name']}")
        print(f"  Instance Type: {config['instance_type']}")
        print(f"  AMI ID: {config['ami_id']}")
        print(f"  Region: {config['region']}")

        if config.get('provider') == 'aws':
            print("Creating AWS VM. Disabled for now.")
            #return self.create_aws_vm(resource)
        else:
            print(f"Unsupported provider for VM: {config.get('provider')}")

    def update(self, resource):
        config = resource['config']
        print(f"Updating VM: {resource['name']}")
        print(f"  Instance Type: {config['instance_type']}")
        print(f"  AMI ID: {config['ami_id']}")
        print(f"  Region: {config['region']}")

        if config.get('provider') == 'aws':
            print("Updating AWS VM. Disabled for now.")
            #return self.update_aws_vm(resource)
        else:
            print(f"Unsupported provider for VM: {config.get('provider')}")

    def delete(self, resource):
        config = resource['config']
        print(f"Deleting VM: {resource['name']}")

        if config.get('provider') == 'aws':
            print("Deleting AWS VM. Disabled for now.")
            #return self.delete_aws_vm(resource)
        else:
            print(f"Unsupported provider for VM: {config.get('provider')}")

    def create_aws_vm(self, resource):
        config = resource['config']
        try:
            response = self.ec2_client.run_instances(
                ImageId=config['ami_id'],
                InstanceType=config['instance_type'],
                MinCount=1,
                MaxCount=1,
                KeyName=config.get('key_name'),
                SecurityGroupIds=config.get('security_group_ids', []),
                SubnetId=config.get('subnet_id'),
                TagSpecifications=[
                    {
                        'ResourceType': 'instance',
                        'Tags': [
                            {
                                'Key': 'Name',
                                'Value': resource['name']
                            },
                        ]
                    },
                ]
            )
            instance_id = response['Instances'][0]['InstanceId']
            print(f"Created EC2 instance: {instance_id}")
            return {'instance_id': instance_id}
        except Exception as e:
            print(f"Error creating AWS VM: {str(e)}")
            raise

    def update_aws_vm(self, resource):
        config = resource['config']
        try:
            # Update instance type
            self.ec2_client.modify_instance_attribute(
                InstanceId=config['instance_id'],
                InstanceType={'Value': config['instance_type']}
            )

            # Update tags
            self.ec2_client.create_tags(
                Resources=[config['instance_id']],
                Tags=[{'Key': 'Name', 'Value': resource['name']}]
            )

            print(f"Updated EC2 instance: {config['instance_id']}")
            return {'instance_id': config['instance_id']}
        except Exception as e:
            print(f"Error updating AWS VM: {str(e)}")
            raise

    def delete_aws_vm(self, resource):
        config = resource['config']
        try:
            self.ec2_client.terminate_instances(InstanceIds=[config['instance_id']])
            print(f"Terminated EC2 instance: {config['instance_id']}")
            return {'message': f"Deleted VM {resource['name']}"}
        except Exception as e:
            print(f"Error deleting AWS VM: {str(e)}")
            raise