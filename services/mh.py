import requests
from mediahaven import MediaHaven
from mediahaven.resources.base_resource import MediaHavenPageObject
from mediahaven.mediahaven import MediaHavenException, AcceptFormat
from mediahaven.oauth2 import RequestTokenError, ROPCGrant


class MediaHavenService(object):
    def __init__(self, config: dict):
        # self.auth_header = f"Basic {config['mediahaven']['auth']}"
        client_id = config['mediahaven']["client_id"]
        client_secret = config['mediahaven']["client_secret"]
        user = config['mediahaven']["username"]
        password = config['mediahaven']["password"]
        url = config['mediahaven']["host"]
        grant = ROPCGrant(url, client_id, client_secret)
        try:
            grant.request_token(user, password)
        except RequestTokenError as e:
            raise e
        self.mediahaven_client = MediaHaven(url, grant)

    def query_item(self, fragment_id: str) -> bytes:
        try:
            item = self.mediahaven_client.records.get(
                fragment_id, AcceptFormat.XML
            )
            return item.raw_response.encode()
        except MediaHavenException as e:
            print(e)
            print(f"Could not query: `{fragment_id}`")
            return b""

    def query_collaterals(self, pid: str) -> MediaHavenPageObject | None:
        querystring = {"q": f"+(ExternalId:{pid}_*)"}
        try:
            return self.mediahaven_client.records.search(AcceptFormat.JSON, **querystring)
        except MediaHavenException as e:
            print(e)
            print(f"Could not query collaterals: `{pid}`")
            return None

    def delete_fragment_id(self, fragment_id: str) -> None:
        try:
            self.mediahaven_client.records.delete(fragment_id)
        except MediaHavenException as e:
            print(e)
            print(f"Could not delete: `{fragment_id}`")

    def update_item(self, fragment_id: str, sidecar) -> None:
        try:
            form_data={"reason": "VRT V2 Migration", "metadata": sidecar, "metadata_content_type": "application/xml"}
            self.mediahaven_client.records.update(
                fragment_id, **form_data
            )
        except MediaHavenException as e:
            print(e)
            print(f"Could not update: `{fragment_id}`")
