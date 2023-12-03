import requests
import os
import random
import pathlib
from dotenv import load_dotenv
import time


def handle_response(response):
    if "error" in response.json():
        raise Exception(f"Произошла ошибка VK api: \n{response.json()['error']['error_msg']}")
    else:
        return response.json()


def get_random_comics_url(comics_count):
    comics_number = random.randint(1, comics_count)
    comics_url = f"https://xkcd.com/{comics_number}/info.0.json"
    return comics_url


def fetch_comics_content(comics_url):
    response = requests.get(comics_url)
    response.raise_for_status()
    fetched_comics_content = response.json()
    return fetched_comics_content


def get_comics_count():
    last_comics_url = "https://xkcd.com/info.0.json"
    response = requests.get(last_comics_url)
    response.raise_for_status()
    comics_count = response.json()["num"]
    return comics_count


def download_image(image_url, image_path):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(image_path, "wb") as file:
        file.write(response.content)
    file.close()


def get_server_upload_url(vk_group_id, vk_access_token, vk_api_version):
    server_upload_url = "https://api.vk.com/method/photos.getWallUploadServer"
    params = {
        "group_id": vk_group_id,
        "access_token": vk_access_token,
        "v": vk_api_version
    }
    response = requests.get(server_upload_url, params=params)
    response.raise_for_status()
    server_upload = handle_response(response)
    return server_upload["response"]["upload_url"]


def upload_image_on_server(upload_url, image_path):
    with open(image_path, 'rb') as file:
        files = {
            'photo': file
        }
        response = requests.post(upload_url, files=files)
    response.raise_for_status()
    server, uploaded_photo, photo_hash = response.json().values()
    return server, uploaded_photo, photo_hash


def save_image_in_album(vk_group_id, vk_access_token, vk_api_version, uploaded_photo, photo_hash, server):
    vk_save_image_url = "https://api.vk.com/method/photos.saveWallPhoto"
    params = {
        "group_id": vk_group_id,
        "access_token": vk_access_token,
        "v": vk_api_version,
        "photo": uploaded_photo,
        "hash": photo_hash,
        "server": server
    }
    response = requests.post(vk_save_image_url, params=params)
    response.raise_for_status()
    vk_save_response = handle_response(response)
    return vk_save_response["response"]


def publish_vk_image(vk_group_id, vk_access_token, vk_api_version, image_alt, owner_id, media_id):
    vk_publish_url = "https://api.vk.com/method/wall.post"
    params = {
        "owner_id": f"-{vk_group_id}",
        "access_token": vk_access_token,
        "v": vk_api_version,
        "from_group": 1,
        "message": image_alt,
        "attachments": f"photo{owner_id}_{media_id}"
    }
    response = requests.post(vk_publish_url, params=params)
    response.raise_for_status()
    publish_response = handle_response(response)
    return publish_response


def main():
    load_dotenv()

    vk_access_token = os.environ["VK_ACCESS_TOKEN"]
    vk_group_id = os.environ["VK_GROUP_ID"]
    vk_api_version = "5.154"
    comics_count = get_comics_count()
    publication_frequency = 86400

    while True:
        comics_url = get_random_comics_url(comics_count)
        fetched_comics_content = fetch_comics_content(comics_url)

        image_alt = fetched_comics_content["alt"]
        image_url = fetched_comics_content["img"]
        image_name = f"{fetched_comics_content['title']}.png"

        try:
            download_image(image_url, image_name)
            server_upload_url = get_server_upload_url(vk_group_id, vk_access_token, vk_api_version)
            server, uploaded_photo, photo_hash = upload_image_on_server(server_upload_url, image_name)
        finally:
            pathlib.Path.unlink(image_name)

        album_saving_response = save_image_in_album(vk_group_id, vk_access_token, vk_api_version,
                                                    uploaded_photo, photo_hash, server)
        media_id = album_saving_response[0]["id"]
        owner_id = album_saving_response[0]["owner_id"]

        publish_vk_image(vk_group_id, vk_access_token, vk_api_version, image_alt, owner_id, media_id)
        time.sleep(publication_frequency)


if __name__ == "__main__":
    main()
