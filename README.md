# Minimale Dokumentation (Selenium HTTP Projekt)

## Lokale Test-Webseite starten
Im Ordner `web/`:

```bash
cd web
python3 -m http.server 8000
```

Danach ist die Seite erreichbar unter:
- `http://127.0.0.1:8000/index.html`

## Verwendung der Commands
Alle Commands werden im Projektordner (da wo `myproject.py` liegt) ausgeführt.

Hinweis zu `--headless`:
- **mit** `--headless` läuft Firefox ohne sichtbares Fenster
- **ohne** `--headless` wird ein Browserfenster angezeigt (hilfreich fürs Debugging)

### 1) Title Scraping
Liest den `<title>` von `index.html`.

```bash
python myproject.py title --headless
```

### 2) GET mit Variablen
Ruft `get.html` mit Query-Parametern auf und liest den Text aus `#result`.

```bash
python myproject.py get --name Giuliano --room A101 --headless
```

**Defaults verwenden** (Parameter weglassen):
```bash
python myproject.py get --headless
```

### 3) POST / Form Submission
Öffnet `post.html`, füllt `user` und `msg` aus, klickt Submit und gibt `#out` aus.

```bash
python myproject.py post --user giu --msg "Hallo zusammen" --headless
```

### 4) Cookies ausgeben
Öffnet `cookies.html`, setzt Cookies per Button-Klick und gibt alle Cookies aus.

```bash
python myproject.py list-cookies --headless
```

### 5) Datei herunterladen
Startet auf `index.html`, klickt den Download-Link und prüft, ob die Datei im Download-Ordner angekommen ist.

```bash
python myproject.py download --file test.pdf --download-dir ./downloads --headless
```

**Voraussetzung in `index.html`:**
```html
<a id="dl" href="files/test.pdf" download>Download test.pdf</a>
```

```bash
python myproject.py dropdown --dropdown drop1 --headless
python myproject.py dropdown --dropdown drop2 --headless
python myproject.py dropdown --dropdown drop3 --headless
```

### 6) Checkbox auswählen
Öffnet `checkbox.html` (über Index-Navigation), wählt Checkbox 1 oder 2 aus und gibt `#status` aus.

```bash
python myproject.py checkbox --check 1 --headless
python myproject.py checkbox --check 2 --headless
```

### 7) Dropdown auswählen
Öffnet `dropdown.html` (über Index-Navigation), wählt eine Option im Dropdown und gibt `#selected` aus.


## Wichtige HTML-IDs (damit Selenium Elemente findet)
- `index.html`
  - Navigation-Links (empfohlen): `nav-get`, `nav-post`, `nav-cookies`, `nav-checkbox`, `nav-dropdown`
  - Download-Link: `dl`
- `get.html`
  - Output-Element: `result`
- `post.html`
  - Inputs: `name="user"`, `name="msg"`
  - Output-Element: `out`
- `cookies.html`
  - Button zum Setzen: `set`
- `checkbox.html`
  - Checkboxen: `cb1`, `cb2`
  - Status-Element: `status`
- `dropdown.html`
  - Dropdown: `drop`
  - Output-Element: `selected`

