"""Consent-gated HubSpot contact creation with a server-side private-app token."""

from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class HubSpotLeadRejected(RuntimeError):
    """HubSpot definitely refused the lead request."""


class HubSpotLeadUncertain(RuntimeError):
    """The provider outcome cannot be confirmed safely."""


@dataclass(frozen=True)
class HubSpotSettings:
    private_app_token: str

    @classmethod
    def from_environment(cls, environment: Mapping[str, str]) -> "HubSpotSettings":
        token = environment.get("HUBSPOT_PRIVATE_APP_TOKEN")
        if not token:
            raise ValueError("missing HubSpot configuration: HUBSPOT_PRIVATE_APP_TOKEN")
        return cls(token)


@dataclass(frozen=True)
class HubSpotLeadRequest:
    name: str
    email: str
    consent: bool


class HubSpotClient:
    """Minimal client that sends only the explicitly consented lead fields."""

    def __init__(self, settings: HubSpotSettings, request: Callable[[Request, float], object] = urlopen) -> None:
        self._settings = settings
        self._request = request

    def create_lead(self, lead: HubSpotLeadRequest) -> str:
        if not lead.consent:
            raise HubSpotLeadRejected("consent_required")
        payload = json.dumps({"properties": {"firstname": lead.name, "email": lead.email}}).encode("utf-8")
        request = Request(
            "https://api.hubapi.com/crm/v3/objects/contacts",
            data=payload,
            headers={"Accept": "application/json", "Authorization": f"Bearer {self._settings.private_app_token}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with self._request(request, timeout=10.0) as response:
                body = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            raise HubSpotLeadRejected(f"hubspot_rejected_{error.code}") from error
        except (TimeoutError, URLError, OSError, ValueError, json.JSONDecodeError) as error:
            raise HubSpotLeadUncertain("hubspot_request_outcome_unknown") from error
        contact_id = body.get("id")
        if not isinstance(contact_id, str) or not contact_id:
            raise HubSpotLeadUncertain("hubspot_response_missing_contact_id")
        return contact_id
