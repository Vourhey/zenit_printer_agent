import requests

# OctoPi client
class OctoPi:
    def __init__(self, server_url: str, api_key: str):
        self.url = server_url
        self.API_KEY = api_key

    def upload_file(self, local_path: str) -> str:
        url = "{}/api/files/local".format(self.url)

        headers = {
                "X-Api-Key": self.API_KEY,
                "Content-Type": "multipart/form-data"
                }

        payload = {
                "file": open(local_path, "rb")
                }
        response = requests.post(url, files=payload, headers=headers)
        print(response)

        jres = response.json()
        print(jres)
        return jres["files"]["local"]["name"]   # uploaded file name

    def get_gcode_analysis(self, name: str) -> dict:
        url = "{}/api/files/local/{}".format(self.url, name)

        headers = {
                "X-Api-Key": self.API_KEY
                }

        response = requests.get(url, headers=headers)
        print(response.status_code)

        jres = response.json()
        return jres["gcodeAnalysis"]

