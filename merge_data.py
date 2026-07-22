import json

#INPUT_FILE = "json_ideal/profiles.json"
#OUTPUT_FILE = "json_ideal/processed.json"

INPUT_FILE = "json_candidates/candidates_profiles.json"
OUTPUT_FILE = "json_candidates/candidates_processed.json"

with open(
    INPUT_FILE,
    encoding="utf-8"
) as f:
    data = json.load(f)

processed = []

for blogger in data:
    if "error" in blogger:
        continue
    username = blogger.get(
        "username",
        ""
    )
    profile = {
        "username":
            username,
        "instagram_url":
            f"https://instagram.com/{username}"
            if username
            else "",
        "full_name":
            blogger.get("fullName"),
        "bio":
            blogger.get("biography"),
        "category":
            blogger.get("businessCategoryName"),
        "followers":
            blogger.get("followersCount", 0),
        "following":
            blogger.get("followsCount", 0),
        "posts_count":
            blogger.get("postsCount", 0),
        "highlights":
            blogger.get("highlightReelCount", 0)
    }

    posts = []
    images = []

    latest_posts = blogger.get(
        "latestPosts",
        []
    )

    for post in latest_posts[:20]:
        image = post.get(
            "displayUrl"
        )
        if image:
            images.append(image)
        posts.append({
            "type":
                post.get("type"),
            "product_type":
                post.get("productType"),
            "caption":
                post.get("caption"),
            "hashtags":
                post.get("hashtags"),
            "likes":
                post.get("likesCount", 0),
            "comments":
                post.get("commentsCount", 0),
            "views":
                post.get("videoViewCount", 0),
            "image":
                image,
            "date":
                post.get("timestamp")
        })

    likes = [
        p["likes"]
        for p in posts
    ]
    comments = [
        p["comments"]
        for p in posts
    ]
    views = [
        p["views"]
        for p in posts
        if p["views"]
    ]

    avg_likes = (
        sum(likes) / len(likes)
        if likes
        else 0
    )
    avg_comments = (
        sum(comments) / len(comments)
        if comments
        else 0
    )
    avg_views = (
        sum(views) / len(views)
        if views
        else 0
    )
    reels_count = len(
        [
            p for p in posts
            if p["product_type"] == "clips"
        ]
    )
    reels_percentage = (
        reels_count /
        len(posts) *
        100
        if posts
        else 0
    )
    content = {
        "posts":
            posts,

        "reels_percentage":
            round(reels_percentage, 2),

        "avg_likes":
            round(avg_likes, 2),

        "avg_comments":
            round(avg_comments, 2),

        "avg_views":
            round(avg_views, 2)
    }
    followers = (
        blogger.get(
            "followersCount"
        )
        or 0
    )
    ER = (
        (avg_likes + avg_comments)
        /
        followers
        *
        100
        if followers
        else 0
    )
    view_rate = (
        avg_views /
        followers *
        100
        if followers
        else 0
    )
    bio = (
        blogger.get(
            "biography"
        )
        or ""
    ).lower()
    commercial_words = [
        "сотруд",
        "реклама",
        "collab",
        "pr",
        "ambassador",
        "партнер"
    ]
    commercial_ready = any(
        word in bio
        for word in commercial_words
    )
    metrics = {
        "ER":
            round(ER, 2),

        "view_rate":
            round(view_rate, 2),

        "commercial_ready":
            commercial_ready
    }
    processed.append({
        "profile":
            profile,

        "content":
            content,

        "metrics":
            metrics,

        "visual_data": {
            "images":
                images[:10]
        }
    })

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        processed,
        f,
        ensure_ascii=False,
        indent=4
    )

print(
    "Processed:",
    len(processed)
)