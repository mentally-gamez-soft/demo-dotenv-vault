import unittest
from core import env_loader
from core.services.spam_ham_scoring_ws.api_email_scoring import get_payload_spam_ham

class TestLoadEnvVariables(unittest.TestCase):

    def setUp(self) -> None:
        self.spam_email = "Nobody Beats Our Pricing And Quality. #1 Rated Backlink Building SEO Agency. Get Started.\
                            1,500+ SEO's Use Our Backlink Service Every Month To Power Their SEO Campaign.\
                            \
                            Our backlink service is used and trusted by 1,500+ digital marketing agencies to power their clients SEO. Whether you're a business owner or an agency, we can help propel your SEO.\
                            \
                            Check out for the Best SEO LINK BUILDING Packages: https://alwaysdigital.co/lgt/\
                            \
                            \
                            kindra.hugo24@gmail.com"
        
        self.ham_email = "Hola Paulo que tal,\
                            Mira te contacto para verificar contigo si ma;ana podriamos vernos sobre las 11.\
                            \
                            De hecho, por de momento sigo fuera de Madrid asi que no veo otra manera.\
                            \
                            Te agradezco de antemano. \
                            Benedicto V."
        return super().setUp()

    def test_load_env_for_local_dev(self):
        if not env_loader.is_application_executed_on_cicd_runner():
            print("test dev local executed")
            self.assertEqual(env_loader.get("APP_ENV"), "local.dev","The local dev APP_ENV variable is not set")

    def test_load_env_for_cicd(self):
        if env_loader.is_application_executed_on_cicd_runner():
            print("test ci_cd executed")
            self.assertEqual(env_loader.get("APP_ENV"), "cicd_runner","The local dev APP_ENV variable is not set")

    def test_email_is_spam(self):
        self.assertEqual(get_payload_spam_ham(self.spam_email).get("classification"),"spam","The email message was expected to be a SPAM and the verification failed.")

    def test_email_is_ham(self):
        self.assertEqual(get_payload_spam_ham(self.ham_email).get("classification"),"ham","The email message was expected to be a HAM and the verification failed.")
