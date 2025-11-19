# octaclient

Lightweight sync-only Python client for the Octadesk API (minimal initial implementation).

Install dependencies (recommended in a venv):

```bash
pip install .[dev]
```

Quick example:

```python
from octaclient import OctadeskClient
from octaclient.services.contacts import ContactsService
from octaclient.models.contact import ContactUpdate

client = OctadeskClient(api_key="<KEY>", agent_email="me@example.com")
svc = ContactsService(client)

updated = svc.update_contact("contact-id", ContactUpdate(name="Jane Doe"))
print(updated)
```
