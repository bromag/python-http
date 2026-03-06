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

---

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
Öffnet `input.html` (über Index-Navigation), schreibt Text in `#txt`, klickt `#send` und gibt `#echo` aus.

```bash
python myproject.py input --text "Hallo Input" --headless
```

### 9) Slider-Test
Öffnet `slider.html` (über Index-Navigation), setzt den Slider-Wert und gibt `#value` aus.

```bash
python myproject.py slider --slider 80 --headless
```

### 10) Hover-Test
Öffnet `hover.html` (über Index-Navigation), hovert über `#box` und prüft `#tooltip`.

```bash
python myproject.py hover --headless
```

### 11) Drag & Drop-Test
Öffnet `dragdrop.html` (über Index-Navigation), zieht `#source` auf `#target` und gibt `#result` aus.

```bash
python myproject.py dragdrop --headless
```

### 12) New Window-Test
Öffnet `newwindow.html` (über Index-Navigation), öffnet ein neues Fenster/Tab, wechselt hinein, prüft Inhalt, schliesst und geht zurück.

```bash
python myproject.py newwindow --headless
```

### 13) Login-Test
Öffnet `login.html` (über Index-Navigation), füllt User/Pass, klickt Login und gibt `#result` aus.

```bash
python myproject.py login --login-user admin --login-pass secret --headless
```

### 14) Upload-Test
Öffnet `upload.html` (über Index-Navigation), setzt eine Datei im `<input type="file">` und gibt `#result` aus.

```bash
python myproject.py upload --upload-file ./web/files/test.pdf --headless
```

### 15) Key Presses-Test
Öffnet `keys.html` (über Index-Navigation), sendet Tasten und gibt `#last` aus.

```bash
python myproject.py keys --headless
```

---

## Wichtige HTML-IDs (damit Selenium Elemente findet)

- `index.html`
  - Navigation-Links (empfohlen):  
    `nav-get`, `nav-post`, `nav-cookies`, `nav-checkbox`, `nav-dropdown`, `nav-input`, `nav-slider`, `nav-hover`, `nav-dragdrop`, `nav-newwindow`, `nav-login`, `nav-upload`, `nav-keys`
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

- `hover.html`
  - Hover-Element: `box`
  - Tooltip: `tooltip`

- `dragdrop.html`
  - Drag-Quelle: `source`
  - Drop-Ziel: `target`
  - Output-Element: `result`

- `newwindow.html`
  - Link zum Öffnen: `open`
- `popup.html`
  - Header/Text: `popup-title`

- `login.html`
  - Username: `username`
  - Password: `password`
  - Button: `login`
  - Output-Element: `result`

- `upload.html`
  - File Input: `file`
  - Button: `show`
  - Output-Element: `result`

- `keys.html`
  - Input: `box`
  - Output-Element: `last`
