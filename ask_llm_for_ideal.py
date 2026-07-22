import json
import os
from dotenv import load_dotenv
from groq import Groq
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
# Загружаем очищенный JSON

with open(
        "json_ideal/clean_bloggers_for_llm_shortened.json",
        encoding="utf-8"
) as f:
    bloggers = json.load(f)

# Только первые 10
bloggers = bloggers[:10]

data = json.dumps(
    bloggers,
    ensure_ascii=False
)

prompt = f"""
We are a fashion brand of women clothes, focus on elegancy and feminity.
You are analyzing a dataset of  female influencers who we believe represent the 
ideal target profile for our brand.
Your task is to create a detailed "Ideal Influencer Profile" based on common patterns 
across all analyzed creators, that can later be used to find new similar creators for our brand.
Important rules:
1. Analyze patterns across all influencers, not individual creators.
2. The influencers are female creators.
3. Their niches can be multiple and overlapping
4. Do not take into consideration username and urls.
Do not force a single category.
Analyze:
1. Profile characteristics:
- follower range
- account maturity
- bio patterns
- positioning
2. Content:
- main niches
- recurring topics
- caption style
- content formats
3. Engagement:
The ideal influencer should have engagement and commercial metrics 
that are not much worse than the analyzed examples, can deviate.
Consider:
- ER (Engagement Rate)
- View Rate
- Commercial readiness
4. Visual identity:
- colors
- photography style
- fashion style
- lifestyle atmosphere
- locations (we focus on CIS market)
- mood
5. Brand compatibility:
- suitable collaborations
- products that fit naturally
Return ONLY JSON:
{{
 "ideal_influencer_profile": {{

    "gender":"",
    "followers_range":"",
    "account_characteristics":[],
    "bio_patterns":[],
    "main_niches":[],
    "content_style":[],
    "caption_style":[],
    "visual_style":[],
    "fashion_style":[],
    "lifestyle_style":[],
    "engagement_profile":{{}},
    "brand_fit":[],
 }}
}}
Dataset:
{data}
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
    max_completion_tokens=8000,
    top_p=1,
    reasoning_effort="high",
    stream=True
)

answer = ""

for chunk in completion:
    text = chunk.choices[0].delta.content or ""
    print(text, end="")
    answer += text

# сохранить результат

with open(
        "json_ideal/ideal_influencer_profile.json",
        "w",
        encoding="utf-8"
) as f:
    f.write(answer)