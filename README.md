# Glückszahlen – LOTTO 6aus49 & Eurojackpot

Statische Web-App (HTML/JS, keine Abhängigkeiten, kein Backend). Lädt die Ziehungen live als CSV aus zwei
öffentlichen, per GitHub Actions automatisch aktualisierten Archiven:

- LOTTO 6aus49: https://github.com/daowa89/lottery-archive (seit 1955)
- Eurojackpot:  https://github.com/bostjanvihar/eurojp (seit 2012, MIT)

Quellen lassen sich in der App unter ⚙︎ ändern.

## Hosten (empfohlen: GitHub Pages, kostenlos)
1. Neues Repo anlegen, z. B. `glueckszahlen` (darf privat sein bei GitHub Pro, sonst öffentlich).
2. Alle Dateien dieses Ordners hochladen (Drag & Drop im Browser reicht).
3. Settings → Pages → Source: „Deploy from a branch“, Branch `main`, Ordner `/ (root)`.
4. Nach ~1 Min erreichbar unter `https://<user>.github.io/glueckszahlen/`.

## Auf dem iPhone als App
Seite in Safari öffnen → Teilen → „Zum Home-Bildschirm“. Läuft dann im Vollbild mit eigenem Icon,
die letzten Daten sind auch offline verfügbar.

## Alternativ lokal / Heimserver
Jeder statische Webserver geht, z. B. `python3 -m http.server 8000` im Ordner.
(Direkt per Doppelklick als file:// klappt das Laden der Daten je nach Browser nicht.)
