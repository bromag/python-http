# Selenium HTTP Projekt – Dokumentation

## 1) Minimale Dokumentation

## Voraussetzungen
- Python 3.x
- Virtuelle Umgebung (empfohlen)
- Selenium installiert (`pip install selenium`)
- Firefox installiert
- Geckodriver verfügbar (meist via Selenium Manager automatisch; alternativ: `brew install geckodriver`)

## Projektstruktur (Beispiel)
```text
python-http/
  myproject.py
  web/
    index.html
    get.html
    post.html
    cookies.html
    checkbox.html
    dropdown.html
    input.html
    slider.html
    files/
      test.pdf
```

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

### 6) Checkbox auswählen
Öffnet `checkbox.html` (über Index-Navigation), wählt Checkbox 1 oder 2 aus und gibt `#status` aus.

```bash
python myproject.py checkbox --check 1 --headless
python myproject.py checkbox --check 2 --headless
```

### 7) Dropdown auswählen
Öffnet `dropdown.html` (über Index-Navigation), wählt eine Option im Dropdown und gibt `#selected` aus.

```bash
python myproject.py dropdown --dropdown drop1 --headless
python myproject.py dropdown --dropdown drop2 --headless
python myproject.py dropdown --dropdown drop3 --headless
```

### 8) Input-Test
Öffnet `input.html` (über Index-Navigation), schreibt Text in ein Input-Feld, klickt Button und gibt `#echo` aus.

```bash
python myproject.py input --text "Hallo Input" --headless
```

### 9) Slider-Test
Öffnet `slider.html` (über Index-Navigation), setzt den Slider-Wert und gibt `#value` aus.

```bash
python myproject.py slider --slider 80 --headless
```

## Wichtige HTML-IDs (damit Selenium Elemente findet)
- `index.html`
  - Navigation-Links (empfohlen): `nav-get`, `nav-post`, `nav-cookies`, `nav-checkbox`, `nav-dropdown`, `nav-input`, `nav-slider`
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
- `input.html`
  - Textfeld: `txt`
  - Button: `send`
  - Output-Element: `echo`
- `slider.html`
  - Slider: `slider`
  - Output-Element: `value`

## Troubleshooting (kurz)
- `ModuleNotFoundError: No module named 'selenium'`
  - In venv installieren: `python -m pip install selenium`
- `NoSuchElementException`
  - Prüfen, ob die IDs im HTML exakt stimmen (z.B. `id="dl"`, `id="nav-get"`, …)
- Download wird nicht gespeichert
  - Prüfen, ob Datei existiert (`web/files/test.pdf`) und MIME-Type passt (PDF: `application/pdf`)
- Dropdown zeigt keinen Status
  - Prüfen, ob JS die richtige ID referenziert (z.B. `document.getElementById("drop")`)

---

## 2) Noten-/Feature-Dokumentation

Diese Tabelle zeigt die umgesetzten Features inkl. Datei/Zeilenbereich.  
**Wichtig:** Zeilennummern können je nach Version leicht variieren.  
Ermittle die exakten Zeilen mit:

```bash
nl -ba myproject.py | sed -n '1,260p'
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
| Dropdown auswählen | Ja | Navigiert via Index nach `dropdown.html`, wählt Option im `<select>` und liest `#selected` | `myproject.py` + `web/dropdown.html` | (mit `nl -ba` prüfen) |
| Input-Test | Ja | Navigiert via Index nach `input.html`, schreibt Text in `#txt`, klickt `#send`, liest `#echo` | `myproject.py` + `web/input.html` | (mit `nl -ba` prüfen) |
| Slider-Test | Ja | Navigiert via Index nach `slider.html`, setzt Range-Input `#slider`, liest `#value` | `myproject.py` + `web/slider.html` | (mit `nl -ba` prüfen) |
| Startpunkt immer `index.html` | Ja | Helper navigiert von Index über Link-IDs (`nav-*`) | `myproject.py` + `web/index.html` | (mit `nl -ba` prüfen) |
| Headless Mode | Ja | `--headless` startet Firefox ohne UI | `myproject.py` | (mit `nl -ba` prüfen) |
| Download-Ordner Konfiguration | Ja | Firefox Preferences: Download dir, PDF ohne Prompt | `myproject.py` | (mit `nl -ba` prüfen) |

## Verwendete Dateien (Übersicht)

- `web/index.html`
  - Navigation: Links zu GET/POST/Cookies/Checkbox/Dropdown/Input/Slider (empfohlen via IDs: `nav-get`, `nav-post`, `nav-cookies`, `nav-checkbox`, `nav-dropdown`, `nav-input`, `nav-slider`)
  - Download-Link: `id="dl"` (PDF)
- `web/get.html`
  - Liest Query-Parameter (`name`, `room`) und schreibt in `#result`
- `web/post.html`
  - Formular mit Inputs `user`/`msg`, Ausgabe in `#out`
- `web/cookies.html`
  - Button `#set` setzt Cookies, Ausgabe (optional) auf der Seite
- `web/checkbox.html`
  - Checkboxen `#cb1` / `#cb2`, Status in `#status`
- `web/dropdown.html`
  - Dropdown `<select id="drop">` mit Optionen, Anzeige in `#selected`
- `web/input.html`
  - Text-Input `#txt`, Button `#send`, Ausgabe in `#echo`
- `web/slider.html`
  - Range-Input `#slider`, Ausgabe in `#value`
