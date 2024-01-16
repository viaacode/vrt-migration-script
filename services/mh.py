import requests
from mediahaven import MediaHaven
from mediahaven.resources.base_resource import MediaHavenPageObject
from mediahaven.mediahaven import MediaHavenException, AcceptFormat
from mediahaven.oauth2 import RequestTokenError, ROPCGrant


class MediaHavenService(object):
    def __init__(self, config: dict):
        # self.auth_header = f"Basic {config['mediahaven']['auth']}"
        client_id = config["mh_client_id"]
        client_secret = config["mh_client_secret"]
        user = config["mh_username"]
        password = config["mh_password"]
        url = config["mh_host"]
        grant = ROPCGrant(url, client_id, client_secret)
        try:
            grant.request_token(user, password)
        except RequestTokenError as e:
            raise e
        self.mediahaven_client = MediaHaven(url, grant)

    def query_item(self, fragment_id: str) -> bytes:
        try:
            return self.mediahaven_client.records.get(
                fragment_id, AcceptFormat.XML
            ).raw_response.encode()
        except MediaHavenException as e:
            print(e)
            print(f"Could not query: `{fragment_id}`")
            return b""

    def query_collaterals(self, pid: str) -> MediaHavenPageObject | None:
        querystring = {"q": f"+(ExternalId:{pid}_*)"}
        try:
            return self.mediahaven_client.records.search(query_params=querystring)
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
            self.mediahaven_client.records.update(
                fragment_id, xml=sidecar, form_data={"reason": "VRT V2 Migration"}
            )
        except MediaHavenException as e:
            print(e)
            print(f"Could not update: `{fragment_id}`")
