import respx
import httpx
from octaclient.client import OctadeskClient


def test_header_injection_and_put_success():
    client = OctadeskClient(api_key="key-123", agent_email="me@example.com", base_url="https://api.octadesk.test")

    url = "https://api.octadesk.test/contacts/abc-1"

    expected_response = {"id": "abc-1", "name": "Jane Doe"}

    with respx.mock(assert_all_called=True) as rsps:
        rsps.put(url, headers={"x-api-key": "key-123", "octa-agent-email": "me@example.com"}).respond(
            200, json=expected_response
        )

        resp = client.put(url, json={"name": "Jane Doe"})
        assert resp == expected_response


def test_put_raises_not_found():
    client = OctadeskClient(api_key="key-123", agent_email="me@example.com", base_url="https://api.octadesk.test")
    url = "https://api.octadesk.test/contacts/missing"

    with respx.mock(assert_all_called=True) as rsps:
        rsps.put(url).respond(404, json={"error": "Not found"})

        try:
            client.put(url, json={"name": "x"})
            assert False, "expected NotFoundError"
        except Exception as exc:
            from octaclient.errors import NotFoundError

            assert isinstance(exc, NotFoundError)
