# pip install groq

import json
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
with open(
        "json_ideal/ideal_influencer_profile.json",
    encoding="utf-8"
) as f:

    ideal_profile = json.load(f)



ideal_profile_text = json.dumps(
    ideal_profile,
    ensure_ascii=False,
    indent=2
)

prompt = f"""

You are an expert in Instagram influencer discovery
for CIS markets.

Based on this Ideal Influencer Profile,
generate search queries that can be used to find similar
female Instagram creators.
Target countries:
- Russia
- Belarus
- Kazakhstan
- Ukraine
- CIS
Important:
Do not translate English words literally.
Generate real Russian phrases used by influencers
in Instagram usernames, bios, captions and hashtags.
Create:
1. Profile search queries
Generate queries that can be used for Instagram search.
Examples:
- fashion blogger
- стиль одежды
- женский стиль
- мама блогер
- уютный дом
- бьюти блогер
- рецепты
2. Hashtags
Generate Instagram hashtags.
Examples:
#модныйобраз
#стильнаядевушка
#рецепты
#уютныйдом
#распаковкаодежды (этот хэштег очень важный)
3. Bio keywords
Generate words that indicate:
- influencer profile
- commercial readiness
- collaboration availability
Examples:
- сотрудничество
- реклама
- блогер
- beauty
- lifestyle
- обзоры
- pr
Return ONLY JSON:
{{
"candidate_generation":{{
    "profile_search_queries_ru":[],
    "profile_search_queries_en":[],
    "hashtags_ru":[],
    "hashtags_en":[],
    "bio_keywords":[]
}}
}}
Ideal profile:
{ideal_profile_text}
"""
completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }

    ],
    temperature=0.3,
    max_completion_tokens=3000,
    top_p=1,
    reasoning_effort="medium",
    stream=True
)

answer = ""
for chunk in completion:
    text = chunk.choices[0].delta.content or ""
    print(
        text,
        end=""
    )
    answer += text
with open(
        "json_ideal/instagram_candidate_queries.json",
    "w",
    encoding="utf-8"
) as f:

    f.write(answer)

print("\nDONE")