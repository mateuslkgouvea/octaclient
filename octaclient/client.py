import time
from typing import Any, Dict, Optional

import httpx

from .errors import (
    APIError,
    AuthenticationError,
    NotFoundError,
    RateLimitError,
    ServerError,
    ValidationError,
)


class OctadeskClient:
    def __init__(
        self,
        api_key: str,
        agent_email: str,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
    ) -> None:
        self.api_key = api_key
        self.agent_email = agent_email
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._client = httpx.Client(base_url=self.base_url, timeout=self.timeout)

    def _default_headers(self) -> Dict[str, str]:
        return {
            "x-api-key": self.api_key,
            "octa-agent-email": self.agent_email,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _raise_for_status(self, response: httpx.Response) -> Any:
        status = response.status_code
        body = None
        try:
            body = response.json()
        except Exception:
            body = response.text

        if 200 <= status < 300:
            return body

        if status == 401:
            raise AuthenticationError("Authentication failed")
        if status == 404:
            raise NotFoundError("Resource not found")
        if status == 400:
            raise ValidationError(body)
        if status == 429:
            retry_after = None
            try:
                retry_after = int(response.headers.get("Retry-After", "0")) or None
            except Exception:
                retry_after = None
            raise RateLimitError("Rate limit exceeded", retry_after=retry_after)
        if 500 <= status < 600:
            raise ServerError(f"Server error ({status})")

        raise APIError(status_code=status, body=body)

    def _request(self, method: str, path: str, json: Optional[Dict] = None, params: Optional[Dict] = None) -> Any:
        url = path if path.startswith("http") else path
        headers = self._default_headers()

        last_exc = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self._client.request(method, url, headers=headers, json=json, params=params)
            except httpx.RequestError as exc:
                last_exc = exc
                if attempt == self.max_retries:
                    raise APIError(status_code=0, message=str(exc)) from exc
                time.sleep(2 ** (attempt - 1))
                continue

            # Retry on transient server errors and rate limits
            if response.status_code in (429, 502, 503, 504) and attempt < self.max_retries:
                retry_after = response.headers.get("Retry-After")
                try:
                    wait = int(retry_after) if retry_after and retry_after.isdigit() else 2 ** (attempt - 1)
                except Exception:
                    wait = 2 ** (attempt - 1)
                time.sleep(wait)
                continue

            return self._raise_for_status(response)

        # If we exit loop unexpectedly
        raise last_exc or APIError(status_code=0, message="Unknown error")

    def get(self, path: str, params: Optional[Dict] = None) -> Any:
        return self._request("GET", path, params=params)

    def post(self, path: str, json: Optional[Dict] = None) -> Any:
        return self._request("POST", path, json=json)

    def put(self, path: str, json: Optional[Dict] = None) -> Any:
        return self._request("PUT", path, json=json)
    
    def patch(self, path: str, json: Optional[Dict] = None) -> Any:
        return self._request("PATCH", path, json=json)

    def delete(self, path: str) -> Any:
        return self._request("DELETE", path)
    
    def healthcheck(self) -> bool:
        """Check if the API credentials are valid"""
        return self.get("/auth/check")
        
