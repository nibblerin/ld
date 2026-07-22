# Этап подготовки входных данных для Apify:
# 1. Загружаем список Instagram-профилей из Google Sheets через CSV-экспорт.
# 2. Извлекаем ссылки на профили из таблицы.
# 3. Проверяем и нормализуем данные:
#    - очищаем ссылки от лишних параметров Instagram;
#    - восстанавливаем URL из записей, где есть только @username;
#    - приводим все профили к единому формату https://www.instagram.com/username/.
# 4. Формируем JSON-файл apify_input.json с подготовленным списком ссылок,
#    который используется как входные данные для Apify Instagram Scraper.
#pip install pandas
import pandas as pd
import json
import re

def convert_instagram_url(value):
    value = str(value).strip()
    # Если уже есть Instagram ссылка
    if "instagram.com/" in value:
        match = re.search(
            r"instagram\.com/([A-Za-z0-9._]+)",
            value
        )
        if match:
            username = match.group(1)
            return f"https://www.instagram.com/{username}/"
    # Если есть @username
    username_match = re.search(
        r"@([A-Za-z0-9._]+)",
        value
    )
    if username_match:
        username = username_match.group(1)
        return f"https://www.instagram.com/{username}/"
    return None

url = "https://docs.google.com/spreadsheets/d/1J1HtHP-CMQ8skFOuFtspu2GhmSzeWPcehmrAK-P6gR4/export?format=csv&gid=0"

# читаем таблицу
df = pd.read_csv(
    url,
    header=None
)

print(df.head())

# берем колонку со ссылками
raw_urls = df.iloc[:, 1].dropna().tolist()

# преобразуем ссылки
urls = []
for item in raw_urls:
    converted = convert_instagram_url(item)
    if converted:
        urls.append(converted)

print("Итоговые ссылки:")
for url in urls:
    print(url)

# создаем файл для Apify
payload = {
    "directUrls": urls,
    "resultsType": "posts",
    "resultsLimit": 10
}

with open(
        "json_ideal/apify_input.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        payload,
        f,
        ensure_ascii=False,
        indent=4
    )
print(
    f"Создан apify_input.json. Ссылок: {len(urls)}"
)