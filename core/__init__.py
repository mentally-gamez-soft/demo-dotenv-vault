"""Configure the application with envs."""

from core.app_config.config import EnvLoader

# Expose Config object to the application
env_loader = EnvLoader()
env_loader.get_env_config()