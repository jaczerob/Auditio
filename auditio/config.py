from typing import Dict, Any

from loguru import logger
import yaml


with open('config/config.yaml', 'r') as file:
    app_config: Dict[str, Any] = yaml.load(file, Loader=yaml.FullLoader)