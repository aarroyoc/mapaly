import datetime

from azure.storage.blob import ContainerClient, ContentSettings

from mapaly.settings import AZURE_CONTAINER_URL_FRONT, AZURE_ACCESS_KEY


def upload_image(f):
    content_settings = ContentSettings(content_type=f.content_type)
    container_client = ContainerClient.from_container_url(
        AZURE_CONTAINER_URL_FRONT, AZURE_ACCESS_KEY
    )
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    name = f"{date}_{f.name}"
    container_client.upload_blob(
        name, f, content_settings=content_settings, overwrite=False
    )
    return name


def delete_image(name):
    container_client = ContainerClient.from_container_url(
        AZURE_CONTAINER_URL_FRONT, AZURE_ACCESS_KEY
    )
    container_client.delete_blob(name)
