import json
import re

#INPUT_FILE = "json_ideal/processed_bloggers_with_visual.json"
#OUTPUT_FILE = "json_ideal/clean_bloggers_for_llm.json"

INPUT_FILE = "json_candidates/candidates_processed_with_visual.json"
OUTPUT_FILE = "json_candidates/clean_candidates_for_llm.json"

def clean_analysis_text(text):
    if not text:
        return None

    start = text.find(
        "**Visual Style:**"
    )

    if start != -1:
        text = text[start:]

    remove_parts = [
        "To find similar influencers",
        "Examples of hashtags",
    ]

    for part in remove_parts:
        index = text.find(part)

        if index != -1:
            text = text[:index]

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()

def extract_visual_style(blogger):
    visual_style = []

    image_descriptions = (
        blogger
        .get("visual_data", {})
        .get("image_descriptions", [])
    )

    for image_item in image_descriptions:
        analyses = image_item.get(
            "analysis",
            []
        )
        for analysis in analyses:
            if isinstance(analysis, dict):

                description = analysis.get(
                    "analysisResult"
                )

                cleaned_description = clean_analysis_text(
                    description
                )

                if cleaned_description:
                    visual_style.append(
                        cleaned_description
                    )

    return visual_style
with open(
    INPUT_FILE,
    encoding="utf-8"
) as f:
    bloggers = json.load(f)

cleaned = []

for blogger in bloggers:
    profile = blogger.get(
        "profile",
        {}
    )
    content = blogger.get(
        "content",
        {}
    )
    metrics = blogger.get(
        "metrics",
        {}
    )

    clean_profile = {

        "username":
            profile.get(
                "username",
                ""
            ),

        "instagram_url":
            profile.get(
                "instagram_url",
                ""
            ),
        "gender":
            "female",
        "bio":
            profile.get(
                "bio",
                ""
            ),

        "category":
            profile.get(
                "category",
                ""
            ),
        "followers":
            profile.get(
                "followers",
                0
            ),
        "following":
            profile.get(
                "following",
                0
            ),
        "posts_count":
            profile.get(
                "posts_count",
                0
            ),
        "highlights":
            profile.get(
                "highlights",
                0
            )

    }
    captions = []
    for post in content.get(
        "posts",
        []
    )[:10]:
        caption = post.get(
            "caption"
        )
        if caption:
            captions.append(
                caption
            )
    clean_content = {
        "avg_likes":
            content.get(
                "avg_likes",
                0
            ),
        "avg_comments":
            content.get(
                "avg_comments",
                0
            ),

        "avg_views":
            content.get(
                "avg_views",
                0
            ),
        "reels_percentage":
            content.get(
                "reels_percentage",
                0
            ),
        "captions":
            captions

    }

    clean_metrics = {

        "ER":
            metrics.get(
                "ER",
                0
            ),

        "view_rate":
            metrics.get(
                "view_rate",
                0
            ),

        "commercial_ready":
            metrics.get(
                "commercial_ready",
                False
            )

    }
    cleaned.append({

        "profile":
            clean_profile,
        "content_summary":
            clean_content,
        "metrics":
            clean_metrics,
        "visual_style":
            extract_visual_style(
                blogger
            )
    })

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        cleaned,
        f,
        ensure_ascii=False,
        indent=4
    )