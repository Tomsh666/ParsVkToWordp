import requests
import json
import base64
from datetime import datetime
def vkData():
    print()
    # access token
    access_token = "fd218039fd218039fd2180391dfe34becdffd21fd21803999f0bb0cea30602a831c43c0"
    group_id = -221937101     #для пользователя положительное, для группы отрицательное
    count = 5

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
            json_data = json.dumps(wp_dict)
            # print(json_data) # выводит готовый json
            SendWp(json_data)
            wp_dict["text"]=""
            wp_dict["photos"]=[]
    else:
        print("Ошибка при получении данных.")

def SendWp(json_data):
    # url сайта на wp
    wp_url = "http://localhost/wp_test/wp-json/wp/v2"
    # в wp-config.php define( 'WP_ENVIRONMENT_TYPE', 'local' );
    # creds юзер + пароль приложения
    user = "admin"
    password = "I08Y aqua 6zcT wt84 4r8Q AXtA"
    # Получаем текущую дату и время
    current_datetime = datetime.now()
    # Форматируем дату и время в нужный формат
    formatted_datetime = current_datetime.strftime('%Y-%m-%dT%H:%M:%S')
    creds = user + ':' + password
    token = base64.b64encode(creds.encode())
    header = {"Authorization":"Basic" + token.decode('utf-8')}
    post ={
        'date': formatted_datetime,
        'title': 'hello api',
        'content': 'asasaasasasaasaaassaaa',
        'status': 'publish'
    }


    response = requests.post(wp_url + '/posts', headers=header,json=post)  # отправка в wp
    if response.status_code == 201:
        print('Запись успешно создана.')
    else:
        print('Произошла ошибка:', response.text)






if __name__ == "__main__":
    vkData()