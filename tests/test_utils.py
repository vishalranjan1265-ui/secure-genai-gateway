import unittest
from utils import load_gateway_config

class TestUtilityParsers(unittest.TestCase):
    def test_configuration_loading_integrity(self) -> None:
        config = load_gateway_config()
        self.assertIsNotNone(config)
        self.assertIn("global", config)
        self.assertIn("security", config)