from apify_client import ApifyClient
import json
import os
from dotenv import load_dotenv

load_dotenv()
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
client = ApifyClient(APIFY_TOKEN)

with open(
        "json_ideal/apify_input.json",
    "r",
    encoding="utf-8"
) as f:
    input_data = json.load(f)

urls = input_data["directUrls"]

profile_input = {
    "directUrls": urls,
    "resultsType": "details"
}

profile_run = client.actor(
    "apify/instagram-scraper"
).call(
    run_input=profile_input
)

profile_dataset = client.dataset(
    profile_run.default_dataset_id
).list_items()

profiles = profile_dataset.items

with open(
        "json_ideal/profiles.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        profiles,
        f,
        ensure_ascii=False,
        indent=4
    )

print(
    "Profiles:",
    len(profiles)
)