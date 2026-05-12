from pydantic import BaseModel
import os
from typing import Optional

class PaymentProviderConfig(BaseModel):
    provider_name: str
    api_key: str
    base_url: str = "https://api.example.com"

    @classmethod
    def from_env(cls, provider_name: str) -> "PaymentProviderConfig":
        """
        Loads configuration for a specific provider from environment variables.
        Expected format: PAYMENT_{PROVIDER_NAME}_API_KEY, PAYMENT_{PROVIDER_NAME}_BASE_URL
        """
        prefix = f"PAYMENT_{provider_name.upper()}_"
        return cls(
            provider_name=provider_name,
            api_key=os.getenv(f"{prefix}API_KEY", ""),
            base_url=os.getenv(f"{prefix}BASE_URL", "https://api.example.com")
        )
