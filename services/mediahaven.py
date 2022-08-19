import requests


class MediaHavenService(object):
    def __init__(self, config: dict):
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
            print(e)
            print(f"Something went wrong during `query_item` for item: `{fragment_id}`")
            return b""

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
            print(e)
            print(f"Something went wrong during `query_collaterals` for item: `{pid}`")
            return b""

        return response.content

    def delete_fragment_id(self, fragment_id: str) -> None:
        url = (
            f"https://archief.viaa.be/mediahaven-rest-api/resources/media/{fragment_id}"
        )

        headers = {"Authorization": self.auth_header}

        try:
            response = requests.request("DELETE", url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print(e)
            print(
                f"Something went wrong during `delete_fragment_id` for item: `{fragment_id}`"
            )

    def update_item(self, fragment_id: str, sidecar) -> None:
        url = (
            f"https://archief.viaa.be/mediahaven-rest-api/resources/media/{fragment_id}"
        )

        headers = {"Authorization": self.auth_header}

        files = {"metadata": sidecar}

        try:
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()
        except Exception as e:
            print(e)
            print(
                f"Something went wrong during `update_item` for item: `{fragment_id}`"
            )
