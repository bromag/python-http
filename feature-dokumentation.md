# Noten-/Feature-Dokumentation

Diese Tabelle zeigt die umgesetzten Features inkl. Datei/Zeilenbereich.
**Wichtig:** Zeilennummern können je nach Version leicht variieren.  
Ermittle die exakten Zeilen mit:

```bash
nl -ba myproject.py | sed -n '1,220p'
```

oder gezielt:
```bash
nl -ba myproject.py | grep -n "def cmd_"
```

## Feature-Tabelle

| Feature | Implementiert | Beschreibung (kurz) | Datei | Zeilen (von–bis) |
|---|---:|---|---|---|
| Scraping: `<title>` | Ja | Öffnet `index.html` und gibt `driver.title` aus | `myproject.py` | (mit `nl -ba` prüfen) |
| GET Request mit Variablen | Ja | Ruft `get.html?name=...&room=...` auf, liest `#result` | `myproject.py` + `web/get.html` | (mit `nl -ba` prüfen) |
| POST/Form Submission | Ja | Navigiert via Index nach `post.html`, füllt Inputs, klickt Submit, liest `#out` | `myproject.py` + `web/post.html` | (mit `nl -ba` prüfen) |
| Cookies lesen | Ja | Navigiert via Index nach `cookies.html`, klickt `#set`, listet `driver.get_cookies()` | `myproject.py` + `web/cookies.html` | (mit `nl -ba` prüfen) |
| Datei-Download | Ja | Klickt `#dl` auf `index.html`, wartet bis Datei im Download-Ordner stabil ist | `myproject.py` + `web/index.html` + `web/files/test.pdf` | (mit `nl -ba` prüfen) |
| Checkbox auswählen | Ja | Navigiert via Index nach `checkbox.html`, wählt `cb1` oder `cb2`, gibt `#status` aus | `myproject.py` + `web/checkbox.html` | (mit `nl -ba` prüfen) |
| Startpunkt immer `index.html` | Ja | Helper navigiert von Index über Link-IDs (`nav-*`) | `myproject.py` + `web/index.html` | (mit `nl -ba` prüfen) |
| Headless Mode | Ja | `--headless` startet Firefox ohne UI | `myproject.py` | (mit `nl -ba` prüfen) |
| Download-Ordner Konfiguration | Ja | Firefox Preferences: Download dir, PDF ohne Prompt | `myproject.py` | (mit `nl -ba` prüfen) |

## Verwendete Dateien (Übersicht)

- `web/index.html`
  - Navigation: Links zu GET/POST/Cookies/Checkbox
  - Download-Link: `id="dl"` (PDF)
- `web/get.html`
  - Liest Query-Parameter (`name`, `room`) und schreibt in `#result`
- `web/post.html`
  - Formular mit Inputs `user`/`msg`, Ausgabe in `#out`
- `web/cookies.html`
  - Button `#set` setzt Cookies, Ausgabe (optional) auf der Seite
- `web/checkbox.html`
  - Checkboxen `#cb1` / `#cb2`, Status in `#status`
