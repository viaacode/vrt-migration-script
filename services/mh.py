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
        return self.mediahaven_client.records.get(fragment_id, AcceptFormat.XML).raw_response.encode()

    def query_collaterals(self, pid: str) -> MediaHavenPageObject:
        querystring = {"q": f"+(ExternalId:{pid}_*)"}
        return self.mediahaven_client.records.search(querystring)

    def delete_fragment_id(self, fragment_id: str) -> None:
        self.mediahaven_client.records.delete(fragment_id)

    def update_item(self, fragment_id: str, sidecar) -> None:
        self.mediahaven_client.records.update(fragment_id, xml = sidecar, form_data={"reason": "VRT V2 Migration"})
