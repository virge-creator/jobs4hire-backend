import httpx
from typing import Dict, Any


async def fetch_github_profile(username: str) -> Dict[str, Any]:
    """
    Fetch GitHub user profile and repositories.
    Returns structured data to store in Developer.github_data JSONB field.
    """
    async with httpx.AsyncClient() as client:
        # Fetch user profile
        user_response = await client.get(
            f"https://api.github.com/users/{username}",
            headers={"Accept": "application/vnd.github.v3+json"},
            timeout=10.0
        )
        if user_response.status_code == 404:
            raise ValueError(f"GitHub user '{username}' not found")
        user_response.raise_for_status()
        user_data = user_response.json()

        # Fetch repositories
        repos_response = await client.get(
            f"https://api.github.com/users/{username}/repos",
            params={"sort": "updated", "per_page": 100},
            headers={"Accept": "application/vnd.github.v3+json"},
            timeout=10.0
        )
        repos_response.raise_for_status()
        repos_data = repos_response.json()

        # Extract language statistics
        languages = {}
        total_stars = 0
        for repo in repos_data:
            if repo.get("language"):
                lang = repo["language"]
                languages[lang] = languages.get(lang, 0) + 1
            total_stars += repo.get("stargazers_count", 0)

        # Top languages by repo count
        top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:10]

        # Extract contribution activity (simplified)
        public_repos = user_data.get("public_repos", 0)
        followers = user_data.get("followers", 0)
        following = user_data.get("following", 0)

        # Build structured data
        github_data = {
            "username": username,
            "avatar_url": user_data.get("avatar_url"),
            "bio": user_data.get("bio"),
            "location": user_data.get("location"),
            "company": user_data.get("company"),
            "blog": user_data.get("blog"),
            "twitter_username": user_data.get("twitter_username"),
            "public_repos": public_repos,
            "followers": followers,
            "following": following,
            "created_at": user_data.get("created_at"),
            "updated_at": user_data.get("updated_at"),
            "total_stars": total_stars,
            "top_languages": dict(top_languages),
            "recent_repos": [
                {
                    "name": repo.get("name"),
                    "description": repo.get("description"),
                    "language": repo.get("language"),
                    "stargazers_count": repo.get("stargazers_count", 0),
                    "forks_count": repo.get("forks_count", 0),
                    "url": repo.get("html_url"),
                    "updated_at": repo.get("updated_at"),
                }
                for repo in repos_data[:10]  # Top 10 most recently updated
            ],
        }

        return github_data
