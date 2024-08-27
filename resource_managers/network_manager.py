import boto3

class NetworkManager:
    def __init__(self):
        self.ec2_client = boto3.client('ec2')
        self.ec2_resource = boto3.resource('ec2')

    def create(self, resource):
        config = resource['config']
        print(f"Creating Network: {resource['name']}")
        print(f"  VPC CIDR: {config['vpc_cidr']}")
        for subnet in config['subnets']:
            print(f"  Subnet: {subnet['name']}")
            print(f"    CIDR: {subnet['cidr']}")
            print(f"    AZ: {subnet['availability_zone']}")

        if config.get('provider') == 'aws':
            print("Creating AWS network. Disabled for now.")
            #return self.create_aws_network(resource)
        else:
            print(f"Unsupported provider for network: {config.get('provider')}")

    def update(self, resource):
        config = resource['config']
        print(f"Updating Network: {resource['name']}")
        print(f"  VPC CIDR: {config['vpc_cidr']}")
        for subnet in config['subnets']:
            print(f"  Subnet: {subnet['name']}")
            print(f"    CIDR: {subnet['cidr']}")
            print(f"    AZ: {subnet['availability_zone']}")

        if config.get('provider') == 'aws':
            print("Updating AWS network. Disabled for now.")
            #return self.update_aws_network(resource)
        else:
            print(f"Unsupported provider for network: {config.get('provider')}")

    def delete(self, resource):
        config = resource['config']
        print(f"Deleting Network: {resource['name']}")

        if config.get('provider') == 'aws':
            print("Deleting AWS network. Disabled for now.")
            #return self.delete_aws_network(resource)
        else:
            print(f"Unsupported provider for network: {config.get('provider')}")

    def create_aws_network(self, resource):
        config = resource['config']
        try:
            # Create VPC
            vpc = self.ec2_resource.create_vpc(CidrBlock=config['vpc_cidr'])
            vpc.create_tags(Tags=[{'Key': 'Name', 'Value': resource['name']}])
            vpc.wait_until_available()
            print(f"Created VPC: {vpc.id}")

            # Create Internet Gateway
            igw = self.ec2_resource.create_internet_gateway()
            vpc.attach_internet_gateway(InternetGatewayId=igw.id)
            print(f"Created and attached Internet Gateway: {igw.id}")

            # Create subnets
            for subnet_config in config['subnets']:
                subnet = vpc.create_subnet(
                    CidrBlock=subnet_config['cidr'],
                    AvailabilityZone=subnet_config['availability_zone']
                )
                subnet.create_tags(Tags=[{'Key': 'Name', 'Value': subnet_config['name']}])
                print(f"Created Subnet: {subnet.id}")

            # Create route table and add public route
            route_table = vpc.create_route_table()
            route_table.create_route(
                DestinationCidrBlock='0.0.0.0/0',
                GatewayId=igw.id
            )
            print(f"Created Route Table: {route_table.id}")

            return {
                'vpc_id': vpc.id,
                'igw_id': igw.id,
                'subnet_ids': [subnet.id for subnet in vpc.subnets.all()],
                'route_table_id': route_table.id
            }

        except Exception as e:
            print(f"Error creating AWS network: {str(e)}")
            raise

    def update_aws_network(self, resource):
        config = resource['config']
        try:
            print(f"Updating AWS network {resource['name']} is not implemented.")
            print("To modify a VPC, you typically need to add or remove subnets, update route tables, etc.")
            return None
        except Exception as e:
            print(f"Error updating AWS network: {str(e)}")
            raise

    def delete_aws_network(self, resource):
        config = resource['config']
        try:
            vpc = self.ec2_resource.Vpc(config['vpc_id'])

            # Delete subnets
            for subnet in vpc.subnets.all():
                subnet.delete()
                print(f"Deleted Subnet: {subnet.id}")

            # Detach and delete internet gateway
            for igw in vpc.internet_gateways.all():
                vpc.detach_internet_gateway(InternetGatewayId=igw.id)
                igw.delete()
                print(f"Deleted Internet Gateway: {igw.id}")

            # Delete route tables
            for rt in vpc.route_tables.all():
                if not rt.associations_attribute:
                    rt.delete()
                    print(f"Deleted Route Table: {rt.id}")

            # Delete VPC
            vpc.delete()
            print(f"Deleted VPC: {vpc.id}")

            return {'message': f"Deleted network {resource['name']}"}

        except Exception as e:
            print(f"Error deleting AWS network: {str(e)}")
            raise