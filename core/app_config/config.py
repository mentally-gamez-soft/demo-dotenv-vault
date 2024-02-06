"""Configuration file for the application."""

import os
from io import StringIO
from os import environ as env

import dotenv_vault.main as vault
from dotenv import load_dotenv as std_load_dotenv
from dotenv_vault import load_dotenv as load_dotenv_vault

GITHUB_CICD_ENV = "cicd_runner"
LOCAL_DEV_ENV = "local.dev"

class ConfigurationNotFoundException(Exception):
    """Raised when the configuration files of the application is not available."""

    pass


class EnvLoader:
    """Load the environment variables."""

    def __init__(self, env_path: str = ".") -> None:
        """Init the env variables.

        Args:
            env_path (str, optional): the path to the application .env file. Defaults to '.'.
        """
        self.app_env_path = env_path
        self.vault = vault
        self.env = env

    def __check_available_env(self) -> bool:
        if not self.env["APP_ENV"]:
            raise ConfigurationNotFoundException(
                "The APP_ENV variable is not set."
            )

        if self.env["APP_ENV"] == GITHUB_CICD_ENV:
            return True

        elif not os.path.exists(os.path.join(self.app_env_path, ".env.keys")):
            raise ConfigurationNotFoundException(
                "The .env.keys file does not exists in the environment."
            )

    def __load_appplication_physical_environment(self):
        """Load the APP_ENV variable which determines on which physical system the application is currently running"""
        std_load_dotenv(os.path.join(self.app_env_path, ".env.app_env"))

    def __load_env_keys(self) -> bool:
        return std_load_dotenv(os.path.join(self.app_env_path, ".env.keys")) 

    def __load_env(self) -> bool:
        """Load all the environment variables and the keys pass.

        Returns:
            bool: True if the environment variables are loaded, False otherwise
        """
        self.__load_appplication_physical_environment()
        if env["APP_ENV"] == GITHUB_CICD_ENV:
            return True
        
        try:
            self.__check_available_env()
        except ConfigurationNotFoundException:
            return False

        return self.__load_env_keys() 

    def __init_env_key(self) -> str:
        """Load all the encrypted environment variables.

        Returns:
            str: The encrypted env variable
        """

        if self.env["APP_ENV"] in (LOCAL_DEV_ENV):
            self.env["DOTENV_KEY"] = self.env.get("DOTENV_KEY_DEV")

        return self.env["DOTENV_KEY"]

    def __load_decyphered_env(self):
        if not std_load_dotenv(os.path.join(self.app_env_path, ".env.vault")):
            raise ConfigurationNotFoundException(
                "The .env.vault file does not exists"
            )

        try:
            dot_env_vault = None
            if self.env["APP_ENV"] in (LOCAL_DEV_ENV):
                dot_env_vault = self.env["DOTENV_VAULT_DEV"]

            if dot_env_vault is None:
                raise ConfigurationNotFoundException(
                    "The .env.vault file does not exists"
                )

            stream = self.vault.parse_vault(StringIO(dot_env_vault))
            load_dotenv_vault(stream=stream, override=False)
        finally:
            os.unsetenv("DOTENV_KEY")  # erase the keys from the knowledge of the application (system memory)

    def get_env_config(self):
        """Load the environment variables of the application."""
        if self.__load_env():
            if self.env["APP_ENV"] != GITHUB_CICD_ENV:
                self.__init_env_key()
                self.__load_decyphered_env()
        else:
            raise ConfigurationNotFoundException(
                "The .env.keys file does not exists"
            )
        
    def get(self,key:str) -> str:
        return self.env.get(key)
    
    def is_application_executed_on_cicd_runner(self) -> bool:
        return GITHUB_CICD_ENV in self.env.get("APP_ENV")
