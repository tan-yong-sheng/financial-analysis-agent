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
    """
    Setup enhanced logging configuration with structured logging support.
    
    Args:
        default_level: Default logging level if config fails
        log_dir: Base directory for log files
        config_file: JSON config file path
        env_key: Environment variable key for alternate config
    """
    # Create log directory structure
    log_subdirs = {
        "agents": os.path.join(log_dir, "agents"),
        "api": os.path.join(log_dir, "api"),
        "errors": os.path.join(log_dir, "errors"),
        "general": os.path.join(log_dir, "general")
    }
    
    for subdir in log_subdirs.values():
        os.makedirs(subdir, exist_ok=True)
        
    # Get config file path from environment if specified
    path = os.getenv(env_key, config_file)
    
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
            
        # Add timestamp and update paths for file handlers
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        for handler_name, handler in config.get("handlers", {}).items():
            if handler.get("filename"):
                # Map handlers to appropriate subdirectories
                if "agent" in handler_name:
                    subdir = "agents"
                elif "api" in handler_name:
                    subdir = "api"
                elif "error" in handler_name:
                    subdir = "errors"
                else:
                    subdir = "general"
                    
                # Update handler filename with timestamp and proper directory
                base_filename = os.path.basename(handler["filename"])
                handler["filename"] = os.path.join(
                    log_subdirs[subdir],
                    f"{timestamp}_{base_filename}"
                )
                
        try:
            logging.config.dictConfig(config)
            logging.getLogger("setup").info(
                "Logging configuration loaded successfully",
                extra={
                    "config_file": path,
                    "log_dir": log_dir,
                    "timestamp": timestamp
                }
            )
        except Exception as e:
            print(f"Error loading logging configuration: {str(e)}")
            _setup_basic_logging(default_level, log_dir, timestamp)
    else:
        print(f"Logging config file not found at {path}")
        _setup_basic_logging(default_level, log_dir, timestamp)

def _setup_basic_logging(level, log_dir, timestamp):
    """Setup basic logging if config fails."""
    basic_log_file = os.path.join(log_dir, "general", f"{timestamp}_fallback.log")
    os.makedirs(os.path.dirname(basic_log_file), exist_ok=True)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(basic_log_file),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger("setup")
    logger.warning(
        "Falling back to basic logging configuration",
        extra={
            "log_file": basic_log_file,
            "level": level
        }
    )
