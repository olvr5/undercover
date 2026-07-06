# Undercover — Édition Animé 🎭

Le jeu **Undercover** en version animé : un seul téléphone qu'on fait passer,
des personnages cultes en guise de mots secrets, avec leur image.

- **Civils** : ils reçoivent tous le même personnage (ex. *Gojo*).
- **Undercover** : ils reçoivent un personnage qui ressemble (ex. *Kakashi*).
- **Mr. White** : il ne reçoit rien du tout et doit improviser. S'il est éliminé,
  il peut gagner en devinant le mot des civils.

41 paires de personnages (One Piece, Naruto, Dragon Ball, Demon Slayer,
JJK, MHA, Ghibli…), tirées sans répétition tant que toutes n'ont pas été jouées.

## Jouer sur ton téléphone

### Option 1 — En ligne (recommandé, installable en PWA)
Héberge le dossier sur **GitHub Pages** (gratuit) :

1. Crée un dépôt sur github.com, glisse-dépose tout le contenu du dossier.
2. Settings → Pages → Source : branche `main`, dossier `/ (root)`.
3. Ouvre l'URL `https://<ton-pseudo>.github.io/<repo>/` sur le téléphone.
4. Safari/Chrome → **« Ajouter à l'écran d'accueil »** : l'app se lance en
   plein écran et fonctionne ensuite **hors ligne** (service worker).

(Netlify Drop marche aussi : netlify.com → glisser le dossier.)

### Option 2 — En local sur le même Wi-Fi
```bash
cd ~/Desktop/Undercover
python3 -m http.server 8000
```
Puis sur le téléphone : `http://<IP-du-Mac>:8000`
(IP visible dans Réglages Système → Wi-Fi. Pas de mode hors ligne dans ce cas.)

## Fichiers

| Fichier | Rôle |
|---|---|
| `index.html` | le jeu complet (logique + design) |
| `data.js` | les 41 paires (généré par le script) |
| `images/` | les 82 portraits (téléchargés une fois) |
| `galerie.html` | aperçu de toutes les paires |
| `fetch_images.py` | régénère `data.js` + images depuis l'API Jikan (MyAnimeList) |
| `sw.js`, `manifest.json`, `icon.png` | mode hors ligne + installation PWA |

## Ajouter / modifier des paires

Édite la liste `PAIRS` en haut de `fetch_images.py`
(format : `[("Nom affiché", "Requête MyAnimeList", "Anime"), (...)]`),
puis relance :

```bash
python3 fetch_images.py
```

Les images déjà téléchargées sont conservées ; seules les nouvelles sont récupérées.
Si la recherche par nom se trompe de personnage, ajoute son ID MyAnimeList
dans le dictionnaire `MAL_IDS`.
