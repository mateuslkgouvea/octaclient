#%%
import os
from dotenv import load_dotenv

from octaclient import OctadeskClient, ContactsService

load_dotenv()

octa = OctadeskClient(
    api_key = os.environ["X_API_KEY"],
    agent_email= os.environ["OCTA_AGENT_EMAIL"],
    base_url= os.environ["OCTA_BASE_URL"]
    )

service = ContactsService(octa)

# %%
contacts = service.list()
# %%
