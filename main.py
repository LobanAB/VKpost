import os
import random

import requests
from pathlib import Path

from dotenv import load_dotenv


def fetch_image_xkcd(images_dir=''):
    rand_num = random.randint(1, 2503)
    xkcd_api_url = f'https://xkcd.com/{rand_num}/info.0.json'
    response = requests.get(xkcd_api_url)
    response.raise_for_status()
    return save_image(response.json()['img'], Path.cwd() / images_dir), response.json()['alt']


def save_image(image_url: str, target_path: Path):
    image_name = image_url.split('/')[-1]
    Path(target_path).mkdir(parents=True, exist_ok=True)
    filename = target_path.joinpath(f'{image_name}')
    response = requests.get(image_url, verify=False)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename


def get_upload_url(vk_access_token: str, vk_group_id: str):
    vk_api_method = 'photos.getWallUploadServer'
    vk_api_url = f'https://api.vk.com/method/{vk_api_method}'
    payload = {'group_id': vk_group_id,
               'access_token': vk_access_token,
               'v': '5.131'
               }
    response = requests.post(vk_api_url, params=payload)
    response.raise_for_status()
    return response.json()['response']['upload_url']


def upload_image(vk_access_token, vk_group_id, upload_url, image_name):
    with open(image_name, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
    vk_api_method = 'photos.saveWallPhoto'
    vk_api_url = f'https://api.vk.com/method/{vk_api_method}'
    payload = {'group_id': vk_group_id,
               'photo': response.json()['photo'],
               'server': response.json()['server'],
               'hash': response.json()['hash'],
               'access_token': vk_access_token,
               'v': '5.131'
               }
    response = requests.post(vk_api_url, params=payload)
    response.raise_for_status()
    media_id = int(response.json()['response'][0]['id'])
    owner_id = int(response.json()['response'][0]['owner_id'])
    return owner_id, media_id


def post_image(vk_access_token, vk_group_id, owner_id, media_id, image_title):
    attachments = f'photo{owner_id}_{media_id}'
    from_group = 1
    payload = {'owner_id': -int(vk_group_id),
               'from_group': from_group,
               'attachments': attachments,
               'message': image_title,
               'access_token': vk_access_token,
               'v': '5.131'
               }
    vk_api_method = 'wall.post'
    vk_api_url = f'https://api.vk.com/method/{vk_api_method}'
    requests.post(vk_api_url, params=payload)


def main():
    load_dotenv()
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')
    image_name, image_title = fetch_image_xkcd()
    upload_url = get_upload_url(vk_access_token, vk_group_id)
    owner_id, media_id = upload_image(vk_access_token, vk_group_id, upload_url, image_name)
    post_image(vk_access_token, vk_group_id, owner_id, media_id, image_title)
    os.remove(image_name)


if __name__ == '__main__':
    main()
