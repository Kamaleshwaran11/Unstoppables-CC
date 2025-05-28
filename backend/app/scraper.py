import requests
from bs4 import BeautifulSoup

def scrape_matches():
    url = "https://cricheroes.com/player-profile/8817881/kamalesh-s/matches"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    matches = []
    match_cards = soup.select(".match-card")  # Adjust selector if needed

    for card in match_cards:
        title = card.select_one(".match-title") or card.find("h5")
        date = card.select_one(".match-date") or card.find("p")
        result = card.select_one(".match-result") or card.find("span")

        if title and date:
            matches.append({
                "title": title.text.strip(),
                "date": date.text.strip(),
                "location": "unknown",
                "result": result.text.strip() if result else "N/A"
            })
    return matches


def scrape_stats():
    url = "https://cricheroes.com/player-profile/8817881/kamalesh-s/stats"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    stats = {}
    stat_blocks = soup.select(".player-profile-stats-card")  # Adjust selector

    for block in stat_blocks:
        items = block.select("div.col")
        for item in items:
            label = item.select_one(".text-muted")
            value = item.select_one("h5")
            if label and value:
                stats[label.text.strip()] = value.text.strip()
    return stats
