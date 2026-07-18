import unittest
from unittest.mock import patch, MagicMock
from gateway import GatewayOrchestratorEngine

class TestGatewayOperationalCore(unittest.TestCase):
    def setUp(self) -> None:
        self.orchestrator = GatewayOrchestratorEngine()

    @patch('llm_client.AmazonBedrockGatewayClient.invoke_model_endpoint')
    def test_end_to_end_successful_path(self, mock_invoke: MagicMock) -> None:
        mock_invoke.return_value = {
            "response_text": "Safe verified response content matrix layout.",
            "token_usage": {"input_tokens": 10, "output_tokens": 12}
        }
        
        result = self.orchestrator.orchestrate_request("Hello model, provide general analytics metrics summaries.")
        self.assertEqual(result["status"], "SUCCESS")
        self.assertIn("output", result)
        self.assertIn("secure_audit_token", result)