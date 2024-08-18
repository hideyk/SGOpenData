## Extract data from Website
## Support different file formats
## Publish to an object storage facility 

import requests
from pprint import pprint
          
base_url = "https://data.gov.sg/api/action/datastore_search"
url = base_url + "?resource_id=d_c9f57187485a850908655db0e8cfe651&limit=100"
response = requests.get(url)
pprint(response.json())
print(type(response.json()))
def main():
    pass

if __name__ == "__main__":
    main()