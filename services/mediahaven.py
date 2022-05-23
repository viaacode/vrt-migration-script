import requests


class MediaHavenService(object):
    def __init__(self, config: dict = None):
        self.auth_header = f"Basic {config['mediahaven']['auth']}"
        pass

    def query_item(self, fragment_id: str) -> bytes:
        url = (
            f"https://archief.viaa.be/mediahaven-rest-api/resources/media/{fragment_id}"
        )

        # querystring = {"q": f"+(isFragment:0) +(mediaObjectid:{media_id})"}

        payload = ""
        headers = {
            "Accept": "application/vnd.mediahaven.v2+xml",
            "Authorization": self.auth_header,
        }

        try:
            response = requests.request("GET", url, data=payload, headers=headers)
            response.raise_for_status()
        except Exception as e:
            pass

        return response.content

    def query_collaterals(self, pid: str) -> bytes:
        url = "https://archief.viaa.be/mediahaven-rest-api/resources/media"

        querystring = {"q": f"+(ExternalId:{pid}_*)"}

        payload = ""
        headers = {
            "Accept": "application/vnd.mediahaven.v2+xml",
            "Authorization": self.auth_header,
        }

        try:
            response = requests.request(
                "GET", url, data=payload, headers=headers, params=querystring
            )
            response.raise_for_status()
        except Exception as e:
            pass

        return response.content

    def delete_fragment_id(self, fragment_id: str) -> bool:
        url = (
            f"https://archief.viaa.be/mediahaven-rest-api/resources/media/{fragment_id}"
        )

        headers = {"Authorization": self.auth_header}

        try:
            response = requests.request("DELETE", url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            pass

    def update_item(self, fragment_id: str, sidecar) -> bool:
        url = (
            f"https://archief.viaa.be/mediahaven-rest-api/resources/media/{fragment_id}"
        )

        headers = {"Authorization": self.auth_header}

        files = {"metadata": sidecar}

        try:
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
        except Exception as e:
            pass
