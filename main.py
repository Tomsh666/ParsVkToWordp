import requests
import os
import base64
import json
from urllib.parse import urlparse
def vkData():
    print()
    # access token vk
    access_token = "fd218039fd218039fd2180391dfe34becdffd21fd21803999f0bb0cea30602a831c43c0"
    group_id = -221937101     #для пользователя положительное, для группы отрицательное
    count = 1

    # Ссылка на метод VK API для получения постов со стены группы
    vk_api_url = f"https://api.vk.com/method/wall.get?owner_id={group_id}&count={count}&access_token={access_token}&v=5.131"

    # Выполняем запрос к API
    response = requests.get(vk_api_url)
    data = response.json()
    wp_dict = {
        "title":"1",
        "text":"",
        "photos":[]
    }
    
    # Обработка данных
    if "response" in data and "items" in data["response"]:
        wall_posts = data["response"]["items"]
        for post in wall_posts:
            # print(post["text"]) # текст поста
            wp_dict["text"]=post["text"]
            if "attachments" in post:
                for attachment in post["attachments"]:
                    if attachment["type"] == "photo":
                        photo = attachment["photo"]
                        largest_photo = max(photo["sizes"], key=lambda x: x["width"])
                        photo_url = largest_photo["url"]
                        # print("Фотография:", photo_url) # url фотографии
                        wp_dict["photos"].append(photo_url)
            # print(wp_dict) # вывод словарь для json
            # print(json_data) # выводит готовый json
            SendWp(wp_dict)
            wp_dict["text"]=""
            wp_dict["photos"]=[]
    else:
        print("Ошибка при получении данных.")

#загрузка изображений в папку(не факт что нужно)
def PicDown(image_url):
    save_directory = "D:\MAMP\htdocs\wp_test\wp-content\images"  # дириктория где храняться картинки
    response = requests.get(image_url)

    if response.status_code == 200:
        parsed_url = urlparse(image_url)
        image_filename = os.path.basename(parsed_url.path)
        image_path = os.path.join(save_directory, image_filename)
        with open(image_path, "wb") as f:
            f.write(response.content)

        return image_filename, save_directory
    else:
        print("Ошибка при скачивании изображения.")



def SendWp(data):
    # url сайта на wp
    wp_url = "http://localhost/wp_test/wp-json/wp/v2/"
    # в wp-config.php define( 'WP_ENVIRONMENT_TYPE', 'local' );
    # creds юзер + пароль приложения
    user = 'admin'
    password = '2KgQ W4cd_VhM7 Epk9 vTS9 iBBK'
    creds = user + ':' + password
    token = base64.b64encode(creds.encode())
    header = {"Authorization": "Basic " + token.decode('utf-8')}
    # текс в wp
    post = {
        'content': '<!-- wp:paragraph -->' + data["text"] + '<!-- /wp:paragraph -->',
        'status': 'publish'
    }

    # скачивание картинки по url и создание записи в wp
    for pic in data["photos"]:
        file_name, direct = PicDown(pic)
        media={
            'file': open(direct+'\\'+file_name,'rb')
        }
        image = requests.post(wp_url + 'media', headers=header, files=media)
        imageURL = str(json.loads(image.content)['source_url'])
        post['content']+='<!-- wp:image --><figure class="wp-block-image"><img src="' + imageURL + '" alt="picture"></figure><!-- /wp:image -->'



    response = requests.post(wp_url + 'posts', headers=header,json=post)  # отправка в wp
    if response.status_code == 201:
        print('Запись успешно создана.')
    else:
        print('Произошла ошибка:', response.text)



if __name__ == "__main__":
    vkData()