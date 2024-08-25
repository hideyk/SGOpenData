import extract
from utils.gcs_client import GCSClient
import argparse
import os

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Process variables from arguments, with environment fallback.')
    parser.add_argument('--project', type=str, help='Google Cloud Project', default=os.environ.get('GOOGLE_PROJECT', ''))
    parser.add_argument('--bucket', type=str, help='Google Cloud Bucket', default=os.environ.get('GOOGLE_BUCKET', ''))

    args = parser.parse_args()

    for arg in vars(args):
        argvalue = getattr(args, arg)
        if isinstance(argvalue, str) and not argvalue:
            raise Exception(f"Required argument {arg}:{argvalue} not properly defined.")
    return args

def main():
    args = parse_args()
    datagovsgextractor = extract.DataGovSgExtractor(f"{os.path.dirname(os.path.realpath(__file__))}/data-gov-sg.json")
    for dataset in datagovsgextractor.config.datasets:
        if not dataset['active']:
            print(f"Skipping download for: {dataset['id']}")
            continue
        download_path = ".".join([dataset['id'], dataset['type']])
        err = datagovsgextractor.downloadDataset(dataset['resource_id'], download_path)
        if err:
            print(f"Failed to download dataset {dataset['id']} - Error: {err}")
            continue
        gcs_client = GCSClient(project=args.project, bucket = args.bucket)
        gcs_client.upload(download_path)


if __name__ == "__main__":
    main()