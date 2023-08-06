import yaml
import pathlib


def load_yaml(path: pathlib.Path) -> dict:
    """
    Load a YAML file
    """
    with open(path, 'r') as stream:
        return yaml.safe_load(stream)
        
    
def load_toml(path: pathlib.Path) -> dict:
    """
    Load a TOML file
    """
    with open(path, 'r') as stream:
        return {}


def load_json(path: pathlib.Path) -> dict:
    """
    Load a JSON file
    """
    with open(path, 'r') as stream:
        return {}
