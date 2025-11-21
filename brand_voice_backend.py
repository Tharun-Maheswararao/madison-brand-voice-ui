# brand_voice_backend.py

import os
import requests
from typing import Dict, Any

# This will come from an environment variable / Streamlit secret
N8N_BRAND_VOICE_WEBHOOK_URL = os.getenv("N8N_BRAND_VOICE_WEBHOOK_URL")


class BrandVoiceBackendError(Exception):
    """Custom error type for backend issues."""
    pass


def _unwrap_n8n_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Your n8n response currently looks like:
        {"object Object": [ { ...actual data... } ] }

    This function unwraps it so Streamlit gets just:
        { ...actual data... }
    """
    if "object Object" in raw and isinstance(raw["object Object"], list):
        items = raw["object Object"]
        if items:
            return items[0]
    return raw


def generate_brand_voice(
    brand_name: str,
    brand_info: str,
    audience: str,
    offer: str,
) -> Dict[str, Any]:
    """
    Calls your n8n Brand Voice Generator workflow.

    Expects n8n to return a JSON object with keys like:
      timestamp, brandName, audience, offer, tone,
      voice_description, keywords_to_use, phrases_to_avoid,
      emotional_angle, selling_points, website_headline,
      website_subheadline, website_bullets, newsletter_email,
      voice_script_for_sales_calls
    """

    if not N8N_BRAND_VOICE_WEBHOOK_URL:
        raise BrandVoiceBackendError(
            "N8N_BRAND_VOICE_WEBHOOK_URL is not set. "
            "Set it in your environment or Streamlit secrets."
        )

    payload = {
        "brandName": brand_name,
        "brandInfo": brand_info,
        "audience": audience,
        "offer": offer,
    }

    try:
        resp = requests.post(
            N8N_BRAND_VOICE_WEBHOOK_URL,
            json=payload,
            timeout=90,
        )
    except requests.RequestException as e:
        raise BrandVoiceBackendError(f"Error calling n8n webhook: {e}") from e

    if resp.status_code >= 400:
        raise BrandVoiceBackendError(
            f"n8n returned HTTP {resp.status_code}: {resp.text}"
        )

    try:
        data = resp.json()
    except ValueError:
        raise BrandVoiceBackendError("n8n response was not valid JSON.")

    # unwrap {"object Object": [ { ... } ]}
    data = _unwrap_n8n_payload(data)
    return data
