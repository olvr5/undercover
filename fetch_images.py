#!/usr/bin/env python3
"""Télécharge les images des personnages via l'API Jikan (MyAnimeList)
et génère data.js pour le jeu Undercover Anime."""

import json
import re
import time
import unicodedata
import urllib.request
import urllib.parse
from pathlib import Path

HERE = Path(__file__).parent
IMG_DIR = HERE / "images"
IMG_DIR.mkdir(exist_ok=True)

# (nom affiché FR, requête de recherche MAL, anime affiché)
PAIRS = [
    [("Luffy", "Monkey D. Luffy", "One Piece"), ("Naruto", "Naruto Uzumaki", "Naruto")],
    [("Son Goku", "Son Goku", "Dragon Ball Z"), ("Saitama", "Saitama", "One Punch Man")],
    [("Zoro", "Roronoa Zoro", "One Piece"), ("Levi", "Levi Ackerman", "L'Attaque des Titans")],
    [("Sasuke", "Sasuke Uchiha", "Naruto"), ("Vegeta", "Vegeta", "Dragon Ball Z")],
    [("Light Yagami", "Light Yagami", "Death Note"), ("Lelouch", "Lelouch Lamperouge", "Code Geass")],
    [("L", "L Lawliet", "Death Note"), ("Conan", "Conan Edogawa", "Détective Conan")],
    [("Nezuko", "Nezuko Kamado", "Demon Slayer"), ("Hinata", "Hinata Hyuga", "Naruto")],
    [("Tanjiro", "Tanjirou Kamado", "Demon Slayer"), ("Deku", "Izuku Midoriya", "My Hero Academia")],
    [("Gojo", "Satoru Gojou", "Jujutsu Kaisen"), ("Kakashi", "Kakashi Hatake", "Naruto")],
    [("All Might", "Toshinori Yagi", "My Hero Academia"), ("Might Guy", "Maito Gai", "Naruto")],
    [("Eren", "Eren Yeager", "L'Attaque des Titans"), ("Kaneki", "Ken Kaneki", "Tokyo Ghoul")],
    [("Mikasa", "Mikasa Ackerman", "L'Attaque des Titans"), ("Erza", "Erza Scarlet", "Fairy Tail")],
    [("Ace", "Portgas D. Ace", "One Piece"), ("Natsu", "Natsu Dragneel", "Fairy Tail")],
    [("Todoroki", "Shouto Todoroki", "My Hero Academia"), ("Grey", "Gray Fullbuster", "Fairy Tail")],
    [("Gon", "Gon Freecss", "Hunter x Hunter"), ("Killua", "Killua Zoldyck", "Hunter x Hunter")],
    [("Zenitsu", "Zenitsu Agatsuma", "Demon Slayer"), ("Bakugo", "Katsuki Bakugou", "My Hero Academia")],
    [("Ichigo", "Ichigo Kurosaki", "Bleach"), ("Inuyasha", "Inuyasha", "Inuyasha")],
    [("Sanji", "Sanji", "One Piece"), ("Soma", "Souma Yukihira", "Food Wars")],
    [("Usopp", "Usopp", "One Piece"), ("Mr. Satan", "Mr. Satan", "Dragon Ball Z")],
    [("Nami", "Nami", "One Piece"), ("Bulma", "Bulma", "Dragon Ball")],
    [("Chopper", "Tony Tony Chopper", "One Piece"), ("Pikachu", "Pikachu", "Pokémon")],
    [("Freezer", "Frieza", "Dragon Ball Z"), ("Aizen", "Sousuke Aizen", "Bleach")],
    [("Itachi", "Itachi Uchiha", "Naruto"), ("Obito", "Obito Uchiha", "Naruto")],
    [("Rem", "Rem", "Re:Zero"), ("Zero Two", "Zero Two", "Darling in the Franxx")],
    [("Edward Elric", "Edward Elric", "Fullmetal Alchemist"), ("Alphonse Elric", "Alphonse Elric", "Fullmetal Alchemist")],
    [("Jiraiya", "Jiraiya", "Naruto"), ("Tortue Géniale", "Muten Roshi", "Dragon Ball")],
    [("Tsunade", "Tsunade", "Naruto"), ("Boa Hancock", "Boa Hancock", "One Piece")],
    [("Kaido", "Kaidou", "One Piece"), ("Broly", "Broly", "Dragon Ball")],
    [("Shanks", "Shanks", "One Piece"), ("Barbe Blanche", "Edward Newgate", "One Piece")],
    [("Kirito", "Kazuto Kirigaya", "Sword Art Online"), ("Subaru", "Subaru Natsuki", "Re:Zero")],
    [("Ryuk", "Ryuk", "Death Note"), ("Beerus", "Beerus", "Dragon Ball Super")],
    [("Sakura", "Sakura Haruno", "Naruto"), ("Orihime", "Orihime Inoue", "Bleach")],
    [("Denji", "Denji", "Chainsaw Man"), ("Yuji Itadori", "Yuuji Itadori", "Jujutsu Kaisen")],
    [("Anya", "Anya Forger", "Spy x Family"), ("Mob", "Shigeo Kageyama", "Mob Psycho 100")],
    [("Sacha", "Satoshi", "Pokémon"), ("Yugi", "Yami Yugi", "Yu-Gi-Oh!")],
    [("Kenshiro", "Kenshirou", "Ken le Survivant"), ("Jotaro", "Jotaro Kujo", "JoJo's Bizarre Adventure")],
    [("Dio", "Dio Brando", "JoJo's Bizarre Adventure"), ("Muzan", "Muzan Kibutsuji", "Demon Slayer")],
    [("Totoro", "Totoro", "Mon Voisin Totoro"), ("Ronflex", "Snorlax", "Pokémon")],
    [("Hisoka", "Hisoka", "Hunter x Hunter"), ("Orochimaru", "Orochimaru", "Naruto")],
    [("Genos", "Genos", "One Punch Man"), ("C-18", "Android 18", "Dragon Ball Z")],
    [("Chihiro", "Chihiro Ogino", "Le Voyage de Chihiro"), ("Sophie", "Sophie Hatter", "Le Château Ambulant")],
]


