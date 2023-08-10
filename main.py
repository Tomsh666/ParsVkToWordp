import requests
import json
def vkData():
    print()
    # access token
    access_token = "fd218039fd218039fd2180391dfe34becdffd21fd21803999f0bb0cea30602a831c43c0"
    group_id = -221937101     #для пользователя положительное, для группы отрицательное
    count = 5

    # Ссылка на метод API для получения постов со стены пользователя
    api_url = f"https://api.vk.com/method/wall.get?owner_id={group_id}&count={count}&access_token={access_token}&v=5.131"

    # Выполняем запрос к API
    response = requests.get(api_url)
    data = response.json()
    wp_dict = {
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
            wp_dict = {
                "text": "",
                "photos": []
            }
    else:
        print("Ошибка при получении данных.")





if __name__ == "__main__":
    vkData()