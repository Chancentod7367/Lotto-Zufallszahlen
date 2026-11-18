#!/usr/bin/env python3
"""Holt das offizielle KENO-Archiv von LOTTO Bayern und schreibt data/keno.csv.

Läuft per GitHub Action (siehe .github/workflows/keno.yml), nur Python-Standardbibliothek.
Format der Ausgabe: date,n1,...,n20 (neueste Ziehung zuerst, Zahlen aufsteigend sortiert).
"""
import csv, io, re, sys, urllib.request, zipfile
from datetime import date
from pathlib import Path

URL = "https://www.lotto-bayern.de/static/gamebroker_2/de/download_files/archiv_keno.zip"
OUT = Path(__file__).resolve().parents[1] / "data" / "keno.csv"


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (glueckszahlen-app)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def decode(raw: bytes) -> str:
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            pass
    return raw.decode("utf-8", errors="replace")


def texts_from_zip(blob: bytes):
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        names = [n for n in z.namelist() if not n.endswith("/")]
        # KENO-Datei bevorzugen, "plus 5" nach hinten
        names.sort(key=lambda n: (("plus" in n.lower()), ("keno" not in n.lower())))
        for n in names:
            yield n, decode(z.read(n))


DATE_RE = re.compile(r"^\s*(\d{1,2})[.\s;,/-]+(\d{1,2})[.\s;,/-]+(\d{4})\b")


def find_window(nums):
    """Erstes Fenster aus 20 verschiedenen Zahlen im Bereich 1..70."""
    for i in range(0, len(nums) - 19):
        w = nums[i:i + 20]
        if all(1 <= x <= 70 for x in w) and len(set(w)) == 20:
            return w
    return None


def parse(text: str):
    draws = {}
    for line in text.splitlines():
        m = DATE_RE.match(line)
        if not m:
            continue
        d, mo, y = map(int, m.groups())
        try:
            dt = date(y, mo, d)
        except ValueError:
            continue
        rest = [int(t) for t in re.findall(r"\d+", line[m.end():])]
        w = find_window(rest)
        if w:
            draws[dt.isoformat()] = sorted(w)
    return draws


def main():
    blob = download(URL)
    draws = {}
    for name, text in texts_from_zip(blob):
        found = parse(text)
        print(f"{name}: {len(found)} Ziehungen erkannt")
        if len(found) > len(draws):
            draws = found
    if len(draws) < 100:
        sys.exit(f"Zu wenige Ziehungen erkannt ({len(draws)}) – Format geändert? Abbruch ohne Überschreiben.")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["date"] + [f"n{i}" for i in range(1, 21)])
        for d in sorted(draws, reverse=True):
            w.writerow([d] + draws[d])
    newest = max(draws)
    print(f"OK: {len(draws)} Ziehungen, neueste {newest}: {draws[newest]}")


if __name__ == "__main__":
    main()
