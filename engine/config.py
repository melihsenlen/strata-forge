import yaml
from pathlib import Path


def load_config(config_path: str = "config.yaml") -> dict:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at {config_path}")
    with open(path) as y:
        return yaml.safe_load(y)

def get_mesh(config: dict) -> Path:
    return Path(config["output"]["mesh_dir"]) / config["output"]["mesh_name"]