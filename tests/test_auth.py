import unittest
from fastapi import HTTPException
from auth import authenticate_gateway_request

class TestAuthenticationShield(unittest.TestCase):
    def test_auth_rejection_on_invalid_keys(self) -> None:
        with self.assertRaises(HTTPException) as ctx:
            authenticate_gateway_request("sk-invalid-malicious-attacker-token")
        self.assertEqual(ctx.exception.status_code, 401)