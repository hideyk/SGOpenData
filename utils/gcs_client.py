from google.cloud import storage
import os

class GCSClient:
    def __init__(self, project, bucket):
        self._project = project
        self._bucket = bucket
        self.client = storage.Client(project=project)
        self.bucket = self.client.bucket(bucket)

    def upload(self, object: str, path: str = ""):
        object_name = os.path.basename(object)
        blob = self.bucket.blob(os.path.join(path, object_name))
        generation = 0
        if blob.exists:
            generation = blob.generation
        blob.upload_from_filename(object_name, num_retries=3, if_generation_match=generation)
        return None
    
    def download(self, object: str, path: str):
        blob = self.bucket.blob(object)
        blob.download_to_filename(path)
        return None
    

def main():
    uploader = GCSUploader()