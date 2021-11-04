# Публикация комиксов

Программа скачивает случайную картинку и ее описание с сайта [xkcd.com](https://xkcd.com/  "xkcd.com") и размещает в группу социальной сети Вконтакте [vk.com](https://vk.com/  "vk.com").

## Как установить

- Скачайте код.
```
git clone https://github.com/LobanAB/VKpost.git
```
- Для работы скачайте Python - https://www.python.org/.
- Установите зависимости 
```
pip install -r requirements.txt
```
- Создайте файл .env со следующим содержимым.
Для работы нужен ключ api Вконтакте (как получить можно узнать [тут](https://vk.com/dev/first_guide  "vk.com")) и id группы (можно узнать [тут](https://regvk.com/id/  "regvk.com")).
Ключ можно получить вручную. Вам потребуются следующие права: photos, groups, wall и offline
```
VK_ACCESS_TOKEN={api токен Вконтакте}
VK_GROUP_ID={id группы куда будем постить}
```
- Запустите программу
```
python main.py
```

Будет скачана случайная картинка с сайта [xkcd.com](https://xkcd.com/  "xkcd.com") и размещена постом в группе [Вконтакте](https://vk.com/  "vk.com").

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).