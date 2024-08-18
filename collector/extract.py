import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
import json
import dataclasses
from typing import List

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
                status_forcelist=[429,500,502,503,504]
            )))
        self.initiateDownloadUrl = self.config.initiateDownloadUrl
        self.pollDownloadUrl = self.config.pollDownloadUrl

    def _get(self, url: str) -> dict:
        try:
            r = self.session.get(url)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
            return {}

        return r

    def _getInitiateDownload(self, datasetId: str) -> bool:
        resp = self._get(self.initiateDownloadUrl.format(datasetId = datasetId))
        r = resp.json()
        if r.get('code', 1) == 0:
            return True
        print(r.get('errorMsg'))
        return False
    
    def _getPollDownload(self, datasetId: str):
        resp = self._get(self.pollDownloadUrl.format(datasetId = datasetId))
        r = resp.json()
        if r.get('code', 1) == 0:
            return r['data']['url']
        print(r.get('errorMsg'))
        return r

    def _getDownload(self, url: str, path: str):
        resp = self._get(url)
        with open(path, 'wb') as f:
            f.write(resp.content)
        
    def downloadDataset(self, datasetId: str, path: str):
        if not self._getInitiateDownload(datasetId):
            return
        
        url = self._getPollDownload(datasetId)
        self._getDownload(url, path)
        


def main():
    datagovsgextractor = DataGovSgExtractor("data-gov-sg.json")
    for dataset in datagovsgextractor.config.datasets:
        resp = datagovsgextractor.downloadDataset(dataset['resource_id'], ".".join([dataset['id'], dataset['type']]))
    print(resp)

if __name__ == "__main__":
    main()