import argparse
import os
from config_parser import ConfigParser
from resource_managers import VMManager, NetworkManager, DatabaseManager
from state_manager import StateManager
from config_parser import ConfigParser
from resource_managers.vm_manager import VMManager
from resource_managers.network_manager import NetworkManager
from resource_managers.database_manager import DatabaseManager
from state_manager import StateManager

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="IaC Tool")
        self.setup_arguments()
        self.config_parser = ConfigParser()
        self.state_manager = StateManager()
        self.resource_managers = {
            'virtual_machine': VMManager(),
            'network': NetworkManager(),
            'database': DatabaseManager()
        }

    def setup_arguments(self):
        self.parser.add_argument('action', choices=['apply', 'plan', 'destroy'], help='Action to perform')
        self.parser.add_argument('config_file', help='Path to the YAML configuration file')

    def run(self):
        args = self.parser.parse_args()
        if not os.path.exists(args.config_file):
            print(f"Error: Configuration file not found: {args.config_file}")
            return

        if args.action == 'apply':
            self.apply(args.config_file)
        elif args.action == 'plan':
            self.plan(args.config_file)
        elif args.action == 'destroy':
            self.destroy(args.config_file)

    def apply(self, config_file):
        config = self.config_parser.parse(config_file)
        current_state = self.state_manager.load_state()
        
        for resource in config['resources']:
            resource_type = resource['type']
            if resource_type in self.resource_managers:
                manager = self.resource_managers[resource_type]
                if resource['name'] in current_state.get(resource_type, {}):
                    manager.update(resource)
                else:
                    manager.create(resource)
            else:
                print(f"Warning: Unknown resource type '{resource_type}'")

        self.state_manager.save_state(config['resources'])

    def plan(self, config_file):
        config = self.config_parser.parse(config_file)
        current_state = self.state_manager.load_state()
        
        for resource in config['resources']:
            resource_type = resource['type']
            if resource_type in self.resource_managers:
                manager = self.resource_managers[resource_type]
                if resource['name'] in current_state.get(resource_type, {}):
                    print(f"Would update {resource_type}: {resource['name']}")
                else:
                    print(f"Would create {resource_type}: {resource['name']}")
            else:
                print(f"Warning: Unknown resource type '{resource_type}'")

    def destroy(self, config_file):
        config = self.config_parser.parse(config_file)
        current_state = self.state_manager.load_state()
        
        for resource in config['resources']:
            resource_type = resource['type']
            if resource_type in self.resource_managers:
                manager = self.resource_managers[resource_type]
                if resource['name'] in current_state.get(resource_type, {}):
                    manager.delete(resource)
                    self.state_manager.remove_resource(resource_type, resource['name'])
                else:
                    print(f"Resource does not exist: {resource_type} - {resource['name']}")
            else:
                print(f"Warning: Unknown resource type '{resource_type}'")