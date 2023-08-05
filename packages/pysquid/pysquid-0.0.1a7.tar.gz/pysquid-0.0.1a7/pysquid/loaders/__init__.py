import yaml
import pathlib


def load_yaml(path: pathlib.Path) -> dict:
    """
    Load a YAML file
    """
    with open(path, 'r') as stream:
        return yaml.safe_load(stream)
        
    
