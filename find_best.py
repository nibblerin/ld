from groq import Groq
import json
import csv
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

with open(
    "json_ideal/ideal_influencer_profile.json",
    encoding="utf-8"
) as f:
    ideal_profile = json.load(f)

with open(
    "json_candidates/clean_candidates_for_llm_shortened.json",
    encoding="utf-8"
) as f:
    candidates = json.load(f)

ideal_data = json.dumps(
    ideal_profile,
    ensure_ascii=False
)

batch_size = 6

batches = [
    candidates[i:i + batch_size]
    for i in range(0, len(candidates), batch_size)
]

os.makedirs(
    "candidates_search_results",
    exist_ok=True
)

all_selected = []

for index, batch in enumerate(batches):

    print(
        f"Processing batch {index+1}/{len(batches)}"
    )

    candidate_data = json.dumps(
        batch,
        ensure_ascii=False
    )

    prompt = f"""
    You are an expert influencer marketing analyst specialized in selecting creators for an elegant and feminine fashion brand. \
    Your task is to compare Instagram creators against the Ideal Influencer Profile and select only creators who are the closest match.Analyze each candidate using the following criteria:
    PROFILE MATCH
    Evaluate: gender match, followers range compatibility, account maturity, number of posts, highlights/stories organization, posting activity, bio structure, collaboration contact information, niche keywords
    FASHION AND BRAND FIT
    Evaluate: whether the creator naturally fits an elegant feminine clothing brand, fashion style similarity:, classic, minimal, 
    chic, feminine, timeless, casual luxury, boho, lifestyle fashion, whether outfits are the main part of the content, whether the audience could be interested in clothing collaborations
    VISUAL STYLE SIMILARITY
    Compare: color palette, lighting style, photo composition, backgrounds, image quality, aesthetic atmosphere, lifestyle feeling Pay special attention to: warm neutral colors, beige, ivory, white, soft brown, pastel tones, clean minimalist compositions, natural lighting, polished but authentic appearance
    CONTENT MATCH
    Evaluate:, main niche, Reels usage, content formats:
    outfit videos
    styling ideas
    lifestyle videos
    beauty content
    day-in-the-life
    product reviews
    fashion recommendations
    caption style:
    emojis
    CTA
    line breaks
    hashtags
    personal storytelling
    ENGAGEMENT AND COMMERCIAL QUALITY
    Evaluate: engagement rate (ER), view rate, follower quality, commercial readiness, previous collaboration signals, suitability for brand partnerships
    Selection rules: Do not select creators only because they have many followers. A smaller creator with stronger visual and fashion similarity is preferred.
     Prioritize creators who already create content matching the brand aesthetic. 
     Prioritize VISUAL STYLE SIMILARITY and fashion fit over audience size. Select from 1 to 5 creators. If you think there is no plausible candidate, return at least 1 with similar aesthetics and number of followers > 2000. 
    If no creator is a strong match, return an empty array. Do not invent missing information. Return ONLY valid JSON.The reason field must be written in Russian.
    Ideal Influencer Profile:
    {ideal_data}
    Candidates:
    {candidate_data}
    Return exactly this JSON:
    {{
    "selected":[
    {{
    "instagram_url":"",
    "username":"",
    "reason":""
    }}
    ]
    }}
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],
        temperature=0.2,
        max_completion_tokens=3000,
        response_format={
            "type":"json_object"
        }
    )

    answer = completion.choices[0].message.content

    result = json.loads(answer)

    selected_from_batch = result.get(
        "selected",
        []
    )

    all_selected.extend(
        selected_from_batch
    )

    with open(
        "candidates_search_results/selected_candidates.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "selected": all_selected
            },
            f,
            ensure_ascii=False,
            indent=4
        )

    with open(
        "candidates_search_results/selected_candidates.csv",
        "w",
        encoding="utf-8",
        newline=""
    ) as f:

        writer = csv.writer(f)

        writer.writerow(
            [
                "Instagram URL",
                "Username",
                "Причина"
            ]
        )

        for item in all_selected:

            writer.writerow(
                [
                    item.get("instagram_url"),
                    item.get("username"),
                    item.get("reason")
                ]
            )

    print(
        "Saved after batch:",
        index + 1,
        "Total selected:",
        len(all_selected)
    )

print(
    "Finished. Selected:",
    len(all_selected)
)