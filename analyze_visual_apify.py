import json
import copy
import requests
import os
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")

ACTOR_ID = "akash9078/analyze-image"
#INPUT_FILE = "json_ideal/processed_bloggers.json"
#OUTPUT_FILE = "json_ideal/processed_bloggers_with_visual.json"
INPUT_FILE = "json_candidates/candidates_processed.json"
OUTPUT_FILE = "json_candidates/candidates_processed_with_visual.json"
with open(
        INPUT_FILE,
    encoding="utf-8"
) as f:
    original = json.load(f)

# копия
bloggers = copy.deepcopy(original)


def analyze_image(image_url):

    endpoint = (
        "https://api.apify.com/v2/acts/"
        "akash9078~analyze-image/"
        "run-sync-get-dataset-items"
    )
    params = {
        "token": APIFY_TOKEN
    }

    payload = {
        "imageUrl": image_url,
        "analysisType": "detailed",
        "customPrompt": """
Analyze this Instagram influencer photo.

Focus on:

- visual style
- color palette
- fashion style
- composition
- mood
- lifestyle category
- possible brand collaborations

Return a description useful for finding similar influencers.
"""
    }

    try:
        response = requests.post(
            endpoint,
            params=params,
            json=payload,
            timeout=180
        )
        response.raise_for_status()

        return response.json()

    except Exception as e:

        print(
            "Apify error:",
            e
        )

        return {
            "error": str(e)
        }

for index, blogger in enumerate(bloggers):

    username = blogger["profile"]["username"]

    print(
        f"\n[{index+1}/{len(bloggers)}]",
        username
    )
    images = (
        blogger
        .get(
            "visual_data",
            {}
        )
        .get(
            "images",
            []
        )
    )

    if not images:
        print(
            "No images"
        )
        continue
    image_results = []

    for img_index, img in enumerate(images):

        print(
            f"Image {img_index+1}/{len(images)}"
        )
        result = analyze_image(
            img
        )
        image_results.append(
            {
                "image": img,
                "analysis": result
            }
        )
    blogger["visual_data"][
        "image_descriptions"
    ] = image_results

    with open(
            OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            bloggers,
            f,
            ensure_ascii=False,
            indent=4
        )
print(
    "\nFinished all bloggers"
)