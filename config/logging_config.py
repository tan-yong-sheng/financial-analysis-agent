import logging
import logging.config
import os
import json
from datetime import datetime

def setup_logging(
    default_level=logging.INFO,
    log_dir="logs",
    config_file="config/logging.json",
    env_key="LOG_CONFIG"
):
    """Setup logging configuration."""
    path = config_file
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        # Add timestamp to file handlers
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        for handler in config.get("handlers", {}).values():
            if handler.get("filename"):
                os.makedirs(log_dir, exist_ok=True)
                handler["filename"] = os.path.join(log_dir, f"{timestamp}_{os.path.basename(handler['filename'])}")
        logging.config.dictConfig(config)
    else:
        # Basic configuration if no config file
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            level=default_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, f"{timestamp}_app.log")),
                logging.StreamHandler()
            ]
        )
