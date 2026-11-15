import os 
import requests
from datetime import datetime

USERNAME = "donovan057"
TOKEN = os.environ.get("GITHUB_TOKEN")
HEADERS = {"Authorization": f"token {TOKEN}"} if TOKEN else {}

def get_github_stats():
    user_url = f"https://api.github.com/users/{USERNAME}"
    user_res = requests.get(user_url, headers=HEADERS)
    user_data = user_res.json()

    repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    repos_res = requests.get(repos_url, headers=HEADERS)
    repos_data = repos_res.json()

    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos_data)
    public_repos = user_data.get("public_repos", 0)
    followers = user_data.get("followers", 0)
    following = user_data.get("following", 0)

    languages = {}
    for repo in repos_data:
        lang = repo.get("language")
        if lang:
            languages[lang] = languages.get(lang, 0) + 1

    top_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3]
    langs_text = " • ".join([f"{lang} ({count})" for lang, count in top_langs]) if top_langs else "En cours d'apprentissage"

    return {
        "stars": total_stars,
        "repos": public_repos,
        "followers": followers,
        "following": following,
        "top_langs": langs_text
    }

def generate_svg(stats):
    bg_color = "#0d1117"
    border_color = "#30363d"
    title_color = "58a6ff"
    text_color = "c9d1d9"
    accent_color = "3fb950"

    svg = f'''<svg width="450" height="195" wmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" rx="10" fill="{bg_color}" stroke="{border_color}" stroke-width="1"/>

    <text x="25" y="35" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="16" font-weight="bold" fill="{title_color}">Mes Statistiques GitHub</text>

    <g transform="translate(25, 60)" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="13" fill="{text_color}">
        <text y="0">⭐️ Étoiles reçues : <tspan font-weight="bold" fill="{accent_color}">{stats["stars"]}</tspan</text>
        <text y="25">📦 Dépôts Publics : <tspan font-weight="bold" fill="{accent_color}">{stats["repos"]}</tspan</text>
        <text y="50">👥 Followers : <tspan font-weight="bold" fill="{accent_color}">{stats["followers"]}</tspan</text>
        <text y="75">💻 Langages principaux : <tspan font-weight="bold" fill="{accent_color}">{stats["top_langs"]}</tspan</text>
    </g>

    <text x="25" y="100" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif" font-size="10" fill="#8b949e">Généré automatiquement le {datetime.now().strftime("%d/%m/%Y")}</text>
    </svg>'''

    with open("stats.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("Image stats.svg généré avec succès !")

if __name__ == "__main__":
    stats = get_github_stats()
    generate_svg(stats)