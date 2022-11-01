import argparse
import multiprocessing
from pathlib import Path

from azure.storage.blob import ContainerClient, ContentSettings


class AzureBlobService:
    def __init__(self, azure_container_url, azure_access_key):
        self.container_client = ContainerClient.from_container_url(
            azure_container_url, azure_access_key
        )

    def get_settings(self, path):
        if path.suffix == ".png":
            return ContentSettings(content_type="image/png")
        elif path.suffix == ".jpg":
            return ContentSettings(content_type="image/jpeg")
        elif path.suffix == ".json":
            return ContentSettings(content_type="application/json")
        else:
            raise Exception("Not valid file")

    def upload(self, path):
        settings = self.get_settings(path)

        with open(path, "rb") as f:
            self.container_client.upload_blob(
                path.name, f, content_settings=settings, overwrite=True
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--azure-container-url", help="Azure container URL", required=True
    )
    parser.add_argument("--azure-access-key", help="Azure Access Key", required=True)
    args = parser.parse_args()

    data_dir = Path.cwd() / "wizard-map-data"
    if not data_dir.exists():
        raise Exception("Data folder doesn't exist yet")

    azure = AzureBlobService(args.azure_container_url, args.azure_access_key)
    pool = multiprocessing.Pool()
    pool.map(azure.upload, data_dir.glob("*"))


if __name__ == "__main__":
    main()