def slugify(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def api_get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "undercover-anime/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


# IDs MAL directs pour les persos que la recherche par nom ne trouve pas
MAL_IDS = {
    "Son Goku": 246,
    "Nami": 723,
    "Sacha": 2473,
    "All Might": 117921,
    "Might Guy": 307,
    "Tortue Géniale": 6167,
    "Jotaro": 4003,
    "Ronflex": 222122,
    "C-18": 4318,
}


def norm_tokens(text):
    s = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    # normalise les romanisations japonaises (Joutarou -> Jotaro, Yuugi -> Yugi)
    words = []
    for w in s.split():
        w = w.replace("ou", "o").replace("uu", "u").replace("oo", "o")
        words.append(w)
    return set(words)


def search_character(query, display=None):
    if display in MAL_IDS:
        return api_get(f"https://api.jikan.moe/v4/characters/{MAL_IDS[display]}")["data"]
    url = "https://api.jikan.moe/v4/characters?q=" + urllib.parse.quote(query) + "&limit=15"
    data = api_get(url).get("data", [])
    if not data:
        return None
    q = norm_tokens(query)
    matches = []
    for c in data:
        names = norm_tokens(c.get("name") or "")
        for nick in c.get("nicknames") or []:
            names |= norm_tokens(nick)
        if q <= names:
            matches.append(c)
    if not matches:
        print(f"  pas de match exact pour '{query}', candidats: "
              + ", ".join((c.get("name") or "?") for c in data[:5]))
        return None
    # parmi les vrais matchs, le plus célèbre = le plus de favoris
    matches.sort(key=lambda c: c.get("favorites") or 0, reverse=True)
    return matches[0]


def download(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "undercover-anime/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        dest.write_bytes(r.read())


def main():
    out_pairs = []
    failures = []
    for pair in PAIRS:
        entry = []
        for display, query, anime in pair:
            slug = slugify(display)
            img_path = IMG_DIR / f"{slug}.jpg"
            ok = img_path.exists()
            mal_name = ""
            if not ok:
                try:
                    c = search_character(query, display)
                    time.sleep(1.1)  # rate limit Jikan
                    if c:
                        img_url = c["images"]["jpg"]["image_url"]
                        mal_name = c.get("name", "")
                        if img_url and "questionmark" not in img_url:
                            download(img_url, img_path)
                            time.sleep(0.4)
                            ok = True
                except Exception as e:
                    print(f"  ERREUR {display}: {e}")
            status = "OK " if ok else "FAIL"
            print(f"[{status}] {display:18s} <- {query} ({mal_name})")
            if not ok:
                failures.append(display)
            entry.append({"name": display, "anime": anime, "img": f"images/{slug}.jpg", "ok": ok})
        out_pairs.append(entry)

    kept = [[{k: v for k, v in c.items() if k != "ok"} for c in p]
            for p in out_pairs if all(c["ok"] for c in p)]
    js = "const PAIRS = " + json.dumps(kept, ensure_ascii=False, indent=1) + ";\n"
    (HERE / "data.js").write_text(js, encoding="utf-8")
    print(f"\n{len(kept)}/{len(PAIRS)} paires complètes -> data.js")
    if failures:
        print("Échecs:", ", ".join(failures))


if __name__ == "__main__":
    main()
