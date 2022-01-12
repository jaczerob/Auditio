from typing import Dict, Any

import yaml


with open('config.yaml', 'r') as file:
    config: Dict[str, Any] = yaml.load(file, Loader=yaml.FullLoader)