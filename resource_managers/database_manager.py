import boto3

class DatabaseManager:
    def __init__(self):
        self.aws_client = boto3.client('rds')

    def create(self, resource):
        config = resource['config']
        print(f"Creating Database: {resource['name']}")
        print(f"  Engine: {config['engine']} {config['engine_version']}")
        print(f"  Instance Class: {config['instance_class']}")
        print(f"  Allocated Storage: {config['allocated_storage']} GB")

        if config.get('provider') == 'aws':
            print("Creating AWS database. Disabled for now.")
            #self.create_aws_database(resource)
        elif config.get('provider') == 'azure':
            # Add Azure provider
            pass
        else:
            print(f"Unsupported provider for database: {config.get('provider')}")

    def update(self, resource):
        config = resource['config']
        print(f"Updating Database: {resource['name']}")
        print(f"  Engine: {config['engine']} {config['engine_version']}")
        print(f"  Instance Class: {config['instance_class']}")
        print(f"  Allocated Storage: {config['allocated_storage']} GB")

        if config.get('provider') == 'aws':
            print("Updating AWS database. Disabled for now.")
            #self.update_aws_database(resource)
        elif config.get('provider') == 'azure':
            # Add Azure provider
            pass
        else:
            print(f"Unsupported provider for database: {config.get('provider')}")

    def delete(self, resource):
        config = resource['config']
        print(f"Deleting Database: {resource['name']}")

        if config.get('provider') == 'aws':
            print("Deleting AWS database. Disabled for now.")
            #self.delete_aws_database(resource)
        elif config.get('provider') == 'azure':
            # Add Azure provider
            pass
        else:
            print(f"Unsupported provider for database: {config.get('provider')}")

    def create_aws_database(self, resource):
        config = resource['config']
        try:
            response = self.aws_client.create_db_instance(
                DBInstanceIdentifier=resource['name'],
                Engine=config['engine'],
                EngineVersion=config['engine_version'],
                DBInstanceClass=config['instance_class'],
                AllocatedStorage=config['allocated_storage'],
                MasterUsername=config['master_username'],
                MasterUserPassword=config['master_password'],
                VpcSecurityGroupIds=config.get('vpc_security_group_ids', []),
                DBSubnetGroupName=config.get('subnet_group'),
                MultiAZ=config.get('multi_az', False),
                PubliclyAccessible=config.get('publicly_accessible', False)
            )
            print(f"AWS RDS instance {resource['name']} creation initiated.")
            return response
        except Exception as e:
            print(f"Error creating AWS RDS instance: {str(e)}")

    def update_aws_database(self, resource):
        config = resource['config']
        try:
            response = self.aws_client.modify_db_instance(
                DBInstanceIdentifier=resource['name'],
                EngineVersion=config['engine_version'],
                DBInstanceClass=config['instance_class'],
                AllocatedStorage=config['allocated_storage'],
                MultiAZ=config.get('multi_az', False),
                PubliclyAccessible=config.get('publicly_accessible', False)
            )
            print(f"AWS RDS instance {resource['name']} update initiated.")
            return response
        except Exception as e:
            print(f"Error updating AWS RDS instance: {str(e)}")

    def delete_aws_database(self, resource):
        try:
            response = self.aws_client.delete_db_instance(
                DBInstanceIdentifier=resource['name'],
                SkipFinalSnapshot=True
            )
            print(f"AWS RDS instance {resource['name']} deletion initiated.")
            return response
        except Exception as e:
            print(f"Error deleting AWS RDS instance: {str(e)}")