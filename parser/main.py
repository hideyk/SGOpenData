
import argparse
import os

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Process variables from arguments, with environment fallback.')
    parser.add_argument('--project', type=str, help='Google Cloud Project', default=os.environ.get('GOOGLE_PROJECT', ''))
    parser.add_argument('--bucket', type=str, help='Google Cloud Bucket', default=os.environ.get('GOOGLE_BUCKET', ''))

    args = parser.parse_args()
    return args


def main():
    return False

if __name__ == "__main__":
    main()