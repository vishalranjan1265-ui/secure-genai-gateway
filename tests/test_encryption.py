import unittest
import os
from unittest.mock import patch
from encryption import PayloadEncryptor

class TestCryptographicModuleBounds(unittest.TestCase):
    def test_symmetric_encryption_loop_integrity(self) -> None:
        encryptor = PayloadEncryptor()
        secret_payload = "Sensitive system instruction sequence data values strings."
        
        cipher = encryptor.encrypt_data_string(secret_payload)
        decrypted = encryptor.decrypt_data_string(cipher)
        
        self.assertNotEqual(secret_payload, cipher)
        self.assertEqual(secret_payload, decrypted)