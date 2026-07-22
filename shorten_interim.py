import json
from groq import Groq
from dotenv import load_dotenv
import os

#INPUT_FILE = "json_ideal/clean_bloggers_for_llm.json"
#OUTPUT_FILE = "json_ideal/clean_bloggers_for_llm_shortened.json"

INPUT_FILE = "json_candidates/clean_candidates_for_llm.json"
OUTPUT_FILE = "json_candidates/clean_candidates_for_llm_shortened.json"

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
def summarize_text(text, instruction):
    if not text:
        return ""

    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role":"system",
                "content":instruction
            },
            {
                "role":"user",
                "content":text[:12000]
            }
        ],
        temperature=0.3,
        max_completion_tokens=500
    )

    return completion.choices[0].message.content.strip()

with open(
    INPUT_FILE,
    encoding="utf-8"
) as f:
    bloggers = json.load(f)

shortened = []

for i, blogger in enumerate(bloggers):

    print(
        f"{i+1}/{len(bloggers)}"
    )

    profile = blogger["profile"]
    content = blogger["content_summary"]
    metrics = blogger["metrics"]

    captions = "\n".join(
        content.get(
            "captions",
            []
        )
    )

    caption_summary = summarize_text(
        captions,
        """
Analyze influencer captions.
Summarize:
- writing style
- topics
- emotional tone
- use of emojis
- product mentions
Return only a short description.
"""
    )

    visual_text = "\n\n".join(
        blogger.get(
            "visual_style",
            []
        )
    )

    visual_summary = summarize_text(
        visual_text,
        """
Analyze influencer visual style.
Summarize:
- aesthetics
- colors
- fashion style
- locations
- lifestyle impression
- brand suitability
Return only concise description.
"""
    )
    shortened.append(
        {
            "profile": {
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
            },
            "content_summary": {
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
                "caption_style":
                    caption_summary
            },
            "metrics": {
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
            },
            "visual_style_summary":
                visual_summary
        }
    )

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        shortened,
        f,
        ensure_ascii=False,
        indent=4
    )