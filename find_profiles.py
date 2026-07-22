from apify_client import ApifyClient
import json
import os
from dotenv import load_dotenv

load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
client = ApifyClient(APIFY_TOKEN)

# создаем папку автоматически
os.makedirs("json_candidates", exist_ok=True)

actor_input = {
    "enhanceUserSearchWithFacebookPage": False,
    "liveSearch": False,
    "search": "стильные образы, бьюти, лайфстайл, мама блогер,лайфстайл блогер, эко лайф, семейные влоги",
    "searchLimit": 5,
    "searchType": "user"
}
run = client.actor(
    "apify/instagram-search-scraper"
).call(
    run_input=actor_input
)

dataset = client.dataset(
    run.default_dataset_id
).list_items()

results = dataset.items

with open(
    "json_candidates/candidates_profiles.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        results,
        f,
        ensure_ascii=False,
        indent=4
    )

print(f"Found {len(results)} candidates")