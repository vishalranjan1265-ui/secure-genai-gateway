import logging
from typing import Any
import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger("SecureGateway.IAM")

class IAMContextResolver:
    def __init__(self, region_name: str = "us-east-1") -> None:
        self.region = region_name

    def resolve_session_client(self) -> boto3.Session:
        try:
            # Resolves native runtime credentials via task profiles or OIDC configurations
            session = boto3.Session(region_name=self.region)
            sts = session.client("sts")
            identity = sts.get_caller_identity()
            logger.info(f"Verified IAM execution credentials context: {identity.get('Arn')}")
            return session
        except ClientError as e:
            logger.error(f"Failed to verify IAM environment contexts bounds: {str(e)}")
            raise