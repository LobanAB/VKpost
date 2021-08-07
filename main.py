import os
import requests
from pathlib import Path

from dotenv import load_dotenv


def fetch_image_xkcd(images_dir='images'):
    xkcd_api_url = 'https://xkcd.com/353/info.0.json'
    response = requests.get(xkcd_api_url)
    response.raise_for_status()
    save_image(response.json()['img'], Path.cwd() / images_dir)
    print(response.json()['alt'])


def save_image(image_url: str, target_path: Path, image_id=''):
    image_name = image_url.split('/')[-1]
    Path(target_path).mkdir(parents=True, exist_ok=True)
    filename = target_path.joinpath(f'{image_id}{image_name}')
    response = requests.get(image_url, verify=False)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_from_vk(vk_access_token: str, vk_group_id: str):
    vk_api_method = 'photos.getWallUploadServer'
    vk_api_url = f'https://api.vk.com/method/{vk_api_method}'
    payload = {'group_id': vk_group_id,
               'access_token': vk_access_token,
               'v': '5.131'
               }
    response = requests.get(vk_api_url, params=payload)
    response.raise_for_status()
    print(response.json())
    upload_url = response.json()['response']['upload_url']
    with open('python.png', 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        print(response.json())
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
    print(response.json())
    media_id = response.json()['response'][0]['id']
    owner_id = -int(response.json()['response'][0]['owner_id'])
    attachments = f'photo{owner_id}_{media_id}'
    print(attachments)
    message = "I wrote 20 short programs in Python yesterday.  It was wonderful.  Perl, I'm leaving you."
    from_group = 1
    payload = {'owner_id': -int(vk_group_id),
               'from_group': from_group,
               'attachments ': attachments,
               #'message': message,
               'access_token': vk_access_token,
               'v': '5.131'
               }
    vk_api_method = 'wall.post'
    vk_api_url = f'https://api.vk.com/method/{vk_api_method}'
    response = requests.post(vk_api_url, params=payload)
    print(response.json())

def main():
    # Path(target_path).mkdir(parents=True, exist_ok=True)
    # fetch_image_xkcd()
    load_dotenv()
    vk_app_id = os.getenv('VK_APP_ID')
    vk_access_token = os.getenv('VK_ACCESS_TOKEN')
    vk_group_id = os.getenv('VK_GROUP_ID')
    get_from_vk(vk_access_token, vk_group_id)


if __name__ == '__main__':
    main()
