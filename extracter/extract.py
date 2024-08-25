import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import json
import dataclasses
from typing import List
import os
from utils import gcs_client

@dataclasses.dataclass
class DataGovSgConfig:
    initiateDownloadUrl: str
    pollDownloadUrl: str
    datasets: List[str]

class DataGovSgExtractor:
    def __init__(self, configFile: str):
        with open(configFile) as f:
            self.config = DataGovSgConfig(**json.load(f))
        self.session = requests.Session()
        self.session.mount('https://', HTTPAdapter(
            max_retries = Retry(
                total = 5,
                backoff_factor=2,
                status_forcelist=[400, 429,500,502,503,504]
            )))
        self.headers = {'Accept': 'application/json'}
        self.initiateDownloadUrl = self.config.initiateDownloadUrl
        self.pollDownloadUrl = self.config.pollDownloadUrl

    def _get(self, url: str) -> dict:
        try:
            r = self.session.get(url, headers = self.headers)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as err:
            print(f"Http error: {err}")
            return requests.Response()
        except json.decoder.JSONDecodeError as err:
            print(f"Json decode error: {err}, r.text: {r.text}")
            return requests.Response()

    def _getInitiateDownload(self, datasetId: str) -> bool:
        r = self._get(self.initiateDownloadUrl.format(datasetId = datasetId))
        if not r.status_code:
            return
        resp = r.json()
        if resp.get('code', 1) == 0:
            return True
        return False
    
    def _getPollDownload(self, datasetId: str):
        r = self._get(self.pollDownloadUrl.format(datasetId = datasetId))
        if not r.status_code or not r.text:
            return "", f"No status code or text present"
        resp = r.json()
        if resp.get('code', 1) == 0:
            return resp['data']['url'], ""
        return "", f"{resp.get('code', 'undefined')}"

    def _download(self, url: str, path: str):
        r = self._get(url)
        if not r.status_code:
            return
        with open(path, 'wb') as f:
            f.write(r.content)
        
    def downloadDataset(self, datasetId: str, path: str):
        print(f"Starting download for: {datasetId}")
        if not self._getInitiateDownload(datasetId):
            return f"Failed to initiate download on {datasetId}"
        
        url, err = self._getPollDownload(datasetId)
        if err:            
            return err
        self._download(url, path)
        print(f"Download succesfully completed for: {datasetId}")
        return None


def main():
    datagovsgextractor = DataGovSgExtractor(f"{os.path.dirname(os.path.realpath(__file__))}/data-gov-sg.json")
    for dataset in datagovsgextractor.config.datasets:
        if not dataset['active']:
            print(f"Skipping download for: {dataset['id']}")
            continue
        resp = datagovsgextractor.downloadDataset(dataset['resource_id'], ".".join([dataset['id'], dataset['type']]))

if __name__ == "__main__":
    main()