import yaml
from utils.exceptions import ConfigurationError

class ConfigParser:
    @staticmethod
    def parse(config_file):
        try:
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)
            ConfigParser.validate(config)
            return config
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Error parsing YAML file: {e}")

    @staticmethod
    def validate(config):
        if 'resources' not in config or not isinstance(config['resources'], list):
            raise ConfigurationError("Configuration must contain a 'resources' list")

        for resource in config['resources']:
            if 'type' not in resource or 'name' not in resource or 'config' not in resource:
                raise ConfigurationError("Each resource must have 'type', 'name', and 'config' fields")

            if resource['type'] == 'virtual_machine':
                ConfigParser.validate_vm(resource['config'])
            elif resource['type'] == 'network':
                ConfigParser.validate_network(resource['config'])
            elif resource['type'] == 'database':
                ConfigParser.validate_database(resource['config'])
            else:
                raise ConfigurationError(f"Unknown resource type: {resource['type']}")

    @staticmethod
    def validate_vm(config):
        required_fields = ['instance_type', 'ami_id', 'region']
        for field in required_fields:
            if field not in config:
                raise ConfigurationError(f"Virtual machine configuration missing required field: {field}")

    @staticmethod
    def validate_network(config):
        if 'vpc_cidr' not in config or 'subnets' not in config:
            raise ConfigurationError("Network configuration must include 'vpc_cidr' and 'subnets'")
        for subnet in config['subnets']:
            if 'name' not in subnet or 'cidr' not in subnet or 'availability_zone' not in subnet:
                raise ConfigurationError("Each subnet must have 'name', 'cidr', and 'availability_zone'")

    @staticmethod
    def validate_database(config):
        required_fields = ['engine', 'engine_version', 'instance_class', 'allocated_storage', 'master_username', 'master_password']
        for field in required_fields:
            if field not in config:
                raise ConfigurationError(f"Database configuration missing required field: {field}")