import os
import random

import requests
from dotenv import load_dotenv
from urllib.parse import urlparse, unquote


def get_xkcd_current():
    xkcd_api_url = 'https://xkcd.com/info.0.json'
    response = requests.get(xkcd_api_url)
    response.raise_for_status()
    return response.json()['num']


def fetch_xkcd_random_image(xkcd_current):
    rand_num = random.randint(1, xkcd_current)
    xkcd_api_url = f'https://xkcd.com/{rand_num}/info.0.json'
    response = requests.get(xkcd_api_url)
    response.raise_for_status()
    response = response.json()
    return save_image(response['img']), response['alt']


def save_image(image_url: str):
    filename = os.path.split(unquote(urlparse(image_url)[2]))[1]
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
    response = response.json()
    check_error(response)
    return response['response']['upload_url']


def upload_image(upload_url, image_name):
    with open(image_name, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
    response.raise_for_status()
    response = response.json()
    check_error(response)
    return response['photo'], response['server'], response['hash']


def save_wall_image(vk_access_token, vk_group_id, image_data, vk_server, image_hash):
    vk_api_method = 'photos.saveWallPhoto'
    vk_api_url = f'https://api.vk.com/method/{vk_api_method}'
    payload = {'group_id': vk_group_id,
               'photo': image_data,
               'server': vk_server,
               'hash': image_hash,
               'access_token': vk_access_token,
               'v': '5.131'
               }
    response = requests.post(vk_api_url, params=payload)
    response.raise_for_status()
    response = response.json()
    check_error(response)
    media_id = int(response['response'][0]['id'])
    owner_id = int(response['response'][0]['owner_id'])
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
    response = requests.post(vk_api_url, params=payload)
    response.raise_for_status()
    check_error(response.json())


def check_error(response):
    if 'error' in response:
        raise requests.exceptions.HTTPError(response['error']['error_code'],
                                            response['error']['error_msg'])


def main():
    load_dotenv()
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')
    xkcd_current = get_xkcd_current()
    image_name, image_title = fetch_xkcd_random_image(xkcd_current)
    try:
        upload_url = get_upload_url(vk_access_token, vk_group_id)
        image_data, vk_server, image_hash = upload_image(upload_url, image_name)
        owner_id, media_id = save_wall_image(
            vk_access_token,
            vk_group_id,
            image_data,
            vk_server,
            image_hash
        )
        post_image(vk_access_token, vk_group_id, owner_id, media_id, image_title)
    except requests.exceptions.HTTPError as err:
        print(err)
    finally:
        os.remove(image_name)


if __name__ == '__main__':
    main()
