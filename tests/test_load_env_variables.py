import unittest
from core import env_loader

class TestLoadEnvVariables(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def test_load_env_for_local_dev(self):
        if not env_loader.is_application_executed_on_cicd_runner():
            self.assertEqual(env_loader.get("APP_ENV"), "local.dev","The local dev APP_ENV variable is not set")

    def test_load_env_for_cicd(self):
        if env_loader.is_application_executed_on_cicd_runner():
            self.assertEqual(env_loader.get("APP_ENV"), "cicd_runner","The local dev APP_ENV variable is not set")

